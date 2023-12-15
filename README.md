# sport_classification_service #

## Problem statement ##
We aim to address the challenge of accurate and efficient sport image classification within our service. The goal is to enhance the precision of categorizing sports based on user-provided images by leveraging a Convolutional Neural Network (CNN) model trained on a diverse sport-specific dataset. As a part of this application, a pre-trained model -Inceptionv3 was further trained with a dataset containing images of different sports classes- cricket, wrestling, tennis, badminton, soccer, swimming, and karate and wrapped as tf-serving. The trained model has an accuracy of 94% in classifying the sport. Please note the training dataset contained only 7 sport classes [cricket, wrestling, tennis, badminton, soccer, swimming, and karate]

## Solution ##
Build a Api which given a url of an image will return the predictions based on the classes it has been trained.


Solution Architecture:
![Alt text](image.png)

## Note ##
 Images, model are checked into the repo making it a large repo interms of size. Hence git-lfs was used to store file greater than 100MB. Follow the installation instructions for git-lfs [here](https://git-lfs.com/).


### Project structure ###

Folder  | Description
------------- | -------------
dataset  | Directory containing training and test data - image files.
gateway  | Directory containing flask application which acts as a gateway for tf-serving 
model    | Directory containing '.h5' model which was trianed and tensorflow generated model which can be used in tf-serving.
notebook | Directory containing notebooks which were used for training and testing the model.
kube-config | Configuration related to kubernetes deployments.


## Pre-requisties ##
* python 3.10 or above.
* docker, docker-compose, Kind, kubectl
* pip3, pipenv  
* git-lfs

## How to run locally with Docker compose ##
1. Clone this repo
2. git pull lfs
3. `docker-compose up`
5. check if the containers is up
6. `cd` into `./gateway` directory
7. `pipenv install`
8. `pipenv shell`
9. `python3 predict_test.py` - Will return Swimming as an output string.


## How to run locally on kubernetes ##

1. Ensure [`kind`](https://kind.sigs.k8s.io/) kubernetes in installed
2. run `./deploy-local-kube.sh`
3. `kubectl port-forward services/sports-gateway-service 9696:9696`
4. `cd` into `./gateway` directory
5. `pipenv install`
6. `pipenv shell`
7. `python3 predict_test.py` - Will return Swimming as an output string.


## How to test in AWS cluster ##

Both the Gateway and the Model is deployed on AWS EKS cluster.

The gateway is available for testing 
url:`https://somethinghost:9696/ping`

you can test the application  by running predict_test.py post modification of the host to `https://somethinghost:9696`


## gateway Service API ##

API  | Description | Response | Response-type
------------- | ------------- | -------------  | -------------
`/ping` | ping api to check the status | pong | String
`/predict`| Return the prediction of the classification| one of sports class- example `cricket`  | String
`/predict?show=probability` | shows probability of all classes | example `{}` | json 



