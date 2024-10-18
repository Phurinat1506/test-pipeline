pipeline {
    agent any
    
    

    stages {
        stage('Init'){
            steps {
                echo 'Init'
                echo '******************************'
            }
        }

        // stage('build') {
        //     steps {

        //         echo 'test build docker'
        //         script {
        //             echo 'Building the application...'
        //             // การสร้างแอปพลิเคชัน
        //             def buildResult = sh(script: 'sudo docker build -t test_api_p5000:1.0 .', returnStatus: true)
        //             echo "Build result status: ${buildResult}"
        //             // ตรวจสอบผลลัพธ์การสร้าง
        //             if (buildResult == 0) {
        //                 echo 'Build successfully!'
        //             }else {
        //                 error 'Build failed!'
        //             }
        //         }
                
        //     }
        // }
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    
                    echo 'Read .env'
                    echo '******************************'
                    script {
                        // อ่านไฟล์ .env
                        def envFile = readFile '.env'

                        // echo "${envFile}"
                        def map = [:], lines = envFile.split("\r?\n"); 
                        for (def line : lines) {
                            sh "export ${line}"
                            // def arr = line.split("=");
                            // map.put(arr[0], arr[1]);
                            // echo "${map}"
                        }
                        //envProps = map;
                       
                    }
                
                    //def testResult = sh(script: 'make test', returnStatus: true)

                    // การจัดการผลลัพธ์การทดสอบ
                    // if (testResult == 0) {
                    //     echo 'Tests passed!'
                    // } else {
                    //     error 'Tests failed!'
                    // }
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