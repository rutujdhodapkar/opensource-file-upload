import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime
import base64

app = Flask(__name__)

# Set your GitHub repo details here
GITHUB_TOKEN = os.getenv('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')  # Use an environment variable for the GitHub token
REPO_OWNER = 'rutujdhodapkar'
REPO_NAME = 'opensource-file-upload'
BRANCH = 'main'  # Branch where the files will be uploaded
GITHUB_API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/'

uploaded_files = []  # Keep a list of uploaded files and timestamps

# Function to upload a file to GitHub
def upload_to_github(file_content, file_name):
    url = GITHUB_API_URL + file_name
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Prepare file content in base64 encoding
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    data = {
        "message": f"Upload {file_name}",
        "content": encoded_content,
        "branch": BRANCH
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:  # Created
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Log the error
        return False

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # Read file content
    file_content = file.read()
    file_name = file.filename

    # Upload to GitHub
    success = upload_to_github(file_content, file_name)

    if success:
        # Store the uploaded file details and timestamp
        uploaded_files.append({
            'name': file_name,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Failed to upload to GitHub'}), 500

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify(uploaded_files)

if __name__ == '__main__':
    app.run(debug=True)
