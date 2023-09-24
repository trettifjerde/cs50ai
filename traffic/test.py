import os
import cv2

IMG_WIDTH = 30
IMG_HEIGHT = 30

path = os.getcwd()
img_name = "1.png"

img = cv2.imread(img_name)
res = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
print(len(res))
print(len(res[0]))
print(len(res[0][0]))