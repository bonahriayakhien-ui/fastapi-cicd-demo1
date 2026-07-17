"""
Webapp demo cho lab CI/CD.
API máy tính đơn giản: trang chủ, health check, cộng, chia.
Phần Database: CRUD dùng pyDAL (không viết SQL, đổi được MySQL/
PostgreSQL/MongoDB chỉ bằng connection string).
"""
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import database as db

# Khởi tạo ứng dụng. title/version hiển thị trong trang docs tự sinh.
app = FastAPI(title="CI/CD Demo App", version="1.0.0")


class ItemIn(BaseModel):
    name: str
    price: float
    quantity: int = 0


class ItemOut(ItemIn):
    id: int


@app.get("/")
def read_root():
    """Trang chủ — trả về lời chào."""
    return {"message": "Hello DevOps! App đang chạy."}


@app.get("/health")
def health_check():
    """
    Health check endpoint — QUAN TRỌNG trong DevOps:
    hệ thống giám sát / Docker / load balancer gọi endpoint này
    định kỳ để biết app còn sống hay không.
    """
    return {"status": "ok"}


@app.get("/add")
def add(a: float, b: float):
    """
    Cộng 2 số, truyền qua query string: /add?a=1&b=2
    FastAPI tự validate kiểu dữ liệu: truyền chữ sẽ bị trả lỗi 422.
    """
    return {"a": a, "b": b, "result": a + b}


@app.get("/divide")
def divide(a: float, b: float):
    """Chia 2 số. Chia cho 0 trả lỗi 400 — case này sẽ được test kỹ."""
    if b == 0:
        raise HTTPException(status_code=400, detail="Không thể chia cho 0")
    return {"a": a, "b": b, "result": a / b}


# ---------------------------------------------------------------------------
# CRUD Database (pyDAL) — phần "py4web database" theo yêu cầu của thầy
# ---------------------------------------------------------------------------
@app.get("/items", response_model=List[ItemOut])
def list_items():
    return db.list_items()


@app.post("/items", response_model=ItemOut)
def create_item(item: ItemIn):
    return db.create_item(item.model_dump())


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    result = db.get_item(item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item khong ton tai")
    return result


@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemIn):
    result = db.update_item(item_id, item.model_dump())
    if not result:
        raise HTTPException(status_code=404, detail="Item khong ton tai")
    return result


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if not db.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item khong ton tai")
    return {"message": "Da xoa"}
