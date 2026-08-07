pipeline {
    agent any

    environment {
        IMAGE_NAME = "secure-mlops-platform"
        IMAGE_TAG  = "1.0.${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'

                    withSonarQubeEnv('sonarqube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=secure-mlops-platform \
                              -Dsonar.projectName=secure-mlops-platform \
                              -Dsonar.sources=. \
                              -Dsonar.python.version=3
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Bandit Security Scan') {
            steps {
                sh '''
                    bandit -r app/
                '''
            }
        }

        stage('Verify Docker') {
            steps {
                sh '''
                    docker --version
                    docker info
                '''
            }
        }

        stage('Build ML Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Display Image Information') {
            steps {
                sh '''
                    docker images | grep ${IMAGE_NAME}

                    docker image inspect ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Archive Build Information') {
            steps {
                sh '''
                    mkdir -p build-info

                    docker images ${IMAGE_NAME} > build-info/docker-images.txt

                    docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} \
                    > build-info/image-inspect.json
                '''

                archiveArtifacts artifacts: 'build-info/*', fingerprint: true
            }
        }

        stage('Trivy Container Scan') {
            steps {
                sh '''
                    mkdir -p reports

                    trivy image \
                      --scanners vuln \
                      --severity HIGH,CRITICAL \
                      --exit-code 1 \
                      --format table \
                      --output reports/trivy-report.txt \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {

        success {
            echo "Secure DevSecOps pipeline completed successfully."
        }

        failure {
            echo "Pipeline failed due to quality or security checks. Review the archived reports."
        }

        always {

            archiveArtifacts artifacts: 'reports/trivy-report.txt',
                             allowEmptyArchive: true

            archiveArtifacts artifacts: 'build-info/*',
                             fingerprint: true,
                             allowEmptyArchive: true

            cleanWs()
        }
    }
}