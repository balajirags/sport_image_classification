## Deploying to AWS ##
1. create Aws free tier account with root user
2. Create a new IAM user with full access as admin
3. create username and password for this new iam user
4. create access key and secret key for this user.
5. Configure aws cli profile for hte iam user
6. Download and install eksclt
7. Create eks-config.yaml file and configure cluster settings
8. create cluster with eksclt using below command line
`eksctl create cluster -f ./eks-config.yaml --profile <<Profile>>`
9. create ecr repository for images using below command
`aws ecr create-repository --repository-name <<repo name>>`
10. copy the ecr repo URI and configure as below
    ```
    ACCOUNT_ID=<<Accountid>>
    REGION=<<region>>
    PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/<reponame>

    ```
11. Use docker to tag local image to remote image
```
    GATEWAY_LOCAL=<gatewat-image>
    GATEWAY_REMOTE=${PREFIX}:<gatewat-image>
    MODEL_LOCAL=<model-image>
    MODEL_REMOTE=${PREFIX}:<model-image>
    docker tag ${GATEWAY_LOCAL} ${GATEWAY_REMOTE}
    docker tag ${MODEL_LOCAL} ${MODEL_REMOTE}

```
12. login via awscli 
```
ecr get-login-password \
    --region ${REGION} \
| docker login \
    --username AWS \
    --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/<ecr-repo-name>
```
13. push remote images using docker
    `docker push <<GATEWAY_REMOTE>>`
    `docker push <<MODEL_REMOTE>>`
14. modify the image location in deployments.yaml file to ecr uri
15. use kubectl to apply deployment ans services.




