from fastapi import APIRouter

from api.pillows.router import router as pillows_router

main_router = APIRouter()

main_router.include_router(pillows_router, tags=["Pillows"], prefix="/pillows")
