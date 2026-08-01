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
    }

    post {
        success {
            echo "Docker image ${IMAGE_NAME}:${IMAGE_TAG} built successfully."
        }

        failure {
            echo "Docker image build failed. Check the console output."
        }

        always {
            cleanWs()
        }
    }
}