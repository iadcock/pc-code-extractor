from flask import Flask, request, render_template, jsonify
import fitz  # PyMuPDF for PDF processing
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

app = Flask(__name__)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"

    if not text.strip():  # If no text was found, try OCR
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
    
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf_file = request.files["pdf"]
        if pdf_file:
            pdf_path = f"temp/{pdf_file.filename}"
            pdf_file.save(pdf_path)
            extracted_text = extract_text_from_pdf(pdf_path)
            os.remove(pdf_path)  # Cleanup temp file
            return jsonify({"text": extracted_text})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
