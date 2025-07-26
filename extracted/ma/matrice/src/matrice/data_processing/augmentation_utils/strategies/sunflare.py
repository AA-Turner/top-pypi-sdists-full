import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class SunFlareAugmentation(ImageAugmentationStrategy):
    def __init__(self, flare_roi=(0.0, 0.0, 1.0, 0.5), angle_lower=0.0, angle_upper=1.0, num_flare_circles_lower=6, prob: float = 0.5):
        self.transform = A.Compose([
            A.RandomSunFlare(flare_roi=flare_roi, angle_lower=angle_lower, angle_upper=angle_upper,
                             num_flare_circles_lower=num_flare_circles_lower, src_radius=200, p=prob)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))
    
    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Sun flare applied with flare_roi: {self.transform[0].flare_roi}, angle_lower: {self.transform[0].angle_lower}, angle_upper: {self.transform[0].angle_upper}, num_flare_circles_lower: {self.transform[0].num_flare_circles_lower}")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
