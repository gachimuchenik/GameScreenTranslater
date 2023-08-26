from threading import Thread
from time import sleep
from PIL import ImageGrab
from googletrans import Translator
import pytesseract
from colorama import Fore
import cv2
import numpy as np
import re
import keyboard
import pyautogui

custom_conf = "--psm 11 --oem 1"
translator = Translator()
sharpening_kernel = np.array([
    [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1]
], dtype=np.float32)
preset = 1
last_result = None
last_phone = None


def tr(image):
    global last_result
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
    result = pytesseract.image_to_string(image, config=custom_conf, output_type='string')
    if result != last_result:
        try:
            text = re.sub("\n", " - ", result, count=1)
            text = re.sub("\n", " ", text)
            text = text.replace('|', 'I')
            print(Fore.RED + '--en--')
            print(Fore.RED + text)
            translate = translator.translate(text, dest='ru')
            print(Fore.GREEN + '--ru--')
            print(Fore.GREEN + translate.text)
            last_result = result
        except:
            pass


def tr_phone(image, image_phone):
    global last_result
    global last_phone
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
    phone = pytesseract.image_to_string(image_phone, config=custom_conf, output_type='string')
    if phone != last_phone:
        try:
            ptext = re.sub("\n", " - ", phone, count=1)
            ptext = re.sub("\n", " ", ptext)
            ptext = ptext.replace('|', 'I')
            print(Fore.CYAN + 'Phone')
            print(Fore.RED + '--en--')
            print(Fore.RED + ptext)
            translate = translator.translate(ptext, dest='ru')
            print(Fore.GREEN + '--ru--')
            print(Fore.GREEN + translate.text)
            last_phone = phone
        except:
            pass
    result = pytesseract.image_to_string(image, config=custom_conf, output_type='string')
    if result != last_result:
        try:
            text = re.sub("\n", " - ", result, count=1)
            text = re.sub("\n", " ", text)
            text = text.replace('|', 'I')
            print(Fore.CYAN + 'Kiruy')
            print(Fore.RED + '--en--')
            print(Fore.RED + text)
            translate = translator.translate(text, dest='ru')
            print(Fore.GREEN + '--ru--')
            print(Fore.GREEN + translate.text)
            last_result = result
        except:
            pass


def tr_cut_mess(image):
    global last_result
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
    result = pytesseract.image_to_string(image, config=custom_conf, output_type='string')
    if result != last_result:
        try:
            text = re.sub("\n", " ", result)
            text = text.replace('|', 'I')
            print(Fore.RED + '--en--')
            print(Fore.RED + text)
            translate = translator.translate(text, dest='ru')
            print(Fore.GREEN + '--ru--')
            print(Fore.GREEN + translate.text)
            last_result = result
        except:
            pass


def crop(image):
    match preset:
        case 1:
            crop_sub = image[765:1000, 450:1480]
            preprocessing(crop_sub)
        case 2:
            crop_phone = image[100:260, 500:1500]
            crop_sub = image[765:1000, 450:1480]
            preprocessing_phone(crop_sub, crop_phone)
        case 3:
            crop_cut = image[880:1050, 440:1480]
            preprocessing_cutscene(crop_cut)
        case 4:
            mess_crop = image[400:875, 630:1320]
            preprocessing_message(mess_crop)


def preprocessing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    tr(image)


def preprocessing_phone(image, image_phone):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    gray = cv2.cvtColor(image_phone, cv2.COLOR_BGR2GRAY)
    _, image_phone = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image_phone = cv2.medianBlur(image_phone, 3)
    image_phone = cv2.filter2D(image_phone, -1, sharpening_kernel)
    tr_phone(image, image_phone)


def preprocessing_cutscene(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([230, 230, 230])
    upper_white = np.array([255, 255, 255])
    mask = cv2.inRange(image, lower_white, upper_white)
    image = cv2.bitwise_and(image, image, mask=mask)
    image[np.where((image == [0, 0, 0]).all(axis=2))] = [0, 0, 0]
    image = cv2.bitwise_not(image)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    tr_cut_mess(image)

def preprocessing_message(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    tr_cut_mess(image)


def main():
    global preset
    block_number = 1
    last_clipboard_image = ImageGrab.grabclipboard()
    while True:
        if block_number == 'auto':
            while True:
                screen = pyautogui.screenshot()
                screen = np.array(screen)
                crop(screen)
                sleep(0.5)
                if keyboard.is_pressed('f'):
                    break
                if keyboard.is_pressed('z'):
                    preset = 1
                    print(Fore.YELLOW + 'preset - dialog')
                if keyboard.is_pressed('x'):
                    preset = 2
                    print(Fore.YELLOW + 'preset - phone dialog')
                if keyboard.is_pressed('c'):
                    preset = 3
                    print(Fore.YELLOW + 'preset - cutscene')
                if keyboard.is_pressed('v'):
                    preset = 4
                    print(Fore.YELLOW + 'preset - message')
        elif block_number == 'screen':
            while True:
                clipboard_image = ImageGrab.grabclipboard()
                if clipboard_image is not None and clipboard_image != last_clipboard_image:
                    screen = np.array(clipboard_image)
                    crop(screen)
                    last_clipboard_image = clipboard_image
                sleep(0.5)
                if keyboard.is_pressed('f'):
                    break
                if keyboard.is_pressed('z'):
                    preset = 1
                    print(Fore.YELLOW + 'preset - dialog')
                if keyboard.is_pressed('x'):
                    preset = 2
                    print(Fore.YELLOW + 'preset - phone dialog')
                if keyboard.is_pressed('c'):
                    preset = 3
                    print(Fore.YELLOW + 'preset - cutscene')
                if keyboard.is_pressed('v'):
                    preset = 4
                    print(Fore.YELLOW + 'preset - message')
        block_number = 'auto' if block_number == 'screen' else 'screen'
        print(Fore.YELLOW + block_number)


thread = Thread(target=main)
thread.start()
thread.join()
