"""Module providing triton_server functionality."""

import os
import zipfile
import subprocess
import logging
import threading
import shlex
from matrice.docker_utils import pull_docker_image
from matrice.utils import dependencies_check

TRITON_DOCKER_IMAGE = "nvcr.io/nvidia/tritonserver:23.08-py3"
BASE_PATH = "./model_repository"


class MatriceTritonServer:

    def __init__(self, action_tracker):
        dependencies_check("torch")
        import torch

        logging.info("Initializing MatriceTritonServer")
        self.action_tracker = action_tracker
        self.action_details = action_tracker.action_details
        self.model_id = self.action_details["_idModelDeploy"]
        self.deployment_id = self.action_details["_idDeployment"]
        self.deployment_instance_id = self.action_details["_idModelDeployInstance"]
        logging.info("Model ID: %s", self.model_id)
        logging.info(
            "Deployment ID: %s",
            self.deployment_id,
        )
        logging.info(
            "Deployment Instance ID: %s",
            self.deployment_instance_id,
        )
        self.connection_protocol = (
            "grpc" if "grpc" in self.action_details.get("server_type", "rest").lower() else "rest"
        )
        logging.info(
            "Using connection protocol: %s",
            self.connection_protocol,
        )
        self.job_params = self.action_tracker.get_job_params()
        logging.debug("Job parameters: %s", self.job_params)
        self.gpus_count = torch.cuda.device_count()
        logging.info(
            "Found %s GPUs available for inference",
            self.gpus_count,
        )
        self.docker_pull_process = pull_docker_image(TRITON_DOCKER_IMAGE)

    def check_triton_docker_image(self):
        """Check if docker image download is complete and wait for it to finish"""
        logging.info("Checking docker image download status")
        stdout, stderr = self.docker_pull_process.communicate()
        if self.docker_pull_process.returncode == 0:
            logging.info(
                "Docker image %s downloaded successfully",
                TRITON_DOCKER_IMAGE,
            )
        else:
            error_msg = stderr.decode()
            logging.error(
                "Docker pull failed with return code %s",
                self.docker_pull_process.returncode,
            )
            logging.error("Error message: %s", error_msg)
            raise RuntimeError(f"Docker pull failed: {error_msg}")

    def download_model(self, model_version_dir):
        """Download and extract the model files"""
        try:
            runtime_framework = self.action_tracker.export_format.lower()
            logging.info(
                "Downloading model with runtime framework: %s",
                runtime_framework,
            )
            model_map = {
                "onnx": "model.onnx",
                "torchscript": "model.pt",
                "pytorch": "model.pt",
                "tensorrt": "model.engine",
                "openvino": "model_openvino.zip",
            }
            if runtime_framework not in model_map:
                logging.error(
                    "Runtime framework '%s' not supported. Supported frameworks: %s",
                    runtime_framework,
                    list(model_map.keys()),
                )
                raise ValueError(f"Unsupported runtime framework: {runtime_framework}")
            model_file = os.path.join(
                model_version_dir,
                model_map[runtime_framework],
            )
            logging.info(
                "Downloading model to path: %s",
                model_file,
            )
            model_type = "exported" if self.action_tracker.is_exported else "trained"
            logging.info("Model type: %s", model_type)
            self.action_tracker.download_model(model_file, model_type=model_type)
            logging.info("Model download completed successfully")
            if runtime_framework == "pytorch":

                def compile_torch_model(
                    model_path: str,
                ):
                    import torch

                    logging.info("Compiling PyTorch model")
                    if self.gpus_count > 0:
                        model = torch.load(model_path)
                    else:
                        model = torch.load(
                            model_path,
                            map_location=torch.device("cpu"),
                        )
                    model.eval()
                    compiled_model = torch.jit.script(model)
                    compiled_model.save(model_path)
                    logging.info("PyTorch model compiled successfully")

                compile_torch_model(model_file)
            if runtime_framework == "openvino":
                logging.info("Starting OpenVINO model extraction")
                with zipfile.ZipFile("model_openvino.zip", "r") as zip_ref:
                    zip_ref.extractall("model_openvino")
                logging.info("OpenVINO model extracted successfully")
        except Exception as e:
            logging.error(
                "Model download failed: %s",
                str(e),
                exc_info=True,
            )
            raise

    def create_model_repository(self):
        """Create the model repository directory structure"""
        try:
            model_version = "1"
            model_dir = os.path.join(BASE_PATH, self.model_id)
            version_dir = os.path.join(model_dir, str(model_version))
            logging.info("Creating model repository structure:")
            logging.info("Base path: %s", BASE_PATH)
            logging.info("Model directory: %s", model_dir)
            logging.info(
                "Version directory: %s",
                version_dir,
            )
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
        model_dir,
        max_batch_size=0,
        num_model_instances=1,
        image_size=[224, 224],
        num_classes=10,
        input_data_type: str = "TYPE_FP32",
        output_data_type: str = "TYPE_FP32",
        dynamic_batching: bool = False,
        preferred_batch_size: list = [2, 4, 8],
        max_queue_delay_microseconds: int = 100,
        input_pinned_memory: bool = True,
        output_pinned_memory: bool = True,
        **kwargs,
    ):
        """Write the model configuration file for Triton Inference Server"""
        try:
            runtime_framework = self.action_tracker.export_format.lower()
            logging.info("Starting to write Triton config file")
            platform_map = {
                "onnx": "onnxruntime_onnx",
                "tensorrt": "tensorrt_plan",
                "pytorch": "pytorch_libtorch",
                "torchscript": "pytorch_libtorch",
                "openvino": "openvino",
            }
            platform = platform_map.get(runtime_framework)
            if not platform:
                logging.error(
                    "Runtime framework '%s' not found in platform map",
                    runtime_framework,
                )
                raise ValueError(f"Unsupported runtime framework: {runtime_framework}")
            config_path = os.path.join(model_dir, "config.pbtxt")
            logging.info(
                "Writing config to: %s",
                config_path,
            )
            config_str = """
            name: "{self.model_id}"
            platform: "{platform}"
            max_batch_size: {max_batch_size}
            """
            if platform == "pytorch_libtorch":
                logging.info("Adding PyTorch-specific configuration")
                config_str += """
                # Input configuration
                input [
                {{
                name: "input__0"
                data_type: {input_data_type}
                dims: [ 3, {image_size[0]}, {image_size[1]} ]
                }}
                ]

                # Output configuration
                output [
                {{
                    name: "output__0"
                    data_type: {output_data_type}
                    dims: [ {num_classes} ]
                }}
                ]
                """
            if num_model_instances > 1:
                device_type = "KIND_GPU" if self.gpus_count > 0 else "KIND_CPU"
                logging.info(
                    "Adding instance group configuration for %s %s instances",
                    num_model_instances,
                    device_type,
                )
                config_str += """
                # Instance groups for GPU/CPU execution
                instance_group [
                {{
                    count: {num_model_instances}
                    kind: {device_type}
                }}
                ]
                """
            if dynamic_batching:
                logging.info("Adding dynamic batching configuration")
                config_str += """
                # Dynamic batching config
                dynamic_batching {{
                    preferred_batch_size: {preferred_batch_size}
                    max_queue_delay_microseconds: {max_queue_delay_microseconds}
                }}
                """
            if not input_pinned_memory or not output_pinned_memory:
                logging.info("Adding pinned memory configuration")
                config_str += """
                optimization {{
                    input_pinned_memory {{
                        enable: {input_pinned_memory}
                    }}
                    output_pinned_memory {{
                        enable: {output_pinned_memory}
                    }}
                }}
                """
            with open(config_path, "w") as f:
                f.write(config_str)
            logging.info("Config file written successfully")
            logging.info("Config content:\n%s", config_str)
        except Exception as e:
            logging.error(
                "Failed to write config file: %s",
                str(e),
                exc_info=True,
            )
            raise

    def get_config_params(self):
        try:
            logging.info("Retrieving configuration parameters")
            input_size = self.action_tracker.get_input_size()
            num_classes = len(
                self.action_tracker.get_index_to_category(self.action_tracker.is_exported)
            )
            logging.info(
                "Retrieved input size: %s",
                input_size,
            )
            logging.info(
                "Retrieved number of classes: %s",
                num_classes,
            )
            params = {
                "max_batch_size": 8,
                "num_model_instances": 1,
                "image_size": [
                    input_size,
                    input_size,
                ],
                "num_classes": num_classes,
                "input_data_type": "TYPE_FP32",
                "output_data_type": "TYPE_FP32",
                "dynamic_batching": False,
                "preferred_batch_size": [2, 4, 8],
                "max_queue_delay_microseconds": 100,
                "input_pinned_memory": True,
                "output_pinned_memory": True,
            }
            params.update(self.job_params)
            logging.debug(
                "Final configuration parameters: %s",
                params,
            )
            return params
        except Exception as e:
            logging.error(
                "Failed to get configuration parameters: %s",
                str(e),
                exc_info=True,
            )
            raise

    def start_server(self):
        """Start the Triton Inference Server"""
        gpu_option = "--gpus=all " if self.gpus_count > 0 else ""
        port_mapping = f"-p{os.environ['INTERNAL_PORT']}:{8000 if self.connection_protocol == 'rest' else 8001}"
        start_triton_server = f"docker run {gpu_option}--rm {port_mapping} -v {os.path.abspath(BASE_PATH)}:/models --label action_id={self.action_tracker.action_id_str} {TRITON_DOCKER_IMAGE} tritonserver --model-repository=/models "
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
                os.environ.get("INTERNAL_PORT"),
            )
            return self.process
        except Exception as e:
            logging.error(
                "Failed to start Triton server: %s",
                str(e),
                exc_info=True,
            )
            raise

    def setup(self):
        try:
            logging.info("Beginning Triton server setup")
            logging.info("Step 1: Creating model repository")
            self.model_dir, self.version_dir = self.create_model_repository()
            logging.info("Step 2: Downloading model")
            self.download_model(self.version_dir)
            logging.info("Step 3: Getting configuration parameters")
            self.config_params = self.get_config_params()
            logging.info("Step 4: Writing configuration file")
            self.write_config_file(
                self.model_dir,
                **self.config_params,
            )
            logging.info("Step 5: Starting Triton server")
            self.process = self.start_server()
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
from matrice.utils import dependencies_check


