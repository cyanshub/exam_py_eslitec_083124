# 在一個單一的地方初始化 db 物件, 然後在其他模型文件中導入它。這樣可以確保所有模型都使用同一個 db 實例
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 筆記
# __all__: 這個清單定義了當你使用 from models import * 時，會匯入哪些名稱。這是一個可選的設定，主要用來控制模組的公共 API。

# EX: from models import * 會載入 Todo 模型

# 模型文件中引用 db 時，不要在 models/__init__.py 中直接導入模型
# 確保在 models/__init__.py 中只初始化 db，而不導入具體的模型。這樣就可以避免在 app.py 中初始化 db 時產生循環依賴。
# EX: 這裡不能出現 from .todo import Todo
# EX: 這裡不能出現  __all__ = ["Todo"]
