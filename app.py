from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SERVER_PASSWORD'] = '15010'
is_server_active = False

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/activate', methods=['POST'])
def activate_server():
    global is_server_active
    password = request.json.get('password')
    if password == app.config['SERVER_PASSWORD']:
        is_server_active = True
        return jsonify({"message": "Server activated."}), 200
    return jsonify({"message": "Invalid password."}), 403

@app.route('/deactivate', methods=['POST'])
def deactivate_server():
    global is_server_active
    is_server_active = False
    # Delete files when server is deactivated
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
    return jsonify({"message": "Server deactivated and files deleted."}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if not is_server_active:
        return jsonify({"message": "Server is not active."}), 403
    
    if 'file' not in request.files:
        return jsonify({"message": "No file part."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file."}), 400

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify({"message": "File uploaded successfully."}), 200

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/files', methods=['GET'])
def list_files():
    if not is_server_active:
        return jsonify({"message": "Server is not active."}), 403
    
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files), 200

if __name__ == '__main__':
    app.run(debug=True)
