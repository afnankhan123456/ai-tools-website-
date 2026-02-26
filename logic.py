from flask import request, send_file
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from pdf2docx import Converter
from docx2pdf import convert
import os, uuid


# ---------------- PNG TO PDF ----------------
def png_to_pdf_logic(app):
    file = request.files["file"]
    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    Image.open(file).convert("RGB").save(output_path)
    return send_file(output_path, as_attachment=True)


# ---------------- JPG TO PDF ----------------
def jpg_to_pdf_logic(app):
    file = request.files["file"]
    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    Image.open(file).convert("RGB").save(output_path)
    return send_file(output_path, as_attachment=True)


# ---------------- PDF TO WORD ----------------
def pdf_to_word_logic(app):
    file = request.files["file"]

    # Save uploaded PDF first
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], str(uuid.uuid4()) + ".pdf")
    file.save(input_path)

    # Output path
    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".docx")

    # Convert using file path (IMPORTANT FIX)
    converter = Converter(input_path)
    converter.convert(output_path)
    converter.close()

    return send_file(output_path, as_attachment=True)


# ---------------- WORD TO PDF ----------------
def word_to_pdf_logic(app):
    file = request.files["file"]
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(input_path)
    output_path = input_path.replace(".docx", ".pdf")
    convert(input_path, output_path)
    return send_file(output_path, as_attachment=True)


# ---------------- MERGE PDF ----------------
def merge_pdf_logic(app):
    files = request.files.getlist("files")
    merger = PdfMerger()

    for file in files:
        merger.append(file)

    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)


# ---------------- SPLIT PDF ----------------
import zipfile

def split_pdf_logic(app):
    file = request.files["file"]
    reader = PdfReader(file)

    # Unique ZIP file name
    zip_filename = str(uuid.uuid4()) + ".zip"
    zip_path = os.path.join(app.config["PROCESSED_FOLDER"], zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zipf:

        # Har page ke liye separate PDF banega
        for i in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            temp_pdf_path = os.path.join(
                app.config["PROCESSED_FOLDER"],
                f"page_{i+1}.pdf"
            )

            with open(temp_pdf_path, "wb") as f:
                writer.write(f)

            zipf.write(temp_pdf_path, f"page_{i+1}.pdf")

            os.remove(temp_pdf_path)  # temp file delete

    return send_file(zip_path, as_attachment=True)


# ---------------- COMPRESS PDF ----------------
def compress_pdf_logic(app):
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)


# ---------------- ROTATE PDF ----------------
def rotate_pdf_logic(app):
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)

    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)


# ---------------- PROTECT PDF ----------------
def protect_pdf_logic(app):
    file = request.files["file"]
    password = request.form["password"]

    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)


# ---------------- UNLOCK PDF ----------------
def unlock_pdf_logic(app):
    file = request.files["file"]
    password = request.form["password"]

    reader = PdfReader(file)
    reader.decrypt(password)

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)


# ---------------- RESIZE PDF ----------------
def resize_pdf_logic(app):
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        page.scale_by(0.8)
        writer.add_page(page)

    output_path = os.path.join(app.config["PROCESSED_FOLDER"], str(uuid.uuid4()) + ".pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)

