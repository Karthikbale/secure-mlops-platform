pipeline {
    agent any

    environment {
        IMAGE_NAME = "secure-mlops-platform"
        IMAGE_TAG = "1.0.${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Version') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('List Docker Images') {
            steps {
                sh '''
                docker images | grep ${IMAGE_NAME}
                '''
            }
        }
    }
}