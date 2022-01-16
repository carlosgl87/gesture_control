# Script containing methods to be used in the main script

# Importing libraries
import math

# Method to detect the fist action
def detect_gestures(landmarkList):
    # Initializing the gesture
    recognized_hand_gesture = None

    #finger states
    thumbIsOpen = False
    firstFingerIsOpen = False
    secondFingerIsOpen = False
    thirdFingerIsOpen = False
    fourthFingerIsOpen = False

    # Find the MCP landmark of each finger and detect if the upper landmarks are below than this point.
    # If yes, then the finger is closed
    # if no, the finger is open.

    pseudoFixKeyPoint = landmarkList.landmark[2].x
    # print(pseudoFixKeyPoint)
    if (landmarkList.landmark[3].x < pseudoFixKeyPoint and landmarkList.landmark[4].x < pseudoFixKeyPoint):
        thumbIsOpen = True

    pseudoFixKeyPoint = landmarkList.landmark[6].y
    if (landmarkList.landmark[7].y < pseudoFixKeyPoint and landmarkList.landmark[8].y < pseudoFixKeyPoint):
        firstFingerIsOpen = True

    pseudoFixKeyPoint = landmarkList.landmark[10].y
    if (landmarkList.landmark[11].y < pseudoFixKeyPoint and landmarkList.landmark[12].y < pseudoFixKeyPoint):
        secondFingerIsOpen = True

    pseudoFixKeyPoint = landmarkList.landmark[14].y
    if (landmarkList.landmark[15].y < pseudoFixKeyPoint and landmarkList.landmark[16].y < pseudoFixKeyPoint):
        thirdFingerIsOpen = True

    pseudoFixKeyPoint = landmarkList.landmark[18].y
    if (landmarkList.landmark[19].y < pseudoFixKeyPoint and landmarkList.landmark[20].y < pseudoFixKeyPoint):
        fourthFingerIsOpen = True

#####-----------------***************************************************************************------------------#####
    # Detection of 1 finger hand symbol
    if ((firstFingerIsOpen) and not (secondFingerIsOpen) and not (thirdFingerIsOpen) and not (fourthFingerIsOpen)):
        recognized_hand_gesture = "ACTION 1"
#####-----------------***************************************************************************------------------#####
    # Detection of 2 finger hand symbol
    if ((firstFingerIsOpen) and (secondFingerIsOpen) and not (thirdFingerIsOpen) and not (fourthFingerIsOpen)):
        recognized_hand_gesture = "ACTION 2"
#####-----------------***************************************************************************------------------#####
    # Detection of closed hand symbol
    if (not(firstFingerIsOpen) and not(secondFingerIsOpen) and not(thirdFingerIsOpen) and not(fourthFingerIsOpen)):
        recognized_hand_gesture = "ACTION 3 - CLOSE"
#####-----------------***************************************************************************------------------#####
    # Detection of open hand symbol
    if ((firstFingerIsOpen) and (secondFingerIsOpen) and (thirdFingerIsOpen) and (fourthFingerIsOpen)):
        recognized_hand_gesture = "ACTION 3 - OPEN"
#####-----------------***************************************************************************----------------#####
    return recognized_hand_gesture
#####----------------------------------------- END OF METHOD -------------------------------------#####