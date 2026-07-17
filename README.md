# FastAPI CI/CD Demo (đã bổ sung Database CRUD - pyDAL)

Project gốc của bạn (calculator API + CI/CD pipeline) + phần Database CRUD
dùng pyDAL mà thầy yêu cầu thêm.

## Cấu trúc

```
fastapi-cicd-demo/
├── app/
│   ├── main.py        # API: /, /health, /add, /divide + CRUD /items
│   └── database.py     # Lớp pyDAL — CRUD không viết SQL
├── tests/
│   └── test_main.py    # 10 test: calculator + CRUD
├── requirements.txt
├── Dockerfile
└── .github/workflows/ci.yml   # test -> build & push image lên GHCR
```

## Phần Database (pyDAL) — đúng yêu cầu của thầy

`app/database.py` dùng **pyDAL** (data-abstraction-layer, thành phần lõi của
py4web):

- Khai báo bảng bằng `Field` trong Python — **không viết câu lệnh SQL nào**.
  pyDAL tự sinh SQL, tự tạo bảng (`migrate=True`).
- Đổi database chỉ cần đổi biến môi trường `DATABASE_URL`, **không sửa code**:
  - SQLite (mặc định, dùng khi test/local): `sqlite://storage.db`
  - PostgreSQL: `postgres://user:password@host:port/dbname`
  - MySQL: `mysql://user:password@host:port/dbname`
  - MongoDB: `mongodb://user:password@host:port/dbname`

Endpoint CRUD: `GET/POST /items`, `GET/PUT/DELETE /items/{id}`.

## Chạy local (VS Code)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Mở http://127.0.0.1:8000/docs — mặc định dùng SQLite, không cần cài Postgres.

Chạy test:
```bash
pytest -v
```

## Push GitHub & demo pipeline

```bash
git init
git add .
git commit -m "Init CI/CD demo + database CRUD (pyDAL)"
git branch -M main
git remote add origin https://github.com/<username>/fastapi-cicd-demo.git
git push -u origin main
```

Vào tab **Actions**: job `test` chạy trước, job `build-and-push` (needs: test)
chỉ chạy khi test pass, build & push Docker image lên `ghcr.io`.

### Demo pipeline báo lỗi

Sửa hỏng `add()` trong `app/main.py`, ví dụ:
```python
return {"a": a, "b": b, "result": a + b + 1}   # cố tình sai
```
Commit & push → job `test` báo đỏ → job `build-and-push` bị bỏ qua.

## Deploy PostgreSQL + Render

1. Tạo Web Service trên https://render.com, kết nối repo GitHub, chọn
   Environment: Docker.
2. Tạo PostgreSQL free trên Render, copy connection string.
3. Vào tab Environment của Web Service, thêm biến `DATABASE_URL` = connection
   string vừa copy.
4. Deploy — pyDAL tự tạo bảng `item` trong Postgres, không cần viết SQL tay.
