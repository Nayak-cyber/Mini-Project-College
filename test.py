from flask import Flask, render_template, Response, redirect, url_for
import cv2
import os

app = Flask(__name__)

# Global variable to store the detected face
detected_face_name = None

# Path to the directory containing reference images of people to track
reference_images_dir = 'Gugs'

# Load all reference images and their names
reference_images = []
reference_names = []

for filename in os.listdir(reference_images_dir):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(reference_images_dir, filename)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (100, 100))  # Resize for better performance
        reference_images.append(image)
        reference_names.append(os.path.splitext(filename)[0])

# Create a Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def generate_frames():
    global detected_face_name
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_region = gray_frame[y:y+h, x:x+w]
            best_match_name = "Unknown"
            best_match_value = 0

            for ref_image, name in zip(reference_images, reference_names):
                face_region_resized = cv2.resize(face_region, (ref_image.shape[1], ref_image.shape[0]))
                result = cv2.matchTemplate(face_region_resized, ref_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)

                if max_val > best_match_value:
                    best_match_value = max_val
                    best_match_name = name

            # Set the face name based on the best match
            face_name = best_match_name if best_match_value > 0.2 else "Unknown"
            
            # Update the global variable with the detected face name
            detected_face_name = face_name
            
            # Draw a rectangle around the face and display the name
            color = (0, 255, 0) if face_name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, face_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Encode frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to redirect after detecting a face
@app.route('/detected_face')
def detected_face():
    global detected_face_name
    if detected_face_name:
        return render_template('detected_face.html', name=detected_face_name)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
