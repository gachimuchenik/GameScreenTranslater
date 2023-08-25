from threading import Thread
from time import sleep
from googletrans import Translator
import pytesseract
from colorama import Fore
import cv2
import numpy as np
import re
import keyboard
import pyautogui
from PIL import Image, ImageGrab

#
# def screen_push():
#     last_clipboard_image = ImageGrab.grabclipboard()
#     while True:
#         clipboard_image = ImageGrab.grabclipboard()
#         if clipboard_image is not None and clipboard_image != last_clipboard_image:
#             crop(clipboard_image)
#             last_clipboard_image = clipboard_image
#         sleep(1)
#
#
#
# def autogui():
#     while True:
#         screen = pyautogui.screenshot()
#         screen.save('screen.png', 'png')
#         crop(screen)
#         sleep(1)


def main():
    block_number = 1
    last_clipboard_image = ImageGrab.grabclipboard()
    while True:
        if block_number == 1:
            while True:
                screen = pyautogui.screenshot()
                screen.save('screen.png', 'png')
                print('auto')
                sleep(1)
                if keyboard.is_pressed('f'):
                    break
        elif block_number == 2:
            while True:
                clipboard_image = ImageGrab.grabclipboard()
                if clipboard_image is not None and clipboard_image != last_clipboard_image:
                    last_clipboard_image = clipboard_image
                    clipboard_image.save('clip.png', 'png')
                    print('clip')
                sleep(1)
                if keyboard.is_pressed('f'):
                    break
        block_number = 1 if block_number == 2 else 2
        print('swap')


thread = Thread(target=main)
thread.start()
thread.join()

