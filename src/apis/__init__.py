from fastapi import APIRouter
from src.apis.note_router import router as note_router

public_router = APIRouter(prefix='/v1')

public_router.include_router(note_router)