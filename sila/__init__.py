from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import time

from .models import db, Project
from .blueprints import admin as admin_bp
from .blueprints import projects as projects_bp

app = Flask(__name__, static_folder='static')
app.register_blueprint(admin_bp.bp)
app.register_blueprint(projects_bp.bp)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db.init_app(app)

VERSION = os.environ.get('VERSION', 'unknown')

if __name__ == '__main__':
    app.run()


# Routes

@app.route('/')
def index():
    data = {
        'page_title': 'Dashboard'
    }
    return render_template('index.html', **data)

def get_status():
    return jsonify({
        "status": "OK",
        "version": VERSION,
        "timestamp": time.time()
    })

@app.route('/health')
def health():
    return get_status()

@app.route('/wip')
def wip():
    return render_template('wip.html')

