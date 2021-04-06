from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.Text(2000))
    phases = db.relationship('Phase', backref='project')

    def __repr__(self):
        return '<Project {} {}>'.format(self.id, self.name)


class PhaseTypeEnum(Enum):
    image_moderate = 1
    image_text_detection = 2
    image_crop = 3

    def to_name(self):
        PHASE_TYPE_NAMES = {
            self.image_moderate.value: 'image moderate',
            self.image_text_detection.value: 'image text detection',
            self.image_crop.value: 'image crop',
        }
        print(PHASE_TYPE_NAMES)
        return PHASE_TYPE_NAMES[self.value]


class Phase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(PhaseTypeEnum), unique=False, nullable=False)
    description = db.Column(db.Text(5000))

    db.UniqueConstraint('project_id', 'order', name='unique__phase_order__project_id')

    def __repr__(self):
        return '<Phase id:{} type:{} order:{} in project:{}>'.format(self.id, self.type, self.order, self.project_id)