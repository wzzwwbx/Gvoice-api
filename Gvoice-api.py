# coding=utf-8

from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import send_from_directory
from werkzeug import secure_filename
import sys, os
import crawler
import iat
import tts

app = Flask(__name__)

UPLOAD_FOLDER = 'wav'
ALLOWED_EXTENSIONS = set(['pcm', 'wav'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Something WRONG!'}), 404)


@app.route('/gvoice/api/v1.0/query', methods=['POST'])
def create_query():
    if not request.json or not 'query' in request.json:
        abort(404)
    query_string = request.json['query']
    print(query_string)
    result = query(query_string)
    print(result)
    return jsonify({'result': result}), 200


@app.route('/gvoice/api/v1.0/audio', methods=['POST'])
def create_audio():
    if not request.json or not 'text' in request.json:
        abort(404)
    text = request.json['text']
    print(text)
    result = tts.get_audio(text)
    print(result)
    filename = 'tts.wav'
    return jsonify({'filename': filename}), 200


@app.route('/gvoice/api/v1.0/audio', methods=['GET'])
def download_audio():
    filename = 'tts.wav'
    dir = os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'])
    if os.path.isfile(os.path.join(dir, filename)):
        return send_from_directory(dir, filename, as_attachment=True), 200
    else:
        abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/gvoice/api/v1.0/upload', methods=['POST'])
def get_recognize_result():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename('upload.wav')
        file.save(os.path.join(sys.path[0], app.config['UPLOAD_FOLDER'], filename))
    else:
        return abort(404)
    
    text = iat.get_text()
    print(text)
    return jsonify({'result': text}), 200


def query(query_string):
    return crawler.search(query_string)


if __name__ == '__main__':
    app.run(host='192.168.132.51')
