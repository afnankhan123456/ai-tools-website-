from flask import request, send_file, jsonify
from PIL import Image
import io
import os
import uuid
import random
import math
import numpy as np
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import requests
from io import BytesIO


# GitHub Raw URL — ek ek karke fetch karenge, memory nahi bachega
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/afnankhan123456/Free-AI-Tools-for-PDF-Image-File-Conversion-No-Signup-/main/static/handwriting/alfabat"
HW_DPI = 100
PAGE_W, PAGE_H = int(A4[0] * HW_DPI / 72), int(A4[1] * HW_DPI / 72)
MARGIN = 40 * HW_DPI // 72
FONT_SIZE_PX = 26
LINE_HEIGHT = int(FONT_SIZE_PX * 1.6)

# Cache sirf recently use kiye gaye characters ke liye (max 100 images)
_usage_cache = {}


def fetch_single_glyph(letter):
    """Ek character ke liye koi bhi ek variant GitHub se fetch karo."""
    cache_key = letter
    
    # Agar cache mein hai to turant return
    if cache_key in _usage_cache and _usage_cache[cache_key]:
        return random.choice(_usage_cache[cache_key])
    
    # Nahi to GitHub se fetch karo
    variants = []
    for v in range(1, 5):
        url = f"{GITHUB_RAW_BASE}/{letter}{v}.png"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content)).convert('RGBA')
                variants.append(img)
                if len(variants) >= 2:  # 2 variants enough for variety
                    break
        except:
            pass
    
    if variants:
        _usage_cache[cache_key] = variants
        # Cache size limit — 100 se zyada ho to purane hatao
        if len(_usage_cache) > 100:
            oldest_key = next(iter(_usage_cache))
            del _usage_cache[oldest_key]
        return random.choice(variants)
    
    return None


def extract_text_clean(page):
    words = page.get_text("words")
    if not words:
        return ""
    
    words.sort(key=lambda w: (-w[1], w[0]))
    
    lines = []
    current_line = [words[0]]
    current_y = words[0][1]
    
    for w in words[1:]:
        if abs(w[1] - current_y) < 5:
            current_line.append(w)
        else:
            current_line.sort(key=lambda x: x[0])
            lines.append(current_line)
            current_line = [w]
            current_y = w[1]
    
    if current_line:
        current_line.sort(key=lambda x: x[0])
        lines.append(current_line)
    
    result_lines = []
    for line in lines:
        line_str = ""
        for i, w in enumerate(line):
            line_str += w[4]
            if i < len(line) - 1:
                gap = line[i+1][0] - w[2]
                if gap > 3:
                    line_str += " "
        result_lines.append(line_str)
    
    return "\n".join(result_lines)


def render_page(text):
    """Har character draw karte waqt GitHub se live fetch karo."""
    page = Image.new("RGBA", (PAGE_W, PAGE_H), (255, 255, 255, 255))
    
    # Average widths ke liye temporary cache — pehle use hue characters se calculate
    avg_widths = {}
    default_w = FONT_SIZE_PX * 0.55

    wave_phase = random.uniform(0, 2 * math.pi)
    wave_freq = random.uniform(0.002, 0.005)

    x = MARGIN + random.randint(-4, 4)
    y = MARGIN + FONT_SIZE_PX + random.randint(-4, 4)

    for line in text.split('\n'):
        for word in line.split(' '):
            if not word:
                x += default_w * random.uniform(1.3, 2.2)
                continue
            
            word_width = sum(avg_widths.get(ch, default_w) for ch in word) + len(word) * 2
            if x + word_width > PAGE_W - MARGIN:
                x = MARGIN + random.randint(-4, 4)
                y += LINE_HEIGHT
                if y + LINE_HEIGHT > PAGE_H - MARGIN:
                    break
            
            for ch in word:
                img = fetch_single_glyph(ch)  # GitHub se live fetch
                
                if img:
                    # First time width calculate
                    if ch not in avg_widths:
                        avg_widths[ch] = img.width * (FONT_SIZE_PX / img.height)
                    
                    angle = random.randint(-2, 2)
                    scale = random.uniform(0.95, 1.05)
                    transformed = img.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
                    new_w = int(transformed.size[0] * scale)
                    new_h = int(transformed.size[1] * scale)
                    transformed = transformed.resize((new_w, new_h), Image.LANCZOS)
                    
                    baseline = int(1.5 * math.sin(wave_freq * x + wave_phase))
                    paste_y = y - new_h + baseline + random.randint(-2, 2)
                    page.paste(transformed, (int(x), paste_y), transformed)
                    x += new_w + random.uniform(0, 2.5)
                else:
                    x += default_w + random.uniform(0, 1.5)
            x += default_w * random.uniform(1.3, 2.2)
        x = MARGIN + random.randint(-4, 4)
        y += LINE_HEIGHT + random.randint(-1, 1)
    
    frame = np.array(page.convert("RGB"))
    noise = np.random.normal(0, 2, frame.shape).astype('int16')
    frame = np.clip(frame.astype('int16') + noise, 0, 255).astype('uint8')
    return Image.fromarray(frame)


def pdf_to_handwriting_logic(app):
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    base_dir = os.path.join(os.getcwd(), 'temp')
    upload_folder = os.path.join(base_dir, 'uploads')
    processed_folder = os.path.join(base_dir, 'processed')
    
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)
    
    input_path = os.path.join(upload_folder, str(uuid.uuid4()) + '.pdf')
    output_path = os.path.join(processed_folder, str(uuid.uuid4()) + '_handwritten.pdf')
    
    file.save(input_path)

    try:
        doc = fitz.open(input_path)
        pages_text = []
        for page in doc:
            text = extract_text_clean(page)
            if text.strip():
                pages_text.append(text.upper())
        doc.close()

        if not pages_text:
            return jsonify({'error': 'No text found in PDF'}), 400

        c = canvas.Canvas(output_path, pagesize=A4)
        for text in pages_text:
            img = render_page(text)  # Ab glyphs argument nahi chahiye
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=80)
            buf.seek(0)
            c.drawImage(ImageReader(buf), 0, 0, width=A4[0], height=A4[1])
            c.showPage()
            img.close()
        c.save()

        try:
            os.remove(input_path)
        except:
            pass

        return send_file(output_path, as_attachment=True, download_name='handwritten_assignment.pdf')
    
    except Exception as e:
        try:
            if os.path.exists(input_path): os.remove(input_path)
        except: pass
        try:
            if os.path.exists(output_path): os.remove(output_path)
        except: pass
        return jsonify({'error': str(e)}), 500


print("✅ Handwriting converter ready (Lazy-load mode — zero preload)")







