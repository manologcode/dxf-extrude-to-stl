from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from .my_cadquery import scale_dxf_to_size 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'dxf'}
app.secret_key = 'supersecretkey'

# Asegurar que la carpeta de subida exista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se encontró el archivo', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No seleccionaste ningún archivo', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Obtener otros datos del formulario
            height = request.form.get('height')

            stl_name = filename[:-4] + ".stl"

            scale_dxf_to_size(file_path, stl_name, extrusion_height=int(height))
            
            flash('Archivo subido con éxito y datos recibidos', 'success')
            return render_template('visor.html', stl_name=stl_name)
        else:
            flash('Formato de archivo no permitido. Solo archivos DXF.', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/visor', methods=['GET'])
def visor():
    return render_template('visor.html')

if __name__ == '__main__':
    app.run(debug=True)