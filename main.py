from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
from io import BytesIO


# Inisialisasi aplikasi FastAPI
app = FastAPI(title="OCR API", description="API untuk ekstraksi teks dari gambar.")

# CORS: Izinkan akses dari berbagai sumber (seperti aplikasi Android)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# KONFIGURASI TESSERACT (Khusus Windows)
# Hapus tanda komentar pada baris di bawah jika Tesseract tidak ada di PATH. ⬇️⬇️
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.get("/")
def root():
    """Endpoint sederhana untuk mengecek apakah server berjalan."""
    return {"message": "OCR API is running"}

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """
    Menerima file gambar, memprosesnya dengan OCR, dan mengembalikan teks hasil ekstraksi.
    """
    # 1. Validasi tipe file (opsional)
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return {"error": "Format file tidak didukung. Gunakan JPG atau PNG."}

    try:
        # 2. Baca file gambar yang diunggah
        contents = await file.read()
        img = Image.open(BytesIO(contents))

        # 3. Konversi ke grayscale untuk akurasi OCR yang lebih baik
        img = img.convert('L')  # 'L' = mode grayscale

        # 4. Ekstrak teks dari gambar menggunakan pytesseract
        extracted_text = pytesseract.image_to_string(img, lang='ind+eng')

        # 5. Bersihkan teks (opsional)
        cleaned_text = ' '.join(extracted_text.split())

        # 6. Kembalikan hasil sebagai JSON
        return {
            "filename": file.filename,
            "extracted_text": cleaned_text
        }
    except Exception as e:
        return {"error": f"Terjadi kesalahan saat memproses gambar: {str(e)}"}