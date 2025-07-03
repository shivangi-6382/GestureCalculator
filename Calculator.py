import cv2
import numpy as np
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)


def distance(p1,p2):
    return np.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)

def gestureDetection(handData1, handData2):
    (hand1, label1), (hand2, label2) = handData1, handData2
    fingerCount_1 = fingersUp(hand1, label1)
    fingerCount_2 = fingersUp(hand2, label2)

    dist = distance(hand1.landmark[8], hand2.landmark[8])

    print(f"FC1: {fingerCount_1}, FC2: {fingerCount_2}, Dist: {dist:.3f}")

    if fingerCount_1 == 1 and fingerCount_2 == 1:
        if dist < 0.06:
            print("Gesture: exit")
            return "exit"
        print("Gesture: +")
        return "+"
    elif (fingerCount_1 == 1 and fingerCount_2 == 2) or (fingerCount_1 == 2 and fingerCount_2 == 1):
        print("Gesture: -")
        return "-"
    elif (fingerCount_1 == 1 and fingerCount_2 == 3) or (fingerCount_1 == 3 and fingerCount_2 == 1):
        print("Gesture: *")
        return "*"
    elif (fingerCount_1 == 1 and fingerCount_2 == 4) or (fingerCount_1 == 4 and fingerCount_2 == 1):
        print("Gesture: /")
        return "/"
    elif fingerCount_1 == 2 and fingerCount_2 == 2:
        print("Gesture: dlt")
        return "dlt"
    elif (fingerCount_1 == 5 and fingerCount_2 == 1) or (fingerCount_1 == 1 and fingerCount_2 == 5):
        print("Gesture: 6")
        return "6"
    elif (fingerCount_1 == 5 and fingerCount_2 == 2) or (fingerCount_1 == 2 and fingerCount_2 == 5):
        print("Gesture: 7")
        return "7"
    elif (fingerCount_1 == 5 and fingerCount_2 == 3) or (fingerCount_1 == 3 and fingerCount_2 == 5):
        print("Gesture: 8")
        return "8"
    elif (fingerCount_1 == 5 and fingerCount_2 == 4) or (fingerCount_1 == 4 and fingerCount_2 == 5):
        print("Gesture: 9")
        return "9"
    elif fingerCount_1 == 0 and fingerCount_2 == 0:
        print("Gesture: =")
        return "="
    elif fingerCount_1 == 5 and fingerCount_2 == 5:
        print("Gesture: clear")
        return "clear"
    return None


#function to count no. of fingers
def fingersUp(hand_landmarks,label):
    tipIds=[4,8,12,16,20]
    fingers=[]
    if label=="Left":
        fingers.append(1 if hand_landmarks.landmark[tipIds[0]].x> hand_landmarks.landmark[tipIds[0]-1].x else 0)

    else:
        fingers.append(1 if hand_landmarks.landmark[tipIds[0]].x < hand_landmarks.landmark[tipIds[0] - 1].x else 0)

    for id in range(1,5):
        if hand_landmarks.landmark[tipIds[id]].y < hand_landmarks.landmark[tipIds[id]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)



#main
prev_fingerCount=None
pTime=0
delay=1.25
expression=""
res=""


cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(imgRGB)
    cTime=time.time()
    handData=[]

    if result.multi_hand_landmarks and result.multi_handedness:
        for handLms, hand_handedness in zip(result.multi_hand_landmarks,result.multi_handedness):
            label=hand_handedness.classification[0].label
            handData.append((handLms, label))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        if len(handData)==1:
            handLms,label=handData[0]
            fingerCount=fingersUp(handLms,label)
            if fingerCount in [0,1,2,3,4,5] and cTime-pTime>delay:
                expression+=str(fingerCount)
                pTime=cTime
                prev_fingerCount=fingerCount

        if len(handData)==2:
            gesture=gestureDetection(handData[0],handData[1])
            print(gesture)



            if gesture=="clear":
                expression=""
                res=""


            if gesture=="exit":
                break

            if gesture and cTime-pTime>delay:

                if gesture=="dlt":
                    expression=expression[:-1]
                    pTime=cTime

                elif gesture=="=":
                    try:
                        res= str(eval(expression))
                        print("Result",res)
                    except:
                        res="Error"
                    pTime=cTime


                else:

                    expression += gesture

                    pTime = cTime

    cv2.putText(img,f'Expression: {expression}',(20,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
    cv2.putText(img,f'Result:{res}',(20,110),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow('Calculator', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("c"):
        expression=""
        res=""

cap.release()
cv2.destroyAllWindows()














