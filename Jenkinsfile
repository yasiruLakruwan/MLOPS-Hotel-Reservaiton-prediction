pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning Github Repo to jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repo to jenkins.............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/yasiruLakruwan/MLOPS-Hotel-Reservaiton-prediction.git']])
                }
            }
        }
        stage('Setting up virtual environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up virtual environment and Installing dependancies.............'
                    sh'''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }
    }
}