"""Module providing triton_server functionality."""

import os
import zipfile
import subprocess
import tempfile
import asyncio
import shutil
import logging
import threading
import shlex
from typing import Tuple, Optional, Any, Dict, Union, List
import importlib.util
from matrice.docker_utils import pull_docker_image
from matrice.utils import dependencies_check

# TRITON_DOCKER_IMAGE = "nvcr.io/nvidia/tritonserver:24.08-py3"
TRITON_DOCKER_IMAGE = "nvcr.io/nvidia/tritonserver:23.08-py3"
BASE_PATH = "./model_repository"

# def dependencies_check(package_name: str) -> bool:
#     """Check if a package is installed."""
#     return importlib.util.find_spec(package_name) is not None


# def pull_docker_image(image_name: str) -> subprocess.Popen:
#     """Pull Docker image using subprocess."""
#     cmd = ["docker", "pull", image_name]
#     return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class TritonServer:
    def __init__(
        self,
        model_name: str,
        model_path: str,
        runtime_framework: str,
        input_size: Union[int, List[int]] = 224,
        num_classes: int = 10,
        dynamic_batching: bool = False,
        num_model_instances: int = 1,
        max_batch_size: int = 8,
        connection_protocol: str = "rest",
        is_yolo: bool = False,
        use_trt_accelerator: bool = False,
        **kwargs,
    ):
        """Initialize the Triton server.

        Args:
            model_name: Name of the model (used for Triton model repository).
            model_path: Path to the model file on the local filesystem.
            runtime_framework: Framework of the model ('onnx', 'pytorch', 'torchscript', 'yolo', 'tensorrt', 'openvino').
            input_size: Input size for the model (int for square images or [height, width]).
            num_classes: Number of output classes.
            dynamic_batching: Enable dynamic batching for the model.
            num_model_instances: Number of model instances to deploy.
            max_batch_size: Maximum batch size for inference.
            connection_protocol: Protocol for Triton server ('rest' or 'grpc').
            use_trt_accelerator: Enable TensorRT acceleration for inference.
        """
        if not dependencies_check("torch"):
            raise ImportError("PyTorch is required but not installed")
        import torch
        
        if not model_name:
            raise ValueError("model_name must be provided")
        if not model_path:
            raise ValueError("model_path must be provided")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        logging.info("Initializing TritonServer")
        
        self.model_name = model_name
        self.model_path = os.path.abspath(model_path)
        self.runtime_framework = runtime_framework.lower()
        self.connection_protocol = connection_protocol.lower()
        
        if isinstance(input_size, (int, float)):
            self.input_size = [int(input_size), int(input_size)]
        elif isinstance(input_size, (list, tuple)):
            if len(input_size) == 2:  # (H, W)
                self.input_size = [int(input_size[0]), int(input_size[1])]
            elif len(input_size) == 3:  # (H, W, C) 
                self.input_size = [int(input_size[0]), int(input_size[1])]
            elif len(input_size) == 4:  # (N, C, H, W) 
                self.input_size = [int(input_size[-2]), int(input_size[-1])]
        else:
            logging.warning("Unexpected input_size length: %s, using default [224, 224]", input_size)
            self.input_size = [224, 224]

        self.num_classes = num_classes
        self.dynamic_batching = dynamic_batching
        self.num_model_instances = num_model_instances
        self.max_batch_size = max_batch_size
        self.use_trt_accelerator = use_trt_accelerator
    
        self.is_yolo = is_yolo or self.runtime_framework == "yolo"
        self.input_name = "images" if self.is_yolo else "input"
        self.output_name = "output0" if self.is_yolo else "output"

        self.gpus_count = torch.cuda.device_count()
        self.config_params = {}
        
        logging.info("Model name: %s", self.model_name)
        logging.info("Model path: %s", self.model_path)
        logging.info("Runtime framework: %s", self.runtime_framework)
        logging.info("Using connection protocol: %s", self.connection_protocol)
        logging.info("Input size: %s", self.input_size)
        logging.info("Number of classes: %s", self.num_classes)
        logging.info("Found %s GPUs available for inference", self.gpus_count)
        
        self.docker_pull_process = pull_docker_image(TRITON_DOCKER_IMAGE)

    def check_triton_docker_image(self):
        """Check if docker image download is complete and wait for it to finish"""
        logging.info("Checking docker image download status")
        stdout, stderr = self.docker_pull_process.communicate()
        if self.docker_pull_process.returncode == 0:
            logging.info(f"Docker image {TRITON_DOCKER_IMAGE} downloaded successfully")
        else:
            error_msg = stderr.decode()
            logging.error(f"Docker pull failed with return code {self.docker_pull_process.returncode}")
            logging.error("Error message: %s", error_msg)
            raise RuntimeError(f"Docker pull failed: {error_msg}")

    def prepare_model(self, model_version_dir: str) -> None:
        """Prepare the model file for Triton Inference Server.

        Copies model from self.model_path to model_version_dir and converts if necessary 
        to the format expected by Triton (model.onnx, model.xml, model.plan).

        Args:
            model_version_dir: Directory to store the model file 
            (e.g., '/models/<model_name>/1').
        """
        try:
            runtime_framework = self.runtime_framework
            logging.info("Preparing model with runtime framework: %s", runtime_framework)
            logging.info("Source model path: %s", self.model_path)

            if runtime_framework not in ["onnx", "pytorch", "torchscript", "yolo", "tensorrt", "openvino"]:
                logging.error("Runtime framework '%s' not supported. Supported: %s", 
                            runtime_framework, ["onnx", "pytorch", "torchscript", "yolo", "tensorrt", "openvino"])
                raise ValueError(f"Unsupported runtime framework: {runtime_framework}")
            
            os.makedirs(model_version_dir, exist_ok=True)
            
            # 1. ONNX - copy to model.onnx
            if runtime_framework == "onnx":
                model_file = os.path.join(model_version_dir, "model.onnx")
                if os.path.abspath(self.model_path) != os.path.abspath(model_file):
                    shutil.copy2(self.model_path, model_file)
                    logging.info("Copied ONNX model to: %s", model_file)
                else:
                    logging.info("Model path is already correct: %s", model_file)
                self._verify_onnx_model(model_file)

            # 2. PyTorch/TorchScript/Yolo - export to ONNX
            elif runtime_framework in ["pytorch", "torchscript", "yolo"]:
                model_file = os.path.join(model_version_dir, "model.onnx")
                img_chw = (3, self.input_size[0], self.input_size[1])
                logging.info("Converting %s model to ONNX with input shape: %s", runtime_framework, img_chw)
                self.to_onnx(self.model_path, model_file, (1, *img_chw))
                logging.info("Exported ONNX model to: %s", model_file)
                self._verify_onnx_model(model_file)
                
            # 3. TensorRT - copy to model.plan
            elif runtime_framework == "tensorrt":
                model_file = os.path.join(model_version_dir, "model.plan") 
                shutil.copy2(self.model_path, model_file)
                logging.info("Copied TensorRT model to: %s", model_file)
                self.runtime_framework = "tensorrt" 
                
            # 4. OpenVINO - extract ZIP or copy files
            elif runtime_framework == "openvino":
                if self.model_path.endswith('.zip'):
                    logging.info("Extracting OpenVINO ZIP to: %s", model_version_dir)
                    with zipfile.ZipFile(self.model_path, "r") as zip_ref:
                        zip_ref.extractall(model_version_dir)
                    model_file = os.path.join(model_version_dir, "model.xml")
                    model_bin_file = os.path.join(model_version_dir, "model.bin")
                else:
                    model_file = os.path.join(model_version_dir, "model.xml")
                    model_bin_file = os.path.join(model_version_dir, "model.bin")
                    
                    shutil.copy2(self.model_path, model_file)
                    
                    source_bin = self.model_path.replace('.xml', '.bin')
                    if os.path.exists(source_bin):
                        shutil.copy2(source_bin, model_bin_file)
                    else:
                        raise RuntimeError(f"OpenVINO model.bin not found at {source_bin}")

                if not os.path.exists(model_file):
                    logging.error("OpenVINO model.xml not found at %s", model_file)
                    raise RuntimeError(f"OpenVINO model.xml not found at {model_file}")
                if not os.path.exists(model_bin_file):
                    logging.error("OpenVINO model.bin not found at %s", model_bin_file)
                    raise RuntimeError(f"OpenVINO model.bin not found at {model_bin_file}")
                logging.info("Prepared OpenVINO model: %s", model_file)

            logging.info("Model preparation completed successfully")
        except Exception as e:
            logging.error("Model preparation failed: %s", str(e), exc_info=True)
            raise

    def to_onnx(self, checkpoint_path: str, onnx_path: str, input_shape: Tuple[int, int, int, int]) -> None:
        """Export PyTorch or YOLO checkpoint to ONNX."""
        try:
            runtime_framework = self.runtime_framework.lower()
            logging.info("Exporting %s model to ONNX on CPU", runtime_framework)

            if runtime_framework == "yolo":
                try:
                    if dependencies_check("ultralytics"):
                        from ultralytics import YOLO
                        logging.info("Using Ultralytics YOLO for ONNX export")
                        model = YOLO(checkpoint_path)
                        # NOTE: Update 4 -- opset=12 for YOLOv8 compatibility
                        export_path = model.export(format="onnx", imgsz=input_shape[2], dynamic=True, opset=12)  # Added opset=12
                        if export_path != onnx_path:
                            shutil.move(export_path, onnx_path)
                        logging.info("Exported YOLO model to ONNX: %s", onnx_path)
                        return
                    else:
                        logging.warning("Ultralytics not available; falling back to PyTorch export for YOLO")
                except Exception as e:
                    logging.warning("Ultralytics YOLO export failed: %s; trying PyTorch export", str(e))

            import torch
            model = torch.load(checkpoint_path, map_location="cpu")
            # TODO: Add support for model_state_dict 
            model.eval()
            dummy_input = torch.randn(*input_shape)
            torch.onnx.export(
                model,
                dummy_input,
                onnx_path,
                opset_version=17,
                input_names=["input__0"],
                output_names=["output__0"],
                dynamic_axes={"input__0": {0: "batch"}, "output__0": {0: "batch"}},
            )
            logging.info("Exported PyTorch model to ONNX: %s", onnx_path)
        except Exception as e:
            logging.error("Failed to export to ONNX: %s", str(e), exc_info=True)
            raise

    def _verify_onnx_model(self, onnx_path: str):
        """Verify that the ONNX model is valid"""
        try:
            if dependencies_check("onnx"):
                import onnx
                model = onnx.load(onnx_path)
                onnx.checker.check_model(model)
                logging.info(f"ONNX model verification successful: {onnx_path}")
            else:
                logging.warning("ONNX library not available for model verification")
        except Exception as e:
            logging.error(f"ONNX model verification failed: %s", str(e))
            raise ValueError(f"Invalid ONNX model at {onnx_path}: {str(e)}")
        
    def create_model_repository(self):
        """Create the model repository directory structure"""
        try:
            model_version = "1"
            model_dir = os.path.join(BASE_PATH, self.model_name)
            version_dir = os.path.join(model_dir, str(model_version))
            logging.info("Creating model repository structure:")
            logging.info("Base path: %s", BASE_PATH)
            logging.info("Model directory: %s", model_dir)
            logging.info("Version directory: %s", version_dir)
            os.makedirs(version_dir, exist_ok=True)
            logging.info("Model repository directories created successfully")
            return model_dir, version_dir
        except Exception as e:
            logging.error(
                "Failed to create model repository: %s",
                str(e),
                exc_info=True,
            )
            raise

    def write_config_file(
        self,
        model_dir: str,
        max_batch_size: int = 8,
        num_model_instances: int = 1,
        image_size: List[int] = [224, 224],
        num_classes: int = 10,
        input_data_type: str = "TYPE_FP32",
        output_data_type: str = "TYPE_FP32",
        dynamic_batching: bool = False,
        preferred_batch_size: list = [2, 4, 8],
        max_queue_delay_microseconds: int = 100,
        input_pinned_memory: bool = True,
        output_pinned_memory: bool = True,
        **kwargs,
    ):
        """Write the model configuration file for Triton Inference Server."""
        try:
            runtime_framework = self.runtime_framework.lower()
            logging.info("Starting to write Triton config file for framework: %s", runtime_framework)
            
            if runtime_framework == "tensorrt":
                platform = "tensorrt_plan"
                model_filename = "model.plan" 
            elif runtime_framework in ["pytorch", "torchscript", "yolo", "onnx"]:
                platform = "onnxruntime_onnx"
                model_filename = "model.onnx"
            else:
                platform = "openvino"
                model_filename = "model.xml"
            logging.info("Using %s backend with model file: %s", platform, model_filename)

            config_path = os.path.join(model_dir, "config.pbtxt")
            logging.info("Writing config to: %s", config_path)

            if platform == "onnxruntime_onnx":
                model_file = os.path.join(model_dir, "1", "model.onnx")
                if os.path.exists(model_file) and dependencies_check("onnx"):
                    import onnx
                    model = onnx.load(model_file)
                    graph = model.graph
                    
                    inputs = []
                    for inp in graph.input:
                        shape = [d.dim_value if d.HasField("dim_value") else -1 for d in inp.type.tensor_type.shape.dim]
                        inputs.append((inp.name, input_data_type, shape))
                    
                    outputs = []
                    for out in graph.output:
                        shape = [d.dim_value if d.HasField("dim_value") else -1 for d in out.type.tensor_type.shape.dim]
                        if self.is_yolo and out.name != "output__0":
                            continue  # Skip intermediate YOLO outputs
                        output_shape = shape[1:] if max_batch_size > 0 and len(shape) > 1 else shape
                        outputs.append((out.name, output_data_type, output_shape))
                    
                    logging.info("ONNX inputs: %s", inputs)
                    logging.info("ONNX outputs: %s", outputs)
                else:
                    # Fallback when ONNX / model 404
                    inputs = [(self.input_name, input_data_type, [3, image_size[0], image_size[1]])]
                    outputs = [(self.output_name, output_data_type, [-1, -1] if self.is_yolo else [num_classes])]
            elif platform == "tensorrt_plan":
                # TensorRT: Use YOLO-specific or fallback input/output configuration
                inputs = [(self.input_name, input_data_type, [3, image_size[0], image_size[1]])]
                outputs = [(self.output_name, output_data_type, [-1, -1] if self.is_yolo else [num_classes])]
            else:
                # OpenVINO fallback
                inputs = [(self.input_name, input_data_type, [3, image_size[0], image_size[1]])]
                outputs = [(self.output_name, output_data_type, [num_classes])]

            logging.info("Final inputs for config: %s", inputs)
            logging.info("Final outputs for config: %s", outputs)

            config_content = f'name: "{self.model_name}"\n'
            config_content += f'platform: "{platform}"\n'
            config_content += f'max_batch_size: {max_batch_size}\n'
            
            # Input section
            config_content += 'input [\n'
            for name, dtype, shape in inputs:
                config_content += '  {\n'
                config_content += f'    name: "{name}"\n'
                config_content += f'    data_type: {dtype}\n'
                if platform == "tensorrt_plan":
                    dims = shape
                else:
                    dims = shape[1:] if max_batch_size > 0 and len(shape) > 1 else shape
                config_content += f'    dims: [{", ".join(str(dim) for dim in dims)}]\n'
                config_content += '  }\n'
            config_content += ']\n'
            
            # Output section
            config_content += 'output [\n'
            for name, dtype, shape in outputs:
                config_content += '  {\n'
                config_content += f'    name: "{name}"\n'
                config_content += f'    data_type: {dtype}\n'
                config_content += f'    dims: [{", ".join(str(dim) for dim in shape)}]\n'
                config_content += '  }\n'
            config_content += ']\n'

            # Instance group
            if num_model_instances > 1 or self.gpus_count > 0:
                device_type = "KIND_GPU" if self.gpus_count > 0 else "KIND_CPU"
                logging.info("Adding instance group configuration for %s %s instances", num_model_instances, device_type)
                config_content += 'instance_group [\n'
                config_content += '  {\n'
                config_content += f'    count: {num_model_instances}\n'
                config_content += f'    kind: {device_type}\n'
                config_content += '  }\n'
                config_content += ']\n'

            # Dynamic batching
            if dynamic_batching:
                logging.info("Adding dynamic batching configuration")
                valid_pref_sizes = [bs for bs in preferred_batch_size if bs <= max_batch_size]
                if valid_pref_sizes:
                    config_content += 'dynamic_batching {\n'
                    config_content += f'  preferred_batch_size: [{", ".join(str(bs) for bs in valid_pref_sizes)}]\n'
                    config_content += f'  max_queue_delay_microseconds: {max_queue_delay_microseconds}\n'
                    config_content += '}\n'

            # Optimization settings
            if input_pinned_memory or output_pinned_memory or self.gpus_count > 0:
                config_content += 'optimization {\n'
                if input_pinned_memory:
                    config_content += '  input_pinned_memory {\n'
                    config_content += '    enable: true\n'
                    config_content += '  }\n'
                if output_pinned_memory:
                    config_content += '  output_pinned_memory {\n'
                    config_content += '    enable: true\n'
                    config_content += '  }\n'
                if self.gpus_count > 0 and self.use_trt_accelerator:
                    config_content += '  execution_accelerators {\n'
                    config_content += '    gpu_execution_accelerator {\n'
                    config_content += '      name: "tensorrt"\n'
                    config_content += '      parameters {\n'
                    config_content += '        key: "precision_mode"\n'
                    config_content += '        value: "FP16"\n'
                    config_content += '      }\n'
                    config_content += '      parameters {\n'
                    config_content += '        key: "max_workspace_size_bytes"\n'
                    config_content += '        value: "1073741824"\n'
                    config_content += '      }\n'
                    config_content += '      parameters {\n'
                    config_content += '        key: "trt_engine_cache_enable"\n'
                    config_content += '        value: "1"\n'
                    config_content += '      }\n'
                    config_content += '      parameters {\n'
                    config_content += '        key: "trt_engine_cache_path"\n'
                    config_content += f'        value: "/models/{self.model_name}/1"\n'
                    config_content += '      }\n'
                    config_content += '    }\n'
                    config_content += '  }\n'
                config_content += '}\n'

            with open(config_path, "w") as f:
                f.write(config_content)
            
            logging.info("Config file written successfully")
            logging.info("Config content:\n%s", config_content)
            
        except Exception as e:
            logging.error("Failed to write config file: %s", str(e), exc_info=True)
            raise

    def get_config_params(self):
        """Get configuration parameters for Triton config file"""
        try:
            logging.info("Retrieving configuration parameters")
            
            logging.info("Using input size: %s", self.input_size)
            logging.info("Using number of classes: %s", self.num_classes)
            
            params = {
                "max_batch_size": self.max_batch_size,
                "num_instances": self.num_model_instances,
                "image_size": self.input_size,
                "num_classes": self.num_classes,
                "input_data_type": "TYPE_FP32",
                "output_data_type": "TYPE_FP32",
                "dynamic_batching": self.dynamic_batching,  
                "preferred_batch_size": [1, 2, 4, 8],
                "max_queue_delay_microseconds": 100,
                "input_pinned_memory": True,
                "output_pinned_memory": True,
            }
                
            logging.debug("Final configuration parameters: %s", params)
            return params
            
        except Exception as e:
            logging.error(
                "Failed to get configuration parameters: %s",
                str(e),
                exc_info=True,
            )
            raise


    def start_server(self, internal_port: int = 8000):
        """Start the Triton Inference Server
        
        Args:
            internal_port: Port to expose the server on
        """
        gpu_option = "--gpus=all " if self.gpus_count > 0 else ""
        logging.debug("Starting Triton server with GPU option: '%s'", gpu_option.strip())
        triton_port = 8000 if self.connection_protocol == 'rest' else 8001
        port_mapping = f"-p{internal_port}:{triton_port}"
        start_triton_server = f"docker run {gpu_option}--rm {port_mapping} -v {os.path.abspath(BASE_PATH)}:/models --label model_name={self.model_name} {TRITON_DOCKER_IMAGE} tritonserver --model-repository=/models "
        logging.info("Checking docker image download status before starting server")
        self.check_triton_docker_image()
        try:
            logging.info(
                "Starting Triton server with command: %s",
                start_triton_server,
            )
            self.process = subprocess.Popen(
                shlex.split(start_triton_server),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            def log_output():
                while True:
                    stdout_line = self.process.stdout.readline()
                    stderr_line = self.process.stderr.readline()
                    if stdout_line:
                        logging.info(stdout_line.strip())
                    if stderr_line:
                        logging.info(stderr_line.strip())
                    if stdout_line == "" and stderr_line == "" and self.process.poll() is not None:
                        break

            threading.Thread(target=log_output, daemon=True).start()
            logging.info(
                "Triton server started successfully on port %s",
                internal_port,
            )
            return self.process
        except Exception as e:
            logging.error(
                "Failed to start Triton server: %s",
                str(e),
                exc_info=True,
            )
            raise

    def setup(self, internal_port: int = 8000):
        """Setup the Triton server with the provided model.
        
        Args:
            internal_port: Port to expose the server on
        """
        try:
            logging.info("Beginning Triton server setup")
            logging.info("Step 1: Creating model repository")
            self.model_dir, self.version_dir = self.create_model_repository()
            logging.info("Step 2: Preparing model")
            self.prepare_model(self.version_dir)
            logging.info("Step 3: Getting configuration parameters")
            self.config_params = self.get_config_params()
            logging.info("Step 4: Writing configuration file")
            self.write_config_file(
                self.model_dir,
                **self.config_params,
            )
            logging.info("Step 5: Starting Triton server")
            self.process = self.start_server(internal_port)
            logging.info("Triton server setup completed successfully")
            return self.process
        except Exception as e:
            logging.error(
                "Triton server setup failed: %s",
                str(e),
                exc_info=True,
            )
            raise


"""Module providing inference_utils functionality for FastAPI and Triton inference."""

from PIL import Image
import httpx
import logging
from typing import Optional, Dict, Union, Any
from datetime import datetime, timezone
from io import BytesIO
import numpy as np

import numpy as np
import torch
import torchvision
from typing import Tuple, Dict, Any, Optional, Union
import logging
from PIL import Image
from io import BytesIO
import os
from datetime import datetime, timezone

class TritonInference:
    """Class for making Triton inference requests."""

    def __init__(
        self,
        server_type: str,
        model_name: str,
        internal_port: int = 80,
        internal_host: str = "localhost",
        task_type: str = "detection",
        runtime_framework: str = "onnx",
        is_yolo: bool = False,
        input_size: Union[int, List[int]] = 224,
        action_tracker: Optional[Any] = None,
    ):
        """Initialize Triton inference client.

        Args:
            server_type: Type of server (grpc/rest)
            model_name: Name of model to use
            internal_port: Port number for internal API
            internal_host: Hostname for internal API
            task_type: Type of task (e.g., detection)
            runtime_framework: Framework used for the model (e.g., onnx)
            is_yolo: Boolean indicating if the model is YOLO
            input_size: Input size for the model (int or [height, width])
            action_tracker: Optional action tracker for tracking actions
        """
        self.model_name = model_name
        self.task_type = task_type
        self.runtime_framework = runtime_framework
        self.is_yolo = is_yolo

        if self.is_yolo:
            self.input_size = 640
        else:
            self.input_size = 224
        self.action_tracker = action_tracker
        # self.input_size = self.action_tracker.get_input_size() if self.action_tracker else self.input_size

        self.data_type_mapping = {
            6: "TYPE_INT8",
            7: "TYPE_INT16",
            8: "TYPE_INT32",
            9: "TYPE_INT64",
            10: "TYPE_FP16",
            11: "TYPE_FP32",
            12: "TYPE_FP64",
        }
        self.numpy_data_type_mapping = {
            "INT8": np.int8,
            "INT16": np.int16,
            "INT32": np.int32,
            "INT64": np.int64,
            "FP16": np.float16,
            "FP32": np.float32,
            "FP64": np.float64,
        }
        self.setup_client_funcs = {
            "grpc": self._setup_grpc_client,
            "rest": self._setup_rest_client,
        }
        self.url = f"{internal_host}:{internal_port}"
        self.connection_protocol = "grpc" if "grpc" in server_type else "rest"
        self.tritonclientclass = None
        self._dependencies_check()
        self.client_info = self.setup_client_funcs[self.connection_protocol]()
        logging.info(
            "Initialized TritonClientUtils with %s protocol",
            self.connection_protocol,
        )

    def _dependencies_check(self):
        """Check and import required Triton dependencies."""
        try:
            if self.connection_protocol == "rest":
                import tritonclient.http as tritonclientclass
            else:
                import tritonclient.grpc as tritonclientclass
            self.tritonclientclass = tritonclientclass
        except ImportError as err:
            package_name = "tritonclient[http]" if self.connection_protocol == "rest" else "tritonclient[grpc]"
            logging.error(
                "Failed to import tritonclient (%s): %s. Please install with: pip install %s",
                package_name, err, package_name
            )
            raise ImportError(f"Required package {package_name} not installed: {err}")
        except Exception as err:
            logging.error(
                "Failed to import tritonclient: %s",
                err,
            )
            raise

    def _setup_rest_client(self):
        """Setup REST client and model configuration.

        Returns:
            Dictionary containing client configuration
        """
        client = self.tritonclientclass.InferenceServerClient(url=self.url)
        model_config = client.get_model_config(model_name=self.model_name, model_version="1")
        input_config = model_config["input"][0]
        input_shape = [1] + input_config["dims"]  # Prepend batch dimension
        input_obj = self.tritonclientclass.InferInput(
            input_config["name"],
            input_shape,
            input_config["data_type"].split("_")[-1],
        )
        output = self.tritonclientclass.InferRequestedOutput(model_config["output"][0]["name"])
        return {
            "client": client,
            "input": input_obj,
            "output": output,
        }

    def _setup_grpc_client(self):
        """Setup gRPC client and model configuration.

        Returns:
            Dictionary containing client configuration
        """
        client = self.tritonclientclass.InferenceServerClient(url=self.url)
        model_config = client.get_model_config(model_name=self.model_name, model_version="1")
        input_config = model_config.config.input[0]
        input_shape = [1] + list(input_config.dims)  # Prepend batch dimension
        input_obj = self.tritonclientclass.InferInput(
            input_config.name,
            input_shape,
            self.data_type_mapping[input_config.data_type].split("_")[-1],
        )
        output = self.tritonclientclass.InferRequestedOutput(model_config.config.output[0].name)
        return {
            "client": client,
            "input": input_obj,
            "output": output,
        }

    def inference(self, input_data: Union[bytes, np.ndarray]) -> np.ndarray:
        """Make a synchronous inference request.

        Args:
            input_data: Input data as bytes or stacked numpy array

        Returns:
            Model prediction as numpy array

        Raises:
            Exception: If inference fails
        """
        try:
            # If already preprocessed ndarray, make it C-contiguous FP32.
            if isinstance(input_data, np.ndarray):
                input_array = np.ascontiguousarray(input_data, dtype=np.float32)
                if input_array.ndim == 5 and input_array.shape[1] == 1:
                    # [B, 1, C, H, W] -> [B, C, H, W]
                    input_array = np.ascontiguousarray(
                        input_array.reshape(input_array.shape[0],
                                           input_array.shape[2],
                                           input_array.shape[3],
                                           input_array.shape[4]),
                        dtype=np.float32
                    )
            else:
                # -> [1, C, H, W], FP32, contiguous
                input_array = self._preprocess_input(input_data)

            # Update InferInput shape to match batch (N,C,H,W)
            self.client_info["input"].set_shape(list(input_array.shape))
            self.client_info["input"].set_data_from_numpy(input_array)

            if self.connection_protocol == "rest":
                resp = self.client_info["client"].infer(
                    model_name=self.model_name,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                )
            else:
                resp = self.client_info["client"].infer(
                    model_name=self.model_name,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                )
                
            return resp.as_numpy(self.client_info["output"].name())

        except Exception as err:
            logging.error("Triton inference failed: %s", err, exc_info=True)
            raise Exception(f"Triton inference failed: {err}") from err

    async def async_inference(self, input_data: Union[bytes, np.ndarray]) -> np.ndarray:
        """Make an asynchronous inference request (REST + gRPC)."""
        try:
            logging.debug("Making async inference request")

            if isinstance(input_data, np.ndarray):
                input_array = input_data
            else:
                input_array = self._preprocess_input(input_data)

            # Ensure C-contiguous
            if not input_array.flags.c_contiguous:
                input_array = np.ascontiguousarray(input_array)

            self.client_info["input"].set_shape(list(input_array.shape))
            self.client_info["input"].set_data_from_numpy(input_array)

            if self.connection_protocol == "rest":
                # REST: async_infer -> InferAsyncRequest, then block with get_result()
                resp = self.client_info["client"].async_infer(
                    model_name=self.model_name,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                )
                result = resp.get_result()

            else:
                # gRPC: async_infer uses callback; wrap it into an awaitable Future
                loop = asyncio.get_running_loop()
                fut: asyncio.Future = loop.create_future()

                def _callback(result, error):
                    if error is not None:
                        loop.call_soon_threadsafe(fut.set_exception, error)
                    else:
                        loop.call_soon_threadsafe(fut.set_result, result)

                self.client_info["client"].async_infer(
                    model_name=self.model_name,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                    callback=_callback,
                )
                result = await fut

            logging.debug(f"Async inference response type: {type(result)}")
            logging.info("Successfully got async inference result")

            output_array = result.as_numpy(self.client_info["output"].name())
            logging.info(f"Output shape: {output_array.shape}")
            return output_array  

        except Exception as err:
            logging.error(f"Async Triton inference failed: {err}")
            raise Exception(f"Async Triton inference failed: {err}") from err
   
    def _preprocess_input(self, input_data) -> np.ndarray:
        """Preprocess input data for YOLOv8 inference.

        Args:
            input_data: Raw input bytes or string (file path)

        Returns:
            Preprocessed numpy array ready for inference
        """
        resize_shape = [int(self.input_size), int(self.input_size)]
        input_shape = [1, 3, resize_shape[0], resize_shape[1]]

        if isinstance(input_data, str) and os.path.exists(input_data):
            with open(input_data, "rb") as f:
                input_data = f.read()

        if isinstance(input_data, bytes):
            try:
                # Image file (JPEG/PNG)
                image = Image.open(BytesIO(input_data)).convert("RGB")
            except Exception as e:
                logging.warning(f"Failed to open input data as image: {e}")
                # Handle raw RGB bytes (video frames, 640x640x3) -- YoLov8 default
                arr = np.frombuffer(input_data, dtype=np.uint8).reshape(640, 640, 3)
                image = Image.fromarray(arr, mode="RGB")
        elif isinstance(input_data, np.ndarray):
            # np.ndarray (direct frame input)
            image = Image.fromarray(input_data, mode="RGB")
        else:
            raise ValueError(f"Unsupported input_data type: {type(input_data)}")

        if self.is_yolo:
            # TODO: Verify and Generalize for Obj Det models
            logging.debug("Preprocessing input for YOLO model")
            # YOLO preprocessing: resize with letterbox padding, normalize to [0, 1]
            image, ratio, (dw, dh) = self._letterbox_resize(image, resize_shape)
            arr = np.array(image).astype(np.float32) / 255.0
            arr = arr.transpose(2, 0, 1)  # Convert to CHW
            arr = np.expand_dims(arr, axis=0)  # Add batch dimension
            self.client_info["padding_info"] = {"ratio": ratio, "dw": dw, "dh": dh}
        else:
            # Classifier preprocessing: resize directly, ImageNet normalization
            image = image.resize(resize_shape)
            arr = np.array(image).astype(np.float32) / 255.0
            arr = arr.transpose(2, 0, 1)  # Convert to CHW
            arr = np.expand_dims(arr, axis=0)  # Add batch dimension
            mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1, 3, 1, 1)
            std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1, 3, 1, 1)
            arr = (arr - mean) / std

        arr = arr.astype(self.numpy_data_type_mapping[self.client_info["input"].datatype()])
        logging.debug("Preprocessed input shape: %s", arr.shape)
        return arr

    def _letterbox_resize(self, image, target_size):
        """Resize image with letterbox padding to maintain aspect ratio."""
        target_h, target_w = target_size
        img_w, img_h = image.size
        ratio = min(target_w / img_w, target_h / img_h)
        new_w, new_h = int(img_w * ratio), int(img_h * ratio)
        image = image.resize((new_w, new_h), Image.LANCZOS)
        padded_image = Image.new("RGB", (target_w, target_h), (114, 114, 114))
        dw, dh = (target_w - new_w) // 2, (target_h - new_h) // 2
        padded_image.paste(image, (dw, dh))
        logging.debug("Letterbox resize: original size %s, new size %s, padding (dw, dh) (%d, %d)", (img_w, img_h), (new_w, new_h), dw, dh)
        logging.debug("Letterbox resize completed for target size: %s", target_size)
        return padded_image, ratio, (dw, dh)

    def _postprocess_yolo(
        self,
        outputs: np.ndarray,
        conf_thres: float = 0.25,
        iou_thres: float = 0.45,
        max_det: int = 300
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Postprocess YOLOv8 outputs (Torch or ONNX/Triton) with pipeline compatibility.

        Args:
            outputs: Raw model output as NumPy array, expected shape [batch, num_boxes, num_classes + 4] for YOLO
            conf_thres: Confidence threshold for filtering detections
            iou_thres: IoU threshold for Non-Maximum Suppression
            max_det: Maximum number of detections to keep

        Returns:
            Tuple of (boxes, scores, class_ids) as NumPy arrays:
            - boxes: [N, 4] array of bounding boxes in xyxy format
            - scores: [N] array of confidence scores
            - class_ids: [N] array of class IDs
        """
        if not self.is_yolo:
            return outputs, np.array([]), np.array([])

        try:
            if isinstance(outputs, np.ndarray):
                outputs = torch.from_numpy(outputs)
            elif not isinstance(outputs, torch.Tensor):
                outputs = torch.tensor(outputs, dtype=torch.float32)

            if outputs.ndim == 2:
                outputs = outputs.unsqueeze(0)
                
            if outputs.shape[1] < outputs.shape[2]:
                # Format [batch, num_classes + 4, num_boxes] -> [batch, num_boxes, num_classes + 4]
                outputs = outputs.transpose(1, 2)  

            boxes = outputs[..., :4]  # xywh, [batch, num_boxes, 4]
            scores_all = outputs[..., 4:]  # class scores, [batch, num_boxes, num_classes]

            all_boxes, all_scores, all_class_ids = [], [], []
            for batch_idx in range(outputs.shape[0]):
                batch_boxes = boxes[batch_idx]  # [num_boxes, 4]
                batch_scores_all = scores_all[batch_idx]  # [num_boxes, num_classes]

                # Get best class per box
                scores, class_ids = batch_scores_all.max(dim=-1)  

                # Confidence filter
                mask = scores > conf_thres
                batch_boxes = batch_boxes[mask]
                batch_scores = scores[mask]
                batch_class_ids = class_ids[mask]

                # Convert xywh -> xyxy
                if batch_boxes.shape[0] > 0:
                    xyxy = torch.zeros_like(batch_boxes)
                    xyxy[:, 0] = batch_boxes[:, 0] - batch_boxes[:, 2] / 2  # x1
                    xyxy[:, 1] = batch_boxes[:, 1] - batch_boxes[:, 3] / 2  # y1
                    xyxy[:, 2] = batch_boxes[:, 0] + batch_boxes[:, 2] / 2  # x2
                    xyxy[:, 3] = batch_boxes[:, 1] + batch_boxes[:, 3] / 2  # y2
                    batch_boxes = xyxy

                    # Adjust for letterbox padding if provided
                    padding_info = self.client_info.get("padding_info", {})
                    if padding_info:
                        ratio = padding_info.get("ratio", 1.0)
                        dw = padding_info.get("dw", 0)
                        dh = padding_info.get("dh", 0)
                        batch_boxes[:, 0] = (batch_boxes[:, 0] - dw) / ratio  # x1
                        batch_boxes[:, 1] = (batch_boxes[:, 1] - dh) / ratio  # y1
                        batch_boxes[:, 2] = (batch_boxes[:, 2] - dw) / ratio  # x2
                        batch_boxes[:, 3] = (batch_boxes[:, 3] - dh) / ratio  # y2

                    # NMS
                    if batch_boxes.shape[0] > 0:
                        keep = torchvision.ops.nms(batch_boxes, batch_scores, iou_thres)
                        batch_boxes = batch_boxes[keep]
                        batch_scores = batch_scores[keep]
                        batch_class_ids = batch_class_ids[keep]

                    if batch_boxes.shape[0] > max_det:
                        topk = batch_scores.topk(max_det).indices
                        batch_boxes = batch_boxes[topk]
                        batch_scores = batch_scores[topk]
                        batch_class_ids = batch_class_ids[topk]

                all_boxes.append(batch_boxes.cpu().numpy())
                all_scores.append(batch_scores.cpu().numpy())
                all_class_ids.append(batch_class_ids.cpu().numpy())

            boxes = np.concatenate(all_boxes, axis=0) if all_boxes else np.empty((0, 4))
            scores = np.concatenate(all_scores, axis=0) if all_scores else np.empty(0)
            class_ids = np.concatenate(all_class_ids, axis=0) if all_class_ids else np.empty(0)

            return boxes, scores, class_ids

        except Exception as e:
            logging.error("YOLO post-processing failed: %s", str(e), exc_info=True)
            return np.empty((0, 4)), np.empty(0), np.empty(0)

    def format_response(self, response: np.ndarray) -> Dict[str, Any]:
        """Format model response for consistent logging.

        Args:
            response: Raw model output

        Returns:
            Formatted response dictionary
        """
        if self.is_yolo:
            boxes, scores, class_ids = self._postprocess_yolo(
                response,
                conf_thres=0.25,
                iou_thres=0.45,
                max_det=300
            )
            predictions = {
                "boxes": boxes.tolist(),
                "scores": scores.tolist(),
                "class_ids": class_ids.tolist()
            }
        else:
            predictions = response.tolist() if isinstance(response, np.ndarray) else response

        return {
            "predictions": predictions,
            "model_id": self.model_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }