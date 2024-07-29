import cv2
import pyautogui as pg
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import time

# Load the trained model
model = load_model('object_detector.h5')

# Function to prepare the image
def prepare_image(image, target_size):
    if image.shape[:2] != target_size:
        image = cv2.resize(image, target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.0
    return image

while True:
    print("Looking for image...")  
    # Capture screenshot
    screenshot = pg.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Prepare the image for prediction
    image = prepare_image(screenshot, target_size=(150, 150))
    
    # Make prediction
    prediction = model.predict(image)
    
    # Check if image is found
    if prediction[0][0] >= 0.8:
        print("Found image!")  
        # Resize the image for better display
        resized_screenshot = cv2.resize(screenshot, (300, 300))  # Resize to desired dimensions
        # Display the result
        cv2.imshow('Detected Region', resized_screenshot)
        cv2.waitKey(500)  # Display the image for 0.5 seconds (500 milliseconds)
        cv2.destroyWindow('Detected Region')  # Close the displayed window
    else:
        print("Image not found.") 
    
    time.sleep(1)  # Wait for 1 second before checking again
