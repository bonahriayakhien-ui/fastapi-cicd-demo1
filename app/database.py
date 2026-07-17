"""
Module database CRUD dùng pyDAL (thành phần data-abstraction-layer của
framework py4web).

Ý tưởng chính (đúng yêu cầu của thầy):
- KHÔNG viết câu lệnh SQL nào cả — chỉ khai báo Field bằng Python,
  pyDAL tự sinh bảng, tự sinh câu lệnh insert/select/update/delete.
- Đổi database (MySQL / PostgreSQL / MongoDB / SQLite...) CHỈ cần đổi
  biến môi trường DATABASE_URL — không cần sửa lại bất kỳ dòng code nào
  khác, không cần viết lại connectstring dạng SQL.
"""
import os

from pydal import DAL, Field

# Mặc định dùng SQLite (không cần cài Postgres) khi chạy test / chạy local.
# Khi deploy thật, chỉ cần set DATABASE_URL=postgres://user:pass@host:port/db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://storage.db")

os.makedirs("databases", exist_ok=True)
db = DAL(DATABASE_URL, pool_size=1, migrate=True, folder="databases")

# Khai báo bảng bằng Python — pyDAL tự tạo bảng thật trong database,
# tự sinh SQL, tự tạo form/CRUD tương ứng.
#
# Lưu ý: trên môi trường container không có ổ đĩa cố định (vd Render free
# tier), file pyDAL dùng để "nhớ" là đã tạo bảng rồi có thể bị mất khi
# container khởi động lại, dù bảng thật vẫn còn trong Postgres. Lúc đó pyDAL
# sẽ cố tạo lại và bị lỗi "already exists". Bắt lỗi này và chuyển sang
# fake_migrate (chỉ ghi nhận lại là đã khớp, không tạo lại) để an toàn.
try:
    db.define_table(
        "item",
        Field("name", "string", length=128, notnull=True),
        Field("price", "double", notnull=True),
        Field("quantity", "integer", default=0),
    )
except Exception as exc:
    if "already exists" in str(exc).lower():
        db.rollback()
        db.define_table(
            "item",
            Field("name", "string", length=128, notnull=True),
            Field("price", "double", notnull=True),
            Field("quantity", "integer", default=0),
            fake_migrate=True,
        )
    else:
        raise


def list_items():
    rows = db(db.item).select()
    return [row.as_dict() for row in rows]


def create_item(data: dict):
    item_id = db.item.insert(**data)
    db.commit()
    return {**data, "id": item_id}


def get_item(item_id: int):
    row = db.item(item_id)
    return row.as_dict() if row else None


def update_item(item_id: int, data: dict):
    row = db.item(item_id)
    if not row:
        return None
    row.update_record(**data)
    db.commit()
    return {**data, "id": item_id}


def delete_item(item_id: int) -> bool:
    row = db.item(item_id)
    if not row:
        return False
    row.delete_record()
    db.commit()
    return True