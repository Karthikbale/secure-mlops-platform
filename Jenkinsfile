pipeline {
    agent any

    environment {
        IMAGE_NAME    = "secure-mlops-platform"
        IMAGE_TAG     = "1.0.${BUILD_NUMBER}"

        AWS_REGION    = "us-east-1"
        AWS_ACCOUNT   = "591064574283"
        ECR_REGISTRY  = "${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        ECR_REPOSITORY = "secure-mlops-platform"

        EKS_CLUSTER   = "secure-mlops-eks"
        EKS_NAMESPACE = "secure-mlops"
        DEPLOYMENT    = "secure-mlops-api"
        CONTAINER     = "secure-mlops-api"
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

        stage('Archive Build Information') {
            steps {
                sh '''
                    mkdir -p build-info

                    docker images ${IMAGE_NAME} \
                      > build-info/docker-images.txt

                    docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} \
                      > build-info/image-inspect.json
                '''

                archiveArtifacts artifacts: 'build-info/*',
                                 fingerprint: true
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    echo "Logging in to Amazon ECR..."

                    aws ecr get-login-password \
                      --region ${AWS_REGION} \
                    | docker login \
                      --username AWS \
                      --password-stdin ${ECR_REGISTRY}

                    echo "Tagging image for ECR..."

                    docker tag \
                      ${IMAGE_NAME}:${IMAGE_TAG} \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    echo "Pushing image to ECR..."

                    docker push \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                    echo "Configuring kubeconfig for EKS..."

                    aws eks update-kubeconfig \
                      --name ${EKS_CLUSTER} \
                      --region ${AWS_REGION}

                    echo "Deploying image to EKS..."

                    kubectl set image deployment/${DEPLOYMENT} \
                      ${CONTAINER}=${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} \
                      --namespace ${EKS_NAMESPACE}
                '''
            }
        }

        stage('EKS Rollout Verification') {
            steps {
                sh '''
                    echo "Waiting for Kubernetes rollout..."

                    kubectl rollout status \
                      deployment/${DEPLOYMENT} \
                      --namespace ${EKS_NAMESPACE} \
                      --timeout=180s
                '''
            }
        }

        stage('Verify EKS Pods') {
            steps {
                sh '''
                    echo "Checking Pods..."

                    kubectl get pods \
                      --namespace ${EKS_NAMESPACE} \
                      -o wide

                    echo "Checking Deployment..."

                    kubectl get deployment ${DEPLOYMENT} \
                      --namespace ${EKS_NAMESPACE}
                '''
            }
        }

        stage('Verify Application') {
            steps {
                sh '''
                    echo "Waiting for Load Balancer endpoint..."

                    for i in $(seq 1 30); do

                        LB_HOST=$(kubectl get service secure-mlops-service \
                          --namespace ${EKS_NAMESPACE} \
                          -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

                        if [ -n "$LB_HOST" ]; then
                            break
                        fi

                        echo "Load Balancer not ready. Waiting..."
                        sleep 10

                    done

                    if [ -z "$LB_HOST" ]; then
                        echo "ERROR: Load Balancer endpoint was not created."
                        exit 1
                    fi

                    echo "Load Balancer:"
                    echo "$LB_HOST"

                    echo "Testing application health..."

                    curl --fail --silent \
                      --show-error \
                      --max-time 20 \
                      http://${LB_HOST}/health

                    echo ""
                    echo "Application health check passed."
                '''
            }
        }
    }

    post {

        success {
            echo "Secure MLOps CI/CD pipeline completed successfully."
            echo "Application successfully deployed to Amazon EKS."
        }

        failure {
            echo "Pipeline failed during build, security, ECR push, EKS deployment, rollout, or application verification."
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