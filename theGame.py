import cv2 as cv
import mediapipe as mp
import random
import pygame

#haarcascade= 'haarcascade_frontalface_default.xml' # read xml file

mp_drawing= mp.solutions.drawing_utils
mp_drawing_styles= mp.solutions.drawing_styles
mp_hands= mp.solutions.hands

gestures=['rock','paper','scissors']

pygame.mixer.init()
win_music=pygame.mixer.Sound('rock-paper-scissors game\game_won.wav')
lose_music=pygame.mixer.Sound('rock-paper-scissors game\game_lost.wav')

def getGesture(hand_landmarks):
   landmarks= hand_landmarks.landmark

   if all([landmarks[i].y<landmarks[i+3].y for i in range(9,20,4)]):
      return 'rock'
   elif landmarks[13].y< landmarks[16].y and landmarks[17].y<landmarks[20].y and landmarks[5].y>landmarks[8].y and landmarks[9].y > landmarks[12].y:
      return 'scissors'
   elif all([landmarks[i+3].y < landmarks[i].y for i in range(1,20,4)]):
      return 'paper'
   else:
      return 'Invalid Gesture'

cap= cv.VideoCapture(0)

with mp_hands.Hands(model_complexity=0,min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

   player_gesture=""
   computer_gesture=""
   result=""
   playerScore=0
   computerScore=0
   match=""
   gameOver=False

   while True:
      success, frame= cap.read()
      if not success:
         break
      
      frame= cv.cvtColor(frame,cv.COLOR_BGR2RGB) #changes the frame from one bgr to rgb color format
      results= hands.process(frame) # this variable figures out where our hands are currently in the frame
      frame=cv.cvtColor(frame,cv.COLOR_RGB2BGR) # again revert back to it's original form

      #add landmarks to the hand
      if results.multi_hand_landmarks: # checks if results variable is not null
         for hand_landmarks in results.multi_hand_landmarks: # hand_landmarks is an array consisting of pose of hand
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())

      frame= cv.flip(frame,1)

      if result=='You Win!':
         color=(0,255,0)
      elif result=='Computer Wins!':
         color=(0,0,255)
      else:
         color=(255,255,255)

      if gameOver:
         cv.putText(frame,f"{match}",(100,200),cv.FONT_HERSHEY_TRIPLEX,1,(255,215,0),2,cv.LINE_AA)
         if cv.waitKey(1) & 0xFF == ord('q'):
               break

      cv.putText(frame,f"User-gesture: {player_gesture}",(20,50),cv.FONT_HERSHEY_DUPLEX,1,(0,255,255),2,cv.LINE_AA)
      cv.putText(frame,f"Computer-gesture: {computer_gesture}",(20,80),cv.FONT_HERSHEY_DUPLEX,1,(0,255,255),2,cv.LINE_AA)
      cv.putText(frame,f"Result: {result}",(20,110),cv.FONT_HERSHEY_DUPLEX,1,color,2,cv.LINE_AA)
      cv.putText(frame,f"Your Score: {playerScore}",(300,420),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2,cv.LINE_AA)
      cv.putText(frame,f"Computer Score: {computerScore}",(300,450),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2,cv.LINE_AA)
      cv.imshow("Rock-Paper-Scissors",frame)

      key= cv.waitKey(1) & 0xff
      if key==ord('q'):
         break
      elif key==ord('p') and results.multi_hand_landmarks:
         player_gesture=getGesture(hand_landmarks=results.multi_hand_landmarks[0])
         computer_gesture=random.choice(gestures)
         if player_gesture==computer_gesture:
            result="It is a Tie!"
         elif player_gesture=='Invalid Gesture':
            result="Invalid Gesture"
         elif (player_gesture=='rock' and computer_gesture=='scissors') or (player_gesture=='paper' and computer_gesture=='rock') or (player_gesture=='scissors' and computer_gesture=='paper'):
            result="You Win!"
            playerScore+=1
            win_music.play()
            if(playerScore==5):
               match="You won the match!"
               gameOver=True
         else:
            result="Computer Wins!"
            computerScore+=1
            lose_music.play()
            if(computerScore==5):
               match="Computer won the match!"
               gameOver=True

cap.release()
cv.destroyAllWindows()
