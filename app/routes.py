from flask import Blueprint, jsonify
from .models import (
    get_course_averages,
    get_overall_average,
    get_student_scores
)
from .metrics import request_counter, response_histogram

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.before_request
def before_request():
    request_counter.inc()

@bp.route('/courses/averages')
def courses_avg():
    data = get_course_averages()
    return jsonify(data)

@bp.route('/student/<int:student_id>/averages')
def student_avg(student_id):
    scores = get_student_scores(student_id)
    overall = get_overall_average()
    courses = get_course_averages()
    return jsonify({
        'student_scores': scores,
        'overall_average': overall,
        'course_averages': courses
    })

@bp.after_request
def after_request(response):
    # response.elapsed not available; skip histogram timing or integrate via middleware
    return response
