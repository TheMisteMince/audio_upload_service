from fastapi import FastAPI
from app.database import database, engine, metadata
from app.auth import fastapi_users, jwt_authentication, yandex_oauth
import os

app = FastAPI()
UPLOAD_DIR = "/app/uploads"


@app.on_event("startup")
async def startup():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    await database.connect()
    metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(fastapi_users.get_auth_router(
    jwt_authentication), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_oauth_router(
    yandex_oauth), prefix="/auth/yandex", tags=["auth"])
app.include_router(fastapi_users.get_register_router(),
                   prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(),
                   prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
