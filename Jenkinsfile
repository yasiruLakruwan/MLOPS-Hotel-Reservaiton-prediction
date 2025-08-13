pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'steam-glass-467515-t4'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
        NO_PROXY = "gcr.io,.gcr.io"
        DOCKER_CLIENT_TIMEOUT = "300"
        COMPOSE_HTTP_TIMEOUT = "300"
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
        stage('Building and pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing Docker Image to GCR..............'
                        sh'''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }
    }
}