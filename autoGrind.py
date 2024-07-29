import time
import pickle
import os
from pynput import mouse, keyboard
import threading
import pyautogui

# Global variables
input_events = []
recording = False
replaying = False  
mouse_listener = None
keyboard_listener = None
replay_thread = None

def on_click(x, y, button, pressed):
    """
    Callback function to handle mouse click events.
    """
    event = {'type': 'mouse_click', 'x': x, 'y': y, 'button': button, 'pressed': pressed, 'time': time.time()}
    input_events.append(event)

def on_move(x, y):
    """
    Callback function to handle mouse move events.
    """
    event = {'type': 'mouse_move', 'x': x, 'y': y, 'time': time.time()}
    input_events.append(event)

def on_scroll(x, y, dx, dy):
    """
    Callback function to handle mouse scroll events.
    """
    event = {'type': 'mouse_scroll', 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'time': time.time()}
    input_events.append(event)

def on_press(key):
    """
    Callback function to handle key press events.
    """
    try:
        event = {'type': 'key_press', 'key': key, 'time': time.time()}
        input_events.append(event)
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    """
    Callback function to handle key release events.
    """
    try:
        event = {'type': 'key_release', 'key': key, 'time': time.time()}
        input_events.append(event)
    except Exception as e:
        print(f"Error: {e}")

def toggle_recording():
    """
    Toggle the recording state.
    """
    global recording, mouse_listener, keyboard_listener
    if recording:
        recording = False
        if mouse_listener is not None:
            mouse_listener.stop()
        if keyboard_listener is not None:
            keyboard_listener.stop()
        print("Recording stopped.")
        filename = input("Enter file name to save: ")
        save_events(input_events, filename)
    else:
        recording = True
        input_events.clear()
        mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        mouse_listener.start()
        keyboard_listener.start()
        print("Recording started.")

def save_events(events, filename):
    """
    Function to save recorded input events to a file.
    """
    with open(filename, 'wb') as f:
        pickle.dump(events, f)

def load_events():
    """
    Function to load recorded input events from a file.
    """
    filename = input("Enter file name to load: ")
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        print("File not found.")
        return None

def replay_events(events, loop_count=1, interval=0):
    """
    Function to replay recorded input events.
    """
    global replaying
    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()
    start_time = events[0]['time']
    
    while replaying:
        for _ in range(loop_count) if loop_count > 0 else iter(int, 1):
            # Reinitialize mouse controller
            mouse_controller = mouse.Controller()
            for event in events:
                if not replaying:
                    break
                event_type = event['type']
                if event_type.startswith('mouse'):
                    if event_type == 'mouse_move':
                        time.sleep(max(0, event['time'] - start_time + interval))
                        mouse_controller.position = (event['x'], event['y'])
                        print(f"Mouse moved to {(event['x'], event['y'])}")
                    elif event_type == 'mouse_click':
                        time.sleep(max(0, event['time'] - start_time))
                        if event['pressed']:
                            mouse_controller.press(event['button'])
                            print(f"Mouse button {event['button']} pressed at {(event['x'], event['y'])}")
                        else:
                            mouse_controller.release(event['button'])
                            print(f"Mouse button {event['button']} released at {(event['x'], event['y'])}")
                    elif event_type == 'mouse_scroll':
                        time.sleep(max(0, event['time'] - start_time + interval))
                        mouse_controller.scroll(event['dx'], event['dy'])
                        print(f"Mouse scrolled by ({event['dx']}, {event['dy']})")
                elif event_type == 'key_press':
                    time.sleep(max(0, event['time'] - start_time + interval))
                    keyboard_controller.press(event['key'])
                    print(f"Key {event['key']} pressed")
                elif event_type == 'key_release':
                    time.sleep(max(0, event['time'] - start_time + interval))
                    keyboard_controller.release(event['key'])
                    print(f"Key {event['key']} released")
                start_time = event['time']
        if loop_count == 0:
            continue
        break

def toggle_replay():
    """
    Toggle the replaying state.
    """
    global replaying, replay_repeat

    def run_replays_sequentially():
        while replaying:
            for events, loop_count in replay_tasks:
                if not replaying:
                    break
                thread = threading.Thread(target=replay_events, args=(events, loop_count))
                thread.start()
                thread.join()  # Wait for the current file to finish before moving to the next one
            if replay_repeat != 'Y':
                break
            print("Replaying again.")

    if replaying:
        # Stop the replaying process
        replaying = False
        print("Replaying stopped.")
    else:
        # Start the replaying process
        replaying = True
        replay_tasks = []
        num_files = int(input("Enter the number of files to replay: "))
        for _ in range(num_files):
            events = load_events()
            if events:
                loop_count = int(input("Enter loop count (0 for infinite) for this file: "))
                replay_tasks.append((events, loop_count))
            else:
                print("No file selected or invalid file format.")
        
        # Ask once for repeat
        replay_repeat = input("Do you want to repeat the replay [Y/N]: ").strip().upper()

        replay_thread = threading.Thread(target=run_replays_sequentially)
        replay_thread.start()
        print("Replaying started.")

def on_key_pressed(key):
    """
    Callback function to handle key press events.
    """
    try:
        if key == keyboard.KeyCode.from_char('9') and keyboard.Controller().pressed(keyboard.Key.ctrl):
            toggle_replay()
    except Exception as e:
        print(f"Error: {e}")

def on_hotkey_pressed():
    """
    Callback function to handle hotkey press events.
    """
    try:
        toggle_recording()
    except Exception as e:
        print(f"Error: {e}")

def on_key_pressed(key):
    """
    Callback function to handle key press events.
    """
    try:
        if key == keyboard.KeyCode.from_char('9') and keyboard.Controller().pressed(keyboard.Key.ctrl):
            toggle_replay()
        elif key == keyboard.KeyCode.from_char('0') and keyboard.Controller().pressed(keyboard.Key.ctrl):
            toggle_replay()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Start the keyboard listener
    with keyboard.GlobalHotKeys({'<ctrl>+8': on_hotkey_pressed}) as h:
        print("Press Ctrl + 8 to start/stop recording input events.")
        print("Press Ctrl + 9 to start/stop replaying input events.")

        with keyboard.Listener(on_press=on_key_pressed) as k:
            h.join()
            k.join()    

