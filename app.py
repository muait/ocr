import os
from flask import Flask, request, render_template_string
from PIL import Image, ImageOps
import pytesseract

app = Flask(__name__)

# Sur Render avec Docker, Tesseract est installé dans le système
# Pas besoin de spécifier le chemin /usr/bin/tesseract

@app.route('/', methods=['GET', 'POST'])
def home():
    txt = ""
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            # Traitement image pour la précision des codes
            img = Image.open(file.stream).convert('L')
            img = ImageOps.autocontrast(img)
            # Agrandissement pour les petits codes
            w, h = img.size
            img = img.resize((w*2, h*2), Image.LANCZOS)
            # OCR rapide
            txt = pytesseract.image_to_string(img, config='--psm 11')

    return render_template_string('''
        <body style="font-family:sans-serif; text-align:center; padding:50px;">
            <h2>OCR Rapide - Dossier OCR</h2>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="image" required onchange="this.form.submit()">
            </form>
            <br>
            <textarea style="width:90%; height:400px; padding:10px;">{{r}}</textarea>
        </body>
    ''', r=txt)

if __name__ == '__main__':
    # Configuration pour Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
