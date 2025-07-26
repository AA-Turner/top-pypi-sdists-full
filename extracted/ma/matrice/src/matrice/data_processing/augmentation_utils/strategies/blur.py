import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class BlurAugmentation(ImageAugmentationStrategy):
    def __init__(self, blur_limit: int = 5, prob: float = 1.0):
        self.transform = A.Compose([
            A.Blur(blur_limit=blur_limit, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(
        self,
        image: np.ndarray,
        bboxes: List[List[float]],
        bbox_format: str = "coco"
    ) -> Tuple[np.ndarray, int, int, List[List[float]]]:
        
        logging.debug(f"blur original bounding boxes: {bboxes}")
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        aug_image = augmented['image']
        aug_bboxes = augmented['bboxes']
        logging.debug(f"Blur applied with limit")
        return aug_image, aug_image.shape[0], aug_image.shape[1], aug_bboxes
