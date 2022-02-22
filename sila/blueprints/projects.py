"""Project related endpoints.
"""
import os
import random
from shutil import move

from flask import abort, Blueprint, render_template, request, flash, redirect, url_for, send_from_directory

from sila.models import db, Project, Phase, PhaseTypeEnum
from sila.forms import ProjectForm, PhaseForm

bp = Blueprint('projects', __name__, url_prefix='/projects')

MODERATE_SAMPLE_SIZE = 5

@bp.route('/', methods=['GET'])
def projects():
    active_projects = Project.query.all()
    data = {
        'page_title': 'Projects',
        'active_projects': active_projects
    }
    return render_template('projects.html', **data)

@bp.route('/new/', methods=['GET', 'POST'])
def project_new():
    form = ProjectForm(request.form)

    if request.method == 'POST' and form.validate():
        project = Project(name=form.name.data, description=form.description.data)
        db.session.add(project)
        db.session.commit()
        flash(f'New project <strong>{project.name}</strong> is created.', 'success')
        return redirect(url_for('projects.projects'))

    else:
        data = {
            'page_title': 'Create Project',
            'form': form
        }
        return render_template('project-form.html', **data)

@bp.route('/<int:project_id>', methods=['GET', 'POST'])
def project_edit(project_id):

    def _render_with_form(form):
        data = {
            'page_title': 'Edit Project',
            'project': project,
            'form': form,
            'new_phase_form': new_phase_form,
        }
        return render_template('project-form.html', **data)

    project = Project.query.get(project_id)
    new_phase_form = PhaseForm()

    if request.method == 'POST':
        form = ProjectForm(request.form)
        if 'delete' in request.form:
            Project.query.filter_by(id=request.form['id']).delete()
            flash(f'Project <strong>{project.name}</strong> deleted', 'warning')
            db.session.commit()
            return redirect(url_for('projects.projects'))

        elif form.validate():
            project.name = form.name.data
            project.description = form.description.data
            db.session.commit()
            flash(f'Project <strong>{project.name}</strong> updated', 'info')
            return redirect(url_for('projects.projects'))

        else:
            return _render_with_form(form)

    else:
        form = ProjectForm(name=project.name, description=project.description, id=project.id)
        return _render_with_form(form)

@bp.route('/<int:project_id>/phase/add', methods=['POST'])
def project_add_phase(project_id):

    project = Project.query.get(project_id)
    phase_type = PhaseTypeEnum(int(request.form.get('type')))
    order = len(project.phases.all()) + 1
    src_dir = request.form.get('src_dir')
    dest_dir = request.form.get('dest_dir')
    reject_dir = request.form.get('reject_dir')

    phase = Phase(project=project, type=phase_type, order=order, src_dir=src_dir, dest_dir=dest_dir, reject_dir=reject_dir)
    db.session.add(phase, )
    db.session.commit()

    return redirect(url_for('projects.project_edit', project_id=project_id))

@bp.route('/<int:project_id>/phase/<int:phase_order>/remove', methods=['POST'])
def project_remove_phase(project_id, phase_order):

    project = Project.query.get(project_id)
    phase = project.phases.filter(Phase.order==phase_order).first()

    db.session.delete(phase)
    db.session.commit()

    return redirect(url_for('projects.project_edit', project_id=project_id))

@bp.route('/<int:project_id>/phase/<int:phase_order>/work', methods=['GET'])
def project_work_phase(project_id, phase_order):

    project = Project.query.get(project_id)
    phase = project.phases.filter(Phase.order==phase_order).first()

    if project.current_phase != phase.order:
        abort(404)

    SRC_DIR = os.path.join(os.environ['IMAGE_STORAGE_ROOT'], phase.src_dir)

    all_files = [f for f in os.listdir(SRC_DIR) if not f.startswith('.')]
    ALLOWED_FILE_EXTENSIONS = ''
    num_remaining = len(all_files)
    try:
        files = random.sample(all_files, MODERATE_SAMPLE_SIZE)
    except ValueError:
        files = all_files

    data = {
        'project': project,
        'phase': phase,
        'num_remaining': num_remaining,
        'files': files,
        'page_title': f'Phase - {phase.order} | {project.name}',
    }

    return render_template('work.html', **data)

@bp.route('/<int:project_id>/phase/<int:phase_order>/image/<path:filename>', methods=['GET'])
def project_phase_get_image(project_id, phase_order, filename):

    project = Project.query.get(project_id)
    phase = project.phases.filter(Phase.order==phase_order).first()

    if project.current_phase != phase.order:
        abort(404)

    SRC_DIR = os.path.join(os.environ['IMAGE_STORAGE_ROOT'], phase.src_dir)

    return send_from_directory(SRC_DIR, filename)

@bp.route('/<int:project_id>/phase/<int:phase_order>/image/<path:filename>/accept', methods=['POST'])
def project_phase_accept_image(project_id, phase_order, filename):

    project = Project.query.get(project_id)
    phase = project.phases.filter(Phase.order==phase_order).first()

    if project.current_phase != phase.order:
        abort(404)

    src = os.path.join(os.environ['IMAGE_STORAGE_ROOT'], phase.src_dir, filename)
    dst = os.path.join(os.environ['IMAGE_STORAGE_ROOT'], phase.dest_dir, filename)

    move(src, dst)
    return ('', 204)

@bp.route('/<int:project_id>/phase/<int:phase_order>/image/<path:filename>/reject', methods=['POST'])
def project_phase_reject_image(project_id, phase_order, filename):

    project = Project.query.get(project_id)
    phase = project.phases.filter(Phase.order==phase_order).first()

    if project.current_phase != phase.order:
        abort(404)

    src = os.path.join(os.environ['IMAGE_STORAGE_ROOT'], phase.src_dir, filename)
    dst = os.path.join(os.environ['IMAGE_STORAGE_ROOT'], phase.reject_dir, filename)

    move(src, dst)
    return ('', 204)