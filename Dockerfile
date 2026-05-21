# 1. Gunakan base image Python versi slim (ringan)
FROM python:3.12-slim

# 2. Instal Tesseract OCR, file bahasa Inggris, dan library development-nya
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev && \
    rm -rf /var/lib/apt/lists/*

# 3. Set working directory di dalam container
WORKDIR /app

# 4. Salin file daftar dependensi Python dan instal
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Salin semua kode aplikasi
COPY . .

# 6. Gunakan shell form agar $PORT dievaluasi
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
