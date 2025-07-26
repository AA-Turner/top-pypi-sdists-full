import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class ISONoiseAugmentation(ImageAugmentationStrategy):
    def __init__(self, color_shift=(0.01, 0.05), intensity=(0.1, 0.5), prob: float = 0.5):
        self.transform = A.Compose([
            A.ISONoise(color_shift=color_shift, intensity=intensity, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        logging.debug(f"ISO noise original bounding boxes: {bboxes}")
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"ISO noise applied with color shift: {self.transform[0].color_shift}, intensity: {self.transform[0].intensity}")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
