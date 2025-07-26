import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class ColorJitterAugmentation(ImageAugmentationStrategy):
    def __init__(self, brightness=[0.8, 1.2], contrast=[0.8, 1.2], saturation=[0.8, 1.2], hue=[-0.5, 0.5], prob: float = 1.0):
        self.transform = A.Compose([
            A.ColorJitter(brightness=brightness, contrast=contrast, saturation=saturation, hue=hue, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        logging.debug(f"color jitter original bounding boxes: {bboxes}")
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Color jitter applied with brightness")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
