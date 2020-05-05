from flask import (
    Flask, render_template, 
    request, redirect, 
    url_for, flash,
    send_file
    )
from werkzeug.utils import secure_filename
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config["UPLOAD_FOLDER"] = os.environ["UPLOAD_FOLDER"]

@app.route("/", methods=['GET', 'POST'])
def home(): 
    if request.method == 'GET':
       return render_template("home.html")
    if request.method == "POST":
        if 'image' not in request.files:
           flash('No file was uploaded')
           return redirect(request.url)
        image_file = request.files['image']

        if image_file.filename == '':
            flash('No file was uploaded')
            return redirect(request.url)
        
        if image_file and is_allowed_file(image_file.filename):
            passed = False
            try:
                filename = generate_filenames(image_file.filename)
                filePath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                print("filepath", filePath)
                image_file.save(filePath)
                passed = True
            except Exception:
                passed = False
            if passed: 
                return redirect(url_for('predict', filename=filename))
            else:
                flash('An error occured, try again')
                return redirect(request.url)

def is_allowed_file(filename):
    VALID_EXTENSIONS = ['png', 'bmp', 'jpg', 'jpeg', 'gif']
    is_valid_ext = filename.rsplit(".", 1)[1].lower() in VALID_EXTENSIONS
    return '.' in filename and is_valid_ext

def generate_filenames(filename):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ext = filename.split(".")[-1]
    random_indexes = [random.randint(0, len(LETTERS)-1) for _ in range(3)]
    random_chars = ''.join([LETTERS[index] for index in random_indexes])
    new_name = "{name}.{extension}".format(name=random_chars, extension=ext)
    return secure_filename(new_name)


@app.route('/predict/<filename>', methods=['GET'])
def predict(filename):
    return render_template('predict.html')

@app.route("/images/<filename>", methods=['GET'])   
def images(filename):
    return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html'), 500

if __name__ == "__main__":
    app.run("127.0.0.1")