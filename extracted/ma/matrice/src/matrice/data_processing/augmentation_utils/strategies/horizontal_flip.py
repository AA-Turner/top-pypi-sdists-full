import numpy as np
import albumentations as A
from ..base import ImageAugmentationStrategy
from typing import List, Tuple
import logging
class HorizontalFlipAugmentation(ImageAugmentationStrategy):
    def __init__(self, prob: float = 1.0):
        self.prob = prob
        self.transform = A.Compose([
            A.HorizontalFlip(p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        # if np.random.rand() < self.prob:
        class_labels = [0] * len(bboxes)
        transformed = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        image = transformed['image']
        bboxes = transformed['bboxes']
        logging.debug(f"Horizontal flip original bounding boxes: {bboxes}")
        return image, image.shape[0], image.shape[1], bboxes
