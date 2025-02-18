from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from routers.memo import router as memo_router
from schemas.memo import ResponseSchema, InsertAndUpdateMemoSchema

app = FastAPI()

# CORS設定
origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ルーターのマウント
app.include_router(memo_router)

# バリデーションエラーのカスタムハンドラ
@app.exception_handler(ValidationError)
async def validation_exception_handler(exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.model
        }
    )