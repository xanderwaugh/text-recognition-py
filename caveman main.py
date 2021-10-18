import numpy as np, cv2
from thrd_stream import Threaded_Webcam
import pytesseract
from pytesseract import Output
from datetime import datetime as dt

TESS_CONFIG = "--psm 3 -l eng"

def ocr(img):
    data = pytesseract.image_to_data(image=img, lang='eng', config=TESS_CONFIG, output_type=Output.DICT)
    return data

def get_boxes(data: dict, frame : np.ndarray, conf : float):
    idx = 0
    for x in data['conf']:
        if float(x) >= conf:
            x1 = int(data['left'][idx])
            y1 = int(data['top'][idx])
            x2 = int(data['left'][idx] + data['width'][idx])
            y2 = int(data['top'][idx] + data['height'][idx])

            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
            #frame = cv2.putText(frame, data['text'][idx], (x1, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            print(f"{data['text'][idx]},",end='')
        idx+=1
    return frame

def apex_crop(frame : np.ndarray):
    frame = frame[220:400, 0:400]
    return frame

counter = 1
stream = Threaded_Webcam(src=1).start()
CONFIDENCE = 90

while True:
    start_time = dt.now()
    frame = stream.read()

    # Is it apex/cod/warzone/ps4 main menu?
    frame = apex_crop(frame)

    
    result_ocr_data = ocr(frame)
    frame = get_boxes(result_ocr_data, frame, CONFIDENCE)

    cv2.imshow("window", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    
    print(f"\nFrame #{counter}--Took: {str(dt.now() - start_time)[6:]}")
    counter+=1

cv2.destroyAllWindows()
stream.stop()