# 1. Import library yang dibutuhkan
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageEnhance
from io import BytesIO
import pytesseract

# 2. Inisialisasi aplikasi FastAPI
app = FastAPI()

# 3. Konfigurasi CORS (izinkan akses dari mana saja)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua origin untuk kemudahan testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Fungsi preprocessing gambar
def preprocess_image(img):
    """
    Preprocessing gambar untuk meningkatkan OCR pada teks kecil/abu-abu.
    - Konversi ke grayscale
    - Tingkatkan kontras dan ketajaman
    - Threshold biner (hitam-putih)
    """
    if img.mode != 'L':
        img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)          # tingkatkan kontras
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)          # tingkatkan ketajaman
    # Threshold: nilai < 150 jadi hitam, >= 150 jadi putih
    threshold = 120
    img = img.point(lambda p: 0 if p < threshold else 255, '1')
    return img

# 5. Endpoint untuk health check (penting untuk Railway)
@app.get("/")
async def root():
    return {"message": "OCR API is running"}

# 6. Endpoint utama OCR dengan preprocessing
@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Baca file gambar
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        
        # Preprocessing gambar untuk hasil OCR yang lebih baik
        img = preprocess_image(img)
        
        # Konfigurasi Tesseract: --psm 6 (satu blok teks homogen), --oem 3 (LSTM + legacy)
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(img, lang='ind', config=custom_config)
        
        # Bersihkan teks (opsional: hapus spasi berlebih)
        cleaned_text = ' '.join(extracted_text.split())
        
        return {"filename": file.filename, "extracted_text": cleaned_text}
    except Exception as e:
        # Log error ke console (akan muncul di log railway)
        print(f"ERROR processing file {file.filename}: {str(e)}")
        return {"error": f"Failed to process image: {str(e)}"}