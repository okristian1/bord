from flask_wtf import Form
from wtforms import StringField, TextAreaField, TextField, SubmitField, validators, ValidationError

class ContactForm(Form):
  name = TextField("Navn",  [validators.Required("Vennligst fyll inn ditt navn.")])
  email = TextField("E-post",  [validators.Required("Vennligst fyll inn din e-post adresse."), validators.Email("Vennligst fyll inn din e-post adresse.")])
  subject = TextField("Emne",  [validators.Required("Venligst skriv inn et emne.")])
  message = TextAreaField("Melding",  [validators.Required("Venligst skriv en melding.")])
  submit = SubmitField("Send")
