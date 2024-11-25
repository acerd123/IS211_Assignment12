from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('hw13.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Login</title>
        </head>
        <body>
            <h1>Login</h1>
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br><br>

                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br><br>

                <button type="submit">Login</button>
            </form>
        </body>
        </html>
    ''')


@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Dashboard</title>
        </head>
        <body>
            <h1>Dashboard</h1>

            <h2>Students</h2>
            <table>
                <tr><th>ID</th><th>First Name</th><th>Last Name</th></tr>
                {% for student in students %}
                <tr>
                    <td>{{ student.id }}</td>
                    <td>{{ student.first_name }}</td>
                    <td>{{ student.last_name }}</td>
                    <td><a href="{{ url_for('student_results', id=student.id) }}">View Results</a></td>
                </tr>
                {% endfor %}
            </table>

            <h2>Quizzes</h2>
            <table>
                <tr><th>ID</th><th>Subject</th><th>Number of Questions</th><th>Quiz Date</th></tr>
                {% for quiz in quizzes %}
                <tr>
                    <td>{{ quiz.id }}</td>
                    <td>{{ quiz.subject }}</td>
                    <td>{{ quiz.num_questions }}</td>
                    <td>{{ quiz.quiz_date }}</td>
                </tr>
                {% endfor %}
            </table>

            <a href="{{ url_for('add_student') }}">Add Student</a><br>
            <a href="{{ url_for('add_quiz') }}">Add Quiz</a><br>
            <a href="{{ url_for('add_result') }}">Add Result</a><br>
        </body>
        </html>
    ''', students=students, quizzes=quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        conn = get_db_connection()
        conn.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Add Student</title>
        </head>
        <body>
            <h1>Add Student</h1>
            <form method="POST">
                <label for="first_name">First Name:</label>
                <input type="text" id="first_name" name="first_name" required><br><br>

                <label for="last_name">Last Name:</label>
                <input type="text" id="last_name" name="last_name" required><br><br>

                <button type="submit">Add Student</button>
            </form>
        </body>
        </html>
    ''')


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = request.form['quiz_date']
        conn = get_db_connection()
        conn.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)', (subject, num_questions, quiz_date))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Add Quiz</title>
        </head>
        <body>
            <h1>Add Quiz</h1>
            <form method="POST">
                <label for="subject">Subject:</label>
                <input type="text" id="subject" name="subject" required><br><br>

                <label for="num_questions">Number of Questions:</label>
                <input type="number" id="num_questions" name="num_questions" required><br><br>

                <label for="quiz_date">Quiz Date:</label>
                <input type="date" id="quiz_date" name="quiz_date" required><br><br>

                <button type="submit">Add Quiz</button>
            </form>
        </body>
        </html>
    ''')


@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()

    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        conn = get_db_connection()
        conn.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)', (student_id, quiz_id, score))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Add Result</title>
        </head>
        <body>
            <h1>Add Result</h1>
            <form method="POST">
                <label for="student_id">Select Student:</label>
                <select id="student_id" name="student_id" required>
                    {% for student in students %}
                        <option value="{{ student.id }}">{{ student.first_name }} {{ student.last_name }}</option>
                    {% endfor %}
                </select><br><br>

                <label for="quiz_id">Select Quiz:</label>
                <select id="quiz_id" name="quiz_id" required>
                    {% for quiz in quizzes %}
                        <option value="{{ quiz.id }}">{{ quiz.subject }}</option>
                    {% endfor %}
                </select><br><br>

                <label for="score">Score:</label>
                <input type="number" id="score" name="score" required><br><br>

                <button type="submit">Add Result</button>
            </form>
        </body>
        </html>
    ''', students=students, quizzes=quizzes)


@app.route('/student/<int:id>')
def student_results(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    results = conn.execute('SELECT * FROM results WHERE student_id = ?', (id,)).fetchall()
    conn.close()
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Student Results</title>
        </head>
        <body>
            <h1>Results for {{ student.first_name }} {{ student.last_name }}</h1>

            {% if results %}
                <table>
                    <tr><th>Quiz ID</th><th>Score</th></tr>
                    {% for result in results %}
                    <tr><td>{{ result.quiz_id }}</td><td>{{ result.score }}</td></tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No results available.</p>
            {% endif %}

            <a href="{{ url_for('dashboard') }}">Back to Dashboard</a>
        </body>
        </html>
    ''', student=student, results=results)


if __name__ == '__main__':
    app.run(debug=True)
