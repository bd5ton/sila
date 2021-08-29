"""Project related endpoints.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for

from sila.models import db, Project, Phase, PhaseTypeEnum
from sila.forms import ProjectForm, PhaseForm

bp = Blueprint('projects', __name__, url_prefix='/projects')


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

    phase = Phase(project=project, type=phase_type, order=order, src_dir=src_dir, dest_dir=dest_dir)
    db.session.add(phase, )
    db.session.commit()

    return redirect(url_for('projects.project_edit', project_id=project_id))

@bp.route('/<int:project_id>/phase/<int:phase_order>/remove', methods=['POST'])
def project_remove_phase(project_id, phase_order):

    project = Project.query.get(project_id)
    phase = project.phases.filter(Phase.order==phase_order).first() # Phase.query.get(phase_id)

    db.session.delete(phase)
    db.session.commit()

    return redirect(url_for('projects.project_edit', project_id=project_id))