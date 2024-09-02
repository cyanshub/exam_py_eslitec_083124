# 從 Flask 模組中導入了 Flask 類。Flask 是一個輕量級的 Python Web 框架
from flask import Flask


# 創建了一個 Flask 應用的實例, 並將其存儲在變數 app 中
app = Flask(__name__)


# 這行是 Flask 的路由裝飾器，用來告訴 Flask 哪個 URL 應該觸發對應的函數
@app.route("/")
# 這是一個名為 hello 的函數，當訪問應用程式的根 URL 時，這個函數會被執行
def hello():
    # 函數返回的內容
    return "Hello from flask"

if __name__ == "__main__":
    print("app.py is being run directly")
    app.run(host="0.0.0.0", port=3000, debug=True)
else:
    print("app.py has been imported")


# 專案筆記
# 建立專案目錄
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
