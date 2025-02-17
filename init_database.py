import os
from sqlalchemy.ext.asyncio import create_async_engine
from models.memo import Base
import asyncio

#DB作成&テーブル作成
base_dir = os.path.dirname(__file__)
# DBのURL
DATABASE_URL = "sqlite+aiosqlite:///" + os.path.join(base_dir, "memodb.sqlite")
# 非同期エンジン作成
engine = create_async_engine(DATABASE_URL, echo=True)
# DB初期化
async def init_db():
    print("=== DBの初期化を開始 ===")
    async with engine.begin() as conn:
        # 既存テーブルの削除
        await conn.run_sync(Base.metadata.drop_all)
        print(">>> 既存のテーブルを削除しました。")
        # テーブル作成
        await conn.run_sync(Base.metadata.create_all)
        print(">>> 新しいテーブルを作成しました。")

if __name__ == "__main__":
    asyncio.run(init_db())