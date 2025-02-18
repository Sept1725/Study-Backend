from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.memo import InsertAndUpdateMemoSchema, MemoSchema, ResponseSchema
import cruds.memo as memo_crud
import db

# ルーターを作成し、タグとURLパスのプレフィックスを設定
router = APIRouter(tags=["Memos"], prefix="/memos")

# 新規作成のエンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_memo(
    memo: InsertAndUpdateMemoSchema,
    db: AsyncSession = Depends(db.get_dbsession)
):
    try:
        # 新しいメモをDBに登録
        await memo_crud.insert_memo(db, memo)
        return ResponseSchema(message="メモが正常に登録されました")
    except Exception as e:
        # 登録失敗の場合はHTTP 400エラーを返す
        raise HTTPException(status_code=400, detail="メモの登録に失敗しました")

# 全件取得のエンドポイント
@router.get("/", response_model=list[MemoSchema])
async def get_memos_list(
    db: AsyncSession = Depends(db.get_dbsession)
):
    # 全てのメモをDBから取得
    memos = await memo_crud.get_memos(db)

    return memos

# 1件取得のエンドポイント
@router.get("/{id}", response_model=MemoSchema)
async def get_memo_detail(
    id: int,
    db: AsyncSession = Depends(db.get_dbsession)
):
    # 指定されたIDのメモをDBから取得
    memo = await memo_crud.get_memo_by_id(db, id)
    if not memo:
        # メモが見つからない場合はHTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="対象のメモが見つかりません")
    
    return memo

# 1件更新のエンドポイント
@router.put("/{id}", response_model=ResponseSchema)
async def modify_memo(id: int, memo: InsertAndUpdateMemoSchema, db: AsyncSession = Depends(db.get_dbsession)):
    # 指定されたIDのメモを新しいデータで更新
    updated_memo = await memo_crud.update_memo(db, id, memo)
    if not updated_memo:
        # 更新対象のメモが見つからない場合はHTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")

    return ResponseSchema(message="メモが正常に更新されました")

# 1件削除のエンドポイント
@router.delete("/{id}", response_model=ResponseSchema)
async def remove_memo(
    id: int,
    db: AsyncSession = Depends(db.get_dbsession)
):
    # 指定されたIDのメモをDBから削除
    result = await memo_crud.delete_memo(db, id)
    if not result:
        # 削除対象が見つからない場合はHTTP404エラーを返す
        raise HTTPException(status_code=404, detail="削除対象のメモが見つかりません")
    
    return ResponseSchema(message="メモが正常に削除されました")