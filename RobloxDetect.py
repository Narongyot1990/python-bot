import cv2
import numpy as np
import mss
import os
import time
import threading
import queue

# Load images from directory, including multiple views
def load_images_from_dir(directory, color_mode=cv2.IMREAD_GRAYSCALE):
    images = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith(".png"):
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path, color_mode)
            if img is not None:
                # Extract the object name (prefix before the view identifier)
                obj_name = "_".join(filename.split('_')[:-1])
                if obj_name not in images:
                    images[obj_name] = []
                images[obj_name].append((img, filename))
            else:
                print(f"Failed to load image: {filename}")
    return images

# Capture screen with resizing
def capture_screen(resize_factor=0.5):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        if resize_factor != 1:
            height, width = screenshot.shape[:2]
            screenshot = cv2.resize(screenshot, (int(width * resize_factor), int(height * resize_factor)))
        return screenshot

# Match features with FLANN and Lowe's ratio test
def match_features(des1, des2):
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
    return good_matches

# Find homography
def find_homography(kp1, kp2, good_matches):
    if len(good_matches) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return M
    else:
        print("Not enough matches are found - {}/{}".format(len(good_matches), 10))
        return None

# Draw object bounds
def draw_object_bounds(bg, obj, kp_obj, kp_bg, good_matches, filename):
    M = find_homography(kp_obj, kp_bg, good_matches)
    if M is not None:
        h, w = obj.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        bg = cv2.polylines(bg, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
        label = os.path.splitext(filename)[0]
        cv2.putText(bg, label, (int(dst[0][0][0]), int(dst[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
    return bg

# Detect objects
def detect_objects(bg, obj_images, confidence_threshold=25):
    sift = cv2.SIFT_create()
    kp_bg, des_bg = sift.detectAndCompute(cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY), None)
    
    for obj_name, views in obj_images.items():
        for obj, filename in views:
            kp_obj, des_obj = sift.detectAndCompute(obj, None)
            if des_obj is not None and des_bg is not None:
                good_matches = match_features(des_obj, des_bg)
                print(f"Best match confidence for {filename}: {len(good_matches)}")
                if len(good_matches) > confidence_threshold:
                    bg = draw_object_bounds(bg, obj, kp_obj, kp_bg, good_matches, filename)
                    break  # Stop after the first successful match for this object
    
    return bg

# Main function with threading
def main():
    obj_images_directory = "RobloxObj"
    obj_images = load_images_from_dir(obj_images_directory)
    capture_interval = 0.0167  # 60 FPS -> 1/60 seconds

    frame_queue = queue.Queue()

    def capture_and_process():
        while True:
            start_time = time.time()
            frame = capture_screen()
            processed_frame = detect_objects(frame, obj_images)
            frame_queue.put(processed_frame)
            elapsed_time = time.time() - start_time
            if elapsed_time < capture_interval:
                time.sleep(capture_interval - elapsed_time)

    capture_thread = threading.Thread(target=capture_and_process)
    capture_thread.start()

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            cv2.imshow('Detected Objects', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture_thread.join()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
