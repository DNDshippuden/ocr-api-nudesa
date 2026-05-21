# 1. Import library yang dibutuhkan
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import pytesseract

# 2. Inisialisasi aplikasi FastAPI
app = FastAPI()

# 3. Konfigurasi CORS (izinkan akses dari mana saja)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Izinkan semua origin untuk kemudahan testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Endpoint untuk health check (penting untuk Railway)
@app.get("/")
async def root():
    return {"message": "OCR API is running"}

# 5. Endpoint utama OCR
@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Baca file gambar
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        
        # Ekstrak teks menggunakan pytesseract
        # pastikan tesseract terinstall di railway
        extracted_text = pytesseract.image_to_string(img)
        
        return {"filename": file.filename, "extracted_text": extracted_text.strip()}
    except Exception as e:
        # Log error ke console (akan muncul di log railway)
        print(f"ERROR processing file {file.filename}: {str(e)}")
        return {"error": f"Failed to process image: {str(e)}"}