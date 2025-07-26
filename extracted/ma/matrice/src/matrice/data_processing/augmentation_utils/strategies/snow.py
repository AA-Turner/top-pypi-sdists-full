import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class SnowAugmentation(ImageAugmentationStrategy):
    def __init__(self, brightness_coeff=2.5,
                snow_point_range=[0.1, 0.3],
                method="bleach",
                prob: float = 1.0):
        self.transform = A.Compose([
            A.RandomSnow(brightness_coeff=brightness_coeff, snow_point_range=snow_point_range, method=method, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))
    
    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Snow applied")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
