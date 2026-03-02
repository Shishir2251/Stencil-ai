import cv2
import numpy as np

def outline_style(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,100, 200)
    return edges

def pencil_style(image):
    gray, sketch = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07,shade_factor=0.05)
    return sketch

def shadow_style(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,120,125,255)
    return thresh

def Bold_system(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    kernel = np.ones((3,3), np.uint8)
    bold = cv2.dilate(edges, kernel, iterations=2)
    return bold