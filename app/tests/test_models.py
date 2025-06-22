import sqlite3
import pytest
from app.models import get_course_averages, get_overall_average, get_student_scores, DB_PATH

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    db_file = tmp_path / 'grades.db'
    conn = sqlite3.connect(db_file)
    conn.execute('CREATE TABLE grades(student_id INT, course TEXT, grade REAL)')
    conn.execute("INSERT INTO grades VALUES (1, 'Math', 85), (1, 'CS', 90), (2, 'Math', 75)")
    conn.commit()
    monkeypatch.setattr('app.models.DB_PATH', str(db_file))
    return conn


def test_course_averages():
    avgs = get_course_averages()
    assert any(c['course'] == 'Math' for c in avgs)


def test_overall_average():
    assert get_overall_average() == pytest.approx((85 + 90 + 75) / 3)


def test_student_scores():
    scores = get_student_scores(1)
    assert len(scores) == 2
