from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

uploaded_files = []  # In-memory storage for files and timestamps

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Store the filename and the upload timestamp
    uploaded_files.append({
        'name': filename,
        'timestamp': datetime.now().isoformat()
    })

    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify(uploaded_files)

if __name__ == '__main__':
    app.run(debug=True)
