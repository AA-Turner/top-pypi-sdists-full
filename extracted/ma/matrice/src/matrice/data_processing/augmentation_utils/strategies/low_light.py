import numpy as np
from ..base import ImageAugmentationStrategy
from typing import List, Tuple
import logging
class LowLightSimulationAugmentation(ImageAugmentationStrategy):
    def __init__(self, brightness_factor=0.3, prob: float = 1.0):
        self.brightness_factor = brightness_factor
        self.prob = 1.0

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        #if np.random.rand() < self.prob:
        image = (image * self.brightness_factor).astype(np.uint8)
        logging.debug(f"Low light simulation applied with brightness factor: {self.brightness_factor}")
        return image, image.shape[0], image.shape[1], bboxes
