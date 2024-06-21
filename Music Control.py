import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
import pygame

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)
print(len(overLayList))
header = overLayList[0]


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

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 75)


detector = htm.handDetector(detectionCon=0.85)
player.play_song(player.current_song_index)
print("playing the Song")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 75)

detector = htm.handDetector(detectionCon=0.85)

# Initialize a flag variable
operation_executed = False

while True:
    # 1. Import the Image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. If Selection Mode - Two Fingers are up
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4] and not operation_executed:
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
            #print(x1, y1)
            if y1 < 110:
                if 10 < x1 < 70:
                    header = overLayList[1]
                    #print("Task-1")
                    player.prev_song()

                elif 100 < x1 < 170:
                    header = overLayList[2]
                    #print("Task-2")
                    player.decrease_volume()

                elif 210 < x1 < 290:
                    header = overLayList[3]
                    #print("Task-3")
                    player.resume_song()

                elif 330 < x1 < 400:
                    header = overLayList[4]
                    #print("Task-4")
                    player.pause_song()

                elif 450 < x1 < 490:
                    header = overLayList[5]
                    #print("Task-5")
                    player.increase_volume()

                elif 530 < x1 < 620:
                    header = overLayList[6]
                    #print("Task-6")
                    player.next_song()


                # Set the flag to True to indicate that the operation has been executed
                operation_executed = True

        # Reset the flag if the fingers are not in the required position
        elif not fingers[1] or not fingers[2] or fingers[3] or fingers[4]:
            operation_executed = False

    # Resize the header image to match the region dimensions
    header_resized = cv2.resize(header, (640, 75))
    img[0:75, 0:640] = header_resized

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)  # Wait for a key event
    if key == 27:  # ASCII code for the ESC key
        break  # Break out of the loop if ESC is pressed
