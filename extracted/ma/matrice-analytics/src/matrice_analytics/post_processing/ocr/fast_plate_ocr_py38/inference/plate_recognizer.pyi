"""Auto-generated stub for module: plate_recognizer."""
from typing import Any, Optional, Union

# Classes
class LicensePlateRecognizer:
    # ONNX inference class for performing license plates OCR.

    def __init__(self: Any, hub_ocr_model: Optional[Any] = None, device: Any['Any', 'Any', 'Any'] = 'auto', providers: Optional[Any[Union[str, tuple[str, dict]]]] = None, sess_options: Optional[Any.Any] = None, onnx_model_path: Optional[Any] = None, plate_config_path: Optional[Any] = None, force_download: bool = False) -> None:
        """
        Initializes the `LicensePlateRecognizer` with the specified OCR model and inference device.
        
        The current OCR models available from the HUB are:
        
        - `cct-s-v1-global-model`: OCR model trained with **global** plates data. Based on Compact
            Convolutional Transformer (CCT) architecture. This is the **S** variant.
        - `cct-xs-v1-global-model`: OCR model trained with **global** plates data. Based on Compact
            Convolutional Transformer (CCT) architecture. This is the **XS** variant.
        - `argentinian-plates-cnn-model`: OCR for **Argentinian** license plates. Uses fully conv
            architecture.
        - `argentinian-plates-cnn-synth-model`: OCR for **Argentinian** license plates trained with
            synthetic and real data. Uses fully conv architecture.
        - `european-plates-mobile-vit-v2-model`: OCR for **European** license plates. Uses
            MobileVIT-2 for the backbone.
        - `global-plates-mobile-vit-v2-model`: OCR for **global** license plates (+65 countries).
            Uses MobileVIT-2 for the backbone.
        
        Args:
            hub_ocr_model: Name of the OCR model to use from the HUB.
            device: Device type for inference. Should be one of ('cpu', 'cuda', 'auto'). If
                'auto' mode, the device will be deduced from
                `onnxruntime.get_available_providers()`.
            providers: Optional sequence of providers in order of decreasing precedence. If not
                specified, all available providers are used based on the device argument.
            sess_options: Advanced session options for ONNX Runtime.
            onnx_model_path: Path to ONNX model file to use (In case you want to use a custom one).
            plate_config_path: Path to config file to use (In case you want to use a custom one).
            force_download: Force and download the model, even if it already exists.
        Returns:
            None.
        """
        ...

    def benchmark(self: Any, n_iter: int = 2500, batch_size: int = 1, include_processing: bool = False, warmup: int = 250) -> None:
        """
        Run an inference benchmark and pretty print the results.
        
        It reports the following metrics:
        
        * **Average latency per batch** (milliseconds)
        * **Throughput** in *plates / second* (PPS), i.e., how many plates the pipeline can process
          per second at the chosen ``batch_size``.
        
        Args:
            n_iter: The number of iterations to run the benchmark. This determines how many times
                the inference will be executed to compute the average performance metrics.
            batch_size : Batch size to use for the benchmark.
            include_processing: Indicates whether the benchmark should include preprocessing and
                postprocessing times in the measurement.
            warmup: Number of warmup iterations to run before the benchmark.
        """
        ...

    def run(self: Any, source: Union[str, list[str], Any.Any, list[Any.Any]], return_confidence: bool = False) -> Union[tuple[list[str], Any.Any], list[str]]:
        """
        Performs OCR to recognize license plate characters from an image or a list of images.
        
        Args:
            source: One or more image inputs, which can be:
        
                - A file path (`str` or `PathLike`) to an image.
                - A list of file paths.
                - A NumPy array of a single image, with shape (H, W), (H, W, 1) or (H, W, 3).
                - A list of NumPy arrays, each representing an image.
                - A 4D NumPy array of shape (N, H, W, C), ready for inference.
        
                Images will be automatically resized and converted as needed based on the model's
                configuration (including color mode and aspect ratio settings).
        
            return_confidence: Whether to return confidence scores along with plate predictions.
        
        Returns:
            A list of recognized license plates (one per image). If `return_confidence` is True,
            also returns a NumPy array of shape `(N, plate_slots)` containing the confidence scores
            for each predicted character.
        """
        ...

