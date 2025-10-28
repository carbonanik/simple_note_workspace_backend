from fastapi import APIRouter, Depends, status
from src.interfaces.controllers.auth_controller import AuthController
from src.interfaces.schemas.auth import SignupSchema, TokenRequestSchema, TokenResponseSchema
from src.models.response_model import ResponseModel


router = APIRouter(prefix="/auth", tags=["auth"]) 


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupSchema, controller: AuthController = Depends()):
    user = controller.signup(username=payload.username, password=payload.password)
    return ResponseModel(message="User created", data={"id": user.id, "username": user.username})


@router.post("/token", response_model=ResponseModel[TokenResponseSchema])
async def login(payload: TokenRequestSchema, controller: AuthController = Depends()):
    token = controller.token(username=payload.username, password=payload.password)
    return ResponseModel(data=TokenResponseSchema(access_token=token), message="Token issued")


