from wtforms import Form, HiddenField, StringField, TextAreaField, validators

class ProjectForm(Form):
    id = HiddenField('id')
    name = StringField('Name', [validators.Length(min=1, max=100)])
    description = TextAreaField('Description', [validators.Length(min=0, max=2000)])
