# routes/todos.py
from flask import Blueprint, jsonify, request, redirect, url_for

# 建立 Blueprint
# 建立一個名為 'todos' 的 Blueprint，並將這個 Blueprint 的名稱設置為 __name__
# Blueprint 扮演類似 module.exports 導出一個路由模塊的功能
todos_bp = Blueprint("todos", __name__)

# 假設有測試資料 todos dummy data
todos = [
    {"id": 1, "name": "Buy groceries", "completed": False},
    {"id": 2, "name": "Read a book", "completed": False},
    {"id": 3, "name": "Write Flask app", "completed": True},
]

# 可以像在 Flask 應用中定義路由一樣，在 Blueprint 中定義路由
@todos_bp.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos), 200


@todos_bp.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo), 200


# 筆記
# 使用了 Flask 的 Blueprint 來組織路由。Blueprint 可以看作是微型應用，可以在應用程式中方便地分割與管理不同的路由，這類似於在 Express 中使用多個路由模組的方式。

# Blueprint 允許你將路由模塊化，便於管理。

# app.register_blueprint() 將 Blueprint 中的路由整合到主應用中。

# 在 Flask 中，Blueprint 和 register_blueprint 提供了一個更清晰的結構來管理大型應用程式的路由，類似於在 Express 中使用 router 和 app.use()。

