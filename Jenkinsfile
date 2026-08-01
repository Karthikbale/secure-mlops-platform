pipeline {
    agent any

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

        stage('Docker Info') {
            steps {
                sh 'docker info'
            }
        }

        stage('Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }
}