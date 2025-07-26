import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class ShadowAugmentation(ImageAugmentationStrategy):
    def __init__(self, prob: float = 1.0, 
                shadow_roi_x=[0,1],
                shadow_roi_y=[0,1],
                num_shadows_limit=[2, 3],
                shadow_dimension=4,
                shadow_intensity_range=[0.2, 0.7]
                ):
        self.shadows_roi = [shadow_roi_x[0], shadow_roi_y[0], shadow_roi_x[1], shadow_roi_y[1]]
        self.transform = A.Compose([
            A.RandomShadow(shadow_roi=self.shadows_roi,num_shadows_limit=num_shadows_limit, shadow_intensity_range=shadow_intensity_range, shadow_dimension=shadow_dimension, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))
    
    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Shadow applied with shadow_dimension")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
