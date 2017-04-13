from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired

class CourseForm(FlaskForm):

	course = StringField('course', validators=[DataRequired()])