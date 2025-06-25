# 🧪 DevOps Final Project – Flask Service Monitor

[![CI](https://github.com/Alex-Nouriev/DevOps-Final-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/Alex-Nouriev/DevOps-Final-Project/actions/workflows/ci.yml)
[![CD](https://github.com/Alex-Nouriev/DevOps-Final-Project/actions/workflows/deploy.yml/badge.svg)](https://github.com/Alex-Nouriev/DevOps-Final-Project/actions/workflows/deploy.yml)
![Last Commit](https://img.shields.io/github/last-commit/Alex-Nouriev/DevOps-Final-Project)
![GitHub stars](https://img.shields.io/github/stars/Alex-Nouriev/DevOps-Final-Project?style=social)

---

## 📌 Overview

A simple **Flask-based API service monitor** built as part of a DevOps course.  
The app allows users to register external services and continuously monitor their health (uptime) using HTTP checks, with **Prometheus & Grafana** for metrics collection and visualization.

---

## 🧱 Project Architecture

```plaintext
                        ┌────────────┐
                        │  Grafana   │◄────┐
                        └─────┬──────┘     │
                              │            │
                       ┌──────▼─────┐      │
                       │ Prometheus │◄─────┘
                       └──────┬─────┘
                              │
                ┌─────────────┴─────────────┐
                │ Flask API (monitored app)│
                └──────────────────────────┘
```

- `Flask` app exposes:
  - Health monitoring endpoints
  - Prometheus metrics
- `Prometheus` scrapes metrics from Flask + node-exporter
- `Grafana` displays live dashboard
- `CI/CD`: GitHub Actions builds/tests/deploys automatically

---

## 🚀 Quick Start (Local Monitoring)

> ⚠️ Make sure Docker is installed

```bash
# 1. Clone the repository
git clone https://github.com/Alex-Nouriev/DevOps-Final-Project.git
cd DevOps-Final-Project

# 2. Start services locally
docker-compose up --build -d
```

### Access:
- **Flask API**: [http://localhost:5000](http://localhost:5000)
- **Grafana**: [http://localhost:3000](http://localhost:3000)  
  _User_: `admin`, _Password_: `admin`
- **Prometheus**: [http://localhost:9090](http://localhost:9090)

---

## 🔧 API Endpoints

### ➕ Register a Service

```http
POST /service
Content-Type: application/json

{
  "name": "my-service",
  "url": "http://example.com",
  "interval": 10
}
```

### 📊 Get Service Status

```http
GET /service/my-service
```

### 📈 Metrics for Prometheus

```http
GET /metrics
```

### 🔁 CI/CD Test Endpoint

To demo CI/CD, uncomment in `main.py`:

```python
# @app.route('/cicd-test')
# def cicd_test():
#     return "CI/CD Pipeline Working!", 200
```

Commit & push → watch GitHub Actions → auto-deploy via Render.

---

## 🛠 CI/CD with GitHub Actions

| Stage | Trigger | Description |
|-------|---------|-------------|
| ✅ CI | Pull Request | Flake8 lint, pytest, Docker build |
| 🚀 CD | Push to `main` | Docker Hub push + deploy to Render |

### 🔐 GitHub Secrets Required

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

---

## 📊 Dashboards

Grafana dashboard JSON is located in:  
`grafana/dashboards/metrics-dashboard.json`

It visualizes:
- Total registered services
- Per-service uptime ratio
- Health check counters

---

## 📁 Project Structure

```plaintext
DevOps-Final-Project/
├── app/                     # Flask app
├── grafana/                 # Dashboards & provisioning
├── prometheus/              # prometheus.yml config
├── tests/                   # Unit tests
├── .github/workflows/       # GitHub Actions CI/CD
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 📑 Authors & Collaboration

Built by Alex Nouriev  
[Add `saarsalhov@gmail.com` as collaborator for Render deployment access]

---

## ✅ License

MIT License
