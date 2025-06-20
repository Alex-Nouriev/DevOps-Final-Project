# Student Grades CI/CD Project

## תיאור
יישום Flask להצגת ציוני סטודנט בתואר, עם CI/CD מלא ופריסה ב-Render.

## ארכיטקטורה
- Flask API (app/)
- Prometheus metrics + Grafana dashboard
- Containerized with Docker & Docker Compose
- CI: GitHub Actions (lint, tests, build)
- CD: Render via GitHub Actions

## התקנה והרצה מקומית
```bash
git clone <repo_url>
cd student-grades-ci-cd
docker-compose up --build
```

## Endpoints
- `GET /api/courses/averages` — ממוצע ציוני כיתה לפי קורס
- `GET /api/student/{id}/averages` — ציוני סטודנט, ממוצע כולל, השוואות
- `/metrics` — Prometheus metrics

## פריסה ב-Render
כל `push` ל-`main` מפעיל CD אוטומטי ל-Render.

![CI Status](https://img.shields.io/github/actions/workflow/status/<user>/student-grades-ci-cd/ci.yml)
