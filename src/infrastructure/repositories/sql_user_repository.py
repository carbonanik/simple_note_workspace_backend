from typing import Optional
from sqlmodel import Session, select
from src.domain.entities.user import UserEntity
from src.domain.repositories.user_repository import UserRepository
from src.models.user import User


class SqlUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[UserEntity]:
        db_user = self.session.exec(select(User).where(User.username == username)).first()
        if not db_user:
            return None
        return UserEntity(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password)

    def create_user(self, user: UserEntity) -> UserEntity:
        db_user = User(username=user.username, hashed_password=user.hashed_password)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserEntity(id=db_user.id, username=db_user.username, hashed_password=db_user.hashed_password)


