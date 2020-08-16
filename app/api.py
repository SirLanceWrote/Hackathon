import tensorflow as tf
import json
import os
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from . import data_preprocessing


def load_data_from_urls(urls, new_class_name):
    with open('classes.json', 'r') as f:
        classes = json.load(f)

    classes[new_class_name] = len(classes)

    for class_name in classes.keys():
        TRAIN = int((len(urls) * 0.8))
        data_preprocessing.saveImages(urls[:TRAIN], os.path.join(r'tmp\train', class_name))
        data_preprocessing.saveImages(urls[TRAIN:], os.path.join(r'tmp\validation', class_name))

    with open('classes.json', 'w') as f:
        json.dump(classes, f)


def add_class(model):

    to_concat = []
    base_model = ResNet50(include_top=False)
    base_model.trainable = False
    # model.trainable = False

    inputs = tf.keras.Input(shape=(224, 224, 3))
    start = base_model(inputs, training=False)

    pooling = tf.keras.layers.GlobalAveragePooling2D()(start)
    
    x = model.layers[-1]
    name = str(type(x)).split('.')[-1][:-2]
    if name == 'Concatenate':
        for layer in model.layers[3:][:-1]:
            layer.training = False
            to_concat.append(layer(pooling))
    else:
        x.training = False
        to_concat.append(x(pooling))

    new_class = tf.keras.layers.Dense(1, name='Layer'+str(len(to_concat) + 1))(pooling)
    to_concat.append(new_class)

    concatted = tf.keras.layers.Concatenate()(to_concat)
    new_model = tf.keras.Model(inputs, concatted)

    return new_model

def train_model(new_class_name):

    with open('classes.json', 'r') as f:
        classes = json.load(f)

    data_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

    train_generator = data_generator.flow_from_directory(
        directory=r'tmp\train',
        target_size=(224, 224),
        classes=classes,
    )


    validation_generator = data_generator.flow_from_directory(
        directory=r'tmp\validation',
        target_size=(224, 224),
        classes=classes,
    )

    base_model = tf.keras.models.load_model('ResNet50_tuned_v4.h5')
    model = add_class(base_model)

    model.compile(
        optimizer=tf.keras.optimizers.SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True),
        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'],
    )

    model.fit_generator(
        train_generator,
        epochs=3,
        validation_data=validation_generator,
        verbose=0,
    )

    model.save('ResNet50_tuned_v4.h5')