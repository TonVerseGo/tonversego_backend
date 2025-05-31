from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    id: int = Field(..., description="Telegram User ID")
    ton_wallet: str = Field(..., max_length=64)
    nickname: str = Field(..., max_length=32)

class ReturnUser(BaseModel):
    id: int
    ton_wallet: str
    nickname: str