from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'posts.json'
ADMIN_TOKEN = 'secret-token-bernard-2025'

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
    return "✅ BK Admin-Only Backend is Running"

@app.route('/api/post', methods=['POST'])
def create_post():
    token = request.headers.get('Authorization')
    if token != ADMIN_TOKEN:
        return jsonify({'error': '❌ Unauthorized'}), 403

    content = request.json
    if not content:
        return jsonify({'error': 'No JSON provided'}), 400

    posts = load_posts()
    posts.append(content)
    save_posts(posts)
    return jsonify({'message': '✅ Post saved!', 'data': content})

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

if __name__ == '__main__':
    app.run(debug=True)
