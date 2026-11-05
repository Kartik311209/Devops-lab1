// Declarative pipeline for the DevOps Lab 1 Flask app
// Student: Kartik | Roll No.: 2301730205
pipeline {
    agent any

    environment {
        APP_DIR      = '/opt/devops-lab1'
        VENV_DIR     = 'venv'
        DOCKER_IMAGE = "devops-lab1"
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Pulling source code from GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Creating virtualenv and installing dependencies...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ./${VENV_DIR}/bin/pip install --upgrade pip -q
                    ./${VENV_DIR}/bin/pip install -r app/requirements.txt -q
                    echo "Build complete — Flask installed."
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests with pytest...'
                sh '''
                    ./${VENV_DIR}/bin/python -m pytest tests/ -v \
                        --tb=short --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Package') {
            steps {
                sh '''
                    mkdir -p dist
                    tar -czf dist/app-build-${BUILD_NUMBER}.tar.gz app/
                    echo "Package created: dist/app-build-${BUILD_NUMBER}.tar.gz"
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            }
        }

        stage('Docker Build') {
            when {
                // Only run when Docker is available on the agent
                expression { sh(script: 'command -v docker', returnStatus: true) == 0 }
            }
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build \
                        -f docker/Dockerfile \
                        -t ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        -t ${DOCKER_IMAGE}:latest \
                        .
                    echo "Docker image built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    docker images ${DOCKER_IMAGE}
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying app to /opt/devops-lab1 and restarting service...'
                sh 'sudo bash scripts/deploy.sh'
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished: BUILD SUCCESS'
        }
        failure {
            echo 'Pipeline finished: BUILD FAILED'
        }
        always {
            // Clean up dangling Docker build cache
            sh 'docker image prune -f 2>/dev/null || true'
        }
    }
}
