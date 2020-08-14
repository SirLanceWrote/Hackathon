import tensorflow as tf

resizeRescale = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Resizing(224, 224),
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
])

def adjustSaturation(image):
    return tf.image.adjust_saturation(image, 2)

def adjustQuality(image):
    return tf.image.adjust_jpeg_quality(image, 50)

def augment(image):
    tmp = []
    images = []
    operations = [tf.image.flip_left_right, tf.image.flip_up_down, adjustSaturation, adjustQuality]
    images.append(image)
    for operation in operations: 
        for image in images:
            tmp.append(operation(image))
        images += tmp
        tmp = []
    images = [resizeRescale(img) for img in images]
    return images

def augmentAll(imageLocations = []):
    dataset = []
    for imageLocation in imageLocations:
        image = tf.keras.preprocessing.image.load_img(imageLocation, color_mode='rgb', interpolation='nearest')
        dataset += augment(image)
    return tf.data.Dataset.from_tensor_slices(dataset)
