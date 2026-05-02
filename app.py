import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# ============================================
#        STATIC FILES & VERIFICATION
# ============================================

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/google3e04282ea741df4b.html')
def google_verify():
    return send_from_directory('static', 'google3e04282ea741df4b.html')

@app.route('/yandex_3c01d903358ab76d.html')
def yandex_verify():
    return send_from_directory('static', 'yandex_3c01d903358ab76d.html')


# ============================================
#              MAIN PAGES
# ============================================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pdf-tools')
def pdf_tools():
    return render_template('pdf_tools/pdf_all_in_one.html')

@app.route('/image-tools')
def image_tools():
    return render_template('image_tools/image_tools.html')

@app.route('/utility-tools')
def utility_tools():
    return render_template('utility_tools/utility_tools.html')


# ============================================
#           PDF TOOL PAGES (client-side)
#============================================

@app.route('/jpg-to-pdf')
def jpg_to_pdf():
    # Exact filename from GitHub: JPG, JPEG, PNG_to_pdf.html
    return render_template('pdf_tools/JPG, JPEG, PNG_to_pdf.html')

@app.route('/pdf-to-jpg')
def pdf_to_jpg():
    # Exact filename from GitHub: PDF_to-JPG,JPEG,PNG.html
    return render_template('pdf_tools/PDF_to-JPG,JPEG,PNG.html')

@app.route('/compress-pdf')
def compress_pdf():
    return render_template('pdf_tools/compress_pdf.html')

@app.route('/merge-pdf')
def merge_pdf():
    return render_template('pdf_tools/merge_pdf.html')

@app.route('/pdf-to-word')
def pdf_to_word():
    return render_template('pdf_tools/pdf_to_word.html')

@app.route('/resize-pdf')
def resize_pdf():
    return render_template('pdf_tools/resize_pdf.html')

@app.route('/rotate-pdf')
def rotate_pdf():
    return render_template('pdf_tools/rotate_pdf.html')

@app.route('/split-pdf')
def split_pdf():
    return render_template('pdf_tools/split_pdf.html')

@app.route('/word-to-pdf')
def word_to_pdf():
    return render_template('pdf_tools/word_to_pdf.html')


# ============================================
#          IMAGE TOOL PAGES (client-side)
# ============================================

@app.route('/image-compressor')
def image_compressor():
    return render_template('image_tools/image_compress.html')

@app.route('/image-resize')
def image_resize():
    return render_template('image_tools/image_resize.html')


# ============================================
#         UTILITY TOOL PAGES (client-side)
#============================================

@app.route('/base64-encoder', endpoint='Base64 Encoder-Decoder')
def base64_encoder():
    # Exact filename with leading space (from GitHub)
    return render_template('utility_tools/ Base64 Encoder-Decoder.html')

@app.route('/json-formatter', endpoint='JSON Formatter')
def json_formatter():
    return render_template('utility_tools/json_formatter.html')

@app.route('/qr-generator', endpoint='QR Generator')
def qr_generator():
    return render_template('utility_tools/qr_generator.html')

@app.route('/word-counter', endpoint='Word Counter')
def word_counter():
    return render_template('utility_tools/word_counter.html')


# ============================================
#                   ERROR HANDLER
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ============================================
#                     RUN
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)




