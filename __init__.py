from flask import Flask, jsonify, render_template
import os
import time
from .blueprints import tasks as tasks_bp

app = Flask(__name__, static_folder='static')
app.register_blueprint(tasks_bp.bp)

VERSION = os.environ.get('VERSION', 'unknown')

if __name__ == '__main__':
    app.run()

def get_status():
    return jsonify({
        "status": "OK",
        "version": VERSION,
        "timestamp": time.time()
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return get_status()

