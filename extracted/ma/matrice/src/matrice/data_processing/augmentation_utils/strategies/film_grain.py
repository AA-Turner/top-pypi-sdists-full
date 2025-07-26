import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class FilmGrainAugmentation(ImageAugmentationStrategy):
    def __init__(self, std_range=[0.1, 0.2], mean_range=[0, 0], per_channel=True, noise_scale_factor=1, prob: float = 1.0):
        self.transform = A.Compose([
            A.GaussNoise(std_range=std_range, mean_range=mean_range, per_channel=per_channel, noise_scale_factor=noise_scale_factor, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Film grain applied: {self.transform[0]}")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
