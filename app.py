from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ToDoApp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    task = db.Column(db.String(500), nullable = False)
    done = db.Column(db.Boolean)

    def __init__(self, title, task, done):
        self.title = title
        self.task = task
        self.done = done

@app.route('/')
def index():
    all_tasks = db.session.query(Tasks).all()
    return render_template('index.html', tasks = all_tasks)

def task_validation(title, task):
    title = title.strip()
    task = task.strip()

    is_valid = True
    if not title or not task:
        is_valid = False

    return is_valid

@app.route('/add-task', methods = ['POST'])
def add_task():
    task_title = request.form['title']
    task_description = request.form['task']
    is_task_valid = task_validation(task_title, task_description)
    
    if not is_task_valid:
        flash('Please complete all fields', 'error')
        return redirect(url_for('index'))
    
    new_task = Tasks(title = task_title, task = task_description, done = False)

    db.session.add(new_task)
    db.session.commit()

    flash('Task added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/delete-task/<int:id>')
def delete_task(id):
    task = db.session.get(Tasks, id)
    db.session.delete(task)
    db.session.commit()

    flash('Task deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/done-task/<int:id>')
def done_task(id):
    task = db.session.get(Tasks, id)
    task.done = not(task.done)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/edit-task/<int:id>', methods = ['POST'])
def edit_task(id):
    task = db.session.get(Tasks, id)
    task.title = request.form['title']
    task.task = request.form['task']

    is_task_valid = task_validation(task.title, task.task)
    if not is_task_valid:
        flash('Please complete all fields', 'error')
        return redirect(url_for('index'))
    
    db.session.commit()
    flash('Task updated successfully', 'success')
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)