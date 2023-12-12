import tensorflow as tf
import grpc
import numpy as np
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from keras_image_helper import create_preprocessor
from flask import Flask
from flask import request
from flask import jsonify
from proto import np_to_protobuf
import os

app = Flask("gateway")

host = os.getenv('TF_SERVING_HOST', 'localhost:8500')
#host = "localhost:8500"
preprocessor = create_preprocessor('inception_v3', target_size=(299,299))

channel = grpc.insecure_channel(host)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
labels = ['Badminton', 'Cricket', 'Karate', 'Soccer', 'Swimming', 'Tennis', 'Wrestling']
    
def create_request(url):
    X = preprocessor.from_url(url)
    #x_proto = tf.make_tensor_proto(X, shape=X.shape)
    x_proto =  np_to_protobuf(X)   
    pbrequest = predict_pb2.PredictRequest()
    pbrequest.model_spec.name = 'sport-classification-model'
    pbrequest.inputs['input_7'].CopyFrom(x_proto)
    return pbrequest

def decode_response(pb_response):
    output = pb_response.outputs['dense_5'].float_val
    return labels[np.argmax(output)]


def decode_response_detail(pb_response):
    output = pb_response.outputs['dense_5'].float_val
    return dict(zip(labels, output))

def predict(url):
    pbrequest = create_request(url)
    pb_response = stub.Predict(pbrequest, timeout=10)
    return decode_response(pb_response)

@app.route('/predict', methods=['POST'])
def predict_api():
    data = request.get_json()
    url = data['url']
    response = predict(url)
    return jsonify(response)

@app.route('/ping', methods=['GET'])
def ping_api():
    return 'pong'


if __name__ == '__main__':
    #url = 'https://i.pinimg.com/originals/50/c3/16/50c3163dfff9f2e7252f3d40e2d7f571.jpg'
    #response = predict(url)
    #print(response)
    app.run(debug=True, host='0.0.0.0', port=9696)
    