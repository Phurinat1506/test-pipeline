pipeline {
    agent any
    
    stages {
        stage('Init'){
            steps {
                echo 'Init'
                echo '******************************'
            }
        }
 
        stage('install') {
            steps {
                echo 'install'
                echo '******************************'
                
            }
        }
        stage('build') {
            steps {

                echo 'test build docker'
                sh 'sudo docker build -t test_api_p5000:1.0 .'
                script {
                    echo 'Building the application...'
                    // การสร้างแอปพลิเคชัน
                    def buildResult = sh(script: 'sudo docker build -t test_api_p5000:1.0 .', returnStatus: true)
                    echo "Build result status: ${buildResult}"
                    // ตรวจสอบผลลัพธ์การสร้าง
                    if (buildResult != 0) {
                        error 'Build failed!'
                    }else {
                        echo 'Build successfully!'
                    }
                }
                
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            // การทำความสะอาดหลังจาก Pipeline เสร็จสิ้น
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}