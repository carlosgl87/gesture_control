# Importing Libraries and Custom functions from other scripts.
import cv2
import mediapipe as mp
from recognize_gestures import detect_gestures
from perform_actions import scroll, zoom
import pyautogui

# Initializing modules from Mediapipe library
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def magic_control(cap):

# Initializing variables to be used in the function
  last_length = 0
  pressed = False

# Setting the attributes for the detection of hands and face
  with mp_hands.Hands(
      min_detection_confidence=0.7,
      min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
      success, image = cap.read()  # Reading the frames from the input video stream
      if not success:
        print("Ignoring empty camera frame.")
        break

      # Flip the image horizontally and convert the BGR image to RGB.
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

      # To improve performance
      results = hands.process(image)
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      # Initialize the ACTION
      gesture = None  

      if results.multi_hand_landmarks:
        #  Detecting and passing the two hands seperately
        for hand_landmarks, hand_label in zip(results.multi_hand_landmarks, results.multi_handedness):
          hand = (hand_label.classification[0]).label  # Either Left or Right

          index_finger_location = [results.multi_hand_landmarks[0].landmark[8].x,
                                   results.multi_hand_landmarks[0].landmark[8].y]
          pointer_location = [int(image.shape[1] * index_finger_location[0]),
                              int(image.shape[0] * index_finger_location[1])]

# -------------------------------- Code for Action 1 ------------------------------------#
          if (hand == 'Left'):
            #print("Left Hand")
            gesture = detect_gestures(hand_landmarks)  # Detect the ACTION
            if (len(results.multi_hand_landmarks) > 1):
              if (gesture == 'ACTION 1'):

                scroll_direction = scroll(index_finger_location)
                cv2.circle(image, pointer_location, radius=10,color=(0,0,255), thickness=20) # Draw circle at index finger
                cv2.putText(image, scroll_direction, (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0, 255), 3)

# -------------------------------- Code for Action 2 ------------------------------------#

              elif (gesture == 'ACTION 2'):

                thumb_location = [results.multi_hand_landmarks[0].landmark[4].x,
                                         results.multi_hand_landmarks[0].landmark[4].y]

                # Converting to x,y coordinates of the image
                thumb_coordinates = (int(image.shape[1] * thumb_location[0]), int(image.shape[0] * thumb_location[1]))

                image, last_length = zoom(image, last_length, thumb_coordinates, pointer_location)

# -------------------------------- Code for Action 3 ------------------------------------#

              elif (gesture == 'ACTION 3 - OPEN'):
                pyautogui.moveTo(pointer_location[0], pointer_location[1])
                cv2.circle(image, pointer_location, radius=10, color=(255, 0, 0),
                           thickness=20)  # Draw circle at index finger
                if pressed == True:
                  pyautogui.mouseUp()
                  pressed = False

              elif (gesture == 'ACTION 3 - CLOSE'):
                if pressed == False:
                  pyautogui.mouseDown()
                  pressed = True
                pyautogui.moveTo(pointer_location[0], pointer_location[1])
                cv2.circle(image, pointer_location, radius=10, color=(255, 0, 0),
                           thickness=20)  # Draw circle at index finger

# --------------------------- Check for left hand first ----------------------------------- #
          else:
            gesture = "Specify action using left hand first!"

          # DRAWING THE GESTURES AND RESULTS ON THE FRAME
          mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.putText(image, gesture, (10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0, 255), 3)  # Display the action on the image

# --------------------------- Display the results ----------------------------------- #
      # Initializing the output window for displaying the result.
      cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
      cv2.resizeWindow('Output', 420, 240)
      cv2.imshow('Output', image)
      if cv2.waitKey(5) & 0xFF == 27:
        break #  End the script by pressing Escape key

######----------------------------------- END OF METHOD ----------------------------------############

# For webcam input:
cap = cv2.VideoCapture(0)
magic_control(cap) # pass the webcam input to the Method
cap.release()