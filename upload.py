import sys, os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = 'wav'
ALLOWED_EXTENSIONS = set(['txt', 'pcm', 'wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploader')
def upload():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], filename))
        else:
            return 'Unsupported Extension!'

        return 'file uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)