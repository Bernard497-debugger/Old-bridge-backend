from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'posts.json'
UPLOAD_FOLDER = 'uploads'
ADMIN_TOKEN = 'secret-token-bernard-2025'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(DATA_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

@app.route('/')
def home():
    return "✅ Oldbridge Backend with Image Upload is Running"

@app.route('/api/post', methods=['POST'])
def create_post():
    token = request.headers.get('Authorization')
    if token != ADMIN_TOKEN:
        return jsonify({'error': '❌ Unauthorized'}), 403

    title = request.form.get('title')
    message = request.form.get('message')
    image = request.files.get('image')

    image_url = None
    if image:
        filename = image.filename
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        image_url = f"/uploads/{filename}"

    post = {'title': title, 'message': message, 'image': image_url}
    posts = load_posts()
    posts.append(post)
    save_posts(posts)
    return jsonify({'message': '✅ Post saved!', 'data': post})

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify({'posts': load_posts()})

@app.route('/api/delete', methods=['POST'])
def delete_post():
    token = request.headers.get('Authorization')
    if token != ADMIN_TOKEN:
        return jsonify({'error': '❌ Unauthorized'}), 403
    index = request.json.get('index')
    posts = load_posts()
    if index is not None and 0 <= index < len(posts):
        removed = posts.pop(index)
        save_posts(posts)
        return jsonify({'message': '🗑️ Post deleted', 'deleted': removed})
    else:
        return jsonify({'error': 'Invalid index'}), 400

@app.route('/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
