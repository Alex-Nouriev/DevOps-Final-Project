from prometheus_client import Counter, Histogram, make_wsgi_app

request_counter = Counter(
    'flask_requests_total',
    'Total number of HTTP requests'
)
response_histogram = Histogram(
    'flask_response_seconds',
    'Histogram of HTTP response times'
)

def setup_metrics(app):
    app.wsgi_app = make_wsgi_app()
