from flask import (
    Flask,
    request, 
    redirect, 
    url_for,
    jsonify,
    make_response
    )
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import random
from predict import make_prediction

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config["UPLOAD_FOLDER"] = os.environ["UPLOAD_FOLDER"]

@app.route("/api/image", methods=['POST'])
def post_image():
    if 'image' not in request.files:
        return make_response(jsonify({message: "You have to provide an image"}), 401)
    image_file = request.files['image']

    if image_file.filename == '':
        return make_response(jsonify({message: "You have to provide an image"}), 401)

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
            image_file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            prediction =  make_prediction('./trashnet.pt', image_file_path)
            print("prediction", prediction)
            return jsonify({"prediction": prediction}), 200
        else:
            return make_response(jsonify({message: "An internal Error occured"}), 500)


def is_allowed_file(filename):
    VALID_EXTENSIONS = ['png', 'bmp', 'jpg', 'jpeg', 'gif']
    print(filename)
    is_valid_ext = filename.rsplit(".", 1)[1].lower() in VALID_EXTENSIONS
    return '.' in filename and is_valid_ext

def generate_filenames(filename):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    ext = filename.split(".")[-1]
    random_indexes = [random.randint(0, len(LETTERS)-1) for _ in range(3)]
    random_chars = ''.join([LETTERS[index] for index in random_indexes])
    new_name = "{name}.{extension}".format(name=random_chars, extension=ext)
    return secure_filename(new_name)
    
if __name__ == "__main__":
    app.run("192.168.43.156")