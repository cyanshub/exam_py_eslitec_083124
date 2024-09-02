from . import db
from sqlalchemy.sql import func


# 定義 Todo Model, 讓 SQLAlchemy ORM 模型與資料庫溝通
class Todo(db.Model):
    # 資料表名稱
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.String(255), nullable=True)
    time = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    creator = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())  # 設置預設值為當前時間
    updated_at = db.Column(
        db.DateTime, default=func.now(), onupdate=func.now()
    )  # 設置預設值, 並在資料更新時, 自動更新為當前時間

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "remarks": self.remarks,
            "time": self.time,
            "date": self.date.isoformat(),  # datetime 轉換為 ISO 字符串
            "location": self.location,
            "creator": self.creator,
            "isCompleted": self.is_completed,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
