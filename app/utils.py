import cv2
import numpy as np

def adjust_brightness_contrast(image, brightness, contrast):
    """
    Adjusts brightness and contrast of the image.
    brightness: float, -100..100
    contrast: float, 0.0..3.0
    """
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

def image_to_bytes(image):
    """
    Converts OpenCV image to PNG bytes for response.
    """
    _, buffer = cv2.imencode(".png", image)
    return buffer.tobytes()