import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_courses_avg_endpoint(client):
    rv = client.get('/api/courses/averages')
    assert rv.status_code == 200

def test_student_avg_endpoint(client):
    rv = client.get('/api/student/1/averages')
    data = rv.get_json()
    assert 'overall_average' in data
