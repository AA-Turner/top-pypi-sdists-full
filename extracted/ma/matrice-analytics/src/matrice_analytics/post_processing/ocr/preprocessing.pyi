"""Auto-generated stub for module: preprocessing."""
from typing import Any, List

# Classes
class ImagePreprocessor:
    def __init__(self: Any) -> None:
        """
        Initialize the image preprocessor
        """
        ...

    def crop_to_bboxes(self: Any, image_np: Any, bboxes: Any) -> Any:
        """
        Crops the image to the specified bounding boxes.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            bboxes (list): List of bounding boxes. Each box is a list of [xmin, ymin, xmax, ymax].
        
        Returns:
            list: List of cropped images.
        """
        ...

    def preprocess(self: Any, image_np: Any, resize_dim: Any = None, grayscale: Any = True) -> Any:
        """
        Preprocesses the image with various operations.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            resize_dim (tuple): Desired dimensions (width, height). If None, no resizing is done.
            grayscale (bool): Whether to convert the image to grayscale.
        
        Returns:
            np.ndarray: Preprocessed image.
        """
        ...

