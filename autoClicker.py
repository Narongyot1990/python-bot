import pyautogui
import time
from pynput.keyboard import Key, Listener
from pynput import mouse, keyboard
import threading

toggle = False

# Global variables to store the state and recorded clicks
recording = False
playing = False
stop_replay = False
click_records = []

replay_count = 1

def on_click(x, y, button, pressed):
    global recording, click_records
    if recording and pressed:
        timestamp = time.time()
        click_records.append((x, y, timestamp))
        print(f"Recorded click at ({x}, {y}) at time {timestamp}")

def on_press(key):
    global recording, playing, stop_replay, replay_count, toggle
    try:
        if key == keyboard.KeyCode.from_char('8'):  # Start/stop recording with Control + 8
            if not recording:
                print("Started recording clicks. Press Control + 8 again to stop.")
                recording = True
                click_records.clear()
            else:
                print("Stopped recording clicks.")
                recording = False
        elif key == keyboard.KeyCode.from_char('9'):  # Play recorded clicks with Control + 9
            if not playing and click_records:
                replay_count = int(input("Enter the number of times to repeat the clicks (0 for infinite): "))
                print("Playing recorded clicks.")
                playing = True
                stop_replay = False
                replay_thread = threading.Thread(target=replay_clicks)
                replay_thread.start()
        elif key == keyboard.KeyCode.from_char('0'):  # Stop replay with Control + 0
            if playing:
                print("Stopping replay.")
                stop_replay = True
        elif key == keyboard.KeyCode.from_char('v'):  # Toggle autoclick with Control + V
            if not toggle:
                print("Auto clicker is now ON")
                toggle = True
            else:
                print("Auto clicker is now OFF")
                toggle = False
    except AttributeError:
        pass

def replay_clicks():
    global playing, stop_replay
    count = 0
    while not stop_replay and (replay_count == 0 or count < replay_count):
        start_time = click_records[0][2]
        for pos in click_records:
            if stop_replay:
                break
            x, y, timestamp = pos
            wait_time = timestamp - start_time
            time.sleep(wait_time)
            pyautogui.click(x, y)
            start_time = timestamp
        count += 1
    playing = False

def auto_click(click_interval):
    """
    Function to perform infinite auto clicking.

    :param click_interval: Time interval between clicks in seconds
    """
    print("Press Ctrl + V to toggle the auto clicker.")
    try:
        while True:
            if toggle:
                pyautogui.click()
            time.sleep(click_interval)
    except KeyboardInterrupt:
        print("Auto clicker stopped.")

if __name__ == "__main__":
    click_interval = 0.5  # Time between clicks in seconds

    print("Starting auto clicker and click recorder...")
    auto_click_thread = threading.Thread(target=auto_click, args=(click_interval,))
    auto_click_thread.start()

    # Create mouse and keyboard listeners for recording and controlling autoclicker
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)

    # Start listeners
    mouse_listener.start()
    keyboard_listener.start()

    # Keep the script running
    print("Press Control + 8 to start/stop recording clicks, Control + 9 to replay clicks, and Control + 0 to stop replay.")
    mouse_listener.join()
    keyboard_listener.join()
    auto_click_thread.join()