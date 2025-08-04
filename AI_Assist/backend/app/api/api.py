
from fastapi import APIRouter
from app.api.health import health_router as health_router
from app.api.discovery import router as discovery_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(discovery_router)
