import pytest
from app.models import (get_course_averages, get_overall_average,
                        get_student_scores)


def test_course_averages():
    avgs = get_course_averages()
    assert any(c['course'] == 'Math' for c in avgs)


def test_overall_average():
    assert get_overall_average() == pytest.approx((85 + 90 + 75) / 3)


def test_student_scores():
    scores = get_student_scores(1)
    assert len(scores) == 2
