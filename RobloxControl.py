import pyautogui
import time
import os

# Size of the screen (for verification)
screen_size = pyautogui.size()
print(f"Screen size: {screen_size}")

def list_image_paths():
    directory_path = 'RobloxBot'
    files = os.listdir(directory_path)
    return [os.path.join(directory_path, file) for file in files if file.endswith(('.png', '.jpg'))]

def find_and_move_to_image(image_path):
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location is not None:
            x, y = pyautogui.center(location)
            x, y = x / 2, y / 2
            
            pyautogui.moveTo(x, y)
            print(f"Moved to {x}, {y}")
            time.sleep(0.1)

            pyautogui.doubleClick()
            pyautogui.typewrite('Anime Defenders')
            time.sleep(0.1)
            pyautogui.press('enter')
            
        else:
            print("Image not found on the screen.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get all image paths from the directory
image_paths = list_image_paths()

# Use the first image path to find and move to it
if image_paths:  # check if there is at least one image
    find_and_move_to_image(image_paths[0])
else:
    print("No images found in the directory.")