import cv2
import numpy as np
from PIL import ImageGrab

# Load YOLO
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")  # Using YOLOv3-tiny for faster processing
classes = []
with open("coco.names", "r") as f:
    classes = f.read().splitlines()

# Define screen resolution
screen_width = 3840  # Change to your screen width
screen_height = 2160  # Change to your screen height

# Define screen region to capture
screen_region = (0, 0, screen_width, screen_height)

# Create resizable window
cv2.namedWindow("Real-time Object Detection", cv2.WINDOW_NORMAL)

while True:
    # Capture screen frame
    screen = np.array(ImageGrab.grab(bbox=screen_region))
    frame = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    # Resize frame for faster processing
    frame_resized = cv2.resize(frame, (960, 540))  # Reducing the frame size

    # Preprocess frame for YOLO
    blob = cv2.dnn.blobFromImage(frame_resized, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Forward pass through YOLO
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Process detection results
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Adjust confidence threshold as needed
                # Object detected
                center_x = int(detection[0] * frame_resized.shape[1])
                center_y = int(detection[1] * frame_resized.shape[0])
                w = int(detection[2] * frame_resized.shape[1])
                h = int(detection[3] * frame_resized.shape[0])

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Scale coordinates back to the original frame size
                x = int(x * (screen_width / 960))
                y = int(y * (screen_height / 540))
                w = int(w * (screen_width / 960))
                h = int(h * (screen_height / 540))

                # Draw bounding box and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, classes[class_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Resize window based on screen resolution
    aspect_ratio = frame.shape[1] / frame.shape[0]
    window_width = min(screen_width, 800)  # Limit width to 800 pixels
    window_height = int(window_width / aspect_ratio)
    cv2.resizeWindow("Real-time Object Detection", window_width, window_height)

    # Display output frame
    cv2.imshow("Real-time Object Detection", frame)

    # Check for Ctrl + Q key press
    if cv2.waitKey(1) & 0xFF == ord('q') and cv2.getWindowProperty("Real-time Object Detection", cv2.WND_PROP_VISIBLE) >= 0:
        break

# Release resources
cv2.destroyAllWindows()
