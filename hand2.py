import cv2 as cv 
import cv2
import mediapipe as mp 
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from pygame import mixer
import winsound
import random
import numpy as np
import geocoder
import speech_recognition as sr
import requests
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    return angle
g = geocoder.ip('117.216.103.150')
r = sr.Recognizer()
mixer.init()
sound = mixer.Sound('Alarm1.mp3')
def listToString(s): 
    float_string=""
    for num in s:
        float_string=float_string+str(num)+" "
    return float_string
def send_msg(text):
    token = "5500588613:AAH5XwGTh3YCJgJhZDnxTjYDKR-ct9AhFro"
    chat_id = "-775064526"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" +"?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
class handLandmarkDetector():
    def __init__(self,image_mode=False,max_hands=2, modelC=1 ,min_detection_confidence=0.8,min_tracking_confidence=0.5):
        self.image_mode = image_mode
        self.max_hands=max_hands
        self.modelC = modelC
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.image_mode,self.max_hands,self.modelC,self.min_detection_confidence,self.min_tracking_confidence)
        self.mpDraw=mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        
    def detect_landmarks(self,image,draw=True,draw_connections=True,draw_default_style=False):
        imageRGB = cv.cvtColor(image,cv.COLOR_BGR2RGB)
        land_mark_data=[]
        hand_classified_landmarks=[[],[]]
        results = self.hands.process(imageRGB)
        landmarks=results.multi_hand_landmarks
        data=None
        if landmarks:
            for hand_landmarks in landmarks:
                for id,landmark in enumerate(hand_landmarks.landmark):
                    h,w,c = image.shape
                    px,py = int(landmark.x*w), int(landmark.y*h)
                    data=(id,px,py)
                    land_mark_data.append(data)
                if draw and not draw_connections:
                    self.mpDraw.draw_landmarks(image,hand_landmarks)
                elif draw and draw_connections and not draw_default_style:
                    self.mpDraw.draw_landmarks(image,hand_landmarks,self.mpHands.HAND_CONNECTIONS)
                elif draw and draw_connections and draw_default_style:
                    self.mpDraw.draw_landmarks(image,hand_landmarks,self.mpHands.HAND_CONNECTIONS,self.mp_drawing_styles.get_default_hand_landmarks_style(),self.mp_drawing_styles.get_default_hand_connections_style())
            if land_mark_data[0][1]>land_mark_data[4][1]:
                if len(land_mark_data)>20:
                    hand_classified_landmarks[1]=land_mark_data[0:21]
                    hand_classified_landmarks[0]=land_mark_data[21::]
                else:
                    hand_classified_landmarks[1]=land_mark_data[0:21]
            elif land_mark_data[4][1]>land_mark_data[0][1]:
                if len(land_mark_data)>20:
                    hand_classified_landmarks[0]=land_mark_data[0:21]
                    hand_classified_landmarks[1]=land_mark_data[21::]
                else:
                    hand_classified_landmarks[0]=land_mark_data[0:21]
        return hand_classified_landmarks,image
    def count_up_fingers(self,data):
        fingers=[[],[]]
        if len(data[1]) != 0:
            if (data[1][3][1] > data[1][4][1]):
                fingers[1].append(1)
            else:
                fingers[1].append(0)
            
            if (data[1][5][2] > data[1][8][2] and data[1][7][2] > data[1][8][2]) :
                fingers[1].append(1)
            else:
                fingers[1].append(0)
            if (data[1][9][2] > data[1][12][2] and data[1][11][2] > data[1][12][2]) :
                fingers[1].append(1)
            else:
                fingers[1].append(0)
            if (data[1][13][2] > data[1][16][2] and data[1][15][2] > data[1][16][2]) :
                fingers[1].append(1)
            else:
                fingers[1].append(0)
            if (data[1][17][2] > data[1][20][2] and data[1][19][2] > data[1][20][2]) :
                fingers[1].append(1)
            else:
                fingers[1].append(0)
        if len(data[0]) != 0:
            if (data[0][3][1] < data[0][4][1]):
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][5][2] > data[0][8][2] and data[0][7][2] > data[0][8][2]) :
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][9][2] > data[0][12][2] and data[0][11][2] > data[0][12][2]) :
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][13][2] > data[0][16][2] and data[0][15][2] > data[0][16][2]) :
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][17][2] > data[0][20][2] and data[0][19][2] > data[0][20][2]) :
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            
        return fingers
