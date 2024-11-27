import cv2
import numpy as np
import os
from datetime import datetime

def detect_cones_in_image(image_path, output_folder):

    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([25, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 500:  
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, 'Cone', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"output_{timestamp}.png")

    cv2.imwrite(output_path, image)
    print(f"Output saved at: {output_path}")

if __name__ == "__main__":
    project_folder = r"C:\Users\mozam\Documents\Project\OpenCV-Cone-Detection"
    image_folder = os.path.join(project_folder, "image")
    output_folder = os.path.join(project_folder, "output")

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # File paths
    input_image = os.path.join(image_folder, "image1.png")

    # Detect cones in the image
    detect_cones_in_image(input_image, output_folder)
