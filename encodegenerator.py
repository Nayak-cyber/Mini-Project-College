import cv2
import numpy as np
import os

# Path to the directory containing reference images of people to track
reference_images_dir = 'Gugs'

# Load all reference images and their names
reference_images = []
reference_names = []

for filename in os.listdir(reference_images_dir):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        image_path = os.path.join(reference_images_dir, filename)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (100, 100))  # Resize for better performance
        reference_images.append(image)
        reference_names.append(os.path.splitext(filename)[0])

# Create a Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Initialize the name for the detected face
    face_name = "Unknown"

    # Check each detected face
    for (x, y, w, h) in faces:
        # Extract the face region from the frame
        face_region = gray_frame[y:y+h, x:x+w]

        # Initialize the best match values
        best_match_name = "Unknown"
        best_match_value = 0

        # Compare the face region with all reference images
        for ref_image, name in zip(reference_images, reference_names):
            # Resize the face region to match the template size
            face_region_resized = cv2.resize(face_region, (ref_image.shape[1], ref_image.shape[0]))

            # Perform template matching
            result = cv2.matchTemplate(face_region_resized, ref_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            # Update the best match if this one is better
            if max_val > best_match_value:
                best_match_value = max_val
                best_match_name = name

        # Set face name based on the best match
        face_name = best_match_name if best_match_value > 0.2 else "Unknown"

        # Draw rectangle around the face
        color = (0, 255, 0) if face_name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, face_name, (x + 6, y - 6), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        print(f"{face_name}: {best_match_value}")

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Exiting...')
        break

# Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()
