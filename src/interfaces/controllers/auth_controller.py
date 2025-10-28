from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.application.auth_service import AuthService
from src.database.database import get_session
from src.infrastructure.repositories.sql_user_repository import SqlUserRepository


def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    repo = SqlUserRepository(session)
    return AuthService(repo)


class AuthController:
    def __init__(self, service: AuthService = Depends(get_auth_service)):
        self.service = service

    def signup(self, username: str, password: str):
        try:
            return self.service.signup(username=username, password=password)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def token(self, username: str, password: str) -> str:
        token = self.service.authenticate(username=username, password=password)
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return token


