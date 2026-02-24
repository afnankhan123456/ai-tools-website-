import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Folders
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ==============================
# Home Page
# ==============================
@app.route("/")
def home():
    return render_template("home.html")


# ==============================
# Image Compressor Page
# ==============================
@app.route("/image-compressor", methods=["GET", "POST"])
def image_compressor():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file selected")
            return redirect(request.url)

        file = request.files["image"]

        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(upload_path)

            # Compress Image
            img = Image.open(upload_path)
            output_path = os.path.join(app.config["PROCESSED_FOLDER"], filename)

            img.save(output_path, optimize=True, quality=60)

            return send_file(output_path, as_attachment=True)

        else:
            flash("Invalid file type")
            return redirect(request.url)

    return render_template("image_compressor.html")


# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    app.run(debug=True)