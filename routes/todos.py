# routes/todos.py
from flask import Blueprint, jsonify, request
from datetime import datetime, date

# 操作資料庫會話時會用到
from models import db

# 從 models/todo.py 載入 Todo Model
from models.todo import Todo

# 建立 Blueprint
# 建立一個名為 'todos' 的 Blueprint，並將這個 Blueprint 的名稱設置為 __name__
# Blueprint 扮演類似 module.exports 導出一個路由模塊的功能
# 在這裡指定 url_prefix 為 "/api"，所有這個 Blueprint 中的路由都會自動帶有這個前綴
todos_bp = Blueprint("todos", __name__, url_prefix="/api")

# # 假設有測試資料 todos dummy data => 因為使用 MySQL 的資料, 故註解掉
# from models.data import todos


# 可以像在 Flask 應用中定義路由一樣，在 Blueprint 中定義路由
# 這個路由將會處理用戶提交的 GET 請求，回傳 todos 列表
@todos_bp.route("/todos", methods=["GET"])
def get_todos():
    try:
        # 查詢資料庫中的所有 Todo 項目
        todo_instances = Todo.query.all()

        # 將每個 Todo 實例轉換為可序列化的字典
        todos = [todo.to_dict() for todo in todo_instances]

        response = {"status": 200, "data": {"todos": todos}}
        return jsonify(response), 200

    except Exception as e:
        # 捕捉任何資料庫錯誤，並返回500
        return (
            jsonify({"status": 500, "error": "Database error", "message": str(e)}),
            500,
        )


# 這個路由將會處理用戶提交的 GET 請求，回傳指定的 todo 資料
@todos_bp.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    try:
        # 查詢指定 id 的 Todo 項目
        todo_instance = Todo.query.filter_by(id=id).first()

        # 如果找不到實例，返回 404
        if todo_instance is None:
            return jsonify({"status": 404, "error": "Todo not found"}), 404

        # 將 Todo 實例轉換為字典
        todo = todo_instance.to_dict()

        response = {"status": 200, "data": {"todo": todo}}
        return jsonify(response), 200

    except Exception as e:
        # 捕捉任何資料庫錯誤，並返回 500
        return (
            jsonify({"status": 500, "error": "Database error", "message": str(e)}),
            500,
        )


# 這個路由將會處理用戶提交的 POST 請求，並將新的 Todo 項目加入到 todos 列表
@todos_bp.route("/todos", methods=["POST"])
def post_todo():
    try:
        new_todo = request.get_json()

        # 將 time 和 date 先進行轉換
        if "time" in new_todo:
            try:
                new_todo["time"] = float(new_todo["time"])
            except ValueError:
                return (
                    jsonify({"status": 422, "error": "Invalid value for time"}),
                    422,
                )

        if "date" in new_todo:
            try:
                new_todo["date"] = datetime.strptime(
                    new_todo["date"], "%Y-%m-%d"
                ).date()
            except ValueError:
                return (
                    jsonify(
                        {
                            "status": 422,
                            "error": "Invalid date format, should be YYYY-MM-DD",
                        }
                    ),
                    422,
                )

        # 定義需要驗證的屬性及其驗證規則
        validation_rules = {
            "name": lambda v: isinstance(v, str) and v.strip(),
            "content": lambda v: isinstance(v, str) and v.strip(),
            "time": lambda v: isinstance(v, float) and v > 0,
            "date": lambda v: isinstance(v, date),
            "creator": lambda v: isinstance(v, str) and v.strip(),
            # 允許為空值
            "remarks": lambda v: v is None or isinstance(v, str),
            "location": lambda v: v is None or isinstance(v, str),
        }

        # 驗證並處理資料
        for key, value in new_todo.items():
            if key in validation_rules:
                if not validation_rules[key](value):
                    return (
                        jsonify({"status": 422, "error": f"Invalid value for {key}"}),
                        422,
                    )

        # 創建新的 Todo 實例
        new_todo_instance = Todo(
            name=new_todo["name"],
            content=new_todo["content"],
            remarks=new_todo.get("remarks", ""),
            time=new_todo["time"],
            date=new_todo["date"],
            location=new_todo.get("location", ""),
            creator=new_todo["creator"],
            is_completed=new_todo.get("isCompleted", False),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # 加入資料庫並提交
        db.session.add(new_todo_instance)
        db.session.commit()

        response = {"status": 200, "data": {"todo": new_todo_instance.to_dict()}}
        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": 500, "error": "Database error", "message": str(e)}),
            500,
        )


