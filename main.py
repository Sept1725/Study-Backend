from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from schemas.memo import InsertAndUpdateMemoSchema, MemoSchema, ResponseSchema

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

#  新規登録
@app.post("/memos", response_model=ResponseSchema)
async def create_memo(memo: InsertAndUpdateMemoSchema):
    print(memo)
    return ResponseSchema(message="メモが正常に登録されました")

# 全件取得
@app.get("/memos", response_model=list[MemoSchema])
async def get_memos_list():
    return [
        MemoSchema(title="タイトル1", description="詳細1", id=1),
        MemoSchema(title="タイトル2", description="詳細2", id=2),
        MemoSchema(title="タイトル3", description="詳細3", id=3),
    ]

# 特定のメモ取得
@app.get("/memos/{memo_id}", response_model=MemoSchema)
async def get_memo_detail(memo_id: int):
    return MemoSchema(title="タイトル1", description="詳細1", id=memo_id),

# 特定のメモ更新
@app.put("/memos/{memo_id}", response_model=ResponseSchema)
async def modify_memo(memo_id: int, memo: InsertAndUpdateMemoSchema):
    print(memo_id, memo)
    return ResponseSchema(message=f"id: {memo_id}のメモが正常に更新されました")

# 特定のメモ削除
@app.delete("/memos/{memo_id}", response_model=ResponseSchema)
async def delete_memo(memo_id: int):
    print(memo_id)
    return ResponseSchema(message=f"id: {memo_id}のメモが正常に削除されました")

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