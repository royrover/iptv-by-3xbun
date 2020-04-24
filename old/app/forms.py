from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddChannel(FlaskForm):
    channel = StringField('Channel', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    img_url = StringField('Image Url', validators=[DataRequired()])
    submit = SubmitField('Add')