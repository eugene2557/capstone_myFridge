import RPi.GPIO as GPIO
import time
import cv2
import os.path

from yolov5 import detect
from src import send

key = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(key, GPIO.IN)

PATH1 = "./images"
PATH2 = "./yolov5"
PATH3 = "./images/images2/labels"
prev_input = 0
i = 0
t = 0

try:
    while True:
        input = GPIO.input(key)
        if prev_input == 0 and input == 1:
            print('* door closed')
            camera = cv2.VideoCapture(0)
            ret, image = camera.read()
            cv2.imwrite(os.path.join(PATH1, 'images1/yolo' + str(i)) + '.png', image)
            time.sleep(1)

            # image processing
            detect.run(
                weights=os.path.join(PATH2, 'best_v2.pt'), 
                source=os.path.join(PATH1, 'images1/yolo' + str(i) + '.png'),
                # imgsz=(640, 640)
                save_txt=True,
                project=os.path.join(PATH1),
                name='images2',
                num=t
            )

            if not os.path.isfile(os.path.join(PATH3, (f'yolo{i}.txt'))):
                f = open(os.path.join(PATH3, ('yolo' + str(i) + '.txt')), 'w')
                f.write(f'{t} -1 \n')
                f.close()

            print('* detection finished')

            send.sk_client(i, t)
            print('* socket finished')
            camera.release()

            i += 1
            t += 1
            if i == 5:
                if os.path.exists(PATH3):
                    for file in os.scandir(PATH3):
                        if os.path.isdir(file):
                            continue
                        os.remove(file.path)
                    print('* remove labels')
                i = 0

        prev_input = input
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()