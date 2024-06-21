import cv2
import os
import HandTrackingModule as htm
import ctypes
import pygame
import pyautogui
import time

folderPath1 = "MPannel"
folderPath2 = "SPannel1"
folderPath3 = "SPannel2"
myList1 = os.listdir(folderPath1)
myList2 = os.listdir(folderPath2)
mylist3 = os.listdir(folderPath3)

print(myList1)
print(myList2)
print(mylist3)

overLayList1 = [cv2.imread(f'{folderPath1}/{imPath1}') for imPath1 in myList1]
overLayList2 = [cv2.imread(f'{folderPath2}/{imPath2}') for imPath2 in myList2]
overLaylist3 = [cv2.imread(f'{folderPath3}/{impath3}') for impath3 in mylist3]

#print(len(overLayList1))

header_main = overLayList1[0]
header_secondary = None  # Initialize header_secondary as None
header_tertiary = None



def increase_brightness():
    os.system(
        'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 100)')



def decrease_brightness():
    os.system(
        'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 0)')


def lock_screen():
    ctypes.windll.user32.LockWorkStation()


class AlbumPlayer:
    def __init__(self, album_path):
        self.album_path = album_path
        self.songs = [song for song in os.listdir(album_path) if song.endswith('.mp3')]
        self.current_song_index = 0
        self.paused = False
        # Set initial volume (0.5 means 50% volume)
        self.volume = 0.5
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

    def play_song(self, song_index):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(self.album_path, self.songs[song_index]))
        pygame.mixer.music.play()

    def pause_song(self):
        pygame.mixer.music.pause()
        print("Paused song.")

    def resume_song(self):
        pygame.mixer.music.unpause()
        print("Resumed song.")

    def next_song(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_song(self.current_song_index)
        print("Playing Next song.")

    def prev_song(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.play_song(self.current_song_index)
        print("Playing Previous song.")

    def increase_volume(self):
        if self.volume < 1.0:
            self.volume += 0.1
            pygame.mixer.music.set_volume(self.volume)
            print(f"Volume increased: {self.volume}")

    def decrease_volume(self):
        if self.volume > 0.0:
            self.volume -= 0.1
            pygame.mixer.music.set_volume(self.volume)
            print(f"Volume decreased: {self.volume}")


if __name__ == "__main__":
    album_path = r"C:\Users\jahed\iotproject\Virtual  Control\Songs"
    player = AlbumPlayer(album_path)


def Brightness_control():
    global header_secondary  # Declare header_secondary as a global variable
    # print(cx,cy)
    if cy < 160:

        if 220 < cx < 290:
            # print("function executing")
            header_secondary = overLayList2[1]
            decrease_brightness()
            pyautogui.hotkey('2', 'enter')
            #time.sleep(2)
            print("Brightness decreased.")

        if 480 < cx < 560:
            header_secondary = overLayList2[2]
            increase_brightness()
            pyautogui.hotkey('1', 'enter')
            print("Brightness increased")


        if 730 < cx < 800:
            header_secondary = overLayList2[3]
            pyautogui.hotkey('2', 'enter')
            header_secondary = None


def Music_Control():
    global header_tertiary
    #player.play_song(player.current_song_index)

    # print(cx,cy)
    if cy < 160:

        if 100 < cx < 170:
            header_tertiary = overLaylist3[1]
            player.prev_song()

        if 240 < cx < 310:
            header_tertiary = overLaylist3[2]
            player.decrease_volume()

        elif 430 < cx < 480:
            header_tertiary = overLaylist3[3]
            player.pause_song()

        elif 600 < cx < 660:
            header_tertiary = overLaylist3[4]
            player.resume_song()

        elif 780 < cx < 830:
            header_tertiary = overLaylist3[5]
            player.increase_volume()

        elif 930 < cx < 990:
            header_tertiary = overLaylist3[6]
            player.next_song()

        elif 1070 < cx < 1130:
            header_tertiary = overLaylist3[7]
            player.pause_song()
            header_tertiary = None

        #else:
            #player.play_song(player.current_song_index)


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        fingers = detector.fingersUp()

        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            #cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx,cy),18, (255,0,255), cv2.FILLED)
            if y1 < 100:
                if 340 < cx < 420:
                    header_main = overLayList1[1]
                    header_tertiary = None
                    header_secondary = overLayList2[0]
                    pyautogui.hotkey('1', 'enter')
                elif 580 < cx < 660:
                    header_main = overLayList1[2]
                    player.play_song(player.current_song_index)
                    header_secondary = None  # Reset header_secondary when changing main header
                    header_tertiary = overLaylist3[0]
                elif 840 < cx < 920:
                    header_main = overLayList1[3]
                    header_secondary = None  # Reset header_secondary when changing main header
                    header_tertiary = None
                    print("Locking the screen...")
                    lock_screen()
                    pyautogui.hotkey('3', 'enter')

        if header_secondary is not None:
            Brightness_control()

        if header_tertiary is not None:
            Music_Control()


    img[0:75, 0:1280] = header_main
    if header_secondary is not None:
        img[75:150, 0:1280] = header_secondary
    if header_tertiary is not None:
        img[75:150, 0:1280] = header_tertiary
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
