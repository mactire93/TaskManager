from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, Email, ValidationError
from task_manager.models import User


class AddTaskForm(FlaskForm):
    name = StringField(label='Nazwa zadania:', validators=[Length(min=2, max=30), DataRequired()])
    description = TextAreaField(label='Krótki opis zadania:', validators=[Length(min=2, max=1024), DataRequired()])
    submit = SubmitField(label='Dodaj zadanie')

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Ta nazwa użytkownika już istnieje, proszę wprowadź inną.')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Ten adres e-mail już istnieje, proszę wprowadź inny.')

    username = StringField(label='Nazwa użytkownika:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Adres e-mail:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Hasło:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Powtórz hasło:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Zarejestruj')

class LoginForm(FlaskForm):
    username = StringField(label='Nazwa użytkownika:', validators=[DataRequired()])
    password = PasswordField(label='Hasło:', validators=[DataRequired()])
    submit = SubmitField(label='Zaloguj')

class DoneTaskForm(FlaskForm):
    submit = SubmitField(label='Oznacz jako wykonane')

class DeleteTask(FlaskForm):
    submit = SubmitField(label='Usuń zadanie')