from threading import Thread
from time import sleep
from PIL import Image, ImageGrab
from googletrans import Translator
import pytesseract
from colorama import Fore
import cv2
import numpy as np
import re
import keyboard

custom_conf = "--psm 11 --oem 1"
translator = Translator()
sharpening_kernel = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
], dtype=np.float32)
preset = 1


def tr(image):
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
    result = pytesseract.image_to_string(image, config=custom_conf, output_type='string')
    result = re.sub("\n", " - ", result, count=1)
    result = re.sub("\n", " ", result)
    result = result.replace('|', 'I')
    print(Fore.RED + '--en--')
    print(Fore.RED + result)
    translate = translator.translate(result, dest='ru')
    print(Fore.GREEN + '--ru--')
    print(Fore.GREEN + translate.text)


def tr_phone(image, image_phone):
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
    result = pytesseract.image_to_string(image_phone, config=custom_conf, output_type='string')
    result = re.sub("\n", " - ", result, count=1)
    result = re.sub("\n", " ", result)
    result = result.replace('|', 'I')
    print(Fore.RED + '--en--')
    print(Fore.RED + result)
    translate = translator.translate(result, dest='ru')
    print(Fore.GREEN + '--ru--')
    print(Fore.GREEN + translate.text)
    result = pytesseract.image_to_string(image, config=custom_conf, output_type='string')
    result = re.sub("\n", " - ", result, count=1)
    result = re.sub("\n", " ", result)
    result = result.replace('|', 'I')
    print(Fore.RED + '--en--')
    print(Fore.RED + result)
    translate = translator.translate(result, dest='ru')
    print(Fore.GREEN + '--ru--')
    print(Fore.GREEN + translate.text)


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
            image.save('subs.png', 'png')
            preprocessing()


def preprocessing():
    image = cv2.imread('subs.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    cv2.imwrite('image.png', image)
    tr(image)


def preprocessing_phone():
    image = cv2.imread('subs.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image = cv2.medianBlur(image, 3)
    image = cv2.filter2D(image, -1, sharpening_kernel)
    # cv2.imwrite('image.png', image)
    image_phone = cv2.imread('phone.png')
    gray = cv2.cvtColor(image_phone, cv2.COLOR_BGR2GRAY)
    _, image_phone = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image_phone = cv2.medianBlur(image_phone, 3)
    image_phone = cv2.filter2D(image_phone, -1, sharpening_kernel)
    cv2.imwrite('imagephone.png', image_phone)
    tr_phone(image, image_phone)


def switch_case_dialog():
    global preset
    preset = 1
    print(Fore.YELLOW + 'preset - dialog')


def switch_case_phone_dialog():
    global preset
    preset = 2
    print(Fore.YELLOW + 'preset - phone dialog')


def switch_case_cutscene():
    global preset
    preset = 3
    print(Fore.YELLOW + 'preset - cutscene')


dialog_key = 'z'
phone_dialog_key = 'x'
cutscene_key = 'c'
keyboard.add_hotkey(dialog_key, switch_case_dialog)
keyboard.add_hotkey(phone_dialog_key, switch_case_phone_dialog)
keyboard.add_hotkey(cutscene_key, switch_case_cutscene)


def screen_push():
    last_clipboard_image = ImageGrab.grabclipboard()
    while True:
        clipboard_image = ImageGrab.grabclipboard()
        if clipboard_image is not None and clipboard_image != last_clipboard_image:
            crop(clipboard_image)
            last_clipboard_image = clipboard_image
        sleep(1)


thread = Thread(target=screen_push)
thread.start()
thread.join()
