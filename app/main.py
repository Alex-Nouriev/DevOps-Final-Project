import logging
import threading
import time
import requests
from typing import Any, Dict

from flask import Flask, request, jsonify, Response
from prometheus_client import (
    Counter, Gauge, CONTENT_TYPE_LATEST, generate_latest)

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
SERVICE_COUNT = Gauge(
    'service_tracker_total_services',
    'Total number of monitored services',
)
SERVICE_UPTIME_RATIO = Gauge(
    'service_tracker_uptime_ratio',
    'Service uptime ratio (per service)',
    ['name'],
)
CHECK_COUNT = Counter(
    'service_tracker_check_count_total',
    'Total number of health checks performed',
    ['name', 'status'],
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
            'up_since': None,
            'up_time': 0.0,
            'start_time': time.time(),
        }
        SERVICE_COUNT.set(len(services))

    logging.info("Added service %s for monitoring\
                  (interval=%s s)", name, interval)
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
        'up_since': svc['up_since'],
        'uptime_seconds': svc['up_time'],
    })

# @app.route('/cicd-test')
# def cicd_test():
#     return "CI/CD Pipeline Working!", 200


@app.route('/metrics', methods=['GET'])
def metrics() -> Response:
    data = generate_latest()
    return data, 200, {'Content-Type': CONTENT_TYPE_LATEST}


def _monitor_loop() -> None:
    logging.info("Starting monitor thread")
    while True:
        now = time.time()
        with services_lock:
            items = list(services.items())
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
                prev = svc['is_up']
                svc['last_check'] = now
                svc['is_up'] = is_up
                if is_up:
                    if not prev:
                        svc['up_since'] = now
                    svc['up_time'] += svc['interval']
                else:
                    svc['up_since'] = None

                uptime_ratio = svc['up_time'] / max(now - svc['start_time'], 1)
                SERVICE_UPTIME_RATIO.labels(name=name).set(uptime_ratio)
                status_label = 'up' if is_up else 'down'
                CHECK_COUNT.labels(name=name, status=status_label).inc()
        time.sleep(1)


if __name__ == '__main__':
    thread = threading.Thread(target=_monitor_loop, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
