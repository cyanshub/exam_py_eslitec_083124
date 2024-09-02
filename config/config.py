import os

# 載入環境變數工具
from dotenv import load_dotenv

load_dotenv()  # 加載 .env 檔案


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if os.environ.get("FLASK_ENV") == "production":
        # 遠端環境，使用 DATABASE_URL
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        # 本地環境，使用本地的 MySQL 連接字串
        SQLALCHEMY_DATABASE_URI = "mysql://root:password@127.0.0.1/exam_eslitec"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 筆記
# SQLALCHEMY_TRACK_MODIFICATIONS = False 禁用資料庫修改的訊號追蹤。
# 這是默認的建議設置，因為在大多數情況下不需要追蹤所有的模型變更，而且這樣可以節省系統資源
