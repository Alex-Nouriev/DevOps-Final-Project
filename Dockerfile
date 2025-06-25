FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/metrics || exit 1
CMD ["python", "main.py"]