import os
from PIL import Image

# Ordner definieren
input_dir = "./img"
output_dir = "./img_resized"
size = (180, 180)

# Zielordner erstellen
os.makedirs(output_dir, exist_ok=True)

# Alle Bilder im Ordner verkleinern
for file in os.listdir(input_dir):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(input_dir, file)
        img = Image.open(img_path)
        img = img.resize(size, Image.ANTIALIAS)
        img.save(os.path.join(output_dir, file))

