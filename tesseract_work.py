import cv2, pytesseract, pyautogui
from pytesseract import Output
import numpy as np, time
from datetime import datetime as dt

SCALE_FACTOR = 1
tesseract_config = r"--psm 3 --oem 1"

images = []
time.sleep(4)

iteration = 1
while True:
    start_t = dt.now()
    screen_grab = np.array(pyautogui.screenshot()) # Grab Screen
    img = cv2.cvtColor(screen_grab, cv2.COLOR_RGB2BGR) # Convert screen_grab to cv2 image
    img = cv2.resize(img, (int(img.shape[1]*SCALE_FACTOR), int(img.shape[0]*SCALE_FACTOR))) # Rescale for performance

    data = pytesseract.image_to_data(img, output_type=Output.DICT)

    for i in range(len(data['text'])):
        if float(data['conf'][i]) > 60: # confidence higher than 60%
            x, y, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            img = cv2.rectangle(img, (x,y), (x+width, y+height), (0, 255, 255))
            img = cv2.putText(img, data['text'][i], (x, y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    images.append(img)

    print(f"Run #{iteration}, took {dt.now() - start_t}")
    cv2.imshow('Text Recognition', img)
    cv2.waitKey(delay=1)

    iteration+=1

