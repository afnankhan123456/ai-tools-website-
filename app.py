import os
import uuid
from flask import Flask, render_template, request, send_file, redirect, flash
from werkzeug.utils import secure_filename
from PIL import Image

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
    return render_template("image_tools/image_compress.html")


@app.route("/utility-tools")
def utility_tools():
    return render_template("utility_tools/word_counter.html")


# ===============================
# PDF TOOL ROUTES
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
# IMAGE TOOLS
# ===============================
@app.route("/image-compressor", methods=["GET", "POST"])
def image_compressor():

    if request.method == "POST":

        # Clear old files
        for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
            for f in os.listdir(folder):
                os.remove(os.path.join(folder, f))

        file = request.files.get("image")
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


@app.route("/image-resize")
def image_resize():
    return render_template("image_tools/image_resize.html")


@app.route("/bg-remove")
def bg_remove():
    return render_template("image_tools/bg_remover.html")


# ===============================
# UTILITY TOOLS
# ===============================
@app.route("/word-counter", methods=["GET", "POST"])
def word_counter():

    if request.method == "POST":
        text = request.form.get("text", "")
        word_count = len(text.split())
        char_count = len(text)

        return render_template(
            "utility_tools/word_counter.html",
            word_count=word_count,
            char_count=char_count,
            text=text
        )

    return render_template("utility_tools/word_counter.html")


@app.route("/qr-generator")
def qr_generator():
    return render_template("utility_tools/qr_generator.html")


@app.route("/base64-encoder")
def base64_encoder():
    return render_template("utility_tools/base64_encoder.html")


@app.route("/json-formatter")
def json_formatter():
    return render_template("utility_tools/json_formatter.html")


# ===============================
# LOCAL RUN
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
