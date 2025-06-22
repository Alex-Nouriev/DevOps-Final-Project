import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_home_endpoint(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.get_json() == {'status': 'ok'}


def test_courses_avg_endpoint(client):
    rv = client.get('/api/courses/averages')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert 'course' in data[0]


def test_student_avg_endpoint(client):
    rv = client.get('/api/student/1/averages')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'overall_average' in data
    assert 'student_scores' in data
    assert 'course_averages' in data
