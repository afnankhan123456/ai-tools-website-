import os
import uuid
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
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
# HOME ROUTE
# ===============================
@app.route("/")
def home():
    return render_template("home.html")


# ===============================
# CATEGORY PAGES (FIXED)
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
# CLEANUP FUNCTION
# ===============================
def cleanup_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


# ===============================
# IMAGE COMPRESSOR (PATH FIXED)
# ===============================
@app.route("/image-compressor", methods=["GET", "POST"])
def image_compressor():

    if request.method == "POST":

        cleanup_folder(app.config["UPLOAD_FOLDER"])
        cleanup_folder(app.config["PROCESSED_FOLDER"])

        file = request.files.get("image")

        if not file or file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file and allowed_file(file.filename):

            unique_name = str(uuid.uuid4()) + "_" + secure_filename(file.filename)

            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            file.save(upload_path)

            img = Image.open(upload_path)

            output_path = os.path.join(app.config["PROCESSED_FOLDER"], unique_name)
            img.save(output_path, optimize=True, quality=60)

            return send_file(output_path, as_attachment=True)

        else:
            flash("Invalid file type")
            return redirect(request.url)

    return render_template("image_tools/image_compress.html")


# ===============================
# LOCAL RUN
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
