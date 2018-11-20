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
         stage('SonarQube analysis') { 
            steps withSonarQubeEnv('Sonar') { 
            sh " cd  $project_path; mvn sonar:sonar -Dsonar.host.url=http://172.16.91.190:9000 -Dsonar.projectKey=listatarefa -Dsonar.projectName=listatarefa classes -Dsonar.sources=/var/lib/jenkins/workspace/listaTarefasCI/ -Dsonar.login=4da5650dddb05e04cab33180e8b454b11ffa0976 -Dsonar.analysis.mode=preview"                
            }
        }

        stage('RodarApp') {
            steps {
                sh '''
                    bash -c "source venv_listaTarefas/bin/activate ; ${WORKSPACE}/venv_listaTarefas/bin/python manage.py &"
                '''
                }

        } 
        stage('BuildDocker') {
            steps {
                sh '''
                    ls //docker build -t apptest:latest .
                '''
            }
        } 
    stage('PushDockerImage') {
            steps {
                sh '''
                    ls //docker tag apptest:latest apohfarias/apptest:latest
                    //docker push apohfarias/apptest:latest
                    //docker rmi apptest:latest
                '''
            }
        } 
  }
}
