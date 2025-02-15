from pydantic import BaseModel, Field

# 登録・更新で使用するスキーマ
class InsertAndUpdateMemoSchema(BaseModel):
    title: str = Field(..., description="メモのタイトル。1文字以上入力が必須。", example="明日のアジェンダ作成", min_length=1)
    description: str = Field(default="", description="メモの内容の追加情報。任意。", example="14:00まで")

# メモ情報を表すスキーマ
class MemoSchema(InsertAndUpdateMemoSchema):
    id: int = Field(..., description="メモを一意に識別するためのID。データベースで自動割り当て。", example=123)

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    message: str = Field(..., description="API操作の結果を説明するメッセージ。", example="メモ更新成功")