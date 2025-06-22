# app/tests/conftest.py

import sqlite3
import pytest


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    db_file = tmp_path / 'grades.db'
    conn = sqlite3.connect(db_file)
    conn.execute('CREATE TABLE grades(student_id INT,\
                  course TEXT, grade REAL)')
    conn.execute("INSERT INTO grades VALUES (1, 'Math', 85), (1, 'CS', 90),\
                  (2, 'Math', 75)")
    conn.commit()
    monkeypatch.setattr('app.models.DB_PATH', str(db_file))
    return conn
