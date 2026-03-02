import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import namedtuple

ColorInfo = namedtuple('ColorInfo', ['name', 'rgb', 'lab'])

def rgb_to_lab(rgb: tuple) -> np.ndarray:
    rgb = np.array(rgb, dtype=np.uint8).reshape(1, 1, 3)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2Lab)
    return lab[0, 0]

def lab_distance(c1: np.ndarray, c2: np.ndarray) -> float:
    return np.linalg.norm(c1 - c2)

PALETTE_RGB = {
    "red": (255, 0, 0), "dark red": (139, 0, 0), "brick": (203, 65, 84),
    "maroon": (128, 0, 0), "pink": (255, 192, 203), "hot pink": (255, 105, 180),
    "peach": (255, 229, 180), "beige": (245, 245, 220), "light tan": (210, 180, 140),
    "tan": (198, 144, 96), "brown": (165, 42, 42), "light brown": (181, 101, 29),
    "chocolate": (123, 63, 0), "white": (255, 255, 255), "light gray": (211, 211, 211),
    "gray": (128, 128, 128), "dark gray": (64, 64, 64), "charcoal": (54, 69, 79),
    "black": (0, 0, 0), "yellow": (255, 255, 0), "gold": (255, 215, 0),
    "orange": (255, 165, 0), "dark orange": (255, 140, 0), "green": (0, 128, 0),
    "lime": (0, 255, 0), "olive": (128, 128, 0), "teal": (0, 128, 128),
    "cyan": (0, 255, 255), "sky blue": (135, 206, 235), "light blue": (173, 216, 230),
    "blue": (0, 0, 255), "navy": (0, 0, 128), "denim": (21, 96, 189),
    "purple": (128, 0, 128), "violet": (238, 130, 238), "magenta": (255, 0, 255)
}

PALETTE = [
    ColorInfo(name, rgb, rgb_to_lab(rgb)) for name, rgb in PALETTE_RGB.items()
]

def find_nearest_color(lab_color: np.ndarray):
    min_dist = float('inf')
    nearest_color = None
    for color in PALETTE:
        dist = lab_distance(lab_color, color.lab)
        if dist < min_dist:
            min_dist = dist
            nearest_color = color
    return nearest_color, min_dist

def extract_major_colors(image: np.ndarray, k: int = 3):
    if image is None or image.size == 0:
        return []

    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    pixels = lab_image.reshape(-1, 3)

    k = min(k, len(pixels))
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_

    counts = np.bincount(labels)
    total = pixels.shape[0]

    color_results = []
    for i, center_lab in enumerate(centers):
        nearest_color, dist = find_nearest_color(center_lab)
        coverage = counts[i] / total * 100
        confidence = max(0.0, 1 - dist / 40)
        if dist > 30 or coverage < 5:
            continue
        color_results.append((nearest_color.name, round(coverage, 2), round(confidence, 2)))

    color_results.sort(key=lambda x: x[1], reverse=True)
    return color_results