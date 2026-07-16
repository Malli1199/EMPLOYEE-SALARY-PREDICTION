pipeline {
    agent any

    stages {
        stage('Fetch Project Files') {
            steps {
                cleanWs() // Clean the workspace first
                checkout scm
            }
        }

        stage('Scan Code Quality') {
            steps {
                // 1. Grab your existing sonar-token credential from Jenkins
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_PASSWORD')]) {
                    
                    // 2. Connect Jenkins to your SonarQube server configuration
                    withSonarQubeEnv('MY-SONAR-SERVER') {
                        
                        script {
                            // 3. This dynamically resolves your local "sonar-scanner" tool path!
                            // The name in quotes MUST match the tool name in your screenshot exactly.
                            def scannerHome = tool 'sonar-scanner'
                            
                            // 4. Run the scanner using the retrieved path on Windows
                            bat """
                                "${scannerHome}\\bin\\sonar-scanner" \
                                -Dsonar.projectKey=my-local-windows-project \
                                -Dsonar.projectName="Employee Project" \
                                -Dsonar.sources=. \
                                -Dsonar.token=${SONAR_PASSWORD}
                            """
                        }
                        
                    }
                }
            }
        }
    }
}