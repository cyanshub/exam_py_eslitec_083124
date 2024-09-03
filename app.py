# 從 Flask 模組中導入了 Flask 類。Flask 是一個輕量級的 Python Web 框架
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from config.config import Config  # 載入配置
from models import db  # 從 models/__init__.py 導入 db


# 從 routes 資料夾中載入 todos 路由
from routes import todos_bp


# 創建了一個 Flask 應用的實例, 並將其存儲在變數 app 中
app = Flask(__name__)

# 應對瀏覽器 CORS (Cross-Origin Resource Sharing) 政策
CORS(app)  # 為所有路由啟用 CORS

app.config.from_object(Config)  # 使用配置


# 初始化資料庫: 即使 Flask 可以透過 SQLAlchemy 與資料庫溝通
db.init_app(app)

# 設計路由
# 路由: 註冊 Blueprint
app.register_blueprint(todos_bp)  # 相當於 Express 中的 app.use()


# 路由: 設計重導向
@app.route("/")
def index():
    return redirect(url_for("todos.get_todos"))


# 路由: 捕捉所有異常並返回 response
@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response


# 路由: 處理未匹配的路徑, 重導向到根路由
@app.errorhandler(404)
#  error 是 Flask 錯誤處理函數中的一個參數, 代表異常物件, 可以是其他合法的名稱
def page_not_found(errpr):
    return redirect(url_for("index"))


# 這行是 Flask 的路由裝飾器，用來告訴 Flask 哪個 URL 應該觸發對應的函數
@app.route("/")
# 這是一個名為 hello 的函數，當訪問應用程式的根 URL 時，這個函數會被執行
def hello():
    # 函數返回的內容
    return "Hello from flask"


if __name__ == "__main__":
    port = 3000
    print(f"Todo-list application is listening on http://localhost:{port}")
    app.run(host="0.0.0.0", port=3000, debug=True)
else:
    print("app.py has been imported")


# 專案筆記
# (1) 建立專案目錄
# 建立虛擬環境：python -m venv .venv
# 啟動虛擬環境  EX: .\.venv\Scripts\activate
# 若要退出虛擬環境 EX: deactivate
# 安裝 Flask：pip install Flask
# 建立 app.py：並撰寫 Flask 程式碼
# 建立 requirements.txt  EX: pip freeze > requirements.txt
# 運行應用程式：python app.py，啟動伺服器

# 127.0.0.1 或 localhost 代表本地機器，僅本機可訪問。
# EX: app.run(host='localhost', port=3000)   EX: app.run(host='0.0.0.0', port=3000)
# 將 host 設置為 0.0.0.0 可以讓應用程式接受來自任何網絡介面的請求，從而允許局域網內的其他設備訪問
# 127.0.0.1 同意於 localhost
# 192.168.0.6 代表局域網中的 IP 地址，其他同網絡設備可以訪問。
# 將應用程式埠號改為 3000 只需修改 app.run() 中的 port 參數。
# 可以直接在程式碼中, 利用 debug=True 啟用開發模式，如下所示
# EX: app.run(host='0.0.0.0', port=3000, debug=True)


# (2) 設計路由
# 在 Blueprint 中定義了路由後，需要在主應用中「註冊」這個 Blueprint，以便將它的路由整合到主應用中。這就是 app.register_blueprint() 的作用
# register_blueprint 相當於 Express 中的 app.use()

# 在 Python 中，from routes.todos import todos_bp 是用來從 routes 資料夾中的 todos.py 文件中導入 todos_bp 這個 Blueprint 物件的語法; 與 JavaScript 中的 module.exports 是不同的概念，但它們都實現了將模塊或物件從一個文件導入到另一個文件中的功能

# CORS 設置：使用 CORS(app) 在全局啟用 CORS，這意味著所有的路由請求都會自動帶有 Access-Control-Allow-Origin 的 heaeder，解決跨域問題。
