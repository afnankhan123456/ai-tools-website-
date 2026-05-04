from flask import request, send_file, jsonify
from PIL import Image
import io
import os
import uuid
import random
import math
import numpy as np
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import requests


# ============================================
#    HANDWRITING CONVERSION (SERVER-SIDE)
# ============================================

GITHUB_ALPHABET_URL = "https://raw.githubusercontent.com/afnankhan123456/Free-AI-Tools-for-PDF-Image-File-Conversion-No-Signup-/main/static/handwriting/alfabat"
ALPHABET_DIR = 'alfabet_glyphs'
HW_DPI = 150
PAGE_W, PAGE_H = int(A4[0] * HW_DPI / 72), int(A4[1] * HW_DPI / 72)
MARGIN = 50 * HW_DPI // 72
FONT_SIZE_PX = 28
LINE_HEIGHT = int(FONT_SIZE_PX * 1.8)


def ensure_glyphs():
    """GitHub se transparent PNG glyphs download karo (agar nahi hain) aur load karo."""
    if not os.path.exists(ALPHABET_DIR):
        os.makedirs(ALPHABET_DIR)
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            for variant in range(1, 5):
                fname = f"{letter}{variant}.png"
                url = f"{GITHUB_ALPHABET_URL}/{fname}"
                try:
                    resp = requests.get(url, timeout=5)
                    if resp.status_code == 200:
                        with open(os.path.join(ALPHABET_DIR, fname), 'wb') as f:
                            f.write(resp.content)
                except:
                    pass
    
    glyphs = {}
    for fname in os.listdir(ALPHABET_DIR):
        if fname.endswith('.png'):
            letter = fname[0]
            img = Image.open(os.path.join(ALPHABET_DIR, fname)).convert('RGBA')
            if letter not in glyphs:
                glyphs[letter] = []
            glyphs[letter].append(img)
    return glyphs


def render_page(text, glyphs):
    """Ek page ka text le kar handwriting image banata hai."""
    page = Image.new("RGBA", (PAGE_W, PAGE_H), (255, 255, 255, 255))
    
    avg_widths = {}
    for ch, imgs in glyphs.items():
        if imgs:
            avg_widths[ch] = sum(im.size[0] for im in imgs) / len(imgs)
    default_w = FONT_SIZE_PX * 0.55

    wave_phase = random.uniform(0, 2 * math.pi)
    wave_freq = random.uniform(0.002, 0.005)

    x = MARGIN + random.randint(-5, 5)
    y = MARGIN + FONT_SIZE_PX + random.randint(-5, 5)

    for line in text.split('\n'):
        words = line.split(' ')
        for word in words:
            if not word:
                x += default_w * random.uniform(1.5, 2.5)
                continue
            
            word_width = sum(avg_widths.get(ch, default_w) for ch in word) + len(word) * 2
            if x + word_width > PAGE_W - MARGIN:
                x = MARGIN + random.randint(-5, 5)
                y += LINE_HEIGHT
                if y + LINE_HEIGHT > PAGE_H - MARGIN:
                    break
            
            for ch in word:
                if ch in glyphs and glyphs[ch]:
                    variant = random.choice(glyphs[ch])
                    angle = random.randint(-2, 2)
                    scale = random.uniform(0.95, 1.05)
                    transformed = variant.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
                    new_w = int(transformed.size[0] * scale)
                    new_h = int(transformed.size[1] * scale)
                    transformed = transformed.resize((new_w, new_h), Image.LANCZOS)
                    
                    baseline = int(1.5 * math.sin(wave_freq * x + wave_phase))
                    paste_y = y - new_h + baseline + random.randint(-3, 3)
                    page.paste(transformed, (int(x), paste_y), transformed)
                    x += new_w + random.uniform(0, 3)
                else:
                    x += default_w + random.uniform(0, 2)
            x += default_w * random.uniform(1.5, 2.5)
        x = MARGIN + random.randint(-5, 5)
        y += LINE_HEIGHT + random.randint(-2, 2)
    
    # Add noise
    frame = np.array(page.convert("RGB"))
    noise = np.random.normal(0, 3, frame.shape).astype('int16')
    frame = np.clip(frame.astype('int16') + noise, 0, 255).astype('uint8')
    return Image.fromarray(frame)


def pdf_to_handwriting_logic(app):
    """PDF upload ko handwriting PDF mein convert karta hai."""
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Temp paths
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
    processed_folder = app.config.get('PROCESSED_FOLDER', 'processed')
    
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)
    
    input_path = os.path.join(upload_folder, str(uuid.uuid4()) + '.pdf')
    output_path = os.path.join(processed_folder, str(uuid.uuid4()) + '_handwritten.pdf')
    
    file.save(input_path)

    try:
        # Extract text using PyMuPDF (100% words guaranteed)
        doc = fitz.open(input_path)
        pages_text = []
        for page in doc:
            text = page.get_text("text")
            if text.strip():
                pages_text.append(text.upper())
        doc.close()

        if not pages_text:
            return jsonify({'error': 'No text found in PDF'}), 400

        # Load glyphs
        glyphs = ensure_glyphs()

        # Render pages
        rendered = []
        for text in pages_text:
            rendered.append(render_page(text, glyphs))

        # Create PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        for img in rendered:
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=85)
            buf.seek(0)
            c.drawImage(ImageReader(buf), 0, 0, width=A4[0], height=A4[1])
            c.showPage()
        c.save()

        # Cleanup temp input file
        try:
            os.remove(input_path)
        except:
            pass

        return send_file(
            output_path,
            as_attachment=True,
            download_name='handwritten_assignment.pdf'
        )
    
    except Exception as e:
        # Cleanup on error
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
        except:
            pass
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass
        return jsonify({'error': str(e)}), 500





