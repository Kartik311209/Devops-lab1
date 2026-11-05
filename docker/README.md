# Docker — DevOps Lab 1

> **Student:** Kartik | **Roll No.:** 2301730205

This directory contains the Docker configuration for containerising the **DevOps Lab 1 Flask application**.

---

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage production image (builder → runtime, non-root user) |
| `Dockerfile.test` | Single-stage test image — runs pytest and exits |
| `docker-compose.yml` | Orchestrates the app service and optional test runner |

`.dockerignore` lives at the project root and excludes git, venv, docs, and reports from the build context.

---

## Quick Start

All commands are run from the **project root** (`devops-lab-1-kartik/`).

### Build & run (production)
```bash
# Build the image
docker build -f docker/Dockerfile -t devops-lab1:latest .

# Run the container
docker run -d --name devops-lab1-app -p 5000:5000 devops-lab1:latest

# Verify
curl http://localhost:5000/health
# {"status":"UP","version":"1.0.0"}
```

### Using Docker Compose
```bash
# Start the app
docker compose -f docker/docker-compose.yml up -d

# Check health
docker compose -f docker/docker-compose.yml ps

# View logs
docker compose -f docker/docker-compose.yml logs -f app

# Stop
docker compose -f docker/docker-compose.yml down
```

### Run tests in a container
```bash
# Build test image and run pytest
docker build -f docker/Dockerfile.test -t devops-lab1-test:latest .
docker run --rm devops-lab1-test:latest

# Or with Docker Compose (--profile test)
docker compose -f docker/docker-compose.yml --profile test up tests
```

---

## Image Details

| Property | Value |
|----------|-------|
| Base image | `python:3.12-slim` |
| Build strategy | Multi-stage (builder + runtime) |
| Exposed port | `5000` |
| Run as user | `appuser` (non-root) |
| Health check | `GET /health` every 30 s |
| Environment | `FLASK_ENV=production` |

---

## Endpoints

| Route | Method | Response |
|-------|--------|---------|
| `/` | GET | `{"message":"DevOps Lab 1 CI/CD pipeline is working","version":"1.0.0"}` |
| `/health` | GET | `{"status":"UP","version":"1.0.0"}` — HTTP 200 |

