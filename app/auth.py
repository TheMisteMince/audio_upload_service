from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication, OAuth2Authentication
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import models as user_models
from app.models import User
from app.database import database
import os

user_db = SQLAlchemyUserDatabase(User, database, User.__table__)


jwt_authentication = JWTAuthentication(
    secret=os.getenv("SECRET_KEY"), lifetime_seconds=3600)


yandex_oauth = OAuth2Authentication(
    name="yandex",
    authorize_url="https://oauth.yandex.com/authorize",
    token_url="https://oauth.yandex.com/token",
    user_url="https://login.yandex.com/info",
    client_id=os.getenv("YANDEX_CLIENT_ID"),
    client_secret=os.getenv("YANDEX_CLIENT_SECRET"),
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication, yandex_oauth],
    User,
    user_models.UserCreate,
    user_models.UserUpdate,
    user_models.UserDB,
)
