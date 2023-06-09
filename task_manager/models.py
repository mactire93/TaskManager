from task_manager import db, login_manager
from datetime import datetime
from task_manager import bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    # funkcja odpowiadająca za załadowanie logowanego użytkownika
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    tasks = db.relationship('Task', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # funkcja kodująca hasło
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        # funkcja porównująca podane hasło przy próbie logowania
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=False)
    #pub_date = db.Column(db.DateTime(), default=datetime.utcnow)
    pub_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    done_task = db.Column(db.Boolean(), unique=False, default=False)

    def __repr__(self):
        return f'Task {self.name}'

    def done(self):
        self.done_task = True
        self.pub_date = func.now()
        db.session.commit()

    def delete(self, task):
        #usuwa wyszukany element z db
        db.session.delete(task)
        db.session.commit()