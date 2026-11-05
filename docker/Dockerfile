# ─── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install dependencies into an isolated prefix so the final image stays lean
COPY app/requirements.txt .
RUN pip install --upgrade pip --quiet \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="Kartik <kartikjangra5366@gmail.com>" \
      version="1.0.0" \
      description="DevOps Lab 1 — Flask CI/CD demo application"

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy pre-built packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ .

# Ownership
RUN chown -R appuser:appuser /app

USER appuser

# Flask config
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

# Health check — Docker will poll /health every 30 s
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
