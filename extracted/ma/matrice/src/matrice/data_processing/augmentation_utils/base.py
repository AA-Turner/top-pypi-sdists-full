from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple, List, Dict

class ImageAugmentationStrategy(ABC):
    @abstractmethod
    def apply(
        self,
        image: np.ndarray,
        bboxes: List[List[float]],
        bbox_format: str = "coco"
    ) -> Tuple[np.ndarray, int, int, List[List[float]]]:
        pass

def yolo_to_mscoco(bboxes: List[List[float]], image_width: int, image_height: int) -> List[List[float]]:
    """
    Converts YOLO format bounding boxes to MSCOCO format.

    Args:
        bboxes (List[List[float]]): List of bounding boxes in YOLO format [x_center, y_center, width, height].
        image_width (int): Width of the image.
        image_height (int): Height of the image.

    Returns:
        List[List[float]]: List of bounding boxes in MSCOCO format [x_min, y_min, width, height].
    """
    mscoco_bboxes = []
    for bbox in bboxes:
        x_center, y_center, width, height = bbox
        x_min = (x_center - width / 2) * image_width
        y_min = (y_center - height / 2) * image_height
        box_width = width * image_width
        box_height = height * image_height
        mscoco_bboxes.append([x_min, y_min, box_width, box_height])
    return mscoco_bboxes