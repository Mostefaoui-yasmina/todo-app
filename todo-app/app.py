from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialisation de l'application Flask et de la base de données
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'  # Pour la gestion des sessions
db = SQLAlchemy(app)

# Modèle User pour gérer l'inscription et la connexion
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Modèle Task pour gérer les tâches
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(10), nullable=False)
    due_date = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='in_progress')  # in_progress ou done
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Route pour la page d'accueil (tasks)
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    tasks_in_progress = Task.query.filter_by(status='in_progress').all()
    tasks_done = Task.query.filter_by(status='done').all()

    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='done').count()
    progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return render_template('tasks.html', tasks_in_progress=tasks_in_progress, tasks_done=tasks_done, progress_percentage=progress_percentage)

# Route pour la page de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "Username or Password is incorrect"

    return render_template('login.html')

# Route pour la page d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Rediriger vers la page de login après inscription

    return render_template('register.html')

# Route pour ajouter une nouvelle tâche
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    category = request.form['category']
    priority = request.form['priority']
    due_date = request.form['due_date']

    new_task = Task(title=title, category=category, priority=priority, due_date=due_date, user_id=session['user_id'])
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

# Route pour marquer une tâche comme terminée
@app.route('/mark_done/<int:task_id>')
def mark_done(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = 'done'
        db.session.commit()

    return redirect(url_for('index'))

# Route pour supprimer une tâche
@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('index'))
# Route pour se déconnecter
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
if __name__ == 'main':
    app.run(debug=True)