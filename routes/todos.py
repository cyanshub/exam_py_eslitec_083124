# routes/todos.py
from flask import Blueprint, jsonify, request, redirect, url_for
from datetime import datetime

# 建立 Blueprint
# 建立一個名為 'todos' 的 Blueprint，並將這個 Blueprint 的名稱設置為 __name__
# Blueprint 扮演類似 module.exports 導出一個路由模塊的功能
# 在這裡指定 url_prefix 為 "/api"，所有這個 Blueprint 中的路由都會自動帶有這個前綴
todos_bp = Blueprint("todos", __name__, url_prefix="/api")

# 假設有測試資料 todos dummy data
from models.data import todos


# 可以像在 Flask 應用中定義路由一樣，在 Blueprint 中定義路由
# 這個路由將會處理用戶提交的 GET 請求，回傳 todos 列表
@todos_bp.route("/todos", methods=["GET"])
def get_todos():
    response = {"status": 200, "data": {"todos": todos}}
    return jsonify(response), 200


# 這個路由將會處理用戶提交的 GET 請求，回傳指定的 todo 資料
@todos_bp.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo is None:
        responese = {"status": 404, "error": "Todo not found"}
        return jsonify(responese), 404
    responese = {"status": 200, "data": {"todo": todo}}
    return jsonify(responese), 200


# 這個路由將會處理用戶提交的 POST 請求，並將新的 Todo 項目加入到 todos 列表
@todos_bp.route("/todos", methods=["POST"])
def post_todo():
    new_todo = request.get_json()
    new_id = max(todo["id"] for todo in todos) + 1 if todos else 1
    new_todo["id"] = new_id
    new_todo["created_at"] = datetime.now().isoformat()
    new_todo["updated_at"] = datetime.now().isoformat()
    todos.append(new_todo)
    response = {"status": 200, "data": {"todo": new_todo}}
    return jsonify(response), 200


# 這個路由將處理 PATCH 請求，允許用戶更新指定的 Todo 項目
@todos_bp.route("/todos/<int:id>", methods=["PATCH"])
def patch_todo(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo is None:
        response = {"status": 404, "error": "Todo not found"}
        return jsonify({"status": 404, "error": "Todo not found"}), 404

    data = request.get_json()
    todo.update({k: v for k, v in data.items() if k in todo})
    todo["updated_at"] = datetime.now().isoformat()

    response = {"status": 200, "data": {"todo": todo}}
    return jsonify(response), 200


# 這個路由將處理 DELETE 請求，允許用戶刪除指定的 Todo 項目
@todos_bp.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    global todos
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo is None:
        response = {"status": 404, "error": "Todo not found"}
        return jsonify(response), 404

    todos = [todo for todo in todos if todo["id"] != id]
    response = {"status": 200, "data": {"todo": todo}}
    return jsonify({"status": 200, "data": {"todo": todo}}), 200


# 這個路由將處理 PATCH 請求，允許用戶變更指定的 Todo 項目的 is_completed 值
@todos_bp.route("/todos/<int:id>/toggleTodoCompleted", methods=["PATCH"])
def toggle_todo_completed(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo is None:
        response = {"status": 404, "error": "Todo not found"}
        return jsonify(response), 404

    todo["is_completed"] = not todo["is_completed"]
    todo["updated_at"] = datetime.now().isoformat()

    response = {"status": 200, "data": {"todo": todo}}
    return jsonify(response), 200


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
