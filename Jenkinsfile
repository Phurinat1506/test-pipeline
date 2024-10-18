pipeline {
    agent any
    
    stages {
        stage('build') {
            steps {
                echo 'Check version python'
                sh 'python3 -V'
                echo 'test build docker'
                sh 'sudo usermod -aG docker $USER'
                sh 'docker build -t test_api_p5000:1.0 .'
                
            }
        }
    }
}