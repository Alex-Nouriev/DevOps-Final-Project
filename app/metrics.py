from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Metrics
request_counter = Counter(
    'flask_requests_total',
    'Total number of HTTP requests'
)
response_histogram = Histogram(
    'flask_response_seconds',
    'Histogram of HTTP response times'
)


def setup_metrics(app):
    # register metrics middleware on /metrics
    metrics_app = make_wsgi_app()
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': metrics_app
    })
