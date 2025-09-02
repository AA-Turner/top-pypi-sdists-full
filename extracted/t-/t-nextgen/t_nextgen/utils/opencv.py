"""OpenCV module."""

import cv2
import numpy as np


class OpenCV:
    """OpenCV class for image processing."""

    @staticmethod
    def load_image(image_path: str) -> cv2.typing.MatLike:
        """Load image from path.

        Args:
            image_path: path of image

        Returns:
            image: loaded image
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        return image

    @staticmethod
    def is_strikethrough(img: np.ndarray) -> bool:
        """Detects whether text in an image is crossed out.

        Args:
            img (cv2.typing.MatLike): Image to check.

        Returns:
            bool: True if text is crossed out, False otherwise.
        """
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(img, (5, 5), 0)

        # Apply adaptive thresholding to obtain a binary image
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Find horizontal lines using morphological operations
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

        # Find the contours of the horizontal lines
        contours, hierarchy = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Analyze the contours to detect a strikethrough line
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Check if the line is long enough and has a reasonable width
            if w > img.shape[1] * 0.65 and h < img.shape[0] * 0.3:
                return True
        return False

    @staticmethod
    def check_strikethrough_in_text_image(image_path: str) -> bool:
        """Method to load image and check if it has strikethrough.

        Args:
            image_path: path of image

        Returns:
            bool: True if strikethrough is present, False otherwise
        """
        image = OpenCV.load_image(image_path)
        return OpenCV.is_strikethrough(image)
