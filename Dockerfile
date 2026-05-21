# Menggunakan Python versi 3.12 ringan
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Tesseract OCR dan tools sistem yang diperlukan
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements dan install dependencies Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi
COPY . .

# Expose port (Railway akan menggantinya dengan variabel PORT)
EXPOSE 8000

# Jalankan aplikasi dengan shell form agar variabel PORT bisa dievaluasi
# Catatan: Railway akan menyuntikkan variabel environment PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}