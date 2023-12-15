From tensorflow/serving:2.7.0

COPY ./sport-classification-model /models/sport-classification-model/1

ENV MODEL_NAME="sport-classification-model"