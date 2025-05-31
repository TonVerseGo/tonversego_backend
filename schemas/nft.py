from pydantic import BaseModel, Field
from typing import Optional

class GetNearbyNFT(BaseModel):
    lat: float
    lng: float
    radius_meters: int = 1000

class ReturnNearbyNFT(BaseModel):
    hint: str
    distance_m: float

class MintNFT(BaseModel):
    secret_code: str
    lat: float
    lng: float

class ReturnMintNFT(BaseModel):
    status: bool

class CreateNFTData(BaseModel):
    name: str = Field(..., max_length=64)
    ton_address: str = Field(..., max_length=66)
    description: str = Field(..., max_length=256)
    lat: float
    lng: float
    hint: str
    owner_wallet: Optional[str] = Field(None, max_length=64)