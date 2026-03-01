from flask import request, send_file
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from pdf2docx import Converter
from docx2pdf import convert
from pdf2image import convert_from_path
from rembg import remove
import io
import base64
import json
import qrcode
import os
import uuid
import zipfile





# ---------------- PNG TO PDF ----------------
def png_to_pdf_logic(app):
    file = request.files["file"]

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

    Image.open(file).convert("RGB").save(output_path)

    return send_file(output_path, as_attachment=True)


# ---------------- JPG TO PDF ----------------
def jpg_to_pdf_logic(app):
    file = request.files["file"]

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

    Image.open(file).convert("RGB").save(output_path)

    return send_file(output_path, as_attachment=True)


# ---------------- PDF TO JPG ----------------
def pdf_to_jpg_logic(app):
    file = request.files["file"]

    input_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )
    file.save(input_path)

    images = convert_from_path(input_path)

    zip_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".zip"
    )

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for i, image in enumerate(images):
            img_name = f"page_{i+1}.jpg"
            img_path = os.path.join(app.config["PROCESSED_FOLDER"], img_name)
            image.save(img_path, "JPEG")
            zipf.write(img_path, img_name)
            os.remove(img_path)

    return send_file(zip_path, as_attachment=True)


# ---------------- PDF TO WORD ----------------
def pdf_to_word_logic(app):
    file = request.files["file"]

    input_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )
    file.save(input_path)

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".docx"
    )

    converter = Converter(input_path)
    converter.convert(output_path)
    converter.close()

    return send_file(output_path, as_attachment=True)


# ---------------- WORD TO PDF ----------------
def word_to_pdf_logic(app):
    file = request.files["file"]

    input_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        str(uuid.uuid4()) + ".docx"
    )
    file.save(input_path)

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

    convert(input_path, output_path)

    return send_file(output_path, as_attachment=True)


# ---------------- MERGE PDF ----------------
def merge_pdf_logic(app):
    files = request.files.getlist("files")
    merger = PdfMerger()

    for file in files:
        merger.append(file)

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

    merger.write(output_path)
    merger.close()

    return send_file(output_path, as_attachment=True)


# ---------------- SPLIT PDF ----------------
def split_pdf_logic(app):
    file = request.files["file"]
    reader = PdfReader(file)

    zip_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".zip"
    )

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for i in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            temp_path = os.path.join(
                app.config["PROCESSED_FOLDER"],
                f"page_{i+1}.pdf"
            )

            with open(temp_path, "wb") as f:
                writer.write(f)

            zipf.write(temp_path, f"page_{i+1}.pdf")
            os.remove(temp_path)

    return send_file(zip_path, as_attachment=True)


# ---------------- COMPRESS PDF ----------------
def compress_pdf_logic(app):
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

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

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

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

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)


# ---------------- UNLOCK PDF ----------------
def unlock_pdf_logic(app):
    file = request.files["file"]
    password = request.form["password"]

    reader = PdfReader(file)

    if not reader.is_encrypted:
        return "PDF is not password protected."

    reader.decrypt(password)

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

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

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".pdf"
    )

    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)


# ---------------- IMAGE COMPRESS ----------------
def image_compress_logic(app):
    file = request.files["file"]

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".jpg"
    )

    image = Image.open(file).convert("RGB")
    image.save(output_path, "JPEG", quality=40, optimize=True)

    return send_file(output_path, as_attachment=True)


# ---------------- IMAGE RESIZE ----------------
def image_resize_logic(app):
    file = request.files["file"]
    width = int(request.form.get("width", 800))
    height = int(request.form.get("height", 600))

    image = Image.open(file)
    resized = image.resize((width, height))

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".jpg"
    )

    resized.save(output_path)

    return send_file(output_path, as_attachment=True)


# ---------------- BG REMOVER ----------------
from flask import request, send_file
from PIL import Image
from rembg import remove
import os
import uuid
import io

def bg_remover_logic(app):

    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]
    bg_option = request.form.get("bg_option")
    selected_bg = request.form.get("selected_bg")
    custom_bg_file = request.files.get("custom_bg")

    os.makedirs(app.config["PROCESSED_FOLDER"], exist_ok=True)

    # 🔹 Open and remove background
    input_image = Image.open(file).convert("RGBA")
    removed = remove(input_image)
    foreground = Image.open(io.BytesIO(removed)).convert("RGBA")

    width, height = foreground.size

    # ===============================
    # PRESET BACKGROUND (GitHub folder)
    # ===============================
    if bg_option == "preset" and selected_bg:

        preset_path = os.path.join(
            app.root_path,
            "templates/image_tools/backgroud_images",
            selected_bg
        )

        if not os.path.exists(preset_path):
            return "Preset background not found"

        background = Image.open(preset_path).convert("RGB")
        background = background.resize((width, height))
        background.paste(foreground, (0, 0), foreground)

    # ===============================
    #  UPLOAD BACKGROUND
    # ===============================
    elif bg_option == "custom" and custom_bg_file:

        background = Image.open(custom_bg_file).convert("RGB")
        background = background.resize((width, height))
        background.paste(foreground, (0, 0), foreground)

    else:
        return "Please select a valid background option"

    output_filename = str(uuid.uuid4()) + ".jpg"
    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        output_filename
    )

    background.save(output_path, "JPEG")

    return send_file(output_path, as_attachment=True)


# ---------------- BASE64 ENCODER ----------------
def base64_encoder_logic():
    text = request.form.get("text", "")
    return base64.b64encode(text.encode()).decode()


# ---------------- JSON FORMATTER ----------------
def json_formatter_logic():
    raw_json = request.form.get("json_data", "")
    parsed = json.loads(raw_json)
    return json.dumps(parsed, indent=4)


# ---------------- QR GENERATOR ----------------
def qr_generator_logic(app):
    data = request.form.get("data", "")
    img = qrcode.make(data)

    output_path = os.path.join(
        app.config["PROCESSED_FOLDER"],
        str(uuid.uuid4()) + ".png"
    )

    img.save(output_path)
    return send_file(output_path, as_attachment=True)


# ---------------- WORD COUNTER (2000 LIMIT) ----------------
def word_counter_logic():
    text = request.form.get("text", "")

    if len(text) > 2000:
        return {"error": "Sweet limit exceeded ❤️ Please keep text under 2000 characters."}

    return {
        "words": len(text.split()),
        "characters": len(text)
    }

