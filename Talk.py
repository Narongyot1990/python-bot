import pyautogui
import time
import pyperclip

#pyautogui.displayMousePosition()
def double_click(x, y, delay=0.1):
    pyautogui.moveTo(x, y)
    pyautogui.doubleClick()
    time.sleep(delay)

def input_text(text, delay=0.1):
    pyperclip.copy(text)
    time.sleep(0.1)  # Give the system a moment to process the clipboard operation
    pyautogui.hotkey('command', 'v')  # Use 'ctrl' if you're on Windows
    time.sleep(delay)

def send_msg_roblox(cycle_time, texts, duration_time, input_pos, send_pos):
    try:
        for _ in range(cycle_time):
            for text in texts:
                double_click(*input_pos)
                input_text(text)
                double_click(*send_pos)
            time.sleep(duration_time)
    except KeyboardInterrupt:
        print("Process stopped by user.")

def send_msg_discord(cycle_time, texts, duration_time, input_pos):
    try:
        for _ in range(cycle_time):
            for text in texts:
                double_click(*input_pos)
                input_text(text)
                pyautogui.press('enter')
                time.sleep(duration_time)
    except KeyboardInterrupt:
        print("Process stopped by user.")

def text_translate(input_pos, texts, send_pos):
    if isinstance(texts, list):
        for text in texts:
            double_click(*input_pos)
            input_text(text)
            double_click(*send_pos)
    else:
        double_click(*input_pos)
        input_text(texts)
        double_click(*send_pos)

#pyautogui.displayMousePosition()
# Copy text from Chat onto Roblox
while True:
    texts = input('\033[92mType here:\033[0m ')  # \033[92m sets the text color to green
    text_translate(input_pos=(303, 539), texts=texts, send_pos=(720, 534))
    time.sleep(7)
    double_click(96, 460)
    double_click(952, 402)
    pyautogui.hotkey('command', 'v')
    #time.sleep(0.1)
    #   double_click(1218, 399)