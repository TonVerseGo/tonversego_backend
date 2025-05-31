from fastapi import APIRouter, HTTPException
from database.models import User
from schemas.user import CreateUser, ReturnUser

user_router = APIRouter(prefix="/user")

@user_router.post("", response_model=ReturnUser)
async def create_user(user_data: CreateUser):
    existing_user = await User.get_or_none(id=user_data.id)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this Telegram ID already exists"
        )
        
    existing_wallet = await User.get_or_none(ton_wallet=user_data.ton_wallet)
    if existing_wallet:
        raise HTTPException(
            status_code=400,
            detail="User with this TON wallet already exists"
        )

    user = await User.create(
        id=user_data.id,
        ton_wallet=user_data.ton_wallet,
        nickname=user_data.nickname
    )

    return ReturnUser(
        id=user.id,
        ton_wallet=user.ton_wallet,
        nickname=user.nickname
    )

@user_router.get("/{user_id}", response_model=ReturnUser)
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    return ReturnUser(
        id=user.id,
        ton_wallet=user.ton_wallet,
        nickname=user.nickname
    )

@user_router.get("/verify/{token}", response_model=ReturnUser)
async def verify_token(token: str):
    try:
        user_id = int(token.replace("TonVerseGo_", "").strip())
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid token"
        )

    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    return ReturnUser(
        id=user.id,
        ton_wallet=user.ton_wallet,
        nickname=user.nickname
    )