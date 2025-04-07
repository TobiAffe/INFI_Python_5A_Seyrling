import os
import cv2
import time

# Parameter
categories = ["schere", "stein", "papier"]
base_dir = "./img"  # Pfad anpassen
os.makedirs(base_dir, exist_ok=True)

# Kamera starten
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

for category in categories:
    img_counter = 0
    category_path = os.path.join(base_dir, category)
    os.makedirs(category_path, exist_ok=True)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Fehler: Kein Frame erhalten.")
            break

        cv2.imshow('Kamera', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s'):
            img_name = f"{category}_{img_counter}_seyrling.png"
            cv2.imwrite(os.path.join(category_path, img_name), frame)
            print(f"Bild gespeichert: {img_name}")
            img_counter += 1
            time.sleep(0.5)  # Kleine Pause, um nicht zu viele Bilder auf einmal zu machen

capture.release()
cv2.destroyAllWindows()
