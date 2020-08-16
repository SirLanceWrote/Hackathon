import tensorflow as tf
from tensorflow.keras.applications import ResNet50

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

# def train():
#     model.compile(
#         optimizer=tf.keras.optimizers.SGD(learning_rate=hp_learning_rate, momentum=hp_momentum, nesterov=True),
#         loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
#         metrics=['accuracy'],
#     )