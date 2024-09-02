# routes/__init__.py
from .todos import todos_bp


# 筆記
# 如果在 routes 資料夾建立 __init__.py 檔案, 則 routes 資料夾可變成管理模組導出的入口, 則 app.py 的導入方式可以多一種寫法
# 原寫法 from routes.todos import todos_bp
# 簡化寫法 from routes import todos_bp
