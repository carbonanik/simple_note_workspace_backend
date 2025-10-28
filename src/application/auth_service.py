from typing import Optional
from src.domain.entities.user import UserEntity
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security.passwords import hash_password, verify_password
from src.infrastructure.security.jwt import create_access_token


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def signup(self, username: str, password: str) -> UserEntity:
        existing = self.users.get_by_username(username)
        if existing:
            raise ValueError("Username already exists")
        hashed = hash_password(password)
        user = UserEntity(id=None, username=username, hashed_password=hashed)
        return self.users.create_user(user)

    def authenticate(self, username: str, password: str) -> Optional[str]:
        user = self.users.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        token = create_access_token(subject=user.username)
        return token


