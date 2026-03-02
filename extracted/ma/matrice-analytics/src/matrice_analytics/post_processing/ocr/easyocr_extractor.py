import easyocr
import numpy as np
import torch
from matrice_common.utils import log_errors

class EasyOCRExtractor:
    def __init__(self, lang=['en', 'hi', 'ar'], gpu=False, model_storage_directory=None, 
                 download_enabled=True, detector=True, recognizer=True, verbose=False):
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
        self.lang = lang
        self.gpu = gpu
        # Check if GPU is available
        if torch.cuda.is_available():
            self.gpu = True
        else:
            self.gpu = False
        self.model_storage_directory = model_storage_directory
        self.download_enabled = download_enabled
        self.detector = detector
        self.recognizer = recognizer
        self.verbose = verbose
        self.reader = None
        
    @log_errors(default_return=None, raise_exception=True, service_name="py_analytics", log_error=True)
    def setup(self):
        """
        Initializes the EasyOCR reader if not already initialized.
        """
        if self.reader is None:
            lang_list = [self.lang] if isinstance(self.lang, str) else self.lang
            self.reader = easyocr.Reader(
                lang_list=lang_list,
                gpu=self.gpu,
                model_storage_directory=self.model_storage_directory,
                download_enabled=self.download_enabled,
                detector=self.detector,
                recognizer=self.recognizer,
                verbose=self.verbose
            )
    
    def extract(self, image_np, bboxes=None, detail=1, paragraph=False, 
                decoder='greedy', beam_width=5, batch_size=1, workers=0,
                allowlist=None, blocklist=None, min_size=10, rotation_info=None,
                contrast_ths=0.1, adjust_contrast=0.5, text_threshold=0.7,
                low_text=0.4, link_threshold=0.4, canvas_size=2560, mag_ratio=1.0,
                slope_ths=0.1, ycenter_ths=0.5, height_ths=0.5, width_ths=0.5,
                add_margin=0.1):
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
        # Make sure the reader is initialized
        self.setup()
        
        ocr_results = []
        
        # Dictionary of readtext parameters
        readtext_params = {
            'decoder': decoder,
            'beamWidth': beam_width,
            'batch_size': batch_size,
            'workers': workers,
            'allowlist': allowlist,
            'blocklist': blocklist,
            'detail': detail,
            'paragraph': paragraph,
            'min_size': min_size,
            'rotation_info': rotation_info,
            'contrast_ths': contrast_ths,
            'adjust_contrast': adjust_contrast,
            'text_threshold': text_threshold,
            'low_text': low_text,
            'link_threshold': link_threshold,
            'canvas_size': canvas_size,
            'mag_ratio': mag_ratio,
            'slope_ths': slope_ths,
            'ycenter_ths': ycenter_ths,
            'height_ths': height_ths,
            'width_ths': width_ths,
            'add_margin': add_margin
        }
        
        # If no bounding boxes, perform OCR on the entire image
        if bboxes is None:
            text_data = self.reader.readtext(image_np, **readtext_params)
            if detail == 0:
                return text_data  # Simple output format for detail=0
            
            for bbox, text, conf in text_data:
                ocr_results.append({
                    "text": text,
                    "confidence": conf,
                    "bounding_box": bbox
                })
        else:
            # Perform OCR on each bounding box
            for box in bboxes:
                xmin, ymin, xmax, ymax = map(int, box)
                cropped_img = image_np[ymin:ymax, xmin:xmax]
                
                # Skip empty crops
                if cropped_img.size == 0 or cropped_img.shape[0] == 0 or cropped_img.shape[1] == 0:
                    continue
                
                text_data = self.reader.readtext(cropped_img, **readtext_params)
                
                if detail == 0:
                    # Adjust coordinates for the cropped region
                    adjusted_data = []
                    for result in text_data:
                        if isinstance(result, tuple) and len(result) >= 1:
                            # Adjust coordinates based on crop position
                            adjusted_bbox = [[pt[0] + xmin, pt[1] + ymin] for pt in result[0]]
                            if len(result) == 3:  # (bbox, text, confidence)
                                adjusted_data.append((adjusted_bbox, result[1], result[2]))
                            elif len(result) == 2:  # (bbox, text)
                                adjusted_data.append((adjusted_bbox, result[1]))
                    ocr_results.extend(adjusted_data)
                else:
                    for bbox, text, conf in text_data:
                        # Adjust bounding box coordinates relative to the original image
                        adjusted_bbox = [
                            [pt[0] + xmin, pt[1] + ymin] for pt in bbox
                        ]
                        
                        ocr_results.append({
                            "text": text,
                            "confidence": conf,
                            "bounding_box": adjusted_bbox
                        })
        
        return ocr_results
    
    def detect_text_regions(self, image_np, min_size=10, text_threshold=0.7,
                            low_text=0.4, link_threshold=0.4, canvas_size=2560,
                            mag_ratio=1.0, slope_ths=0.1, ycenter_ths=0.5,
                            height_ths=0.5, width_ths=0.5, add_margin=0.1,
                            optimal_num_chars=None):
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
        self.setup()
        return self.reader.detect(
            image_np,
            min_size=min_size,
            text_threshold=text_threshold,
            low_text=low_text,
            link_threshold=link_threshold,
            canvas_size=canvas_size,
            mag_ratio=mag_ratio,
            slope_ths=slope_ths,
            ycenter_ths=ycenter_ths,
            height_ths=height_ths,
            width_ths=width_ths,
            add_margin=add_margin,
            optimal_num_chars=optimal_num_chars
        )
    
    def recognize_from_regions(self, image_np, horizontal_list=None, free_list=None,
                               decoder='greedy', beam_width=5, batch_size=1,
                               workers=0, allowlist=None, blocklist=None,
                               detail=1, paragraph=False, contrast_ths=0.1,
                               adjust_contrast=0.5):
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
        self.setup()
        return self.reader.recognize(
            image_np,
            horizontal_list=horizontal_list,
            free_list=free_list,
            decoder=decoder,
            beamWidth=beam_width,
            batch_size=batch_size,
            workers=workers,
            allowlist=allowlist,
            blocklist=blocklist,
            detail=detail,
            paragraph=paragraph,
            contrast_ths=contrast_ths,
            adjust_contrast=adjust_contrast
        )