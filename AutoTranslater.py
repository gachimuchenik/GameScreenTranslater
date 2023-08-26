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
x1, y1, x2, y2 = (450, 765, 1480, 1000)
px1, py1, px2, py2 = (450, 765, 1480, 1000)


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


def tr_cut(cut):
    global last_result
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
    result = pytesseract.image_to_string(cut, config=custom_conf, output_type='string')
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
            image = image.crop((450, 765, 1480, 1000))
            image.save('subs.png', 'png')
            preprocessing()
        case 2:
            image_phone = image
            image_phone = image_phone.crop((500, 100, 1500, 260))
            image_phone.save('phone.png', 'png')
            image = image.crop((450, 765, 1480, 1000))
            image.save('subs.png', 'png')
            preprocessing_phone()
        case 3:
            image = image.crop((440, 880, 1480, 1050))
            image.save('cut.png', 'png')
            preprocessing_cutscene()


def preprocessing():
    image = cv2.imread('subs.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    # cv2.imwrite('image.png', image)
    tr(image)


def preprocessing_phone():
    image = cv2.imread('subs.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    image_phone = cv2.imread('phone.png')
    gray = cv2.cvtColor(image_phone, cv2.COLOR_BGR2GRAY)
    _, image_phone = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image_phone = cv2.medianBlur(image_phone, 3)
    image_phone = cv2.filter2D(image_phone, -1, sharpening_kernel)
    # cv2.imwrite('image.png', image)
    # cv2.imwrite('imagephone.png', image_phone)
    tr_phone(image, image_phone)


def preprocessing_cutscene():
    image = cv2.imread('cut.png')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([230, 230, 230])
    upper_white = np.array([255, 255, 255])
    mask = cv2.inRange(image, lower_white, upper_white)
    result = cv2.bitwise_and(image, image, mask=mask)
    result[np.where((result == [0, 0, 0]).all(axis=2))] = [0, 0, 0]
    result = cv2.bitwise_not(result)
    result = cv2.medianBlur(result, 3)
    result = cv2.filter2D(result, -1, sharpening_kernel)
    # cv2.imwrite('test.png', result)
    tr_cut(result)


# def switch_case_dialog():
#     global preset
#     preset = 1
#     print(Fore.YELLOW + 'preset - dialog')
#
#
# def switch_case_phone_dialog():
#     global preset
#     preset = 2
#     print(Fore.YELLOW + 'preset - phone dialog')
#
#
# def switch_case_cutscene():
#     global preset
#     preset = 3
#     print(Fore.YELLOW + 'preset - cutscene')
#
#
# dialog_key = 'z'
# phone_dialog_key = 'x'
# cutscene_key = 'c'
# keyboard.add_hotkey(dialog_key, switch_case_dialog)
# keyboard.add_hotkey(phone_dialog_key, switch_case_phone_dialog)
# keyboard.add_hotkey(cutscene_key, switch_case_cutscene)


def main():
    global preset
    block_number = 1
    last_clipboard_image = ImageGrab.grabclipboard()
    while True:
        if block_number == 'auto':
            while True:
                screen = pyautogui.screenshot()
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
        elif block_number == 'screen':
            while True:
                clipboard_image = ImageGrab.grabclipboard()
                if clipboard_image is not None and clipboard_image != last_clipboard_image:
                    crop(clipboard_image)
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
        block_number = 'auto' if block_number == 'screen' else 'screen'
        print(Fore.YELLOW + block_number)


thread = Thread(target=main)
thread.start()
thread.join()
