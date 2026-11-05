# devops-lab1-ci

ENSP461 - DevOps and Automation, Lab 1: DevOps Foundations & Continuous Integration.

### Student Details
- **Student Name**: Kartik
- **Roll Number**: 2301730205
- **Email**: kartikjangra5366@gmail.com
- **Environment**: Ubuntu 24.04 LTS (WSL2) / Windows 11

---

This repository contains a Flask application used to demonstrate a complete CI/CD workflow with Git, GitHub and Jenkins.

## Repository Structure
- `app/`          - Flask application source code
- `tests/`        - pytest unit tests
- `scripts/`      - deployment helper scripts
- `Jenkinsfile`   - declarative pipeline (Checkout -> Build -> Test -> Package -> Deploy)
- `docs/`         - command logs, screenshots, systemd unit, and observations
- `reports/`      - final individual lab report PDFs (Questions 1 through 7)

## Run Locally
```bash
python3 -m venv venv
source venv/bin/activate       # On Windows PowerShell: .\venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
python -m flask --app app.app run --host 0.0.0.0 --port 5000
```

Verify endpoints:
```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

## Pipeline Stages
1. **Checkout**: Pulls source code from repository
2. **Build**: Prepares virtual environment and installs Python dependencies
3. **Test**: Executes pytest unit test suite verifying API responses
4. **Package**: Generates timestamped/build-numbered tarball artifact (`app-build-${BUILD_NUMBER}.tar.gz`)
5. **Deploy**: Deploys application to `/opt/devops-lab1`, restarts system service, and verifies health check (HTTP 200)

