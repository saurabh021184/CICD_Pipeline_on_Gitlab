# Let's Explore .gitlab-ci.yml file 
1. Start with a BASE Image image: ${CI_REGISTRY}/mycicdpipeline/cicdpipelinewithtestingstage/docker:latest
   This base image creates a temporary container which then provides the unix environment which is used to run different
   CICD commands to build and test the your application image
   
   - Now what is the value of CI_REGISTRY??? -> this is  "The address of the GitLab Container Registry. Only available if the Container Registry is enabled for the project. 
   - so value of CI_REGISTRY will be -> 'registry.gitlab.com'
   - Next you should create the images or push some images to your local gitlab account
   - where these images are present?? check the screenshot below..
   
   ![image](https://user-images.githubusercontent.com/109071677/186201635-c3169ff6-72d2-40fa-bc95-edeff6e2a5dc.png)

   - how you push these images from DOCKER public registry to your own account?? checkout the commands below
     1. 1st pull some basic images from publich repo
       
        ~~~~sh
        $ docker pull registry.hub.docker.com/library/docker
        $ docker pull registry.hub.docker.com/library/docker:20.10.17-dind
        ~~~~

     2. 2nd then login to your private registry and then
        TAG the above registries and then push then to your private registry
        
        ~~~~sh
        $ docker login -u samathur -p xxxxx registry.gitlab.com/mycicdpipeline/cicdpipelinewithtestingstage
        $ docker image tag registry.hub.docker.com/library/docker:latest registry.gitlab.com/mycicdpipeline/cicdpipelinewithtestingstage/docker:latest
        $ docker image push registry.gitlab.com/mycicdpipeline/cicdpipelinewithtestingstage/docker:latest

        $ docker image tag registry.hub.docker.com/library/docker:20.10.17-dind registry.gitlab.com/mycicdpipeline/cicdpipelinewithtestingstage/docker:20.10.17-dind
        $ docker image push registry.gitlab.com/mycicdpipeline/cicdpipelinewithtestingstage/docker:20.10.17-dind
        ~~~~

2. Next within the services -> you need 'dind' image 
   services:
     - name: ${CI_REGISTRY}/mycicdpipeline/cicdpipelinewithtestingstage/docker:20.10.17-dind
       alias: docker
       
     And alias of this dind image is called 'docker' globally within the git-ci.yml file
     
     Now what is this 'dind' -> it is called 'docker in docker'
     https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker
     
         
3. Declare global variables
   variables:
         Here the important point again is that you need to create following varibles in the gitlab settings check the image below where it is created.
         Go to Settings -> CI/CD -> Variables -> and create the variables
         ![image](https://user-images.githubusercontent.com/109071677/186205886-2f03d1cc-3396-4b1a-a3ba-4c047efd2ea7.png)

         DOCKER_DEVELOPMENT_LOCAL -> registry.gitlab.com
         ARTIFACTORY_ADDRESS -> registry.gitlab.com/mycicdpipeline/cicdpipelinewithtestingstage/docker
         
         
    CI_PROJECT_PATH
    CI_PROJECT_NAME
    CI_REGISTRY_USER:$CI_REGISTRY_PASSWORD
    All these 4 variables are again default variables (which are basically your project_name, the user and password with which you logged in to the gitlab)
    
4. Stages are ofcourse the KEY part here:
   stages:          # List of stages for jobs, and their order of execution
    - build
    - deploy

5. Before running the actual scripts list down the key actions which you need to execute
   before_script:
    - mkdir ~/.docker
    - echo ${DOCKER_AUTH_CONFIG} > ~/.docker/config.json      
    etc....
    
6. Rest are just some CICD gitlab-ci.yml commands which are used to build and deploy

   some command to get highlighted are:
   - docker pull $CI_REGISTRY_IMAGE:latest || true
   - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
   - docker push "$CI_REGISTRY_IMAGE:${APP_VERSION}"
   - docker push "$CI_REGISTRY_IMAGE:latest"
   
   This will build the image and push it in the registry
   
   As part of deployment:
   - mkdir -p ~/.ssh
   - echo -n "$EC2_SSH_KEY" | tr -d '\r' > ~/.ssh/id_rsa
   - chmod 700 ~/.ssh/id_rsa
   - ssh-keyscan -H $MASTER_NODE >> ~/.ssh/known_hosts
   (This will put the keys of the remote EC2 server where we need to deploy our image as a docker service)
   
   - scp .env .env.vault.local $HOST_USER@$MASTER_NODE:~
   - ssh -tt $HOST_USER@$MASTER_NODE "chmod 700 ~/.env; source ~/.env"
   - ssh -tt $HOST_USER@$MASTER_NODE docker pull "$CI_REGISTRY_IMAGE:$APP_VERSION"
   - scp docker-compose.yml $HOST_USER@$MASTER_NODE:~
   - ssh -tt $HOST_USER@$MASTER_NODE "docker stack rm $APP_STACK; sleep 10s" || true
   - ssh -tt $HOST_USER@$MASTER_NODE "export APP_VERSION=$APP_VERSION CI_REGISTRY_IMAGE=$CI_REGISTRY_IMAGE; chmod 700 ~/docker-compose.yml; docker stack deploy --with-registry-auth -c ~/docker-compose.yml $APP_STACK"
   So basically what we are doing here is -> we are temporarily moving the docker compose and then running 'docker stack deploy' command
   
7. These are the variables that I created as part of this project in 
   Settings -> CICD -> Variables section:
   
   ARTIFACTORY_ADDRESS -> registry.gitlab.com/mycicdpipeline/cicdpipelinewithtestingstage/docker
   ARTIFACTORY_APIKEY -> xxxxxxxx
   ARTIFACTORY_USER -> samathur
   DOCKER_DEVELOPMENT_LOCAL -> registry.gitlab.com
   EC2_SSH_KEY -> xxxxxx
   HOST_USER -> ec2-user
   MASTER_NODE -> ec2-3-94-54-65.compute-1.amazonaws.com
   
   
# References:
  https://docs.gitlab.com/ee/ci/cloud_deployment/
  https://www.youtube.com/watch?v=PGyhBwLyK2U
  https://gitlab.com/gitlab-course-public/freecodecamp-gitlab-ci/-/blob/main/docs/pipeline-configs/lesson-4-10-.gitlab-ci.yml
  https://aws.plainenglish.io/deploy-from-gitlab-to-aws-ec2-48a45c00ad6a
  https://www.1strategy.com/blog/2021/02/16/deploying-gitlab-runners-on-ec2/
  https://docs.gitlab.com/ee/ci/variables/predefined_variables.html#predefined-variables-reference
