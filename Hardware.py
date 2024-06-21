import cv2
import os
import HandTrackingModule as htm
import pyautogui

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)
print(len(overLayList))
header = overLayList[0]

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 75)

detector = htm.handDetector(detectionCon=0.85)


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
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # 4. If Selection Mode - Two Fingers are up
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            #cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            #print(x1, y1)
            if y1 < 110:
                if 10 < x1 < 70:
                    header = overLayList[1]
                    #print("Task-1")

                elif 100 < x1 < 170:
                    header = overLayList[2]
                    #print("Task-2")
                    pyautogui.hotkey('1', 'enter')

                elif 210 < x1 < 290:
                    header = overLayList[3]
                    #print("Task-3")
                    pyautogui.hotkey('2', 'enter')

                elif 330 < x1 < 400:
                    header = overLayList[4]
                    #print("Task-4")
                    pyautogui.hotkey('3', 'enter')

                elif 450 < x1 < 490:
                    header = overLayList[5]
                    #print("Task-5")

                elif 530 < x1 < 620:
                    header = overLayList[6]
                    #print("Task-6")
    header_resized = cv2.resize(header, (640, 75))
    img[0:75, 0:640] = header_resized

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)  # Wait for a key event
    if key == 27:  # ASCII code for the ESC key
        break  # Break out of the loop if ESC is pressed

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
