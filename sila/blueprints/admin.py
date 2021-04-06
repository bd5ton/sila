"""Admin endpoints for SILA.
"""
from flask import Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from sila.models import db, Project, Phase

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/initdb', methods=['GET'])
def initdb():
    print(current_app.config)
    db.drop_all()
    db.create_all()

    fp = Project(name='bla project', description='gu kha shala')
    db.session.add(fp)
    db.session.commit()
    print(Project.query.all())

    ph = Phase(type='image_moderate', description='gu kheye mor shala', project=1, order=2)
    db.session.add(ph)
    db.session.commit()
    print(Phase.query.all())

    return 'Admin wants to initialize DB for SILA'