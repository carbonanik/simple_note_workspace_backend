from pydantic import BaseModel


class SignupSchema(BaseModel):
    username: str
    password: str


class TokenRequestSchema(BaseModel):
    username: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


