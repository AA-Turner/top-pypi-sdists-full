import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class BrightnessContrastAugmentation(ImageAugmentationStrategy):
    def __init__(self, prob: float = 1.0, brightness_limit=[-0.2, 0.2], contrast_limit=[-0.2, 0.2], brightness_by_max=True, ensure_safe_range=False):
        self.prob = prob
        self.transform = A.Compose([
            A.RandomBrightnessContrast(
                brightness_limit=brightness_limit,
                contrast_limit=contrast_limit,
                brightness_by_max=brightness_by_max,
                ensure_safe_range=ensure_safe_range,
                p=1.0
            )
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        #if np.random.rand() < self.prob:
        logging.debug(f"brightness contrast original bounding boxes: {bboxes}")
        class_labels = [0] * len(bboxes)
        transformed = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        image = transformed['image']
        bboxes = transformed['bboxes']
        logging.debug(f"Brightness and contrast applied with limits")
        return image, image.shape[0], image.shape[1], bboxes
