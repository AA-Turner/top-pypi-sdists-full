import cv2
import numpy as np

class ImagePreprocessor:
    def __init__(self):
        """Initialize the image preprocessor"""
        pass
    
    def preprocess(self, image_np, resize_dim=None, grayscale=True):
        """
        Preprocesses the image with various operations.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            resize_dim (tuple): Desired dimensions (width, height). If None, no resizing is done.
            grayscale (bool): Whether to convert the image to grayscale.
            
        Returns:
            np.ndarray: Preprocessed image.
        """
        processed_image = image_np.copy()
        
        # Convert to grayscale if requested
        if grayscale:
            if len(processed_image.shape) == 3:  # Check if image is already grayscale
                processed_image = cv2.cvtColor(processed_image, cv2.COLOR_RGB2GRAY)
        
        # Resize image if dimensions are provided
        if resize_dim:
            processed_image = cv2.resize(processed_image, resize_dim, interpolation=cv2.INTER_LINEAR)
        
        return processed_image
    
    def crop_to_bboxes(self, image_np, bboxes):
        """
        Crops the image to the specified bounding boxes.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            bboxes (list): List of bounding boxes. Each box is a list of [xmin, ymin, xmax, ymax].
            
        Returns:
            list: List of cropped images.
        """
        cropped_images = []
        
        for box in bboxes:
            xmin, ymin, xmax, ymax = map(int, box)
            cropped_img = image_np[ymin:ymax, xmin:xmax]
            cropped_images.append(cropped_img)
        
        return cropped_images