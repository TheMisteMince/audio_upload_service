from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.auth import fastapi_users
from app.models import AudioFile, User
from app.database import async_session
import aiofiles
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

router = APIRouter()

current_user = fastapi_users.current_user(active=True)


@router.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...),
    name: str = Form(...),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(lambda: async_session())
):
    file_path = os.path.join(
        "/app/uploads", f"{user.id}_{int(datetime.now().timestamp())}_{file.filename}")
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    await session.execute(
        insert(AudioFile),
        {"user_id": user.id, "file_name": name,
            "file_path": file_path, "uploaded_at": datetime.now()}
    )
    await session.commit()
    return {"message": "File uploaded successfully"}


@router.get("/my-audio")
async def get_my_audio(user: User = Depends(current_user), session: AsyncSession = Depends(lambda: async_session())):
    query = select(AudioFile).where(AudioFile.user_id == user.id)
    result = await session.execute(query)
    audio_files = result.scalars().all()
    return audio_files
