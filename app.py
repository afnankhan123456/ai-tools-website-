import os
import uuid
from flask import Flask, render_template, request, send_file, redirect, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

from logic import (
    png_to_pdf_logic,
    jpg_to_pdf_logic,
    pdf_to_word_logic,
    word_to_pdf_logic,
    merge_pdf_logic,
    split_pdf_logic,
    compress_pdf_logic,
    rotate_pdf_logic,
    protect_pdf_logic,
    unlock_pdf_logic,
    resize_pdf_logic,
    pdf_to_jpg_logic,
    image_resize_logic,
    bg_remover_logic,
    base64_encoder_logic,
    json_formatter_logic,
    qr_generator_logic,
    word_counter_logic
)

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ===============================
# HOME
# ===============================
@app.route("/")
def home():
    return render_template("home.html")


# ===============================
# CATEGORY PAGES
# ===============================
@app.route("/pdf-tools")
def pdf_tools():
    return render_template("pdf_tools/pdf_all_in_one.html")


@app.route("/image-tools")
def image_tools():
    return render_template("image_tools/image_tools.html")


@app.route("/utility-tools")
def utility_tools():
    return render_template("utility_tools/utility_tools.html")


# ===============================
# UTILITY TOOL ROUTES
# ===============================

@app.route("/base64-encoder", methods=["GET", "POST"])
def base64_encoder():
    result = None

    if request.method == "POST":
        result = base64_encoder_logic()

    return render_template("utility_tools/base64_encoder.html", result=result)


@app.route("/json-formatter", methods=["GET", "POST"])
def json_formatter():
    result = None
    error = None

    if request.method == "POST":
        try:
            result = json_formatter_logic()
        except Exception:
            error = "Invalid JSON format."

    return render_template("utility_tools/json_formatter.html", result=result, error=error)


@app.route("/qr-generator", methods=["GET", "POST"])
def qr_generator():
    if request.method == "POST":
        return qr_generator_logic(app)
    return render_template("utility_tools/qr_generator.html")


@app.route("/word-counter", methods=["GET", "POST"])
def word_counter():
    result = None

    if request.method == "POST":
        result = word_counter_logic()

    return render_template("utility_tools/word_counter.html", result=result)


# ===============================
# PDF TOOL PAGE ROUTES (GET)
# ===============================
@app.route("/png-to-pdf")
def png_to_pdf():
    return render_template("pdf_tools/png_to_pdf.html")


@app.route("/jpg-to-pdf")
def jpg_to_pdf():
    return render_template("pdf_tools/jpg_to_pdf.html")


@app.route("/pdf-to-word")
def pdf_to_word():
    return render_template("pdf_tools/pdf_to_word.html")


@app.route("/word-to-pdf")
def word_to_pdf():
    return render_template("pdf_tools/word_to_pdf.html")


@app.route("/pdf-to-jpg")
def pdf_to_jpg():
    return render_template("pdf_tools/pdf_to_jpg.html")


@app.route("/merge-pdf")
def merge_pdf():
    return render_template("pdf_tools/merge_pdf.html")


@app.route("/split-pdf")
def split_pdf():
    return render_template("pdf_tools/split_pdf.html")


@app.route("/compress-pdf")
def compress_pdf():
    return render_template("pdf_tools/compress_pdf.html")


@app.route("/rotate-pdf")
def rotate_pdf():
    return render_template("pdf_tools/rotate_pdf.html")


@app.route("/unlock-pdf")
def unlock_pdf():
    return render_template("pdf_tools/unlock_pdf.html")


@app.route("/protect-pdf")
def protect_pdf():
    return render_template("pdf_tools/protect_pdf.html")


@app.route("/resize-pdf")
def resize_pdf():
    return render_template("pdf_tools/resize_pdf.html")


# ===============================
# PDF TOOL ACTION ROUTES (POST)
# ===============================
@app.route("/png-to-pdf-action", methods=["POST"])
def png_to_pdf_action():
    return png_to_pdf_logic(app)


@app.route("/jpg-to-pdf-action", methods=["POST"])
def jpg_to_pdf_action():
    return jpg_to_pdf_logic(app)


@app.route("/pdf-to-word-action", methods=["POST"])
def pdf_to_word_action():
    return pdf_to_word_logic(app)


@app.route("/word-to-pdf-action", methods=["POST"])
def word_to_pdf_action():
    return word_to_pdf_logic(app)


@app.route("/pdf-to-jpg-action", methods=["POST"])
def pdf_to_jpg_action():
    return pdf_to_jpg_logic(app)


@app.route("/merge-pdf-action", methods=["POST"])
def merge_pdf_action():
    return merge_pdf_logic(app)


@app.route("/split-pdf-action", methods=["POST"])
def split_pdf_action():
    return split_pdf_logic(app)


@app.route("/compress-pdf-action", methods=["POST"])
def compress_pdf_action():
    return compress_pdf_logic(app)


@app.route("/rotate-pdf-action", methods=["POST"])
def rotate_pdf_action():
    return rotate_pdf_logic(app)


@app.route("/protect-pdf-action", methods=["POST"])
def protect_pdf_action():
    return protect_pdf_logic(app)


@app.route("/unlock-pdf-action", methods=["POST"])
def unlock_pdf_action():
    return unlock_pdf_logic(app)


@app.route("/resize-pdf-action", methods=["POST"])
def resize_pdf_action():
    return resize_pdf_logic(app)


# ===============================
# IMAGE COMPRESSOR
# ===============================
@app.route("/image-compressor", methods=["GET", "POST"])
def image_compressor():

    if request.method == "POST":

        file = request.files.get("file")
        quality = request.form.get("quality", 60)

        if not file or file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file and allowed_file(file.filename):

            unique_name = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            upload_path = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(upload_path)

            img = Image.open(upload_path)

            output_path = os.path.join(PROCESSED_FOLDER, unique_name)
            img.save(output_path, optimize=True, quality=int(quality))

            return send_file(output_path, as_attachment=True)

        else:
            flash("Invalid file type")
            return redirect(request.url)

    return render_template("image_tools/image_compress.html")


# ===============================
# IMAGE RESIZER
# ===============================
@app.route("/image-resize", methods=["GET", "POST"])
def image_resize():

    if request.method == "POST":
        return image_resize_logic(app)

    return render_template("image_tools/image_resize.html")


# ===============================
# BACKGROUND REMOVER
# ===============================
@app.route("/bg-remover", methods=["GET", "POST"])
def bg_remover():

    if request.method == "POST":
        return bg_remover_logic(app)

    return render_template("image_tools/bg_remover.html")


# ===============================
# LOCAL RUN
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


