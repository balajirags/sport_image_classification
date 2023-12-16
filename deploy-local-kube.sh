#!/bin/sh
set -e -u
create_model_image() {
  echo "Building model image..."
  docker build -t sport-classification-model:v1 -f ./model/model_image.dockerfile  ./model
  echo "Built model image."
}

create_gateway_image() {
  echo "Building gateway image..."
  docker build -t sport-classification-gateway:v1 -f ./gateway/gateway_image.dockerfile ./gateway
  echo "Built gateway image."
}

create_kind_cluster() {
  local name="$1"
  echo "Creating local Kubernetes cluster... $name"
  kind create cluster --name $name
  echo "Local Kubernetes cluster created with name $name."
}

load_images_to_kind_cluster() {
  local name="$1"
  echo "Loading images to Kind repository..."
  kind load docker-image sport-classification-gateway:v1 sport-classification-model:v1 --name $name
  echo "Images loaded to Kind repository."
}

deploy_model() {
  echo "Deploying model..."
  kubectl apply -f ./kube-config/model-deployments.yaml
  kubectl apply -f ./kube-config/model-service.yaml
  echo "Model deployed."
}

deploy_gateway() {
  echo "Deploying gateway..."
  kubectl apply -f ./kube-config/gateway-deployments.yaml
  kubectl apply -f ./kube-config/gateway-service.yaml
  echo "Gateway deployed."
}

main() {
  if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <cluster-name>"
    exit 1
  fi
  echo "Starting deployment to local Kubernetes cluster..."

  create_model_image
  create_gateway_image

  create_kind_cluster "$1"
  load_images_to_kind_cluster "$1"

  deploy_model
  deploy_gateway

  echo "Successfully deployed to local Kubernetes cluster. Please port forward and test the deployment."
}

# Execute the main function
main "$@"
