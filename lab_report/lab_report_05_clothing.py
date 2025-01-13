import numpy as np
import pandas as pd
import collections #used for counting items of a list
from tensorflow import keras
from keras import layers
import matplotlib.pyplot as plt
from keras.datasets import mnist, fashion_mnist
import matplotlib.pyplot as plt
from tensorflow import keras
import json
import os

from PIL import Image

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

print (f"Anzahl Trainingsdaten: {len(train_images)}")

fashion = {i:0 for i in range(0,10)}
for label in train_labels:
    for f in fashion:
        if(f == label):
            fashion[label] += 1;
print(f"Häufigkeit der Daten{fashion}")

## 10tes Bild Infos
print (train_labels[10]) ## welches Kleidungsstück?
plt.imshow(train_images[10]) ## Bild anzeigen
plt.grid(False)
plt.show()

for i in range(0,100):
    im = Image.fromarray(train_images[i])
    real = train_labels[i]
    try:
        os.mkdir("./img/fashion/%d" % (train_labels[i]))
    except:
        pass
    im.save("./img/fashion/%d/%d_%d.jpeg" % (train_labels[i], i, real))

