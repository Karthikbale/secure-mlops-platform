pipeline {
    agent any

    environment {
        IMAGE_NAME = "secure-mlops-platform"
        IMAGE_TAG = "v1.0.0"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

    }

    post {

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }

        always {
            cleanWs()
        }
    }
}