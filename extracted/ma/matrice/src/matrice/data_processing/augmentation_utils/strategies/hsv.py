import numpy as np
import albumentations as A
from ..base import ImageAugmentationStrategy
from typing import List, Tuple
import logging
class HueSaturationValueAugmentation(ImageAugmentationStrategy):
    def __init__(self, prob: float = 0.5, hue_shift_limit=[-20, 20], sat_shift_limit=[-30, 30], val_shift_limit=[-20, 20]):
        self.prob = prob
        self.transform = A.Compose([
            A.HueSaturationValue(
                hue_shift_limit=hue_shift_limit,
                sat_shift_limit=sat_shift_limit,
                val_shift_limit=val_shift_limit,
                p=1.0
            )
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        logging.debug(f" hsv original bounding boxes: {bboxes}")
        valid_bboxes = [bbox for bbox in bboxes if bbox[3] > bbox[1] and bbox[2] > bbox[0]]
        
        #if np.random.rand() < self.prob and valid_bboxes:
        class_labels = [0] * len(valid_bboxes)
        transformed = self.transform(image=image, bboxes=valid_bboxes, class_labels=class_labels)
        image = transformed['image']
        bboxes = transformed['bboxes']
        logging.debug(f"Hue, saturation, and value applied with limits: {self.transform[0].hue_shift_limit}, {self.transform[0].sat_shift_limit}, {self.transform[0].val_shift_limit}")
        return image, image.shape[0], image.shape[1], bboxes
