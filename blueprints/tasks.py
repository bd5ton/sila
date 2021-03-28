"""Tasks endpoints.
"""

from flask import Blueprint, request, g, render_template, send_from_directory
import json
import os
import random
from shutil import move
from uuid import uuid4

bp = Blueprint('task', __name__, url_prefix='/task')

MODERATE_SOURCE_DIR = os.environ['MODERATE_SOURCE_DIR']
MODERATE_SINK_DIR = os.environ['MODERATE_SINK_DIR']
MODERATE_REJECTED_DIR = os.environ['MODERATE_REJECTED_DIR']

MODERATE_SAMPLE_SIZE = 5

@bp.route('/moderate', methods=['GET'])
def moderate():
    all_files = os.listdir(MODERATE_SOURCE_DIR)
    num_remaining = len(all_files)
    try:
        files = random.sample(all_files, MODERATE_SAMPLE_SIZE)
    except ValueError:
        files = all_files
    return render_template('moderate.html', files=files, num_remaining=num_remaining)

@bp.route('/moderate/<path:filename>', methods=['GET'])
def moderate_get_file(filename):
    return send_from_directory(MODERATE_SOURCE_DIR, filename)

@bp.route('/moderate/<path:filename>/accept', methods=['POST'])
def moderate_accept_file(filename):
    src = f'{MODERATE_SOURCE_DIR}/{filename}'
    dst = f'{MODERATE_SINK_DIR}/{filename}'
    move(src, dst)
    return ('', 204)

@bp.route('/moderate/<path:filename>/reject', methods=['POST'])
def moderate_reject_file(filename):
    src = f'{MODERATE_SOURCE_DIR}/{filename}'
    dst = f'{MODERATE_REJECTED_DIR}/{filename}'
    move(src, dst)
    return ('', 204)