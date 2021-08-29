from wtforms import Form, HiddenField, StringField, TextAreaField, SelectField, validators
from .models import PhaseTypeEnum


class ProjectForm(Form):
    id = HiddenField('id')
    name = StringField('Name', [validators.Length(min=1, max=100)])
    description = TextAreaField('Description', [validators.Length(min=0, max=2000)])


class PhaseForm(Form):
    type_choices = [(choice.value, choice.to_name()) for choice in list(PhaseTypeEnum)]
    type = SelectField('type', choices=type_choices)
    src_dir = StringField('Directory (relative to SOURCE_ROOT) containing input image files for this phase.', [validators.Length(min=1, max=5000)], default='/')
    dest_dir = StringField('Directory (relative to SOURCE_ROOT) where processed images should be stored.', [validators.Length(min=1, max=5000)], default='/')
