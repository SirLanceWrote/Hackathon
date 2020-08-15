import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO
import os


resize = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Resizing(224, 224),
])

rescale = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
])


def loadImageFromURL(imageURL):
    response = requests.get(imageURL)
    image = Image.open(BytesIO(response.content)).convert('RGB')
    return tf.keras.preprocessing.image.img_to_array(image)


def loadImageFromFile(imagePath):
    try:
        image = Image.open(imagePath).convert('RGB')
    except:
        return (None, False)
    return (tf.keras.preprocessing.image.img_to_array(image), True)


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
        image = loadImageFromURL(imageURL)
        dataset += augment(image)
    return tf.data.Dataset.from_tensor_slices(dataset)


def augmentAllFiles(imagePaths):
    dataset = []
    for imagePath in imagePaths:
        image, loaded = loadImageFromFile(imagePath)
        if loaded:
            if image.shape[2] == 3:
                dataset += augment(image)
    return dataset


def saveImage(imageURL, path, name):
    response = requests.get(imageURL)
    image = Image.open(BytesIO(response.content)).convert('RGB')
    image.save(os.path.join(path, name))


def saveImages(imageURLs, path):
    try:
        os.makedirs(path)
    except Exception:
        pass
    count = len(imageURLs)
    for i, imageURL in enumerate(imageURLs):
        print(str(i) + '/' + str(count))
        saveImage(imageURL, path, str(i) + ".jpg")