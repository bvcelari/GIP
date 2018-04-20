pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }        
        stage('Sanity ') {
            steps {
                input "Does the uilding  looks good?"
            }
        }

         stage('live') {
            steps {
                sh 'python --version'
            }
        }   
        
    }
}
