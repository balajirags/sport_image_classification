#!/bin/bash
set -e -u

make_prediction_request() {
  local gateway_host="$1"
  local image_url="$2"

  echo "Making prediction request to http://$gateway_host:9696/predict..."

  curl --request POST \
    --url "http://$gateway_host:9696/predict" \
    --header 'Content-Type: application/json' \
    --data "{\"url\": \"$image_url\"}"

  echo "Prediction request completed."
}

# Main execution
main() {
  if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <gateway_host> <image_url>"
    exit 1
  fi

  HOST="${1:-localhost}"
  IMAGE_URL="$2"
  make_prediction_request "$HOST" "$IMAGE_URL"
}

# Execute the main function
main "$@"
