import albumentations as A
from ..base import ImageAugmentationStrategy
import numpy as np
from typing import List, Tuple
import logging
class CompressionArtifactsAugmentation(ImageAugmentationStrategy):
    def __init__(self, quality_range=[50,20], prob: float = 1.0):
        self.quality_range= quality_range
        self.prob = 1.0
        self.transform = A.Compose([
            A.ImageCompression(compression_type="jpeg", quality_range=self.quality_range, p=1.0)
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        class_labels = ['object'] * len(bboxes)
        augmented = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        logging.debug(
            f"Compression artifacts applied with quality range"
        )
        return augmented['image'], augmented['image'].shape[0], augmented['image'].shape[1], augmented['bboxes']
