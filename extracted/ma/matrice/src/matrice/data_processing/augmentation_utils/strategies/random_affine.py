import numpy as np
import albumentations as A
from ..base import ImageAugmentationStrategy
from typing import List, Tuple
import logging
import cv2

def strat_map(strategy: str) -> str:
    """Map strategy name to its corresponding class."""
    strategy_mapping = {
        "cv2.INTER_LINEAR": cv2.INTER_LINEAR,
        "cv2.INTER_NEAREST": cv2.INTER_NEAREST,
        "cv2.INTER_CUBIC": cv2.INTER_CUBIC,
        "cv2.INTER_LANCZOS4": cv2.INTER_LANCZOS4,
        "cv2.INTER_AREA": cv2.INTER_AREA,
        "cv2.BORDER_CONSTANT": cv2.BORDER_CONSTANT,
        "cv2.BORDER_REFLECT": cv2.BORDER_REFLECT,
        "cv2.BORDER_REPLICATE": cv2.BORDER_REPLICATE,
        "cv2.BORDER_REFLECT_101": cv2.BORDER_REFLECT_101,
        "cv2.BORDER_WRAP": cv2.BORDER_WRAP,
    }
    return strategy_mapping.get(strategy)
class RandomAffineAugmentation(ImageAugmentationStrategy):
    def __init__(self, prob: float = 0.5, shift_limit=[-0.0625, 0.0625],
        scale_limit=[-0.1, 0.1],
        rotate_limit=[-45, 45],
        interpolation=cv2.INTER_LINEAR,
        border_mode=cv2.BORDER_CONSTANT,
        rotate_method="ellipse",
        mask_interpolation=0,
        fill=0,
        fill_mask=0):
        self.prob = prob
        self.transform = A.Compose([
            A.ShiftScaleRotate(
                shift_limit=shift_limit,
                scale_limit=scale_limit,
                rotate_limit=rotate_limit,
                interpolation=strat_map(interpolation),
                border_mode=strat_map(border_mode),
                rotate_method=rotate_method,
                mask_interpolation=mask_interpolation,
                fill=fill,
                fill_mask=fill_mask,
                p=1.0
            )
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        #if np.random.rand() < self.prob:
        logging.debug(f"random affine original bounding boxes: {bboxes}")
        class_labels = [0] * len(bboxes)  # dummy class labels to satisfy Albumentations
        transformed = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        image = transformed['image']
        bboxes = transformed['bboxes']
        logging.debug(f"Random affine transformation applied with shift limit")
        return image, image.shape[0], image.shape[1], bboxes

