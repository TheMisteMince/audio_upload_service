from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.auth import fastapi_users
from app.models import AudioFile, User
from app.database import database
import aiofiles
import os
from datetime import datetime
from app.main import UPLOAD_DIR

router = APIRouter()
current_user = fastapi_users.current_user(active=True)


@router.post("/upload-audio", tags=["audio"])
async def upload_audio(file: UploadFile = File(...), file_name: str = Form(...), user: User = Depends(current_user)):
    file_path = os.path.join(
        UPLOAD_DIR, f"{user.id}_{datetime.now().timestamp()}_{file.filename}")
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    audio_file = {
        "user_id": user.id,
        "file_name": file_name,
        "file_path": file_path,
        "uploaded_at": datetime.now()
    }
    await database.execute(AudioFile.__table__.insert(), values=audio_file)
    return {"message": "File uploaded successfully"}
