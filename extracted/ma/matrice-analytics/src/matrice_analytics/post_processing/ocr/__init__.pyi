"""Stub file for post_processing.ocr directory."""
from typing import Any, List, Set

# Classes
# From easyocr_extractor
class EasyOCRExtractor:
    def __init__(self: Any, lang: Any = ['en', 'hi', 'ar'], gpu: Any = False, model_storage_directory: Any = None, download_enabled: Any = True, detector: Any = True, recognizer: Any = True, verbose: Any = False) -> None:
        """
        Initializes the EasyOCR text extractor with optimized parameters.
        
        Args:
            lang (str or list): Language(s) to be used by EasyOCR. Default is ['en', 'hi', 'ar'].
            gpu (bool): Enable GPU acceleration if available. Default is True.
            model_storage_directory (str): Custom path to store models. Default is None.
            download_enabled (bool): Allow downloading models if not found. Default is True.
            detector (bool): Load text detection model. Default is True.
            recognizer (bool): Load text recognition model. Default is True.
            verbose (bool): Enable verbose output (e.g., progress bars). Default is False.
        """
        ...

    def detect_text_regions(self: Any, image_np: Any, min_size: Any = 10, text_threshold: Any = 0.7, low_text: Any = 0.4, link_threshold: Any = 0.4, canvas_size: Any = 2560, mag_ratio: Any = 1.0, slope_ths: Any = 0.1, ycenter_ths: Any = 0.5, height_ths: Any = 0.5, width_ths: Any = 0.5, add_margin: Any = 0.1, optimal_num_chars: Any = None) -> Any:
        """
        Detects text regions in the image without performing recognition.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            min_size (int): Filter text boxes smaller than this pixel size.
            text_threshold (float): Text confidence threshold.
            low_text (float): Text low-bound score.
            link_threshold (float): Link confidence threshold.
            canvas_size (int): Maximum image size before resizing.
            mag_ratio (float): Image magnification ratio.
            slope_ths (float): Maximum slope for merging boxes.
            ycenter_ths (float): Maximum y-center shift for merging boxes.
            height_ths (float): Maximum height difference for merging boxes.
            width_ths (float): Maximum width for horizontal merging.
            add_margin (float): Margin to add around text boxes.
            optimal_num_chars (int): Prioritize boxes with this estimated character count.
        
        Returns:
            tuple: (horizontal_list, free_list) containing text regions
        """
        ...

    def extract(self: Any, image_np: Any, bboxes: Any = None, detail: Any = 1, paragraph: Any = False, decoder: Any = 'greedy', beam_width: Any = 5, batch_size: Any = 1, workers: Any = 0, allowlist: Any = None, blocklist: Any = None, min_size: Any = 10, rotation_info: Any = None, contrast_ths: Any = 0.1, adjust_contrast: Any = 0.5, text_threshold: Any = 0.7, low_text: Any = 0.4, link_threshold: Any = 0.4, canvas_size: Any = 2560, mag_ratio: Any = 1.0, slope_ths: Any = 0.1, ycenter_ths: Any = 0.5, height_ths: Any = 0.5, width_ths: Any = 0.5, add_margin: Any = 0.1) -> Any:
        """
        Extracts text from the given image or specific regions within the bounding boxes
        with configurable parameters for optimal performance.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            bboxes (list): List of bounding boxes. Each box is a list of [xmin, ymin, xmax, ymax].
                          If None, OCR is performed on the entire image.
            detail (int): Set to 0 for simple output, 1 for detailed output.
            paragraph (bool): Combine results into paragraphs.
            decoder (str): Decoding method ('greedy', 'beamsearch', 'wordbeamsearch').
            beam_width (int): How many beams to keep when using beam search decoders.
            batch_size (int): Number of images to process in a batch.
            workers (int): Number of worker threads for data loading.
            allowlist (str): Force recognition of only specific characters.
            blocklist (str): Block specific characters from recognition.
            min_size (int): Filter text boxes smaller than this pixel size.
            rotation_info (list): List of rotation angles to try (e.g., [90, 180, 270]).
            contrast_ths (float): Threshold for contrast adjustment.
            adjust_contrast (float): Target contrast level for low-contrast text.
            text_threshold (float): Text confidence threshold.
            low_text (float): Text low-bound score.
            link_threshold (float): Link confidence threshold.
            canvas_size (int): Maximum image size before resizing.
            mag_ratio (float): Image magnification ratio.
            slope_ths (float): Maximum slope for merging boxes.
            ycenter_ths (float): Maximum y-center shift for merging boxes.
            height_ths (float): Maximum height difference for merging boxes.
            width_ths (float): Maximum width for horizontal merging.
            add_margin (float): Margin to add around text boxes.
        
        Returns:
            list: OCR results containing text, confidence, and bounding boxes.
        """
        ...

    def recognize_from_regions(self: Any, image_np: Any, horizontal_list: Any = None, free_list: Any = None, decoder: Any = 'greedy', beam_width: Any = 5, batch_size: Any = 1, workers: Any = 0, allowlist: Any = None, blocklist: Any = None, detail: Any = 1, paragraph: Any = False, contrast_ths: Any = 0.1, adjust_contrast: Any = 0.5) -> Any:
        """
        Recognizes text from previously detected regions.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            horizontal_list (list): List of rectangular regions [x_min, x_max, y_min, y_max].
            free_list (list): List of free-form regions [[x1,y1],[x2,y2],[x3,y3],[x4,y4]].
            Other parameters: Same as extract method.
        
        Returns:
            list: OCR results for the specified regions
        """
        ...

    def setup(self: Any) -> Any:
        """
        Initializes the EasyOCR reader if not already initialized.
        """
        ...


# From postprocessing
class TextPostprocessor:
    def __init__(self: Any, _logging_level: Any = logging.INFO) -> None:
        """
        Initialize the text postprocessor with optional logging configuration.
        
        Args:
            logging_level: The level of logging detail. Default is INFO.
        """
        ...

    def add_task_processor(self: Any, task_name: Any, processor_function: Any) -> Any: ...

    def postprocess(self: Any, texts: Any, confidences: Any, task: Any = None, confidence_threshold: Any = 0.25, cleanup: Any = True, region: Any = None) -> Any:
        """
        Postprocesses the extracted text by cleaning and filtering low-confidence results.
        Applies task-specific processing if a task is specified.
        
        Args:
            texts (list): List of extracted text strings.
            confidences (list): List of confidence scores corresponding to each text.
            task (str): Specific task for customized postprocessing. Default is None.
            confidence_threshold (float): Minimum confidence required to keep the text. Default is 0.5.
            cleanup (bool): Whether to perform text cleanup.
            region (str): Specific region for license plate processing ('india', 'us', 'eu', 'qatar'). Default is None.
        
        Returns:
            list: List of processed texts with corresponding confidence scores and validity flags.
        """
        ...


# From preprocessing
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


from . import easyocr_extractor, postprocessing, preprocessing