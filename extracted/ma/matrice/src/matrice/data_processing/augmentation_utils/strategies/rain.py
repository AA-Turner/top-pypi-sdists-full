import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class RainAugmentation(ImageAugmentationStrategy):
    def __init__(self, slant_range=[-15, 15], drop_length=50, drop_width=1, red_drop_color=200, green_drop_color=255, blue_drop_color=255, blur_value=7, brightness_coefficient=0.7, rain_type="default", prob: float = 1.0):
        self.drop_color = [red_drop_color, green_drop_color, blue_drop_color]
        self.transform = A.Compose([
            A.RandomRain(slant_range=slant_range, drop_length= drop_length,drop_width=drop_width,drop_color=self.drop_color,blur_value=blur_value,brightness_coefficient=brightness_coefficient,rain_type=rain_type, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))
    
    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Rain applied with drop_length")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']