"""Project related endpoints.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for

from sila.models import db, Project
from sila.forms import ProjectForm

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

@bp.route('/project/<int:project_id>', methods=['GET', 'POST'])
def project_edit(project_id):

    def _render_with_form(form):
        data = {
            'page_title': 'Edit Project',
            'form': form
        }
        return render_template('project-form.html', **data)

    project = Project.query.get(project_id)

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
