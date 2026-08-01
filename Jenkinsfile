pipeline {
    agent any

    stages {
        stage('Workspace Information') {
            steps {
                echo '=== Jenkins Workspace Information ==='
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Verify Project Structure') {
            steps {
                echo '=== Project Structure ==='
                sh 'find . -maxdepth 2 -type f | sort'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}