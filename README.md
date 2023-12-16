# sport_classification_service #

## Problem statement ##
We aim to address the challenge of accurate and efficient sport image classification within our service. The goal is to enhance the precision of categorizing sports based on user-provided images by leveraging a Convolutional Neural Network (CNN) model trained on a diverse sport-specific dataset. 

Kaggle data set used - https://www.kaggle.com/datasets/sidharkal/sports-image-classification

## Solution ##
As a part of this application, a pre-trained model - Inceptionv3 was further trained with a dataset containing images of different sports classes- cricket, wrestling, tennis, badminton, soccer, swimming, and karate and wrapped as tf-serving(based on the above kaggle dataset). The trained model has an accuracy of 94% in classifying the sport. Please note the training dataset contained only 7 sport classes [cricket, wrestling, tennis, badminton, soccer, swimming, and karate]



### Solution Architecture ###
![Alt text](image.png)


## Note ##
 Images, model are checked into the repo making it a large repo interms of size. Hence git-lfs was used to store file greater than 100MB. Follow the installation instructions for git-lfs [here](https://git-lfs.com/).


### Project structure ###

Folder  | Description
------------- | -------------
dataset  | Directory containing training and test data - image files.
gateway  | Directory containing flask application which acts as a gateway for tf-serving 
model    | Directory containing '.h5' model which was trianed and tensorflow generated model which can be used in tf-serving.
trainer | Directory containing notebooks and script which were used for training the model. 
kube-config | Configuration related to kubernetes deployments.


## Pre-requisties ##
* python 3.10 or above.
* docker, docker-compose, Kind, kubectl
* pip3, pipenv  
* git-lfs

## Installing dependencies ##
Use `pipenv install` to install dependencies from respective directories, Only if you want to train model and build images yourself.

* Folder `gateway` - contains dependencies related to flask and tf-serving. 
* Folder `trainer` - contains dependencies related to tensorflow and other libraries required for training the model.



## How to run locally with Docker compose ##
1.  Clone this repo
2. `git pull lfs` . The trained model is saved in the `model` directory already.
3. `docker-compose up`
5.  check if the containers is up


## How to run on local kubernetes ##
1. Ensure [`kind`](https://kind.sigs.k8s.io/) kubernetes in installed
2. run `./deploy-local-kube.sh`
3. `kubectl port-forward services/sports-gateway-service 9696:9696`

## Testing with python script ##
1. `cd` into `./gateway` directory
2. `pipenv install`
3. `pipenv shell`
4. `python3 predict_test.py`

## Testing with curl ##
run `./predict_test.sh`
 
 or

```shell
  curl --request POST \
  --url http://localhost:9696/predict \
  --header 'Content-Type: application/json' \
  --data '{"url": <<image url>>}'
  ```


## Cloud Deployment ##

Both the Gateway and the Model is deployed on AWS EKS cluster.

The gateway is available for testing 
url:`https://somethinghost:9696/ping`

you can test the application by running predict_test.py or curl (post modification of the host to `https://somethinghost:9696`)


## gateway Service API ##

API  | Description | Response | Response-type
------------- | ------------- | -------------  | -------------
`/ping` | ping api to check the status | pong | String
`/predict`| Return the prediction of the classification| one of sports class- example `cricket`  | Json
`/predict?show_probability=true` | shows probability for all classes | hash containing all classes and their probabilities | json 



