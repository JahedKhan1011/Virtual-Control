#Increase and decrease Screen Brightness and lock screen

import os
import keyboard
import ctypes

def increase_brightness():
    os.system('powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 100)')

def decrease_brightness():
    os.system('powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 0)')

def lock_screen():
    ctypes.windll.user32.LockWorkStation()

def main():
    print("Press 1 to increase brightness or 2 to decrease brightness. Press any other key to exit.")

    while True:
        key = keyboard.read_event(suppress=True).name
        if key == '1':
            increase_brightness()
            print("Brightness increased.")

        elif key == '2':
            decrease_brightness()
            print("Brightness decreased.")

        elif key == '3':
            print("Locking the screen...")
            lock_screen()

        else:
            print("Exiting.")
            break

if __name__ == "__main__":
    main()
