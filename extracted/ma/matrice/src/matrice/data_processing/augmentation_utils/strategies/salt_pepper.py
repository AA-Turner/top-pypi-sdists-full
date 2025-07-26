import numpy as np
import albumentations as A
from ..base import ImageAugmentationStrategy
from typing import List, Tuple
import logging

class SaltAndPepperNoiseAugmentation(ImageAugmentationStrategy):
    def __init__(self, amount_range=[0.01, 0.06], salt_vs_pepper_range=[0.4, 0.6], prob: float = 0.5):
        self.prob = prob
        # Randomly sample amount and salt_vs_pepper values within range for each instance
        #amount = np.random.uniform(*amount_range)
        #salt_vs_pepper = np.random.uniform(*salt_vs_pepper_range)
        
        self.transform = A.Compose([
            A.SaltAndPepper(
                amount=amount_range,
                salt_vs_pepper=salt_vs_pepper_range,
                p=1.0
            )
        ], bbox_params=A.BboxParams(format='coco', label_fields=['class_labels']))

    def apply(self, image: np.ndarray, bboxes: List[List[float]], bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        logging.debug(f"Salt and Pepper original bounding boxes: {bboxes}")
        class_labels = [0] * len(bboxes)  # Dummy labels
        transformed = self.transform(image=image, bboxes=bboxes, class_labels=class_labels)
        image = transformed['image']
        bboxes = transformed['bboxes']
        logging.debug("Salt and Pepper noise applied using Albumentations' built-in transform.")
        return image, image.shape[0], image.shape[1], bboxes
