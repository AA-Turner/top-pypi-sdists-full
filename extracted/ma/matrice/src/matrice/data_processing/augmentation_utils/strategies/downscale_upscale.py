import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class DownscaleUpscaleAugmentation(ImageAugmentationStrategy):
    def __init__(self, scale_min=0.25, scale_max=0.5, upscale: int =0, downscale: int =0, prob: float = 0.5):
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.scale_range = [scale_min, scale_max]
        self.transform = A.Compose([
            A.Downscale(scale_range=self.scale_range, interpolation_pair={"upscale":upscale,"downscale":downscale}, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(f"Downscale applied with scale range")
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
