import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, Form, File, UploadFile
from typing import Optional
from database.models import NFT
from utils.ipfs import upload_to_ipfs

admin_router = APIRouter(prefix="/admin")

@admin_router.post("/nft/create")
async def create_nft(
    name: str = Form(...),
    ton_address: str = Form(...),
    description: str = Form(...),
    lat: float = Form(...),
    lng: float = Form(...),
    hint: str = Form(...),
    owner_wallet: Optional[str] = Form(None),
    photo: UploadFile = File(...),
    model: UploadFile = File(...)
):
    # Создаем директории если их нет
    photo_folder = os.getenv("PHOTO_FOLDER")
    model_folder = os.getenv("MODEL_FOLDER")
    Path(photo_folder).mkdir(parents=True, exist_ok=True)
    Path(model_folder).mkdir(parents=True, exist_ok=True)

    # Сохраняем фото
    photo_ext = photo.filename.split('.')[-1]
    photo_filename = f"{uuid.uuid4()}.{photo_ext}"
    photo_path = os.path.join(photo_folder, photo_filename)

    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # Сохраняем 3D модель
    model_ext = model.filename.split('.')[-1]
    model_filename = f"{uuid.uuid4()}.{model_ext}"
    model_path = os.path.join(model_folder, model_filename)

    with open(model_path, "wb") as buffer:
        shutil.copyfileobj(model.file, buffer)

    # Upload to IPFS
    photo_ipfs_url = await upload_to_ipfs(photo_path)
    model_ipfs_url = await upload_to_ipfs(model_path)

    # Создаём запись в БД
    nft = await NFT.create(
        name=name,
        ton_address=ton_address,
        description=description,
        lat=lat,
        lng=lng,
        hint=hint,
        ownet_wallet=owner_wallet,
        photo_url=photo_ipfs_url,
        model_url=model_ipfs_url,
    )

    return {
        "status": "success",
        "id": nft.id,
        "photo_url": photo_ipfs_url,
        "model_url": model_ipfs_url,
    }