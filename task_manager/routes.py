from task_manager import app
from flask import render_template, redirect, url_for, flash, request
from task_manager.models import Task, User
from task_manager.forms import AddTaskForm, RegisterForm, LoginForm, DoneTaskForm, DeleteTask
from task_manager import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/task', methods=['GET', 'POST'])
@login_required
def task_page():
    form = AddTaskForm()
    done_form = DoneTaskForm()
    delete_form = DeleteTask()

    tasks = current_user.tasks
    return render_template('task.html', tasks=tasks, form=form, done_form=done_form, delete_form=delete_form)

@app.route('/add', methods=['POST'])
def add_task():
    form = AddTaskForm()
    done_form = DoneTaskForm()
    delete_form = DeleteTask()

    if form.validate_on_submit():
        task_to_create = Task(name=form.name.data,
                              description=form.description.data,
                              owner=current_user.id)
        db.session.add(task_to_create)
        db.session.commit()
        return redirect(url_for('task_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Uups coś poszło nie tak: {err_msg}', category='danger')

    return render_template('task.html', form=form, done_form=done_form, delete_form=delete_form)


@app.route('/done', methods=['POST'])
def done_task():
    form = AddTaskForm()
    done_form = DoneTaskForm()
    delete_form = DeleteTask()

    if request.method == "POST":
            done_task = request.form.get('done_task')# zaczytuje id taska z formularza (zaczytuje obiekt)
            d_task_object = Task.query.filter_by(id=done_task).first()# wyszukuje nazwę obiektu w db
            if d_task_object in current_user.tasks:# sprawdza czy obiekt jest własnością bieżącego użytkownika
                d_task_object.done()# aktywuje metodnę done() celem oznaczenia jako wykonane
                flash(f'Zadanie zostało wykonane!', category='success')
            else:
                flash(f'Nie znaleziono zadania')
            return redirect(url_for('task_page'))

    return render_template('task.html', form=form, done_form=done_form, delete_form=delete_form)

@app.route('/delete', methods=['POST'])
def delete_task():
    form = AddTaskForm()
    done_form = DoneTaskForm()
    delete_form = DeleteTask()

    if request.method == "POST":
            delete_task = request.form.get('delete_task')# wyszukuje id taska z formularza
            del_task_object = Task.query.filter_by(id=delete_task).first()# wyszukuje nazwę zaczytanego obiektu w db
            if del_task_object in current_user.tasks:# sprawdza czy obiekt jest własnością bieżącego użytkownika
                del_task_object.delete(del_task_object)# aktywuje metodę delete() i przekazuje do niej obiekt
                flash(f'Zadanie zostało wykonane!', category='success')
            else:
                flash(f'Nie znaleziono zadania')
            return redirect(url_for('task_page'))

    return render_template('task.html', form=form, done_form=done_form, delete_form=delete_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('task_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Nie można utworzyć konta:{err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Zostałeś poprawnie zalogowany jako: {attempted_user.username}', category='success')
            return redirect(url_for('task_page'))
        else:
            flash(f'Nazwa użytkownika lub hasło są niepoprawne! Spróbuj ponownie', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Zostałeś poprawnie wylogowany.", category='info')
    return redirect(url_for("home_page"))