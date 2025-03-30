from fastapi import APIRouter, Depends
from app.auth import fastapi_users
from app.models import User
from app.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

router = APIRouter()

current_superuser = fastapi_users.current_user(active=True, superuser=True)


@router.get("/")
async def get_users(user: User = Depends(current_superuser), session: AsyncSession = Depends(lambda: async_session())):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.put("/{user_id}")
async def update_user(user_id: int, update_data: dict, user: User = Depends(current_superuser), session: AsyncSession = Depends(lambda: async_session())):
    query = update(User).where(User.id == user_id).values(**update_data)
    await session.execute(query)
    await session.commit()
    return {"message": "User updated"}


@router.delete("/{user_id}")
async def delete_user(user_id: int, user: User = Depends(current_superuser), session: AsyncSession = Depends(lambda: async_session())):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()
    return {"message": "User deleted"}
