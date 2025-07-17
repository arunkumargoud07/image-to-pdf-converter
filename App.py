# from flask import Flask,render_template
# from flask import *
# from i2p import i2pconverter
# app = Flask(__name__)

# @app.route('/Img2Pdf')
# def index():
#     return render_template('index.html')

# @app.route('/converted',methods = ['GET', 'POST'])
# def convert():
#     global f1
#     fi = request.files['img']
#     f1 = fi.filename
#     fi.save(f1)
#     i2pconverter(f1)
#     return render_template('converted.html')

# @app.route('/download')
# def download():
#     filename = f1.split('.')[0]+'converted.pdf'
#     return send_file(filename,as_attachment=True)

# app.run()

from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from i2p import i2pconverter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

# Ensure the upload and converted folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(CONVERTED_FOLDER):
    os.makedirs(CONVERTED_FOLDER)

# Root route
@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/Img2Pdf')
def index():
    return render_template('index.html')

@app.route('/converted', methods=['POST'])
def convert():
    if 'img' not in request.files:
        return redirect(request.url)
    file = request.files['img']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Convert the file
        converted_filename = os.path.splitext(file.filename)[0] + '_converted.pdf'
        converted_filepath = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
        i2pconverter(filename, converted_filepath)
        
        global file_path
        file_path = converted_filepath
        
        return render_template('converted.html')
    return redirect(request.url)

@app.route('/download')
def download():
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run()



