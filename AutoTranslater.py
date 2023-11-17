import pyautogui
from PIL import ImageGrab
from googletrans import Translator
import pytesseract
import cv2
import numpy as np
import re
import keyboard
import textwrap
import tkinter as tk

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
limit = 140
block_number = 'screen'
exit_flag = False

root = tk.Tk()
root.title("Translator")
root.configure(bg='black')
root.geometry("1200x800")
label_list = []
custom_font = ('Arial', 12)
canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas, bg='black')
canvas.create_window((0, 0), window=frame, anchor='nw', width=1200, height=800)

listbox = tk.Listbox(frame, bg='black', fg='white', font=custom_font, selectbackground='black',
                     selectforeground='white')
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


def custom_print(text, color):
    listbox.insert(tk.END, text)
    listbox.itemconfig(tk.END, {'fg': color})
    listbox.see(tk.END)


def on_close():
    global exit_flag
    exit_flag = True
    root.destroy()


def tr(image):
    global last_result
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
    result = pytesseract.image_to_string(image, config=custom_conf, output_type='string')
    if result != last_result:
        try:
            text = re.sub("\n", " - ", result, count=1)
            text = re.sub("\n", " ", text)
            text = text.replace('|', 'I')
            wr_text = textwrap.wrap(text, width=limit)
            custom_print('--en--', 'red')
            for line in wr_text:
                custom_print(line, 'white')
            translate = translator.translate(text, dest='ru')
            wr_translate = textwrap.wrap(translate.text, width=limit)
            custom_print('--ru--', 'green')
            for line in wr_translate:
                custom_print(line, 'white')
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
            wr_text = textwrap.wrap(ptext, width=limit)
            custom_print('Phone', 'cyan')
            custom_print('--en--', 'red')
            for line in wr_text:
                custom_print(line, 'white')
            translate = translator.translate(ptext, dest='ru')
            wr_translate = textwrap.wrap(translate.text, width=limit)
            custom_print('--ru--', 'green')
            for line in wr_translate:
                custom_print(line, 'white')
            last_phone = phone
        except:
            pass
    result = pytesseract.image_to_string(image, config=custom_conf, output_type='string')
    if result != last_result:
        try:
            text = re.sub("\n", " - ", result, count=1)
            text = re.sub("\n", " ", text)
            text = text.replace('|', 'I')
            wr_text = textwrap.wrap(text, width=limit)
            custom_print('Kiruy', 'cyan')
            custom_print('--en--', 'red')
            for line in wr_text:
                custom_print(line, 'white')
            translate = translator.translate(text, dest='ru')
            wr_translate = textwrap.wrap(translate.text, width=limit)
            custom_print('--ru--', 'green')
            for line in wr_translate:
                custom_print(line, 'white')
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
            wr_text = textwrap.wrap(text, width=limit)
            custom_print('--en--', 'red')
            for line in wr_text:
                custom_print(line, 'white')
            translate = translator.translate(text, dest='ru')
            wr_translate = textwrap.wrap(translate.text, width=limit)
            custom_print('--ru--', 'green')
            for line in wr_translate:
                custom_print(line, 'white')
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
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([180, 180, 210])
    upper_white = np.array([255, 255, 255])
    mask = cv2.inRange(image, lower_white, upper_white)
    image = cv2.bitwise_and(image, image, mask=mask)
    image[np.where((image == [0, 0, 0]).all(axis=2))] = [0, 0, 0]
    image = cv2.bitwise_not(image)
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


def process_clipboard():
    global block_number, last_clipboard_image
    clipboard_image = ImageGrab.grabclipboard()
    if clipboard_image is not None and clipboard_image != last_clipboard_image:
        screen = np.array(clipboard_image)
        crop(screen)
        last_clipboard_image = clipboard_image
    if block_number == 'screen' and not exit_flag:
        root.after(500, process_clipboard)
    else:
        root.after(500, auto_capture())


def auto_capture():
    screen = pyautogui.screenshot()
    screen = np.array(screen)
    crop(screen)
    if block_number == 'auto' and not exit_flag:
        root.after(500, auto_capture)
    else:
        root.after(500, process_clipboard())


def check_keyboard():
    global block_number, preset, exit_flag
    if keyboard.is_pressed('a'):
        block_number = 'auto'
        custom_print(block_number, 'yellow')
    if keyboard.is_pressed('s'):
        block_number = 'screen'
        custom_print(block_number, 'yellow')
    if keyboard.is_pressed('z'):
        preset = 1
        custom_print('preset - dialog', 'yellow')
    if keyboard.is_pressed('x'):
        preset = 2
        custom_print('preset - phone dialog', 'yellow')
    if keyboard.is_pressed('c'):
        preset = 3
        custom_print('preset - cutscene', 'yellow')
    if keyboard.is_pressed('v'):
        preset = 4
        custom_print('preset - message', 'yellow')
    if keyboard.is_pressed('q'):
        exit_flag = True
        root.destroy()
    if not exit_flag:
        root.after(100, check_keyboard)


last_clipboard_image = ImageGrab.grabclipboard()
root.protocol("WM_DELETE_WINDOW", on_close)
root.after(0, process_clipboard)
root.after(0, check_keyboard)
root.mainloop()
