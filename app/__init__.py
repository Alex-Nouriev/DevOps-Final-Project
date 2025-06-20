from flask import Flask
from .routes import bp
from .metrics import setup_metrics

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    setup_metrics(app)
    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000)
```  

## app/models.py
```python
import sqlite3

DB_PATH = 'grades.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_course_averages():
    conn = get_connection()
    cur = conn.execute(
        "SELECT course, AVG(grade) AS avg_grade FROM grades GROUP BY course"
    )
    return [dict(row) for row in cur]

def get_overall_average():
    conn = get_connection()
    cur = conn.execute("SELECT AVG(grade) AS avg_grade FROM grades")
    return cur.fetchone()['avg_grade']

def get_student_scores(student_id):
    conn = get_connection()
    cur = conn.execute(
        "SELECT course, grade FROM grades WHERE student_id = ?",
        (student_id,)
    )
    return [dict(row) for row in cur]
