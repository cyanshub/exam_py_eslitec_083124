# 載入工具
from flask import Blueprint


# 載入 controller
from controllers.todo_controller import TodoController


# 設計路由
# 建立 Blueprint
todos_bp = Blueprint("todos", __name__, url_prefix="/api")


# 在 Blueprint 中定義路由
# 這個路由將會處理用戶提交的 GET 請求，回傳 todos 列表
@todos_bp.route("/todos", methods=["GET"])
def get_todos():
    return TodoController.get_todos()


# 這個路由將會處理用戶提交的 GET 請求，回傳指定的 todo 資料
@todos_bp.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    return TodoController.get_todo(id)


# 這個路由將會處理用戶提交的 POST 請求，並將新的 Todo 項目加入到 todos 列表
@todos_bp.route("/todos", methods=["POST"])
def post_todo():
    return TodoController.post_todo()


# 這個路由將處理 PATCH 請求，允許用戶更新指定的 Todo 項目
@todos_bp.route("/todos/<int:id>", methods=["PATCH"])
def patch_todo(id):
    return TodoController.patch_todo(id)


# 這個路由將處理 DELETE 請求，允許用戶刪除指定的 Todo 項目
@todos_bp.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    return TodoController.delete_todo(id)


# 這個路由將處理 PATCH 請求，允許用戶變更指定的 Todo 項目的 is_completed 值
@todos_bp.route("/todos/<int:id>/toggleTodoCompleted", methods=["PATCH"])
def toggle_todo_completed(id):
    return TodoController.toggle_todo_completed(id)


# 筆記
# 使用了 Flask 的 Blueprint 來組織路由。Blueprint 可以看作是微型應用，可以在應用程式中方便地分割與管理不同的路由，這類似於在 Express 中使用多個路由模組的方式。

# Blueprint 允許你將路由模塊化，便於管理。

# app.register_blueprint() 將 Blueprint 中的路由整合到主應用中。

# 在 Flask 中，Blueprint 和 register_blueprint 提供了一個更清晰的結構來管理大型應用程式的路由，類似於在 Express 中使用 router 和 app.use()。


# patchTodo - 更新指定資料
# todo.update({k: v for k, v in data.items() if k in todo}) 解釋
# 1. data.items()：data 是從請求的 JSON 請求體中獲得的字典。data.items() 會返回一個包含鍵值對的迭代器。例如，data 可能是 {"name": "Updated Task", "completed": true}

# 2. {k: v for k, v in data.items() if k in todo}：這是一個字典推導式，用來生成一個新的字典，僅包含 data 中鍵存在於 todo 中的項目。 k 和 v 分別代表 data 中的鍵和值。

# 3. if k in todo：這個條件語句確保只更新 todo 中已存在的鍵。比如，如果 todo 是 {"id": 1, "name": "Buy groceries", "completed": False}，那麼它只會更新 name 和 completed，而不會添加新鍵


# deleteTodo - 刪除指定資料
# global todos
# todos = [todo for todo in todos if todo["id"] != id]
# 1. global todos：這行代碼聲明 todos 為全局變數，確保在函數內對 todos 進行的操作會影響到全局範圍內的 todos 列表。如果不使用 global 關鍵字，函數內的 todos 會被當作局部變數，無法影響全局的 todos 列表。

# 2. todos = [todo for todo in todos if todo["id"] != id]：這是一個列表推導式，用來生成一個新的列表，該列表只包含那些 ID 不等於 id 的 Todo 項目。


# 在 Flask 中使用 SQLAlchemy 操作資料庫時，以下是一些常用操作的語法
# 查詢指定資料：Todo.query.filter_by() 或 Todo.query.filter()。
# 新增一筆資料：創建新實例並使用 db.session.add()。
# 更新指定資料：查詢後修改屬性並使用 db.session.commit()。
# 刪除指定資料：查詢後使用 db.session.delete()。


# 建立 Blueprint
# 建立一個名為 'todos' 的 Blueprint，並將這個 Blueprint 的名稱設置為 __name__
# Blueprint 扮演類似 module.exports 導出一個路由模塊的功能
# 在這裡指定 url_prefix 為 "/api"，所有這個 Blueprint 中的路由都會自動帶有這個前綴


# 路由重構
# 構建路由和處理邏輯的橋樑：Flask 的裝飾器（如 @todos_bp.route）會將 def 定義的函數與一個具體的 URL 路徑和 HTTP 方法（GET、POST 等）綁定，從而在用戶請求這個 URL 時，自動執行該函數的邏輯


# 為什麼 def 不能省略：
# 在 Flask 中，裝飾器必須裝飾一個函數，這個函數可以是用 def 定義的，也可以是 lambda 函數（但仍然是一個函數）。
# 如果你不使用 def 或 lambda 定義函數，就無法滿足 Flask 路由裝飾器的需求，系統無法知道該如何處理特定路徑的請求。
