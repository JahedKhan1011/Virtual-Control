import pyautogui
import time

# Sleep for a few seconds to give you time to focus on the input field
time.sleep(5)

# Replace 'desired_output' with the actual output you want to type
desired_output = "Hello, World!"

# Type the desired output using pyautogui
pyautogui.typewrite(desired_output)

# Press Enter (optional, if you want to simulate pressing Enter)
# pyautogui.press('enter')
