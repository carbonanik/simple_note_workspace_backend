from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.models.response_model import ResponseModel
from src.database.database import create_db_and_tables
from src.apis import public_router

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle FastAPI HTTPException
@app.exception_handler(HTTPException)
async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(message=str(exc.detail), data=None).model_dump(),
    )

# Handle validation errors (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ResponseModel(message="Validation error", data=exc.errors()).dict(),
    )

app.include_router(public_router)

@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
    except Exception as e:
        print(e)
   