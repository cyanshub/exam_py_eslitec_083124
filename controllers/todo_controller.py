# 載入工具
from models import db  # 操作資料庫會話
from datetime import datetime, date  # 日期工具
from flask import jsonify, request  # 發送資料, 接收請求

# 載入操作資料表的 Model
from models.todo import Todo


# python 的 class 的命名習慣為字母開頭大寫
class TodoController:
    # 這個路由將會處理用戶提交的 GET 請求，回傳 todos 列表
    @staticmethod
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
    @staticmethod
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
    @staticmethod
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
                            jsonify(
                                {"status": 422, "error": f"Invalid value for {key}"}
                            ),
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
    @staticmethod
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
                            jsonify(
                                {"status": 422, "error": f"Invalid value for {key}"}
                            ),
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
    @staticmethod
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
    @staticmethod
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
# @staticmethod 是 Python 中的裝飾器，表示這個方法是類別的靜態方法。靜態方法與實例方法不同，它不需要依賴類別的實例來運作，也不會接收 self 或 cls 參數。它們本質上是與類別相關但獨立於任何具體實例的函數。靜態方法常用來將一些不需要操作實例屬性或類別屬性的邏輯封裝在類別中，使程式結構更為清晰
