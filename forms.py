from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators



class ContactForm(Form):
    name = StringField('Ditt navn:', [validators.DataRequired()])
    email = StringField('Din e-post adresse:', [validators.DataRequired(), validators.Email('your@email.com')])
    message = TextAreaField('Din beskjed:', [validators.DataRequired()])
    submit = ''
