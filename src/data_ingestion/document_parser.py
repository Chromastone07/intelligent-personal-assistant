import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_txt(file):
    """Reads and returns text from an uploaded TXT file."""
    return file.getvalue().decode("utf-8")

def parse_pdf(file):
    """
    Hybrid PDF parser: First tries a fast direct text extraction.
    If that fails, it falls back to a slower, more accurate OCR method.
    """
    text = ""
    pdf_bytes = file.getvalue()
    
    try:
        # --- METHOD 1: Fast Direct Extraction ---
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()

        # If the fast method yields very little text, it's likely a scanned PDF.
        if len(text.strip()) < 100:
            print("INFO: Fast extraction yielded little text. Falling back to OCR.")
            raise ValueError("Fallback to OCR")

        print("INFO: Successfully parsed PDF with fast method.")
        return text

    except Exception as e:
        # --- METHOD 2: Slower, More Accurate OCR (Fallback) ---
        print(f"INFO: Fast method failed ({e}). Retrying with OCR.")
        text = ""
        try:
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(dpi=150)  # Use lower DPI for speed
                img_bytes = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_bytes))
                text += pytesseract.image_to_string(image) + "\n"
            pdf_document.close()
            
            if not text.strip():
                return "OCR could not detect any text in this PDF."
            print("INFO: Successfully parsed PDF with OCR method.")
            return text
            
        except Exception as ocr_e:
            print(f"Error parsing PDF with OCR: {ocr_e}")
            return "Error: Could not process the PDF file."