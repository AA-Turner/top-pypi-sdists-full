import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class PosterizeAugmentation(ImageAugmentationStrategy):
    def __init__(self, num_bits=4, prob: float = 1.0):
        self.transform = A.Compose([
            A.Posterize(num_bits=num_bits, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Posterization applied with num_bits: {self.transform[0].num_bits}")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
