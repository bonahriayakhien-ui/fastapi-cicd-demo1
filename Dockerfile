# ============================================================
# Dockerfile cho FastAPI app — mỗi dòng có giải thích
# ============================================================

# 1) Image nền: Debian tối giản + Python 3.12 cài sẵn.
FROM python:3.12-slim

# 2) Biến môi trường:
#    PYTHONDONTWRITEBYTECODE=1 : không sinh file .pyc
#    PYTHONUNBUFFERED=1        : in log ra ngay, không buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3) Thư mục làm việc trong container
WORKDIR /code

# 4) Copy riêng requirements.txt trước để tận dụng layer cache
COPY requirements.txt .

# 5) Cài thư viện lúc BUILD image
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copy source code vào image
COPY ./app ./app

# 7) Khai báo container lắng nghe cổng 8000
EXPOSE 8000

# 8) Lệnh chạy khi container KHỞI ĐỘNG
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