class TritonInference:
    """Class for making Triton inference requests."""

    def __init__(
        self,
        server_type: str,
        model_id: str,
        internal_port: int = 80,
        internal_host: str = "localhost",
    ):
        """Initialize Triton inference client.

        Args:
            server_type: Type of server (grpc/rest)
            model_id: ID of model to use
            internal_port: Port number for internal API
            internal_host: Hostname for internal API
        """
        self.model_id = model_id
        self.data_type_mapping = {
            (6): "TYPE_INT8",
            (7): "TYPE_INT16",
            (8): "TYPE_INT32",
            (9): "TYPE_INT64",
            (10): "TYPE_FP16",
            (11): "TYPE_FP32",
            (12): "TYPE_FP64",
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
                dependencies_check(["tritonclient[http]"])
                import tritonclient.http as tritonclientclass
            else:
                dependencies_check(["tritonclient[grpc]"])
                import tritonclient.grpc as tritonclientclass
            self.tritonclientclass = tritonclientclass
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
        model_config = client.get_model_config(
            model_name=self.model_id,
            model_version="1",
        )
        input_shape = [1, 3, 244, 244][: 4 - len(model_config["input"][0]["dims"])] + model_config[
            "input"
        ][0]["dims"]
        input_obj = self.tritonclientclass.InferInput(
            model_config["input"][0]["name"],
            input_shape,
            model_config["input"][0]["data_type"].split("_")[-1],
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
        model_config = client.get_model_config(
            model_name=self.model_id,
            model_version="1",
        )
        input_shape = [1, 3, 244, 244][: 4 - len(model_config.config.input[0].dims)] + list(
            model_config.config.input[0].dims
        )
        input_obj = self.tritonclientclass.InferInput(
            model_config.config.input[0].name,
            input_shape,
            self.data_type_mapping[model_config.config.input[0].data_type].split("_")[-1],
        )
        output = self.tritonclientclass.InferRequestedOutput(model_config.config.output[0].name)
        return {
            "client": client,
            "input": input_obj,
            "output": output,
        }

    def inference(self, input_data: bytes) -> np.ndarray:
        """Make a synchronous inference request.

        Args:
            input_data: Input data as bytes

        Returns:
            Model prediction as numpy array

        Raises:
            Exception: If inference fails
        """
        try:
            logging.debug(
                "Making inference request for instance %s",
                self.url,
            )
            input_array = self._preprocess_input(input_data)
            self.client_info["input"].set_data_from_numpy(input_array)
            resp = self.client_info["client"].infer(
                model_name=self.model_id,
                model_version="1",
                inputs=[self.client_info["input"]],
                outputs=[self.client_info["output"]],
            )
            logging.debug("Successfully got inference result")
            return resp.as_numpy(self.client_info["output"].name())
        except Exception as err:
            logging.error("Triton inference failed: %s", err)
            raise Exception(f"Triton inference failed: {err}") from err

    async def async_inference(self, input_data: bytes) -> np.ndarray:
        """Make an asynchronous inference request.

        Args:
            input_data: Input data as bytes

        Returns:
            Model prediction as numpy array

        Raises:
            Exception: If inference fails
        """
        try:
            logging.debug(
                "Making async inference request for instance %s",
                self.url,
            )
            input_array = self._preprocess_input(input_data)
            self.client_info["input"].set_data_from_numpy(input_array)
            if self.connection_protocol == "rest":
                resp = await self.client_info["client"].async_infer(
                    model_name=self.model_id,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                )
            else:
                resp = await self.client_info["client"].infer_async(
                    model_name=self.model_id,
                    model_version="1",
                    inputs=[self.client_info["input"]],
                    outputs=[self.client_info["output"]],
                )
            logging.debug("Successfully got async inference result")
            return resp.as_numpy(self.client_info["output"].name())
        except Exception as err:
            logging.error(
                "Async Triton inference failed: %s",
                err,
            )
            raise Exception(f"Async Triton inference failed: {err}") from err

    def _preprocess_input(self, input_data: bytes) -> np.ndarray:
        """Preprocess input data for model inference.

        Args:
            input_data: Raw input bytes

        Returns:
            Preprocessed numpy array ready for inference
        """
        image = Image.open(BytesIO(input_data)).convert("RGB")
        image = image.resize(self.client_info["input"].shape()[2:])
        array = np.array(image).astype(
            self.numpy_data_type_mapping[self.client_info["input"].datatype()]
        )
        array = array.transpose(2, 0, 1)
        array = np.expand_dims(array, axis=0)
        return array

    def format_response(self, response: np.ndarray) -> Dict[str, Any]:
        """Format model response for consistent logging.

        Args:
            response: Raw model output

        Returns:
            Formatted response dictionary
        """
        return {
            "predictions": (response.tolist() if isinstance(response, np.ndarray) else response),
            "model_id": self.model_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
