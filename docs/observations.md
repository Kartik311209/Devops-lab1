# Lab 1 Observations

**Student Name**: Kartik  
**Roll No.**: 2301730205  
**Email**: kartikjangra5366@gmail.com  
**Environment**: Ubuntu 24.04 LTS (WSL2) / Windows 11  

---

## Q4 - Install and configure Git and Jenkins
- Git was installed and verified in Ubuntu Linux (WSL2) and Windows PowerShell.
- Global config (`user.name "Kartik"`, `user.email "kartikjangra5366@gmail.com"`, `init.defaultBranch main`) is stored in `~/.gitconfig` and applies globally to all repositories.
- Jenkins 2.580.2 LTS requires **Java 21 or 25**; running with Java 17 fails startup with an explicit message (`Running with Java 17 ... which is older than the minimum required version (Java 21)`). Hence, OpenJDK 21 is required.
- The older Jenkins apt signing key (2023) expired, producing a `NO_PUBKEY` verification error during `apt update`. Downloading the current `jenkins.io-2026.key` resolved package verification.
- Jenkins listens on port 8080 by default; the initial unlock password is generated in `/var/lib/jenkins/secrets/initialAdminPassword`.

## Q5 - Version control with Git
- `git init` creates the local `.git` metadata directory; `git add` stages changes to the index.
- Developing tests on a feature branch (`feature/unit-tests`) isolated test additions from `main`.
- A fast-forward merge cleanly incorporated the feature branch without unnecessary merge commits.
- Semantic tag `v1.0.0` was annotated to establish the initial production release milestone.

## Q6 - Basic Jenkins CI pipeline
- A Jenkins Pipeline job (`devops-lab-pipeline`) was configured with "Pipeline script from SCM" pointing to the Git repository.
- Storing the pipeline definition in `Jenkinsfile` directly in source control guarantees infrastructure-as-code consistency.
- The pipeline automates repository checkout, dependency isolation in a Python virtual environment, pytest suite execution, and artifact archiving.

## Q7 - Jenkinsfile pipeline stages
- The Declarative Pipeline syntax clearly separates lifecycle stages: `Checkout` -> `Build` -> `Test` -> `Package` -> `Deploy`.
- Jenkins Stage View provides real-time visibility and status tracking for every stage.
- Built distributions are archived as `dist/app-build-${BUILD_NUMBER}.tar.gz` with fingerprinting.
- Post-action blocks (`success` and `failure`) ensure deterministic status logging.

## Q3 - Automated deployment
- SCM polling (`H/5 * * * *`) configures Jenkins to check GitHub periodically for changes and automatically trigger pipeline runs upon new commits.
- The deployment stage executes `scripts/deploy.sh` with granular passwordless sudo rights configured in `/etc/sudoers.d/jenkins-deploy`.
- Deploy script automates code synchronization to `/opt/devops-lab1`, virtualenv dependency resolution, and `systemctl restart devops-lab1.service`.
- An automated health check probes `http://localhost:5000/health` expecting HTTP 200, failing the pipeline if the service fails to respond.

