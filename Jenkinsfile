pipeline{
    agent any

    stages{
        stage('Cloning Github Repo to jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repo to jenkins.............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/yasiruLakruwan/MLOPS-Hotel-Reservaiton-prediction.git']])
                }
            }
        }
    }
}