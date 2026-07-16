pipeline {
    agent any

    stages {
        stage('Checkout Source') {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage('Scan code Quality'){
            steps{
                withCredentials([String(credentialsId:'sonar-scanner',variable:'SONAR-PASSWORD')]){
                    script{
                        def scannerHome=tool "sonar-scanner"
                        bat """
                        "${ScannerHome}\\bin\\sonar-scanner"\
                        -Dsonar.projectkey=my-local-window-project\
                        -Dsonar.projectName="Employee salary"\
                        -Dsonar.sources=.\
                        -Dsonar.token=${SONAR-PASSWORD}
                        """
                    }
                }
            }
        }
    }
}