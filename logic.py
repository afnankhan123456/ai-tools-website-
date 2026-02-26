from flask import Flask, request, send_file
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from pdf2docx import Converter
from docx2pdf import convert
import os, uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# ---------------- PNG TO PDF ----------------
@app.route("/png-to-pdf", methods=["POST"])
def png_to_pdf():
    file = request.files["file"]
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    Image.open(file).convert("RGB").save(output_path)
    return send_file(output_path, as_attachment=True)

# ---------------- JPG TO PDF ----------------
@app.route("/jpg-to-pdf", methods=["POST"])
def jpg_to_pdf():
    file = request.files["file"]
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    Image.open(file).convert("RGB").save(output_path)
    return send_file(output_path, as_attachment=True)

# ---------------- PDF TO WORD ----------------
@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():
    file = request.files["file"]
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".docx")
    converter = Converter(file)
    converter.convert(output_path)
    converter.close()
    return send_file(output_path, as_attachment=True)

# ---------------- WORD TO PDF ----------------
@app.route("/word-to-pdf", methods=["POST"])
def word_to_pdf():
    file = request.files["file"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)
    output_path = input_path.replace(".docx", ".pdf")
    convert(input_path, output_path)
    return send_file(output_path, as_attachment=True)

# ---------------- MERGE PDF ----------------
@app.route("/merge-pdf", methods=["POST"])
def merge_pdf():
    files = request.files.getlist("files")
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    merger.write(output_path)
    merger.close()
    return send_file(output_path, as_attachment=True)

# ---------------- SPLIT PDF (FIRST PAGE) ----------------
@app.route("/split-pdf", methods=["POST"])
def split_pdf():
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()
    writer.add_page(reader.pages[0])
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

# ---------------- COMPRESS PDF (BASIC COPY) ----------------
@app.route("/compress-pdf", methods=["POST"])
def compress_pdf():
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

# ---------------- ROTATE PDF ----------------
@app.route("/rotate-pdf", methods=["POST"])
def rotate_pdf():
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

# ---------------- PROTECT PDF ----------------
@app.route("/protect-pdf", methods=["POST"])
def protect_pdf():
    file = request.files["file"]
    password = request.form["password"]
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

# ---------------- UNLOCK PDF ----------------
@app.route("/unlock-pdf", methods=["POST"])
def unlock_pdf():
    file = request.files["file"]
    password = request.form["password"]
    reader = PdfReader(file)
    reader.decrypt(password)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

# ---------------- RESIZE PDF ----------------
@app.route("/resize-pdf", methods=["POST"])
def resize_pdf():
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        page.scale_by(0.8)
        writer.add_page(page)
    output_path = os.path.join(PROCESSED_FOLDER, str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)