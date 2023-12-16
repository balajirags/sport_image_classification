import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img
import matplotlib.pyplot as plt
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.inception_v3 import decode_predictions
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import ImageDataGenerator

labels = ['Badminton', 'Cricket', 'Karate', 'Soccer', 'Swimming', 'Tennis', 'Wrestling']

dataset_dir='../dataset'
train_dir=f'{dataset_dir}/train'
test_dir=f'{dataset_dir}/test'

train_full_df = pd.read_csv(f'{dataset_dir}/train.csv')
train_full_df.columns = train_full_df.columns.str.lower()

train_df,val_df = train_test_split(train_full_df, test_size=0.2)
len(train_df),len(val_df)

train_gen = ImageDataGenerator(preprocessing_function=preprocess_input,
                               shear_range=0.2,
                              zoom_range=0.2)
train_ds = train_gen.flow_from_dataframe(
    train_df,
    directory=f'{train_dir}',
    x_col='image_id',
    y_col='label',
    target_size=(299,299), 
    batch_size=32)

val_gen = ImageDataGenerator(preprocessing_function=preprocess_input)
val_ds = val_gen.flow_from_dataframe(
    val_df,
    directory=f'{train_dir}',
    x_col='image_id',
    y_col='label',
    target_size=(299,299), 
    batch_size=32)

def make_model(lr, inner_layer_size, droprate):
    base_model = keras.applications.InceptionV3(
    include_top=False,
    weights="imagenet",
    input_shape=(299,299,3),
    pooling=None)
    base_model.trainable = False
    inputs = keras.Input(shape=(299, 299, 3))
    x = base_model(inputs, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(inner_layer_size, activation='relu')(x)
    x = keras.layers.Dropout(droprate)(x)
    outputs = keras.layers.Dense(7, activation='softmax')(x)
    sport_model = keras.Model(inputs, outputs)
    optimizer = keras.optimizers.Adam(lr)
    loss = keras.losses.CategoricalCrossentropy(from_logits=True)
    sport_model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    return sport_model

def create_checkpoint():
    model_file_name_pattern ='Inception_v1_{epoch:02d}_{val_accuracy:.3f}.h5'
    return keras.callbacks.ModelCheckpoint(
    f'../model/{model_file_name_pattern}',
    save_best_only=True,
    monitor='val_accuracy',
    mode='max'
)

def train_model(learning_rate, inner_layer_size, droprate):
    checkpoint = create_checkpoint()
    model = make_model(learning_rate, inner_layer_size, droprate)
    model.fit(train_ds, epochs=10, validation_data=val_ds, callbacks=[checkpoint])
    return model

def predict(img, model):
    x = np.array(img)
    X = np.array([x])
    X = preprocess_input(X)
    predictions = model.predict(X)
    return dict(zip(labels,predictions[0]))

if __name__ == "__main__":        
    final_leanrning_rate= 0.0001
    final_size=1000
    final_drop_rate=0.3
    train_model(final_leanrning_rate, final_size, final_drop_rate)
    


