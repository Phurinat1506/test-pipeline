Jenkinsfile (Declarative Pipeline)
/* Requires the Docker Pipeline plugin */
pipeline {
    agent { docker { image 'python:3.9-slim' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}