def foo():
    foo.counter += 1
foo.counter = 0
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX

def main():
    cap = cv.VideoCapture(0)
    detector = FaceMeshDetector(maxFaces=3)
    current_time = 0
    previous_time= 0
    hand_detector = handLandmarkDetector()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret,image = cap.read()
            image = cv.flip(image,1)
            image = cv.resize(image,(800,600))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image, faces = detector.findFaceMesh(image, draw=False)
            image.flags.writeable = False
      
        # Make detection
            results = pose.process(image)
    
        # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
                lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate angle
                angle1 = calculate_angle(lshoulder, lelbow, lwrist)
                angle2 = calculate_angle(rshoulder, relbow, rwrist)
            
            # Visualize angle
                cv2.putText(image, str(angle1), 
                               tuple(np.multiply(lelbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                cv2.putText(image, str(angle2), 
                               tuple(np.multiply(relbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                       
            except:
                pass
        
        
        # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )
            if faces:
                face = faces[0]
                pointLeft = face[145]
                pointRight = face[374]
                w, _ = detector.findDistance(pointLeft, pointRight)
                W = 6.3
                f = 840
                d = (W * f) / w
                cvzone.putTextRect(image, f'Depth: {int(d)}cm',
                                   (face[10][0] - 100, face[10][1] - 50),
                                   scale=2)
                if d <= 60 and d > 50:
                    cv2.putText(image,"You are coming too close", (50, 450), fonts, 1, (RED), 2)
                    winsound.Beep(500,200)
                elif (d <= 50):
                    cv2.putText(image,"calling cops", (50, 450), fonts, 1, (RED), 2)
                    # sound.play()
                    file = 'C:/Users/nikit/Desktop/AI CAMERA/images/img'+str(random.random())+'.jpg'
                    cv2.imwrite(file, image)
                    send_msg(" Someone breaking camera at shop 27, near kamraj road, coimbatore\n lat/long"+listToString(g.latlng))
            landmarks,image = hand_detector.detect_landmarks(image,draw_default_style=False)

            fingers=hand_detector.count_up_fingers(landmarks)
            fingers_up = int(fingers[0].count(1)) + int(fingers[1].count(1))
            if fingers_up == 10:
                if angle1 >= 30 and angle1 <= 100 and angle2 >= 30 and angle2 <= 100:
                    cv.putText(image,"Suspicion detected!!!",(50,400),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    foo() 
                    if foo.counter >= 15:
                        cv.putText(image,f"Speak now !!! {25-foo.counter}",(50,100),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                        cv.putText(image,f"Pausing the video...",(50,150),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    if foo.counter == 25:
                        foo.counter = 0
                        with sr.Microphone() as source:
                            print("Speak Anything :")
                            audio = r.listen(source)
                            try:
                                text = r.recognize_google(audio)
                                print("You said : {}".format(text))
                                if text == "don't kill me" or text == "help me":
                                    send_msg("burglary at shop 27, near kamraj road, coimbatore\n lat/long"+listToString(g.latlng))
                                    sound.play()
                                else:
                                    print("not a threat")
                            except:
                                print("Sorry could not recognize what you said")

            # cv.rectangle(image,(10,10),(350,210),(0,255,0),-1)
            # cv.putText(image,str(fingers_up),(30,190),cv.FONT_HERSHEY_SIMPLEX,8,(0,0,255),10)
            cv.imshow("Window",image)
            key=cv.waitKey(1)
            if key==ord('q'):
                break
        cv.destroyAllWindows()



if __name__ == '__main__':
     main()