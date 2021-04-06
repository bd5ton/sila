from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import time

from .models import db
from .blueprints import tasks as tasks_bp
from .blueprints import admin as admin_bp

app = Flask(__name__, static_folder='static')
app.register_blueprint(tasks_bp.bp)
app.register_blueprint(admin_bp.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

VERSION = os.environ.get('VERSION', 'unknown')

if __name__ == '__main__':
    app.run()


# Routes

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
