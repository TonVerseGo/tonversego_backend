from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.admin import admin_router
from routers.nft import nft_router
from routers.user import user_router
from database import init, close

async def lifespan(app: FastAPI):
    await init()
    yield
    await close()

app = FastAPI(title="TonVerse GO! API", version="0.0.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(nft_router)
app.include_router(user_router)