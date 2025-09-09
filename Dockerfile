# Dockerfile
FROM python:3.12-slim

# Prevent .pyc files & ensure logs flush
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Add application code
COPY . .

# Drop privileges
USER appuser

# Cloud Run provides $PORT; default to 8080 for local runs
ENV PORT=8080

# Sensible Gunicorn defaults; override via env if needed
# WEB_CONCURRENCY, GUNICORN_THREADS, GUNICORN_TIMEOUT are optional
CMD [ "bash", "-lc", "exec gunicorn --workers ${WEB_CONCURRENCY:-2} --threads ${GUNICORN_THREADS:-4} --timeout ${GUNICORN_TIMEOUT:-120} -b 0.0.0.0:${PORT} wsgi:app" ]
