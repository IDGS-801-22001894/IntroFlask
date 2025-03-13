from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, IntegerField, DateField, RadioField
from wtforms import validators
from wtforms.validators import DataRequired
from datetime import datetime

# Formulario original (para tu otro proyecto)
class UserForm(Form):
    matricula = IntegerField("Matricula", [
        validators.DataRequired(message="El campo es requerido"),
    ])
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])
    apellido = StringField("Apellido", [
        validators.DataRequired(message="El campo es requerido")
    ])
    correo = EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido")
    ])

class ZodiacoForm(Form):
    nombreZ = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")
    ])
    apellidoMaterno = StringField("Apellido Materno", [
        validators.DataRequired(message="El campo es requerido")
    ])
    apellidoPaterno = StringField("Apellido Paterno", [
        validators.DataRequired(message="El campo es requerido")
    ])
    dia = IntegerField("Día", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=31, message="El día debe estar entre 1 y 31")
    ])
    mes = IntegerField("Mes", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=12, message="El mes debe estar entre 1 y 12")
    ])
    año = IntegerField("Año", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1900, max=datetime.now().year, message=f"El año debe estar entre 1900 y {datetime.now().year}")
    ])
    sexo = RadioField("Sexo", choices=[
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino')
    ], validators=[
        validators.DataRequired(message="El campo es requerido")
    ])