from flask_wtf import FlaskForm
from wtforms import SelectField


class AddTagForm(FlaskForm):

    tag = SelectField('Add a Tag: ', coerce=int)