import aiohttp
import aiofiles
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

async def download_from_ipfs(ipfs_hash: str, save_path: str) -> None:
    """
    Download a file from IPFS using the hash and save it locally.

    :param ipfs_hash: The IPFS hash of the file to download.
    :param save_path: The local path where the file should be saved.
    """
    ipfs_gateway_url = os.getenv("IPFS_GATEWAY_URL", "https://ipfs.io/ipfs/")
    file_url = f"{ipfs_gateway_url}{ipfs_hash}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    async with aiofiles.open(save_path, 'wb') as f:
                        await f.write(await response.read())
                else:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to download file from IPFS. Status: {response.status}, Response: {error_text}"
                    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPFS download error: {str(e)}")
