"""Auto-generated stub for module: postprocessing."""
from typing import Any, List

# Classes
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

