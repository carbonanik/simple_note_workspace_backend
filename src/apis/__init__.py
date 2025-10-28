from fastapi import APIRouter
from src.apis.note_router import router as note_router
from src.apis.auth_router import router as auth_router

public_router = APIRouter(prefix='/v1')

public_router.include_router(auth_router)
public_router.include_router(note_router)