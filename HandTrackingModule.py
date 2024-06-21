import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackingCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # if self.results.multi_hand_landmarks:
            #for handLms in self.results.multi_hand_landmarks:
                # if draw:
                #     self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 2, (255, 255, 0), cv2.FILLED)
        return self.lmList

    def fingersUp(self):
        fingers = []

        for id in range(0, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

        # Thumb
        # if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
        #     fingers.append(1)
        # else:
        #     fingers.append(0)

        # 4 Fingers
        # for id in range(1,5):
        #     if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
        #         fingers.append(1)
        #     else:
        #         fingers.append(0)
        # return fingers

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 10, 50), 3)
        cv2.imshow("Image", img)

        key = cv2.waitKey(1)  # Wait for a key event
        if key == 27:  # ASCII code for the ESC key
            break  # Break out of the loop if ESC is pressed

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

