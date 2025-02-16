import collections
import sys

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random


def get_random_greyscale(width: int,
                         height: int,
                         show: bool = False):
    image = np.zeros((height, width))

    # Definieren der Farbzentren
    centers = [
        (random.randint(0, height), random.randint(0, width)),  # Zentrum 1
        (random.randint(0, height), random.randint(0, width)),  # Zentrum 2
        (random.randint(0, height), random.randint(0, width)),  # Zentrum 3
        (random.randint(0, height), random.randint(0, width))  # Zentrum 4
    ]

    # Füllen der Farbzentren
    for center in centers:
        cx, cy = center
        for x in range(width):
            for y in range(height):
                # Berechnung der Distanz zum Zentrum
                distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                # Setzen der Pixelwerte basierend auf der Distanz
                image[y, x] += np.exp(-distance / 50) * 255

    # Normalisieren der Bildwerte auf den Bereich 0-255
    image = np.clip(image, 0, 255)

    # Anzeigen des Bildes
    if show:
        plt.imshow(image, cmap='gray')
        plt.axis('off')  # Achsen ausblenden
        plt.show()
    return image

width = 200
height = 200

img_ar = get_random_greyscale(width, height, True)


train_data = img_ar.flatten().astype(np.float32)
x_train = np.arange(len(train_data)).reshape(-1, 1).astype(np.float32)


nn = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=(1,)),
    tf.keras.layers.Dense(units=1028, activation='sigmoid'),
    tf.keras.layers.Dense(units=1028, activation='sigmoid'),
    tf.keras.layers.Dense(units=1028, activation='sigmoid'),
    tf.keras.layers.Dense(units=1, activation='relu')
])
nn.compile(optimizer='sgd', loss="mse", metrics=['accuracy'])
print(nn.summary())
nn.fit(x=x_train, y=train_data, epochs=10)

prediction = nn.predict(x_train)

reshaped = np.ndarray.reshape(prediction, (width, height))
plt.imshow(reshaped, cmap='gray', origin='upper')
plt.axis('off')
plt.show()

