pipeline {
    agent any

    stages('Cloning Github repo to Jenkins'){
        steps{
            script{
                echo 'Cloning Github repo to Jenkins................'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/yasiruLakruwan/MLOPS-Hotel-Reservaiton-prediction.git']])
            }
        }
    }
}
