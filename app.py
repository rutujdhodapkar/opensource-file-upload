from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SERVER_PASSWORD'] = '15010'
is_server_active = False
clients_connected = set()  # Set to keep track of connected clients

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
    clients_connected.clear()  # Clear connected clients on deactivation
    # Delete files when server is deactivated
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
    return jsonify({"message": "Server deactivated and files deleted."}), 200

@app.route('/connect', methods=['POST'])
def connect_client():
    client_password = request.json.get('client_password')
    if client_password == app.config['SERVER_PASSWORD']:
        clients_connected.add(request.remote_addr)  # Track connected client
        return jsonify({"message": "Connected to the server."}), 200
    return jsonify({"message": "Invalid passcode."}), 403

@app.route('/upload', methods=['POST'])
def upload_file():
    if not is_server_active:
        return jsonify({"message": "Server is not active."}), 403
    
    if not clients_connected:
        return jsonify({"message": "No clients connected."}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file part."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file."}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
    try:
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully.", "filename": file.filename}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to upload file: {str(e)}"}), 500

@app.route('/files', methods=['GET'])
def list_files():
    if not is_server_active:
        return jsonify({"message": "Server is not active."}), 403
    
    if not clients_connected:
        return jsonify({"message": "No clients connected."}), 403

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files), 200

if __name__ == '__main__':
    app.run(debug=True)
