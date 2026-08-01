pipeline {
    agent any

    environment {
        IMAGE_NAME = "secure-mlops-platform"
        IMAGE_TAG = "v1.0.0"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat 'py --version'
                bat 'py -m pip --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat 'py -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'venv\\Scripts\\python -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
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
            echo '✅ Pipeline completed successfully.'
        }

        failure {
            echo '❌ Pipeline failed.'
        }

        always {
            cleanWs()
        }
    }
}