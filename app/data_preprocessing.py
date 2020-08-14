import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO


resize = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Resizing(224, 224),
])

rescale = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
])

def loadImage(imageURL):
    response = requests.get(imageURL)
    image = Image.open(BytesIO(response.content))
    return tf.keras.preprocessing.image.img_to_array(image)

def adjustSaturation(image):
    return tf.image.adjust_saturation(image, 2)

def adjustQuality(image):
    return tf.image.adjust_jpeg_quality(image, 50)

def augment(image):
    tmp = []
    images = []
    operations = [tf.image.flip_left_right, tf.image.flip_up_down, adjustSaturation, adjustQuality]
    images.append(resize(image))
    for operation in operations: 
        for image in images:
            tmp.append(operation(image))
        images += tmp
        tmp = []
    images = [rescale(img) for img in images]
    return images

def augmentAll(imageURLs):
    dataset = []
    for imageURL in imageURLs:
        image = loadImage(imageURL)
        dataset += augment(image)
    return tf.data.Dataset.from_tensor_slices(dataset)

augmentAll(['https://res.cloudinary.com/nekolya75/image/upload/v1597424646/RealityNeurons/file_ptpxik.jpg'])