# 這個路由將處理 PATCH 請求，允許用戶更新指定的 Todo 項目
@todos_bp.route("/todos/<int:id>", methods=["PATCH"])
def patch_todo(id):
    try:
        todo_instance = Todo.query.filter_by(id=id).first()

        # 如果找不到實例，返回 404
        if todo_instance is None:
            return jsonify({"status": 404, "error": "Todo not found"}), 404

        data = request.get_json()

        # 將 time 和 date 先進行轉換
        if "time" in data:
            try:
                data["time"] = float(data["time"])
            except ValueError:
                return (
                    jsonify({"status": 422, "error": "Invalid value for time"}),
                    422,
                )

        if "date" in data:
            try:
                data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").date()
            except ValueError:
                return (
                    jsonify(
                        {
                            "status": 422,
                            "error": "Invalid date format, should be YYYY-MM-DD",
                        }
                    ),
                    422,
                )

        # 定義驗證規則
        validation_rules = {
            "name": lambda v: isinstance(v, str) and v.strip(),
            "content": lambda v: isinstance(v, str) and v.strip(),
            "time": lambda v: isinstance(v, float) and v > 0,
            "date": lambda v: isinstance(v, date),
            "creator": lambda v: isinstance(v, str) and v.strip(),
            "remarks": lambda v: v is None or isinstance(v, str),
            "location": lambda v: v is None or isinstance(v, str),
        }

        # 驗證並更新資料
        for key, value in data.items():
            if key in validation_rules:
                if not validation_rules[key](value):
                    return (
                        jsonify({"status": 422, "error": f"Invalid value for {key}"}),
                        422,
                    )

            setattr(todo_instance, key, value)

        todo_instance.updated_at = datetime.now()
        db.session.commit()

        response = {"status": 200, "data": {"todo": todo_instance.to_dict()}}
        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": 500, "error": "Database error", "message": str(e)}),
            500,
        )


# 這個路由將處理 DELETE 請求，允許用戶刪除指定的 Todo 項目
@todos_bp.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    try:
        todo_instance = Todo.query.filter_by(id=id).first()

        # 如果找不到實例，返回 404
        if todo_instance is None:
            return jsonify({"status": 404, "error": "Todo not found"}), 404

        # 刪除實例並提交變更
        db.session.delete(todo_instance)
        db.session.commit()

        response = {"status": 200, "data": {"todo": todo_instance.to_dict()}}
        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": 500, "error": "Database error", "message": str(e)}),
            500,
        )


# 這個路由將處理 PATCH 請求，允許用戶變更指定的 Todo 項目的 is_completed 值
@todos_bp.route("/todos/<int:id>/toggleTodoCompleted", methods=["PATCH"])
def toggle_todo_completed(id):
    try:
        todo_instance = Todo.query.filter_by(id=id).first()

        # 如果找不到實例，返回 404
        if todo_instance is None:
            return jsonify({"status": 404, "error": "Todo not found"}), 404

        # 切換 is_completed 狀態
        todo_instance.is_completed = not todo_instance.is_completed
        todo_instance.updated_at = datetime.now()

        db.session.commit()

        response = {"status": 200, "data": {"todo": todo_instance.to_dict()}}
        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": 500, "error": "Database error", "message": str(e)}),
            500,
        )


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
