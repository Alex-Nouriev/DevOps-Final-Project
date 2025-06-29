import logging
import threading
import time
import requests
from typing import Any, Dict

from flask import Flask, request, jsonify, Response
from prometheus_client import (
    CollectorRegistry, Gauge, CONTENT_TYPE_LATEST, generate_latest
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = Flask(__name__)

# Data structures
services: Dict[str, Dict[str, Any]] = {}
services_lock = threading.Lock()

# Prometheus metrics
registry = CollectorRegistry()

SERVICE_COUNT = Gauge(
    'service_tracker_total_services',
    'Total number of monitored services',
    registry=registry,
)
ACTIVE_SERVICES = Gauge(
    'service_tracker_active_services',
    'Number of services currently up',
    registry=registry,
)
INACTIVE_SERVICES = Gauge(
    'service_tracker_inactive_services',
    'Number of services currently down',
    registry=registry,
)
SERVICE_UPTIME_RATIO = Gauge(
    'service_tracker_uptime_ratio',
    'Service uptime ratio (per service)',
    ['name'],
    registry=registry,
)
TOTAL_REQUESTS = Gauge(
    'service_tracker_total_requests',
    'Total number of health check requests across all services',
    registry=registry,
)


@app.route('/service', methods=['POST'])
def add_service() -> Response:
    data = request.get_json(force=True)
    name = data.get('name')
    url = data.get('url')
    interval = int(data.get('interval', 60))

    if not name or not url:
        return jsonify({'error': "Missing 'name' or 'url'"}), 400

    with services_lock:
        if name in services:
            return jsonify({'error': 'Service already exists'}), 400
        services[name] = {
            'url': url,
            'interval': interval,
            'last_check': 0.0,
            'is_up': False,
            'check_count': 0,
            'success_count': 0,
        }
        SERVICE_COUNT.set(len(services))

    logging.info("Added service %s for monitoring (interval\
                 =%s s)", name, interval)
    return jsonify({'message': f"Service '{name}' added."}), 201


@app.route('/service/<name>', methods=['GET'])
def get_service_status(name: str) -> Response:
    with services_lock:
        svc = services.get(name)
    if svc is None:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify({
        'name': name,
        'url': svc['url'],
        'is_up': svc['is_up'],
        'total_checks': svc['check_count'],
        'successful_checks': svc['success_count'],
        'uptime_ratio': (
            svc['success_count'] / svc['check_count']
            if svc['check_count'] > 0 else None
        )
    })


@app.route('/metrics', methods=['GET'])
def metrics() -> Response:
    data = generate_latest(registry)
    return data, 200, {'Content-Type': CONTENT_TYPE_LATEST}


def _monitor_loop() -> None:
    logging.info("Starting monitor thread")
    while True:
        now = time.time()
        with services_lock:
            items = list(services.items())

        up_count = 0
        total_requests = 0

        for name, svc in items:
            if now - svc['last_check'] < svc['interval']:
                continue

            try:
                resp = requests.get(svc['url'], timeout=5)
                is_up = resp.status_code == 200
            except Exception as exc:
                logging.warning("Health check failed for %s: %s", name, exc)
                is_up = False

            with services_lock:
                svc['last_check'] = now
                svc['check_count'] += 1
                if is_up:
                    svc['success_count'] += 1
                    up_count += 1

                if svc['check_count'] > 0:
                    ratio = svc['success_count'] / svc['check_count']
                    SERVICE_UPTIME_RATIO.labels(name=name).set(ratio)

                total_requests += svc['check_count']

        with services_lock:
            total = len(services)
            SERVICE_COUNT.set(total)
            ACTIVE_SERVICES.set(up_count)
            INACTIVE_SERVICES.set(total - up_count)
            TOTAL_REQUESTS.set(sum(s['check_count \
                                     '] for s in services.values()))

        time.sleep(1)


if __name__ == '__main__':
    thread = threading.Thread(target=_monitor_loop, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
