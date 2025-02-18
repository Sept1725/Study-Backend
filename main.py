from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from routers.memo import router as memo_router
from schemas.memo import ResponseSchema, InsertAndUpdateMemoSchema

app = FastAPI()

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

app.include_router(memo_router)

# メモ更新
@app.put("/memos/{id}", response_model=ResponseSchema)
async def modify_memo(id: int, memo: InsertAndUpdateMemoSchema):
    print(id, memo)
    return ResponseSchema(message="メモが正常に更新されました")

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