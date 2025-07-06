from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# Create DB if it doesn't exist
if not os.path.exists('todo.db'):
    with app.app_context():
        db.create_all()

# Home route with optional search
@app.route('/', methods=['GET'])
def index():
    query = request.args.get('q')
    if query:
        tasks = Task.query.filter(Task.content.contains(query)).all()
    else:
        tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Add new task
@app.route('/add', methods=['POST'])
def add():
    content = request.form['task']
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Mark task as completed
@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)