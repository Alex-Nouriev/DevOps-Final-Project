# Student Grades CI/CD Project
![CI](https://github.com/Alex-Nouriev/DevOps-Final-Project/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/Alex-Nouriev/DevOps-Final-Project/actions/workflows/deploy.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/Alex-Nouriev/DevOps-Final-Project)
![GitHub stars](https://img.shields.io/github/stars/Alex-Nouriev/DevOps-Final-Project?style=social)

## תיאור
יישום Flask להצגת ציוני סטודנט עם CI/CD מלא ופריסה חינמית על Render.

## ארכיטקטורה
- Flask API (app/)
- Prometheus metrics + Grafana dashboard
- Containerized with Docker & Docker Compose
- CI: GitHub Actions (lint, tests, build, cache)
- CD: Render via Webhook

## התקנה והרצה מקומית
```bash
git clone <repo_url>
cd student-grades-ci-cd
docker-compose up --build
```

## Endpoints
- `GET /` — בדיקת סטטוס
- `GET /api/courses/averages` — ממוצע ציוני כיתה לפי קורס
- `GET /api/student/{id}/averages` — ציוני סטודנט, ממוצע כולל, והשוואות
- `/metrics` — Prometheus metrics

## פריסה ב-Render
1. צור Web Service ב-Render (Docker)
2. הגדר Deploy Hook והכנס ל-Secrets `RENDER_DEPLOY_HOOK_URL`
3. Push ל-main מפרסם אוטומטית

## Screenshots
