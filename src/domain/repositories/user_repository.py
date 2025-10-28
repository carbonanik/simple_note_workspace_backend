from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        ...


