import numpy as np
import pandas as pd
from tensorflow import keras
from keras import layers
import matplotlib.pyplot as plt
import os
from collections import Counter
from PIL import Image

# Daten laden
(train_images, train_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()

# Anzahl der Trainingsdaten anzeigen
print(f"Anzahl Trainingsdaten: {len(train_images)}")

# Häufigkeit der Labels berechnen
fashion = {i: 0 for i in range(10)}
for label in train_labels:
    fashion[label] += 1
print(f"Häufigkeit der Daten: {fashion}")

# 10. Bild und Label anzeigen
print(f"Label des 10. Bildes: {train_labels[10]}")
plt.imshow(train_images[10], cmap="gray")
plt.title(f"Label: {train_labels[10]}")
plt.grid(False)
plt.show()

# Speichern der ersten 100 Bilder nach Labels in Ordnern
save_path = "./img/fashion/"
for i in range(100):
    img = Image.fromarray(train_images[i])
    label = train_labels[i]
    label_folder = os.path.join(save_path, str(label))
    os.makedirs(label_folder, exist_ok=True)
    img.save(os.path.join(label_folder, f"{i}_{label}.jpeg"))

print("Die ersten 100 Bilder wurden in ./img/fashion/ gespeichert.")

# Daten vorverarbeiten
train_images = train_images.astype("float32") / 255.0
test_images = test_images.astype("float32") / 255.0

# Daten reshapen und Labels in kategorische Matrizen umwandeln
train_images = train_images.reshape(-1, 28 * 28)
test_images = test_images.reshape(-1, 28 * 28)
train_labels = keras.utils.to_categorical(train_labels, 10)
test_labels = keras.utils.to_categorical(test_labels, 10)

# Modell erstellen
model = keras.Sequential(
    [
        keras.Input(shape=(784,)),
        layers.Dense(128, activation="relu"),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax"),
    ]
)

# Modell zusammenfassen
model.summary()

# Modell kompilieren
model.compile(
    loss="categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"],
)

# Modell trainieren
batch_size = 128
epochs = 5
history = model.fit(
    train_images, train_labels, batch_size=batch_size, epochs=epochs, validation_split=0.1
)

# Trainingsverlauf plotten
pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.title("Trainingsverlauf")
plt.show()

# Modell evaluieren
score = model.evaluate(test_images, test_labels, verbose=2)
print(f"Test Loss: {score[0]}")
print(f"Test Accuracy: {score[1]}")

# Vorhersagen treffen
predictions = model.predict(test_images)
for i in range(10):
    pred_label = np.argmax(predictions[i])
    true_label = np.argmax(test_labels[i])
    print(f"Bild {i}: Vorhersage = {pred_label}, Wahres Label = {true_label}")
