import numpy as np
from ..base import ImageAugmentationStrategy
from typing import List, Tuple
import logging
class SpeckleNoiseAugmentation(ImageAugmentationStrategy):
    def __init__(self, prob: float = 1.0, mean: float = 0.0, var: float = 0.01):
        self.prob = prob
        self.mean = mean
        self.var = var

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        #if np.random.rand() < self.prob:
        row, col, ch = image.shape
        gauss = np.random.normal(self.mean, self.var ** 0.5, (row, col, ch))
        noisy = image + image * gauss
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        image = noisy
        logging.debug(f"Speckle noise applied with mean")
        return image, image.shape[0], image.shape[1], bboxes
