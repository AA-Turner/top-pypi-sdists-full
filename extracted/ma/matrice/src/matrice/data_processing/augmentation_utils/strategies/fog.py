import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class FogAugmentation(ImageAugmentationStrategy):
    def __init__(self, alpha_coef=0.1, fog_coef_range=[0.1, 0.5], prob: float = 0.5):
        self.transform = A.Compose([
            A.RandomFog(alpha_coef=alpha_coef, fog_coef_range=fog_coef_range, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))
    
    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Fog applied with coefficients: {self.transform[0].alpha_coef}")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
