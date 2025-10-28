from dataclasses import dataclass


@dataclass
class UserEntity:
    id: int | None
    username: str
    hashed_password: str


