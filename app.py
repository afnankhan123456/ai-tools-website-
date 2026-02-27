import os
from flask import Flask, render_template, request
from logic import *

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER


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
# PDF TOOL ROUTES
# ===============================
@app.route("/png-to-pdf", methods=["GET", "POST"])
def png_to_pdf():
    if request.method == "POST":
        return png_to_pdf_logic(app)
    return render_template("pdf_tools/png_to_pdf.html")


@app.route("/jpg-to-pdf", methods=["GET", "POST"])
def jpg_to_pdf():
    if request.method == "POST":
        return jpg_to_pdf_logic(app)
    return render_template("pdf_tools/jpg_to_pdf.html")


@app.route("/pdf-to-word", methods=["GET", "POST"])
def pdf_to_word():
    if request.method == "POST":
        return pdf_to_word_logic(app)
    return render_template("pdf_tools/pdf_to_word.html")


@app.route("/word-to-pdf", methods=["GET", "POST"])
def word_to_pdf():
    if request.method == "POST":
        return word_to_pdf_logic(app)
    return render_template("pdf_tools/word_to_pdf.html")


@app.route("/pdf-to-jpg", methods=["GET", "POST"])
def pdf_to_jpg():
    if request.method == "POST":
        return pdf_to_jpg_logic(app)
    return render_template("pdf_tools/pdf_to_jpg.html")


@app.route("/merge-pdf", methods=["GET", "POST"])
def merge_pdf():
    if request.method == "POST":
        return merge_pdf_logic(app)
    return render_template("pdf_tools/merge_pdf.html")


@app.route("/split-pdf", methods=["GET", "POST"])
def split_pdf():
    if request.method == "POST":
        return split_pdf_logic(app)
    return render_template("pdf_tools/split_pdf.html")


@app.route("/compress-pdf", methods=["GET", "POST"])
def compress_pdf():
    if request.method == "POST":
        return compress_pdf_logic(app)
    return render_template("pdf_tools/compress_pdf.html")


@app.route("/rotate-pdf", methods=["GET", "POST"])
def rotate_pdf():
    if request.method == "POST":
        return rotate_pdf_logic(app)
    return render_template("pdf_tools/rotate_pdf.html")


@app.route("/protect-pdf", methods=["GET", "POST"])
def protect_pdf():
    if request.method == "POST":
        return protect_pdf_logic(app)
    return render_template("pdf_tools/protect_pdf.html")


@app.route("/unlock-pdf", methods=["GET", "POST"])
def unlock_pdf():
    if request.method == "POST":
        return unlock_pdf_logic(app)
    return render_template("pdf_tools/unlock_pdf.html")


@app.route("/resize-pdf", methods=["GET", "POST"])
def resize_pdf():
    if request.method == "POST":
        return resize_pdf_logic(app)
    return render_template("pdf_tools/resize_pdf.html")


# ===============================
# IMAGE TOOLS
# ===============================
@app.route("/image-resize", methods=["GET", "POST"])
def image_resize():
    if request.method == "POST":
        return image_resize_logic(app)
    return render_template("image_tools/image_resize.html")


@app.route("/bg-remover", methods=["GET", "POST"])
def bg_remover():
    if request.method == "POST":
        return bg_remover_logic(app)
    return render_template("image_tools/bg_remover.html")


# ===============================
# UTILITY TOOLS
# ===============================
@app.route("/base64-encoder", methods=["GET", "POST"])
def base64_encoder():
    if request.method == "POST":
        return base64_encoder_logic()
    return render_template("utility_tools/base64_encoder.html")


@app.route("/json-formatter", methods=["GET", "POST"])
def json_formatter():
    if request.method == "POST":
        return json_formatter_logic()
    return render_template("utility_tools/json_formatter.html")


@app.route("/qr-generator", methods=["GET", "POST"])
def qr_generator():
    if request.method == "POST":
        return qr_generator_logic()
    return render_template("utility_tools/qr_generator.html")


@app.route("/word-counter", methods=["GET", "POST"])
def word_counter():
    if request.method == "POST":
        return word_counter_logic()
    return render_template("utility_tools/word_counter.html")


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
