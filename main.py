from flask import render_template, request, redirect, Blueprint, url_for
from flask_login import login_required, current_user

from models import db, Todo

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.name)


@main.route('/task', methods=['POST', 'GET'])
@login_required
def task():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content,
                        user_id=current_user.id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('main.task'))
        except:
            return render_template('error.html', error='There was an issue adding your task')
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('task.html', tasks=tasks, name=current_user.name)


@main.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    if task_to_delete.user_id != current_user.id:
        return render_template("error.html", error="No task found")

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('main.task'))
    except:
        return render_template("error.html", error='There was problem while deleting')


@main.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if task_to_update.user_id != current_user.id:
        return render_template("error.html", error="No task found")

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for('main.task'))
        except:
            return render_template("error.html", error='There was a problem while update')
    else:
        return render_template('update.html', task=task_to_update)
