from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.database import engine, metadata
from app.auth import fastapi_users, jwt_backend
from app.routers import audio, users
import os
from dotenv import load_dotenv

from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from fastapi.responses import JSONResponse

load_dotenv()

oauth = OAuth()
oauth.register(
    name="yandex",
    client_id=os.getenv("YANDEX_CLIENT_ID"),
    client_secret=os.getenv("YANDEX_CLIENT_SECRET"),
    authorize_url="https://oauth.yandex.com/authorize",
    access_token_url="https://oauth.yandex.com/token",
    userinfo_endpoint="https://login.yandex.com/info",
    client_kwargs={"scope": "login:email login:info"},
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    UPLOAD_DIR = "/app/uploads"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(jwt_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

auth_router = APIRouter(prefix="/auth/yandex", tags=["auth"])


@auth_router.get("/login")
async def yandex_login(request: Request):
    redirect_uri = "http://localhost:8000/auth/yandex/callback"
    return await oauth.yandex.authorize_redirect(request, redirect_uri)


@auth_router.get("/callback")
async def yandex_callback(request: Request):
    token = await oauth.yandex.authorize_access_token(request)
    user_info = await oauth.yandex.userinfo(token=token)

    email = user_info.get("default_email")
    if not email:
        return JSONResponse(status_code=400, content={"message": "Email not found in Yandex user info"})

    from app.database import async_session
    from app.models import User
    from sqlalchemy import select
    async with async_session() as session:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            user = User(
                email=email,
                username=user_info.get("login", email.split("@")[0]),
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

    jwt = await fastapi_users.create_user_token(user)
    return {"access_token": jwt["token"], "token_type": "bearer"}

app.include_router(auth_router)

app.include_router(audio.router, prefix="/audio", tags=["audio"])
app.include_router(users.router, prefix="/users", tags=["users"])
