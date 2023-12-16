import tensorflow as tf
from tensorflow import keras

h5_model_name = 'Inception_v1_25_0.945'   
tensor_model_name = 'sport_model'
model = keras.models.load_model(f'../model/{h5_model_name}')
tf.saved_model.save(model, f'../model/{tensor_model_name}')
