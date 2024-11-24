-- Create Students table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

-- Create Quizzes table
CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    quiz_date TEXT NOT NULL
);

-- Create Results table
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
);

-- Insert initial data
INSERT INTO students (first_name, last_name) VALUES ('John', 'Smith');

INSERT INTO quizzes (subject, num_questions, quiz_date) 
VALUES ('Python Basics', 5, '2015-02-05');

INSERT INTO results (student_id, quiz_id, score) 
VALUES (1, 1, 85);

