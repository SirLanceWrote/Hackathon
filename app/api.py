import tensorflow as tf
from tensorflow.keras.applications import ResNet50

def create_model():
    base_model = ResNet50(
        input_shape=(224, 224, 3),
        include_top=False,
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(CLASSES, activation='softmax')(x)

    model = tf.keras.Model(inputs, outputs)
    return model