import aiohttp
import os
from fastapi import HTTPException

async def upload_to_ipfs(file_path: str) -> str:
    ipfs_url = os.getenv("IPFS_URL", "https://ipfs.tonversego.com/api/v0/add")
    
    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f)
                
                async with session.post(ipfs_url, data=data) as response:
                    if response.status == 200:
                        try:
                            result_json = await response.json()
                            hash_value = result_json.get('Hash')
                            if not hash_value:
                                raise HTTPException(
                                    status_code=500,
                                    detail=f"Missing 'Hash' in IPFS response: {result_json}"
                                )
                            return f"ipfs://{hash_value}"
                        except Exception as parse_error:
                            raise HTTPException(
                                status_code=500,
                                detail=f"Failed to parse IPFS response: {parse_error}"
                            )
                    else:
                        error_text = await response.text()
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed to upload file to IPFS. Status: {response.status}, Response: {error_text}"
                        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPFS upload error: {str(e)}")
