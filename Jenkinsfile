pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "linkedinprojects/demo-flask-app"  // Docker Hub repository name (change this to your own repo)
        K8S_MANIFEST_REPO = 'https://github.com/linkedinprojects/k8s-manifests.git' // GitHub repository for your Kubernetes manifests
        GIT_CREDENTIALS_ID = 'github' // GitHub credentials stored in Jenkins (make sure to store your GitHub credentials under this ID)
        DOCKER_CREDENTIALS_ID = 'dockerhub' // Docker Hub credentials stored in Jenkins (make sure to store your Docker Hub credentials under this ID)
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs() // Clean the workspace to avoid leftover files from previous builds
            }
        }

        stage('Checkout Application Code') {
            steps {
                // Clone the application repository configured in Jenkins
                checkout scm
            }
        }

        stage('Docker Cleanup') {
            steps {
                script {
                    // Clean up old Docker images and containers to avoid disk space issues
                    sh 'docker system prune -f' // Remove unused data such as images, containers, and volumes
                    sh 'docker container prune -f' // Remove stopped containers
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image from the application code
                    app = docker.build("${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub and push the Docker image
                    withDockerRegistry(credentialsId: DOCKER_CREDENTIALS_ID) {
                        sh "docker push ${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
                    }
                }
            }
        }

        stage('Update Kubernetes Manifest and Push to GitHub') {
            steps {
                script {
                    // Clone the Kubernetes manifests repo where ArgoCD watches for changes
                    dir('k8s-manifests') {
                        checkout([ 
                            $class: 'GitSCM', 
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[url: K8S_MANIFEST_REPO]] 
                        ])

                        // Configure Git user information and credentials using Jenkins' stored credentials
                        withCredentials([usernamePassword(credentialsId: GIT_CREDENTIALS_ID, passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                            sh "git config user.email '${GIT_USERNAME}@gmail.com'"
                            sh "git config user.name '${GIT_USERNAME}'"

                            // Update the Docker image tag in deployment.yaml
                            sh "sed -i 's+image: ${DOCKER_HUB_REPO}:[^ ]*+image: ${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}+g' deployment.yaml"

                            // Commit and push the updated deployment.yaml file to GitHub
                            sh "git add deployment.yaml"
                            sh "git commit -m 'Update Docker image to ${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}'"
                            sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${K8S_MANIFEST_REPO} HEAD:main"
                        }
                    }
                }
            }
        }
    }
}
