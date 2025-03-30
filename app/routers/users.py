from fastapi import APIRouter, Depends
from app.models import User
from app.database import database
from app.auth import fastapi_users

router = APIRouter()


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: int,
                      current_user: User = Depends(fastapi_users.current_user(active=True, superuser=True))):
    query = User.__table__.delete().where(User.id == user_id)
    await database.execute(query)
    return {"message": "User deleted"}
