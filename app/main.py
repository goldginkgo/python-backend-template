from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.api_router import api_router
from app.settings import settings
from app.utils.logger import setup_logging

setup_logging(level=settings.log_level, as_json=settings.log_mode_json)

app = FastAPI(title="Backend API", version="0.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
