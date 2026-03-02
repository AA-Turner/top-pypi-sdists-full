from typing import Tuple, Dict, Any, Optional, List, Union, Callable
import logging
from matrice.action_tracker import ActionTracker
from matrice_inference.server.model.model_manager import ModelManager
from matrice_inference.server.model.triton_model_manager import TritonModelManager
import numpy as np

class ModelManagerWrapper:
    """Wrapper class for ModelManager and TritonModelManager to provide a unified interface."""

    def __init__(
        self,
        action_tracker: ActionTracker,
        test_env: bool = False,
        # "default" for ModelManager, "triton" for TritonModelManager
        model_type: str = "default",

        num_model_instances: Optional[int] = None,
        load_model: Optional[Callable] = None,
        predict: Optional[Callable] = None,
        batch_predict: Optional[Callable] = None,

        model_name: Optional[str] = None,
        model_path: Optional[str] = None,
        runtime_framework: Optional[str] = None,
        internal_server_type: Optional[str] = None,
        internal_port: Optional[int] = None,
        internal_host: Optional[str] = None,
        input_size: Optional[Union[int, List[int]]] = None,
        num_classes: Optional[int] = None,
        use_dynamic_batching: Optional[bool] = None,
        max_batch_size: Optional[int] = None,

        is_yolo: Optional[bool] = None,
        is_ocr: Optional[bool] = None,
        use_trt_accelerator: Optional[bool] = None,

        preprocess_fn: Optional[Callable] = None,
        postprocess_fn: Optional[Callable] = None,
        preprocess_params: Optional[Dict[str, Any] ]= None,
        postprocess_params: Optional[Dict[str, Any]] = None,
        async_predict: Optional[Callable] = None,
        async_batch_predict: Optional[Callable] = None,
        async_load_model: Optional[Callable] = None,
    ):
        """
        Initialize the ModelManagerWrapper.

        Args:
            action_tracker: Action tracker for category mapping and configuration.
            test_env: If True, use provided parameters for testing; if False, extract from action_tracker.
            model_type: Type of model manager ("default" for ModelManager, "triton" for TritonModelManager).
            internal_server_type: Type of internal server (e.g., "rest", "grpc").
            internal_port: Internal port number.
            internal_host: Internal host address.
            num_model_instances: Number of model instances to create.
            load_model: Function to load the model (for ModelManager).
            predict: Function to run predictions (for ModelManager).
            batch_predict: Function to run batch predictions (for ModelManager).
            model_name: Name of the model (for TritonModelManager).
            model_path: Path to the model (for TritonModelManager).
            runtime_framework: Runtime framework for the model (for TritonModelManager).
            input_size: Input size for the model (for TritonModelManager).
            num_classes: Number of classes for the model (for TritonModelManager).
            use_dynamic_batching: Whether to use dynamic batching (for TritonModelManager).
            max_batch_size: Maximum batch size (for TritonModelManager).
            is_yolo: Whether the model is YOLO (for TritonModelManager).
            is_ocr: Whether the model is OCR (for TritonModelManager).
            use_trt_accelerator: Whether to use TensorRT accelerator (for TritonModelManager).
            preprocess_fn: User-provided preprocessing function (optional).
            postprocess_fn: User-provided postprocessing function (optional).
            preprocess_params: Parameters for the preprocessing function.
            postprocess_params: Parameters for the postprocessing function.
            async_predict: Function for single async predictions. Defaults to None.
            async_batch_predict: Function for batch async predictions. Defaults to None.
            async_load_model: Function to load model asynchronously (loaded lazily in worker thread's event loop). Defaults to None.
        """
        self.logger = logging.getLogger(__name__)
        self.action_tracker = action_tracker
        self.test_env = test_env
        self.model_type = model_type.lower() if model_type else "default"
        self.model_type = "default" # TODO: remove this once BE is updated with the current types
        # Validate model_type
        if self.model_type not in ["default", "triton"]:
            raise ValueError(f"Invalid model_type '{self.model_type}'. Must be 'default' or 'triton'")

        default_config = {
            "internal_server_type": "rest",
            "internal_port": 8000,
            "internal_host": "localhost",
            "num_model_instances": 1,
            "load_model": None,
            "predict": None,
            "batch_predict": None,
            "async_predict": None,
            "async_batch_predict": None,
            "async_load_model": None,
            "model_name": None,
            "model_path": "",
            "runtime_framework": "onnx",
            "input_size": 640,
            "num_classes": 80,
            "use_dynamic_batching": False,
            "max_batch_size": 8,
            "is_yolo": False,
            "is_ocr": False,
            "use_trt_accelerator": False,
            "preprocess_fn": None,
            "postprocess_fn": None,
            "preprocess_params": {},
            "postprocess_params": {},
        }

        # Extract configuration from action_tracker for production
        if not test_env:
            config = self._extract_config_from_action_tracker(
                model_type=model_type,
                internal_server_type=internal_server_type,
                internal_port=internal_port,
                internal_host=internal_host,
                num_model_instances=num_model_instances,
                load_model=load_model,
                predict=predict,
                batch_predict=batch_predict,
                async_predict=async_predict,
                async_batch_predict=async_batch_predict,
                async_load_model=async_load_model,
                model_name=model_name,
                model_path=model_path,
                runtime_framework=runtime_framework,
                input_size=input_size,
                num_classes=num_classes,
                use_dynamic_batching=use_dynamic_batching,
                max_batch_size=max_batch_size,
                is_yolo=is_yolo,
                is_ocr=is_ocr,
                use_trt_accelerator=use_trt_accelerator,
                preprocess_fn=preprocess_fn,
                postprocess_fn=postprocess_fn,
                preprocess_params=preprocess_params,
                postprocess_params=postprocess_params,
            )
            if not config:
                self.logger.warning("No valid configuration found in action_tracker, using defaults")
                config = default_config
            else:
                for key, value in default_config.items():
                    if key not in config or config[key] is None:
                        self.logger.warning(f"Missing or None config key '{key}' in action_tracker, using default: {value}")
                        config[key] = value
        else:
            # User provided args for testing
            config = {
                "internal_server_type": internal_server_type,
                "internal_port": internal_port,
                "internal_host": internal_host,
                "num_model_instances": num_model_instances,
                "load_model": load_model,
                "predict": predict,
                "batch_predict": batch_predict,
                "async_predict": async_predict,
                "async_batch_predict": async_batch_predict,
                "async_load_model": async_load_model,
                "model_name": model_name,
                "model_path": model_path,
                "runtime_framework": runtime_framework,
                "input_size": input_size,
                "num_classes": num_classes,
                "use_dynamic_batching": use_dynamic_batching,
                "max_batch_size": max_batch_size,
                "is_yolo": is_yolo,
                "is_ocr": is_ocr,
                "use_trt_accelerator": use_trt_accelerator,
                "preprocess_fn": preprocess_fn,
                "postprocess_fn": postprocess_fn,
                "preprocess_params": preprocess_params,
                "postprocess_params": postprocess_params,
            }
            for key, value in default_config.items():
                if config[key] is None:
                    self.logger.warning(f"Missing or None config key '{key}' in test environment, using default: {value}")
                    config[key] = value

        # VALIDATION: Log function types before creating ModelManager
        self.logger.info(f"Config load_model type: {type(config.get('load_model'))}")
        self.logger.info(f"Config predict type: {type(config.get('predict'))}")

        if config.get("load_model") is None:
            self.logger.error("load_model is None in config after extraction!")
        if config.get("predict") is None:
            self.logger.error("predict is None in config after extraction!")

        if self.model_type == "triton":
            # Validate required parameters for TritonModelManager
            required_triton_params = ["model_name", "model_path", "runtime_framework", "preprocess_fn", "postprocess_fn"]
            for param in required_triton_params:
                if not config.get(param):
                    raise ValueError(f"Required parameter '{param}' is missing or invalid for Triton model manager")

            if callable(config["preprocess_fn"]) is False:
                raise ValueError("preprocess_fn must be a callable function for Triton model manager")
            if callable(config["postprocess_fn"]) is False:
                raise ValueError("postprocess_fn must be a callable function for Triton model manager")

            protocol2port = {"rest": 8000, "grpc": 8001}
            if config["internal_server_type"] in protocol2port:
                config["internal_port"] = protocol2port[config["internal_server_type"]]
                self.logger.info(f"Set internal_port to {config['internal_port']} for {config['internal_server_type']}")
            
            self.model_manager = TritonModelManager(
                model_name=config["model_name"],
                model_path=config["model_path"],
                runtime_framework=config["runtime_framework"],
                internal_server_type=config["internal_server_type"],
                internal_port=config["internal_port"],
                internal_host=config["internal_host"],
                input_size=config["input_size"],
                num_classes=config["num_classes"],
                num_model_instances=config["num_model_instances"],
                use_dynamic_batching=config["use_dynamic_batching"],
                max_batch_size=config["max_batch_size"],
                is_yolo=config["is_yolo"],
                is_ocr=config["is_ocr"],
                use_trt_accelerator=config["use_trt_accelerator"],
                preprocess_fn=config["preprocess_fn"],  
                postprocess_fn=config["postprocess_fn"],
                preprocess_params=config["preprocess_params"],
                postprocess_params=config["postprocess_params"],  
            )
        else:
            # Validate required parameters for ModelManager
            if not self.action_tracker:
                raise ValueError("action_tracker is required for default ModelManager")
            
            # Validate that at least one prediction function is provided
            if not config.get("predict") and not config.get("load_model"):
                self.logger.warning("No prediction functions provided for ModelManager. At least 'predict' and 'load_model' should be provided.")
            
            self.model_manager = ModelManager(
                action_tracker=self.action_tracker,
                load_model=config["load_model"],
                predict=config["predict"],
                batch_predict=config.get("batch_predict"),
                async_predict=config.get("async_predict"),
                async_batch_predict=config.get("async_batch_predict"),
                async_load_model=config.get("async_load_model"),
                num_model_instances=config["num_model_instances"],
                model_path=config.get("model_path"),
            )

        self.logger.info(f"Initialized ModelManagerWrapper with {self.model_type} model manager")

    def _extract_config_from_action_tracker(
        self,
        model_type: Optional[str] = None,
        internal_server_type: Optional[str] = None,
        internal_port: Optional[int] = None,
        internal_host: Optional[str] = None,
        num_model_instances: Optional[int] = None,
        load_model: Optional[Callable] = None,
        predict: Optional[Callable] = None,
        batch_predict: Optional[Callable] = None,
        async_predict: Optional[Callable] = None,
        async_batch_predict: Optional[Callable] = None,
        async_load_model: Optional[Callable] = None,
        model_name: Optional[str] = None,
        model_path: Optional[str] = None,
        runtime_framework: Optional[str] = None,
        input_size: Optional[Union[int, List[int]]] = None,
        num_classes: Optional[int] = None,
        use_dynamic_batching: Optional[bool] = None,
        max_batch_size: Optional[int] = None,
        is_yolo: Optional[bool] = None,
        is_ocr: Optional[bool] = None,
        use_trt_accelerator: Optional[bool] = None,
        preprocess_fn: Optional[Callable] = None,
        postprocess_fn: Optional[Callable] = None,
        preprocess_params: Optional[Dict[str, Any]] = None,
        postprocess_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Extract configuration from action_tracker for production use.

        Prioritizes configuration from action_tracker, then user-provided arguments, and finally
        defaults. Logs warnings when falling back to user arguments or defaults.

        Args:
            model_type: User-provided model type.
            internal_server_type: User-provided server type.
            internal_port: User-provided port.
            internal_host: User-provided host.
            num_model_instances: User-provided number of model instances.
            load_model: User-provided load model function.
            predict: User-provided predict function.
            batch_predict: User-provided batch predict function.
            async_predict: User-provided async predict function.
            async_batch_predict: User-provided async batch predict function.
            async_load_model: User-provided async load model function.
            model_name: User-provided model name.
            model_path: User-provided model path.
            runtime_framework: User-provided runtime framework.
            input_size: User-provided input size.
            num_classes: User-provided number of classes.
            use_dynamic_batching: User-provided dynamic batching flag.
            max_batch_size: User-provided max batch size.
            is_yolo: User-provided YOLO flag.
            is_ocr: User-provided OCR flag.
            use_trt_accelerator: User-provided TensorRT accelerator flag.
            preprocess_fn: User-provided preprocessing function (optional).
            postprocess_fn: User-provided postprocessing function (optional).
            preprocess_params: Parameters for the preprocessing function.
            postprocess_params: Parameters for the postprocessing function.

        Returns:
            Configuration dictionary extracted from action_tracker, user arguments, or defaults.
        """
        try:
            config = {}
            # Default configuration
            default_config = {
                "internal_server_type": "rest",
                "internal_port": 8000,
                "internal_host": "localhost",
                "num_model_instances": 1,
                "load_model": None,
                "predict": None,
                "batch_predict": None,
                "async_predict": None,
                "async_batch_predict": None,
                "async_load_model": None,
                "model_name": "default_model",
                "model_path": "/models/default",
                "runtime_framework": "onnx",
                "input_size": 640,
                "num_classes": 10,
                "use_dynamic_batching": False,
                "max_batch_size": 8,
                "is_yolo": False,
                "is_ocr": False,
                "use_trt_accelerator": False,
                "preprocess_fn": preprocess_fn,
                "postprocess_fn": postprocess_fn,
            }

            job_params = getattr(self.action_tracker, "job_params", {})
            action_details = getattr(self.action_tracker, "action_details", {})
            action_tracker_sources: List[Dict, Any] = [action_details, job_params]
            
            # Helper function for normal parameters (action_tracker priority)
            def get_param(
                key: str,
                action_tracker_sources: List[Union[Dict, Any]],
                user_value: Optional[Any],
                default_value: Any,
            ) -> Any:
                value = None
                source = None
                # Try action_tracker sources first
                for src in action_tracker_sources:
                    if isinstance(src, dict) and key in src:
                        value = src.get(key)
                    else:
                        value = src
                    if value is not None:
                        source = "action_tracker"
                        break

                # If !action_tracker.val, try user-provided argument
                if value is None and user_value is not None:
                    value = user_value
                    source = "user-provided"

                # use default as fallback
                if value is None:
                    value = default_value
                    source = "default"

                if source != "action_tracker":
                    self.logger.warning(
                        f"Config key '{key}' not found in action_tracker, using {source} value: {value}"
                    )
                return value

            # Common params for both ModelManager and TritonModelManager
            server_type = get_param(
                "internal_server_type",
                [action_details.get("server_type", "rest").lower()],
                internal_server_type,
                default_config["internal_server_type"],
            )
            server_type_list = server_type.lower().split('_')
            if "triton" in server_type_list:
                config["internal_server_type"] = "grpc" if "grpc" in server_type_list else "rest"
            elif "fastapi" in server_type_list:
                config["internal_server_type"] = None
            else:
                config["internal_server_type"] = server_type
                self.logger.info(f"Set internal_server_type to {config['internal_server_type']}")

            # Map protocol to default port
            protocol2port = {"rest": 8000, "grpc": 8001}
            action_server_type = action_details.get("server_type", "rest").lower()
            config["internal_port"] = get_param(
                "internal_port",
                [protocol2port.get(action_server_type, 8000)],
                internal_port,
                protocol2port.get(config["internal_server_type"], default_config["internal_port"]),
            )

            config["internal_host"] = get_param(
                "internal_host",
                [action_details.get("host")],
                internal_host,
                default_config["internal_host"],
            )

            config["num_model_instances"] = get_param(
                "num_model_instances",
                [action_details.get("num_model_instances")],
                num_model_instances,
                default_config["num_model_instances"],
            )

            # ModelManager-specific parameters
            config["load_model"] = load_model
            config["predict"] = predict
            config["batch_predict"] = batch_predict
            config["async_predict"] = async_predict
            config["async_batch_predict"] = async_batch_predict
            config["async_load_model"] = async_load_model

            if self.model_type != "triton":
                return config
            
            # TritonModelManager-specific parameters
            config["model_name"] = get_param(
                "model_name",
                [action_details.get("modelKey")],
                model_name,
                default_config["model_name"],
            )

            # NOTE : Priority order -> user arg > action_details > default [Overwrite Issue]
            config["model_path"] = get_param(
                "model_path",
                [model_path],  
                [getattr(self.action_tracker, "checkpoint_path", None)],
                default_config["model_path"],
            )

            # NOTE : Priority order -> user arg > action_details > default [Overwrite Issue]
            config["runtime_framework"] = get_param(
                "runtime_framework",
                [runtime_framework],  
                [action_details.get("runtimeFramework"), action_details.get("exportFormat")],
                default_config["runtime_framework"],
            )

            config["input_size"] = get_param(
                "input_size",
                [action_details.get("input_size", None)],
                input_size,
                default_config["input_size"],
            )

            index_to_category = self.action_tracker.get_index_to_category(self.action_tracker.is_exported)
            num_classes_action = len(index_to_category) if index_to_category else None
            class_index_map = action_details.get("class_index_map", {})
            num_classes_from_map = len(class_index_map) if class_index_map else None

            config["num_classes"] = get_param(
                "num_classes",
                [num_classes_from_map, num_classes_action], 
                num_classes,
                default_config["num_classes"],
            )


            config["use_dynamic_batching"] = get_param(
                "use_dynamic_batching",
                [],
                use_dynamic_batching,
                default_config["use_dynamic_batching"],
            )

            config["max_batch_size"] = get_param(
                "max_batch_size",
                [],
                max_batch_size,
                default_config["max_batch_size"],
            )

            config["is_yolo"] = get_param(
                "is_yolo",
                [],
                is_yolo,
                default_config["is_yolo"],
            )

            config["is_ocr"] = get_param(
                "is_ocr",
                [],
                is_ocr,
                default_config["is_ocr"],
            )

            if config["runtime_framework"] == "tensorrt":
                config["use_trt_accelerator"] = False  # Already using TensorRT
                self.logger.info("Disabled TensorRT accelerator (already using TensorRT runtime)")
            else:
                config["use_trt_accelerator"] = get_param(
                    "use_trt_accelerator",
                    [action_details.get("use_trt_accelerator"), job_params.get("use_trt_accelerator")],
                    use_trt_accelerator,
                    default_config["use_trt_accelerator"],
                )

            config["preprocess_fn"] = preprocess_fn
            config["postprocess_fn"] = postprocess_fn
            config["preprocess_params"] = preprocess_params if preprocess_params is not None else {}
            config["postprocess_params"] = postprocess_params if postprocess_params is not None else {}

            return config
        except Exception as e:
            self.logger.error(f"Failed to extract config from action_tracker: {str(e)}", exc_info=True)
            return {}
        
    def inference(
        self,
        input: Any,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, bool]:
        """
        Perform synchronous single inference.
        """
        if input is None:
            raise ValueError("input cannot be None")
        
        try:
            if self.model_type == "triton":
                # TritonModelManager only accepts input parameter
                return self.model_manager.inference(input=input)
            else:
                # ModelManager accepts additional parameters
                return self.model_manager.inference(
                    input=input,
                    extra_params=extra_params,
                    stream_key=stream_key,
                    stream_info=stream_info,
                )
        except Exception as e:
            self.logger.error(f"Inference failed in ModelManagerWrapper: {str(e)}", exc_info=True)
            return None, False

    async def async_inference(
        self,
        input: Union[bytes, np.ndarray],
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Any, bool]:
        """
        Perform asynchronous single inference.
        """
        if input is None:
            raise ValueError("input cannot be None")
        
        try:
            if self.model_type == "triton":
                return await self.model_manager.async_inference(input=input)
            else:
                # ModelManager now has async_inference support
                return await self.model_manager.async_inference(
                    input=input,
                    extra_params=extra_params,
                    stream_key=stream_key,
                    stream_info=stream_info,
                )
        except Exception as e:
            self.logger.error(f"Async inference failed in ModelManagerWrapper: {str(e)}", exc_info=True)
            return None, False

    def batch_inference(
        self,
        input: List[Any],
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Any], bool]:
        """
        Perform synchronous batch inference.
        """
        if not input:
            raise ValueError("input cannot be None or empty")
        
        try:
            if self.model_type == "triton":
                # TritonModelManager only accepts input parameter
                return self.model_manager.batch_inference(input=input)
            else:
                # ModelManager accepts additional parameters
                return self.model_manager.batch_inference(
                    input=input,
                    extra_params=extra_params,
                    stream_key=stream_key,
                    stream_info=stream_info,
                )
        except Exception as e:
            self.logger.error(f"Batch inference failed in ModelManagerWrapper: {str(e)}", exc_info=True)
            return [], False

    async def async_batch_inference(
        self,
        input: List[Any],
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Any], bool]:
        """
        Perform asynchronous batch inference.
        
        Uses async_batch_predict if available, otherwise falls back to sync batch_inference.
        """
        if not input:
            raise ValueError("input cannot be None or empty")
        
        try:
            if self.model_type == "triton":
                return await self.model_manager.async_batch_inference(input=input)
            else:
                # ModelManager has async_batch_inference which falls back to sync if needed
                return await self.model_manager.async_batch_inference(
                    input=input,
                    extra_params=extra_params,
                    stream_key=stream_key,
                    stream_info=stream_info,
                )
        except Exception as e:
            self.logger.error(f"Async batch inference failed in ModelManagerWrapper: {str(e)}", exc_info=True)
            return [], False
