from fastapi import APIRouter, Response, Query
from utils.geoposition import Geoposition
from database.models import NFT, User, NFTMintLog
from utils.bot_messages import send_message
from schemas.nft import GetNearbyNFT, ReturnNearbyNFT, MintNFT, ReturnMintNFT

nft_router = APIRouter(prefix="/nft")

@nft_router.get("/nearby")
async def get_nearby_nft(
    response: Response,
    lat: float = Query(..., description="Latitude of user position"),
    lng: float = Query(..., description="Longitude of user position"),
    radius_meters: int = Query(1000, description="Search radius in meters")
) -> list[ReturnNearbyNFT] | list:
    all_nfts = await NFT.filter(is_found=False).all()
    result: list = []

    for nft in all_nfts:
        distance = Geoposition.get_distance((lat, lng), (nft.lat, nft.lng))
        if distance <= radius_meters:
            direction = Geoposition.get_direction((lat, lng), (nft.lat, nft.lng))
            result.append(
                ReturnNearbyNFT(
                    hint=nft.hint,
                    distance_m=distance,
                    direction=direction
                )
            )
    
    return result

@nft_router.post("/mint")
async def mint_nft(data: MintNFT, response: Response) -> ReturnMintNFT:
    user_id = data.secret_code.strip("TonVerseGo_")

    try: user_id = int(user_id)
    except: 
        response.status_code = 403
        return ReturnMintNFT(status=False)

    user = await User.get_or_none(id=user_id)
    if not user:
        response.status_code = 403
        return ReturnMintNFT(status=False)

    all_nfts = await NFT.filter(is_found=False).all()
    nearest_nft = None
    min_distance = float('inf')

    for nft_item in all_nfts:
        distance = Geoposition.get_distance((data.lat, data.lng), (nft_item.lat, nft_item.lng))
        if distance <= 20 and distance < min_distance:
            nearest_nft = nft_item
            min_distance = distance
            
    if not nearest_nft:
        return ReturnMintNFT(status=False)
        
    # Отмечаем NFT как найденный
    nearest_nft.is_found = True
    await nearest_nft.save()
    
    # Создаем запись о минте
    await NFTMintLog.create(
        user=user,
        nft=nearest_nft
    )
    
    await send_message(f"🥳 You found NFT: {nearest_nft.name}", user_id, nearest_nft.photo_url)
    return ReturnMintNFT(status=True)