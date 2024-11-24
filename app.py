from flask import Flask, render_template_string, request, redirect, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'hw13.db'

# Templates
login_template = """
<!doctype html>
<html>
    <head><title>Login</title></head>
    <body>
        <h1>Login</h1>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
        {% endwith %}
        <form method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    </body>
</html>
"""

dashboard_template = """
<!doctype html>
<html>
    <head><title>Dashboard</title></head>
    <body>
        <h1>Dashboard</h1>
        <h2>Students</h2>
        <table border="1">
            <tr><th>ID</th><th>First Name</th><th>Last Name</th><th>Actions</th></tr>
            {% for student in students %}
            <tr>
                <td>{{ student[0] }}</td>
                <td>{{ student[1] }}</td>
                <td>{{ student[2] }}</td>
                <td><a href="/student/{{ student[0] }}">View Results</a></td>
            </tr>
            {% endfor %}
        </table>
        <a href="/student/add">Add Student</a>
        <h2>Quizzes</h2>
        <table border="1">
            <tr><th>ID</th><th>Subject</th><th>Number of Questions</th><th>Date</th></tr>
            {% for quiz in quizzes %}
            <tr>
                <td>{{ quiz[0] }}</td>
                <td>{{ quiz[1] }}</td>
                <td>{{ quiz[2] }}</td>
                <td>{{ quiz[3] }}</td>
            </tr>
            {% endfor %}
        </table>
        <a href="/quiz/add">Add Quiz</a>
        <br>
        <a href="/results/add">Add Quiz Result</a>
    </body>
</html>
"""

add_student_template = """
<!doctype html>
<html>
    <head><title>Add Student</title></head>
    <body>
        <h1>Add Student</h1>
        <form method="POST">
            <label for="first_name">First Name:</label>
            <input type="text" id="first_name" name="first_name"><br>
            <label for="last_name">Last Name:</label>
            <input type="text" id="last_name" name="last_name"><br>
            <button type="submit">Add Student</button>
        </form>
    </body>
</html>
"""

add_quiz_template = """
<!doctype html>
<html>
    <head><title>Add Quiz</title></head>
    <body>
        <h1>Add Quiz</h1>
        <form method="POST">
            <label for="subject">Subject:</label>
            <input type="text" id="subject" name="subject"><br>
            <label for="num_questions">Number of Questions:</label>
            <input type="number" id="num_questions" name="num_questions"><br>
            <label for="quiz_date">Date:</label>
            <input type="date" id="quiz_date" name="quiz_date"><br>
            <button type="submit">Add Quiz</button>
        </form>
    </body>
</html>
"""

view_results_template = """
<!doctype html>
<html>
    <head><title>Quiz Results</title></head>
    <body>
        <h1>Quiz Results for Student</h1>
        {% if message %}
            <p>{{ message }}</p>
        {% else %}
        <table border="1">
            <tr><th>Quiz ID</th><th>Score</th></tr>
            {% for result in results %}
            <tr>
                <td>{{ result[0] }}</td>
                <td>{{ result[2] }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}
    </body>
</html>
"""

add_result_template = """
<!doctype html>
<html>
    <head><title>Add Quiz Result</title></head>
    <body>
        <h1>Add Quiz Result</h1>
        <form method="POST">
            <label for="student_id">Student:</label>
            <select id="student_id" name="student_id">
                {% for student in students %}
                <option value="{{ student[0] }}">{{ student[1] }} {{ student[2] }}</option>
                {% endfor %}
            </select><br>
            <label for="quiz_id">Quiz:</label>
            <select id="quiz_id" name="quiz_id">
                {% for quiz in quizzes %}
                <option value="{{ quiz[0] }}">{{ quiz[1] }}</option>
                {% endfor %}
            </select><br>
            <label for="score">Score:</label>
            <input type="number" id="score" name="score"><br>
            <button type="submit">Add Result</button>
        </form>
    </body>
</html>
"""

# Database Helpers
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with open('schema.sql', 'r') as f:
        conn = get_db_connection()
        conn.executescript(f.read())
        conn.commit()
        conn.close()

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            flash('Invalid credentials!')
    return render_template_string(login_template)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/login')

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()
    return render_template_string(dashboard_template, students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if 'logged_in' not in session:
        return redirect('/login')

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        conn = get_db_connection()
        conn.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template_string(add_student_template)

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if 'logged_in' not in session:
        return redirect('/login')

    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = request.form['quiz_date']
        conn = get_db_connection()
        conn.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                     (subject, num_questions, quiz_date))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template_string(add_quiz_template)

@app.route('/student/<int:id>')
def student_results(id):
    if 'logged_in' not in session:
        return redirect('/login')

    conn = get_db_connection()
    results = conn.execute('SELECT * FROM results WHERE student_id = ?', (id,)).fetchall()
    conn.close()

    if results:
        return render_template_string(view_results_template, results=results)
    else:
        return render_template_string(view_results_template, message="No Results")

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if 'logged_in' not in session:
        return redirect('/login')

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()

    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        conn = get_db_connection()
        conn.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                     (student_id, quiz_id, score))
        conn.commit()
        conn.close()
        return redirect('/dashboard')

    return render_template_string(add_result_template, students=students, quizzes=quizzes)

if __name__ == '__main__':
    init_db()  # Initialize the database with schema and data
    app.run(debug=True)
