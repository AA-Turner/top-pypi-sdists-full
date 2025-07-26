import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class HorizontalFlipAugmentation(ImageAugmentationStrategy):
    def __init__(self, prob: float = 0.5):
        self.transform = A.Compose([
            A.HorizontalFlip(p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(
        self,
        image: np.ndarray,
        bboxes: List[List[float]],  # [x, y, w, h]
        # bbox_format parameter removed as it is not accessed
    ) -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        # Validate bounding boxes before applying the transformation
        logging.debug(f"flip original bounding boxes: {bboxes}")
        valid_bboxes = [bbox for bbox in bboxes if bbox[3] > bbox[1] and bbox[2] > bbox[0]]
        augmented = self.transform(image=image, bboxes=valid_bboxes, class_labels=class_labels)
        aug_image = augmented['image']
        aug_bboxes = augmented['bboxes']
        logging.debug(f"Horizontal flip applied with probability: {self.transform[0].p}")
        return aug_image, aug_image.shape[0], aug_image.shape[1], aug_bboxes
