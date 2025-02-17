from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from datetime import datetime

class Memo(Base):
    # テーブル名
    __tablename__ = "memos"
    # メモID: PK, 自動インクリメント
    id = Column(Integer, primary_key=True, autoincrement=True)
    # タイトル: 未入力不可
    title = Column(String(50), nullable=False)
    # 詳細
    description = Column(String(225), nullable=True)
    # 作成日時: デフォルト=datetime.now()
    created_at = Column(DateTime, default=datetime.now())
    # 更新日時
    update_at = Column(DateTime)