// Jenkins Pipeline — интеграция SonarQube
// Урок 4: Интеграция SonarQube с CI/CD

pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY  = 'vulnerable-app'
        SONAR_PROJECT_NAME = 'OTUS Vulnerable App'
        SONAR_PROJECT_VER  = '1.0-lesson4'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test') {
            steps {
                sh 'echo "Smoke test passed (test stage placeholder)"'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${tool 'SonarScanner'}/bin/sonar-scanner -Dsonar.projectKey=${SONAR_PROJECT_KEY} -Dsonar.projectVersion=${SONAR_PROJECT_VER} -Dsonar.sources=vulnerable-app"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success { echo "✅ Quality Gate passed" }
        failure { echo "⛔ Quality Gate failed — исправьте уязвимости!" }
    }
}
