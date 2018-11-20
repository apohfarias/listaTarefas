// comment
pipeline {
 agent any
 stages {
        stage('VerificarGit'){
               steps{
        git poll: true, url: 'https://github.com/apohfarias/listaTarefas.git'
               }
        }
        stage('CriarVirtualEnv') {
            steps {
                sh '''
                    bash -c "python3.6 -m venv venv_listaTarefas && source venv_listaTarefas/bin/activate"
                '''

            }
        }
        stage('InstalarRequirements') {
            steps {
                sh '''
                    bash -c "source ${WORKSPACE}/venv_listaTarefas/bin/activate && ${WORKSPACE}/venv_listaTarefas/bin/python ${WORKSPACE}/venv_listaTarefas/bin/pip install -r requirements.txt"
                '''
            }
        }   
        stage('TestarApp') {
            steps {
                sh '''
                    bash -c "source ${WORKSPACE}/venv_listaTarefas/bin/activate && python manage.py test lists"
                '''
            }
        }  
        stage('RodarApp') {
            steps {
                sh '''
                    bash -c "source venv_listaTarefas/bin/activate ; ${WORKSPACE}/venv_listaTarefas/bin/python manage.py &"
                '''
                withSonarQubeEnv {
                    // some block
                    sonar.projectKey=listatarefa
                    sonar.sources=${WORKSPACE}/listaTarefasCI/
                    sonar.host.url=172.16.91.190:9000
                    sonar.login=4da5650dddb05e04cab33180e8b454b11ffa0976
                }

            }
        } 
        stage('BuildDocker') {
            steps {
                sh '''
                    docker build -t apptest:latest .
                '''
            }
        } 
    stage('PushDockerImage') {
            steps {
                sh '''
                    docker tag apptest:latest apohfarias/apptest:latest
                    docker push apohfarias/apptest:latest
                    docker rmi apptest:latest
                '''
            }
        } 
  }
}
