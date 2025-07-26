import numpy as np
from ..base import ImageAugmentationStrategy
from typing import List, Tuple
import logging
class BitDepthReductionAugmentation(ImageAugmentationStrategy):
    def __init__(self, bit_depth: int = 4, prob: float = 1.0):
        self.bit_depth = bit_depth
        self.prob = 1.0

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        #if np.random.rand() < self.prob:
        logging.debug(f"bit depth original bounding boxes: {bboxes}")
        factor = 2 ** (8 - self.bit_depth)
        image = (image // factor * factor).astype(np.uint8)
        logging.debug(f"Bit depth reduced to {self.bit_depth} bits per channel")
        return image, image.shape[0], image.shape[1], bboxes
