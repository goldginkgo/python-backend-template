from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from asgi_correlation_id import CorrelationIdMiddleware

from app.core.middlewares import request_time_middleware
from app.routers.api_router import api_router
from app.utils.logger import setup_logging
from app.utils.settings import settings

setup_logging(level=settings.log_level, as_json=settings.log_mode_json)

app = FastAPI(title="Backend API", version="0.0.0")

app.add_middleware(CorrelationIdMiddleware)
app.middleware("http")(request_time_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

app.include_router(api_router)
