import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

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
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
            #print(x1, y1)
            if y1 < 110:
                if 10 < x1 < 70:
                    header = overLayList[1]
                    print('1')
                elif 100 < x1 < 170:
                    header = overLayList[2]
                    print('2')
                elif 210 < x1 < 290:
                    header = overLayList[3]
                    print('3')
                elif 330 < x1 < 400:
                    header = overLayList[4]
                    print('4')
                elif 450 < x1 < 490:
                    header = overLayList[5]
                    print('5')
                elif 530 < x1 < 620:
                    header = overLayList[6]
                    print('6')

                # Set the flag to True to indicate that the operation has been executed
                operation_executed = True

        # Reset the flag if the fingers are not in the required position
        elif not fingers[1] or not fingers[2] or fingers[3] or fingers[4]:
            operation_executed = False

        # 5. Operation Mode
        # if fingers[1] and fingers[2]==False:
        #     print("operation Mode")

    # Resize the header image to match the region dimensions
    header_resized = cv2.resize(header, (640, 75))
    img[0:75, 0:640] = header_resized

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)  # Wait for a key event
    if key == 27:  # ASCII code for the ESC key
        break  # Break out of the loop if ESC is pressed