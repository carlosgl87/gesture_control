import pyautogui
import math
import cv2
from pynput.keyboard import Key, Controller

keyboard = Controller()

# Method to detect if the index finger is at the top or bottom of the screen and then for scrolling
def scroll(index_finger_location):
    x, y = index_finger_location
    text = None
    if y > 0.9:
        pyautogui.scroll(-10)
        text = "Scrolling Down"
    if y < 0.1:
        pyautogui.scroll(10)
        text = "Scrolling Up"

    return text

# Method for action 2
def zoom(img, last_length, thumb, index):

    x1, y1 = thumb
    x2, y2 = index
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
    cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

    length = math.hypot(x2 - x1, y2 - y1)
    # print(length)

    if last_length:
        if length > last_length and abs(length-last_length) > 5:
            # Pressing Ctrl +
            # keyboard.press(Key.ctrl.value) #this would be for windows
            keyboard.press(Key.cmd.value)
            keyboard.press('+')
            keyboard.release('+')
            # keyboard.release(Key.ctrl.value) #this would be for windows
            keyboard.release(Key.cmd.value)

            print("Zoom In")

        elif length < last_length and abs(length-last_length) > 5:
            # Pressing Ctrl -
            keyboard.press(Key.ctrl.value) #this would be for windows
            keyboard.press('-')
            keyboard.release('-')
            keyboard.release(Key.ctrl.value) #this would be for windows

    last_length = length

    # print(int(length), angle)

    if length < 50:
        cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    return img, last_length

