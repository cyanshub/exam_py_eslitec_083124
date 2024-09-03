# Python Backend App for React TodoList Project
![導覽圖片](/introduce.png)

## 介紹
+ 此專案使用 Python/Flask 來新增一個 TODO 任務項目
+ 每個 TODO 任務項目包含

| Name          | Content   | Remarks        | Time         | Date     | Location    | Creator  | Completed  |
|---------------|-----------|----------------|--------------|----------|-------------|----------|------------|
| 待辦任務名稱   | 內容       | 備註           | 預計時間     | 日期      | 地點        | 創建者    | 是否完成   |



## TEST API routes

| 功能           | 方法  | 路徑                                                                                         |
|----------------|-------|---------------------------------------------------------------------------------------------|
| 取得任務 (Get)  | GET   | https://exam-py-eslitec-083124.onrender.com/api/todos           |
| 新增任務 (Add)  | POST  | https://exam-py-eslitec-083124.onrender.com/api/todos           |
| 編輯任務 (Edit) | PATCH | https://exam-py-eslitec-083124.onrender.com/api/todos/:id       |
| 刪除任務 (Delete) | DELETE | https://exam-py-eslitec-083124.onrender.com/api/todos/:id    |
| 更新完成任務  | PATCH | https://exam-py-eslitec-083124.onrender.com/api/todos/:id/toggleTodoCompleted       |




## 使用 curl 指令工具快速測試後端 API
- 為了方便快速測試後端API, 可以打開 Git Bash 終端機, 輸入以下提供的 curl 指令


### GET api/todos 列出所有 TODO 任務
- 使用以下指令來取得所有 TODO 任務, 並使用 jq 來格式化輸出
```bash
curl --location 'https://exam-py-eslitec-083124.onrender.com/api/todos' | jq
```


### POST api/todos 創建新的 TODO 任務
- 使用以下指令來創建一個新的 TODO 任務
```bash
curl --location 'https://exam-py-eslitec-083124.onrender.com/api/todos' \
--header 'Content-Type: application/json' \
--data '{
"name": "Writing Project",
"content": "Writing Project for FullStack",
"remarks": "Think first",
"time": 4,
"date": "2024-8-31",
"location": "",
"creator": "Chin-yang, Huang"
}'
```


### PATCH api/todos/:id 更新指定的 TODO 任務內容
- 使用以下指令來更新指定 id 的 TODO 任務
- 可先用 GET API 查看並修正以下範例的 id (調整 id = 42 為新的 id)
```bash
curl --location --request PATCH 'https://exam-py-eslitec-083124.onrender.com/api/todos/42' \
--header 'Content-Type: application/json' \
--data '{
"name": "Writing Project",
"content": "FullStack Project using NodeJS, python, and React",
"remarks": "Think first",
"time": 4,
"date": "2024-8-31",
"location": "At home",
"creator": "Chin-yang, Huang"
}'
```

### PATCH api/todos/:id/toggleTodoCompleted 切換指定的 TODO 任務內容的完成狀態
- 使用以下指令來切換指定 id 的 TODO 任務的完成狀態
- 可先用 GET API 查看並修正以下範例的 id (調整 id = 42 為新的 id)
```bash
curl --location --request PATCH 'https://exam-py-eslitec-083124.onrender.com/api/todos/42/toggleTodoCompleted'
```

### DELETE api/todos/:id 刪除指定的 TODO 任務內容
- 使用以下指令來刪除指定 id 的 TODO 任務
- 可先用 GET API 查看並修正以下範例的 id (調整 id = 42 為新的 id)
```bash
curl --location --request DELETE 'https://exam-py-eslitec-083124.onrender.com/api/todos/42'
```




## TEST API documentation
+ 詳細的 API 測試文件可以在以下網址查看：
[TEST API DOC](https://scarlet-page-533.notion.site/1130831-Exam-Todos-Web-APIs-580daf37aa224a19b2d67f373b814eda)

+ 您可以使用 Postman 工具, 並參考 TEST API documentation 說明，測試本專案的 API 功能




## 前端網站互動
您可以透過另外由 React 建立的網站來與本專案提供的 API 功能進行互動：
[REACT WEBSITE](https://cyanshub.github.io/exam_react_eslitec_083124/todos)



## 開始使用
+ 請在本機安裝 Python 3.x（建議使用 3.8 或以上版本）
+ 本專案採用 Python 3.11.6 進行開發，請確認版本的一致性：Bash 指令 `python --version`
+ 複製專案到本機: Bash 指令 `git clone https://github.com/cyanshub/exam_py_eslitec_083124.git`
+ 進入專案資料夾: Bash 指令 `cd exam_py_eslitec_083124`
+ 建立虛擬環境：Bash 指令 `python -m venv .venv`
+ 啟動虛擬環境：
  - 在 Windows：Bash 指令 `.\.venv\Scripts\activate`
  - 在 Mac/Linux：Bash 指令 `source .venv/bin/activate`

+ 安裝套件：Bash 指令 `pip install -r requirements.txt`
+ 確認套件齊全(可參考下方開發工具)
+ 建立 .env 檔案並填入相關資料(可參考 `.env example` 文件): Bash 指令 `touch .env`
+ 本專案可透過設定連線字串之環境變數, 連接 MySQL 遠端資料庫 `DATABASE_URL=mysql://jgadep9sfn7v09ki:fjjqdqknpv3d9syw@qzkp8ry756433yd4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/ud7dsi40j73js8nb`
+ 設定連接遠端 MySQL 資料庫 (本專案與 NodeJS 專案連到同一個資料庫):
  - username: `jgadep9sfn7v09ki`
  - password: `fjjqdqknpv3d9syw`
  - host: `qzkp8ry756433yd4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com`
  - port: `3306`
  - database: `ud7dsi40j73js8nb`
  - dialect: `mysql`
 

+ 啟動專案: Bash 指令 `python app.py`
+ 看到以下訊息，可至瀏覽器輸入下列網址開啟 `Todo-list application is listening on: http://localhost:3000`


## 開發工具
### 依賴項目 (Dependencies)
+ blinker: 1.8.2
+ click: 8.1.7
+ colorama: 0.4.6
+ Flask: 3.0.3
+ Flask-Cors: 5.0.0
+ Flask-SQLAlchemy: 3.1.1
+ greenlet: 3.0.3
+ itsdangerous: 2.2.0
+ Jinja2: 3.1.4
+ MarkupSafe: 2.1.5
+ mysqlclient: 2.2.4
+ python-dotenv: 1.0.1
+ SQLAlchemy: 2.0.32
+ typing_extensions: 4.12.2
+ Werkzeug: 3.0.4


