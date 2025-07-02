import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import socket
import sys
import os
import requests
import threading
from datetime import datetime

from .constants import VLLM_SUFFIX


class ProcessStatus:
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"


class VLLMPyManager:
    """
    A native vLLM engine manager that provides direct access to the vLLM LLM class.
    This replaces the subprocess-based API server approach with direct Python API access.

    Example usage:
        from vllm.sampling_params import SamplingParams, GuidedDecodingParams

        engine = current.vllm.engine
        sampling_params = SamplingParams(temperature=0.7, max_tokens=150)
        outputs = engine.generate(["Hello, world!"], sampling_params)

        # Structured outputs
        guided_params = GuidedDecodingParams(json=my_schema)
        sampling_params = SamplingParams(guided_decoding=guided_params)
        outputs = engine.generate(prompts, sampling_params)
    """

    def __init__(
        self,
        model,
        debug=False,
        **engine_args,
    ):
        if isinstance(model, list):
            if len(model) != 1:
                raise ValueError(
                    f"vLLM native engine can only serve one model per instance. "
                    f"Got {len(model)} models: {model}. "
                    f"Please specify a single model or create multiple @vllm decorators."
                )
            self.model = model[0]
        else:
            self.model = model

        self.debug = debug
        self.engine_args = engine_args
        self.engine = None
        self.initialization_start = time.time()

        if self.debug:
            print(
                f"[@vllm-native] Initializing native vLLM engine for model: {self.model}"
            )

        self._validate_vllm_installation()
        self._initialize_engine()

        total_init_time = time.time() - self.initialization_start
        if self.debug:
            print(
                f"[@vllm-native] Native engine initialization completed in {total_init_time:.1f}s"
            )

    def _validate_vllm_installation(self):
        """Validate that vLLM is properly installed"""
        try:
            import vllm

            if self.debug:
                print(f"[@vllm-native] vLLM {vllm.__version__} is available")
        except ImportError as e:
            raise ImportError(
                "vLLM not installed. Please add vLLM to your environment."
            ) from e

    def _map_engine_args(self, engine_args):
        """
        Map CLI-style engine_args to LLM constructor parameters.
        Most parameters map directly from the API server CLI args to LLM constructor.
        """
        llm_params = {}

        # Direct mappings (parameter names are the same)
        direct_mapping = [
            "tensor_parallel_size",
            "max_model_len",
            "gpu_memory_utilization",
            "swap_space",
            "dtype",
            "quantization",
            "seed",
            "trust_remote_code",
            "revision",
            "tokenizer_revision",
            "enforce_eager",
            "max_seq_len_to_capture",
            "disable_custom_all_reduce",
        ]

        for param in direct_mapping:
            if param in engine_args:
                llm_params[param] = engine_args[param]

        # Handle special mappings if needed
        # (Most/all vLLM CLI args map directly to LLM constructor args)

        return llm_params

    def _initialize_engine(self):
        """Initialize the native vLLM LLM engine"""
        try:
            from vllm import LLM

            # Map engine args to LLM constructor parameters
            llm_params = self._map_engine_args(self.engine_args)

            if self.debug:
                print(f"[@vllm] Initializing LLM with params: {llm_params}")

            # Initialize the native vLLM engine
            self.engine = LLM(model=self.model, **llm_params)

            if self.debug:
                print(f"[@vllm] LLM engine initialized successfully")

        except Exception as e:
            error_msg = f"Failed to initialize vLLM engine: {str(e)}"
            if self.debug:
                print(f"[@vllm-native] ERROR: {error_msg}")
            raise RuntimeError(error_msg) from e

    def terminate_engine(self):
        """
        Clean up the native engine.
        The LLM class handles cleanup automatically when the object is destroyed.
        """
        if self.debug:
            print("[@vllm-] Cleaning up vLLM engine")

        # The vLLM LLM class handles cleanup automatically
        # We just need to clear our reference
        if self.engine:
            del self.engine
            self.engine = None

        if self.debug:
            print("[@vllm] Engine cleanup completed")


class VLLMOpenAIManager:
    """
    A process manager for vLLM runtimes.
    Implements interface @vllm(model=..., ...) to provide a local backend.
    It wraps the vLLM OpenAI-compatible API server to make it easier to profile vLLM use on Outerbounds.

    NOTE: vLLM's OpenAI-compatible server serves ONE model per server instance.
    If you need multiple models, you must create multiple server instances.

    Example usage:
        from vllm import LLM
        llm = LLM(model="meta-llama/Llama-3.2-1B")
        llm.generate("Hello, world!")

    Or via OpenAI-compatible API:
        import openai
        client = openai.OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="token-abc123"
        )
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-1B",
            messages=[{"role": "user", "content": "Hello"}]
        )
    """

    def __init__(
        self,
        model,
        backend="local",
        debug=False,
        status_card=None,
        port=8000,
        host="127.0.0.1",
        stream_logs_to_card=False,
        max_retries=60,
        retry_alert_frequency=5,
        **vllm_args,
    ):
        # Validate that only a single model is provided
        if isinstance(model, list):
            if len(model) != 1:
                raise ValueError(
                    f"vLLM server can only serve one model per instance. "
                    f"Got {len(model)} models: {model}. "
                    f"Please specify a single model or create multiple @vllm decorators."
                )
            self.model = model[0]
        else:
            self.model = model

        self.processes = {}
        self.debug = debug
        self.stream_logs_to_card = stream_logs_to_card
        self.stats = {}
        self.port = port
        self.host = host
        self.vllm_url = f"http://{host}:{port}"
        self.status_card = status_card
        self.initialization_start = time.time()
        self.server_process = None
        self.max_retries = max_retries
        self.retry_alert_frequency = retry_alert_frequency
        self.vllm_args = vllm_args

        if backend != "local":
            raise ValueError(
                "VLLMManager only supports the 'local' backend at this time."
            )

        self._log_event("info", "Starting vLLM initialization")
        self._update_server_status("Initializing")

        self._timeit(self._install_vllm, "install_vllm")
        self._timeit(self._launch_vllm_server, "launch_server")
        self._collect_version_info()

        total_init_time = time.time() - self.initialization_start
        self._update_performance("total_initialization_time", total_init_time)
        self._log_event(
            "success", f"vLLM initialization completed in {total_init_time:.1f}s"
        )

    def _log_event(self, event_type, message):
        if self.status_card:
            self.status_card.add_event(event_type, message)
        if self.debug:
            print(f"[@vllm] {event_type.upper()}: {message}")

    def _update_server_status(self, status, **kwargs):
        if self.status_card:
            update_data = {"status": status}
            update_data.update(kwargs)
            self.status_card.update_status("server", update_data)

    def _update_model_status(self, model_name, **kwargs):
        if self.status_card:
            current_models = self.status_card.status_data.get("models", {})
            if model_name not in current_models:
                current_models[model_name] = {}
            current_models[model_name].update(kwargs)
            self.status_card.update_status("models", current_models)

    def _update_performance(self, metric, value):
        if self.status_card:
            self.status_card.update_status("performance", {metric: value})

    def _timeit(self, f, name):
        t0 = time.time()
        f()
        tf = time.time()
        duration = tf - t0
        self.stats[name] = {"process_runtime": duration}

        if name == "install_vllm":
            self._update_performance("install_time", duration)
        elif name == "launch_server":
            self._update_performance("server_startup_time", duration)

    def _stream_output(self, stream, prefix):
        """Reads and logs output from a stream."""
        for line in iter(stream.readline, ""):
            if line:
                line = line.strip()
                if self.stream_logs_to_card and self.status_card:
                    self.status_card.add_log_line(f"[{prefix}] {line}")
                elif self.debug:
                    print(f"[{prefix}] {line}")
        stream.close()

    def _is_port_open(self, host, port, timeout=1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect((host, port))
                return True
            except socket.error:
                return False

    def _install_vllm(self):
        self._log_event("info", "Checking for existing vLLM installation")
        try:
            import vllm

            self._log_event("success", f"vLLM {vllm.__version__} is already installed")
            if self.debug:
                print(f"[@vllm] vLLM {vllm.__version__} is already installed.")
            return
        except ImportError as e:
            self._log_event(
                "Error", "vLLM not installed. Please add it to your environment."
            )
            if self.debug:
                print(
                    "[@vllm] vLLM not found. The user is responsible for installation."
                )
            raise e
            # We are not installing it automatically to respect user's environment management.

    def _launch_vllm_server(self):
        self._update_server_status("Starting")
        self._log_event("info", f"Starting vLLM server with model: {self.model}")

        # Check if the model is cached
        hf_home = os.environ.get("HF_HOME")
        if hf_home:
            # Construct the expected cache path for the model
            model_path_id = f"models--{self.model.replace('/', '--')}"
            model_cache_path = os.path.join(hf_home, model_path_id)
            if os.path.exists(model_cache_path):
                self._log_event("info", f"Found cached model at: {model_cache_path}")
                self._update_model_status(
                    self.model, status="Found in cache", location=model_cache_path
                )
            else:
                self._log_event(
                    "warning",
                    f"Cached model not found at {model_cache_path}. vLLM will attempt to download it.",
                )
                self._update_model_status(self.model, status="Downloading")
        else:
            self._log_event(
                "warning",
                "HF_HOME environment variable not set. vLLM will use default cache location and may re-download.",
            )

        if not self.model:
            raise ValueError("At least one model must be specified for @vllm.")

        try:
            if self.debug:
                print(
                    f"[@vllm] Starting vLLM OpenAI-compatible server for model: {self.model}"
                )

            ### NOTE: This is not the only way to start the vLLM server.
            #  https://docs.vllm.ai/en/v0.9.0/api/vllm/entrypoints/openai/api_server.html

            # There are other APIs we should consider using in a future extension:
            # https://docs.vllm.ai/en/stable/api/vllm/entrypoints/openai/run_batch.html#vllm.entrypoints.openai.run_batch
            # https://docs.vllm.ai/en/v0.9.0/api/vllm/entrypoints/openai/serving_embedding.html
            # MANY MORE!!! Wait for some feedback and we can add more.
            cmd = [
                sys.executable,
                "-m",
                "vllm.entrypoints.openai.api_server",
                "--model",
                self.model,
                "--host",
                self.host,
                "--port",
                str(self.port),
            ]

            vllm_args_copy = self.vllm_args.copy()
            if self.debug or self.stream_logs_to_card:
                # Note: This is an undocumented argument for the vLLM OpenAI server entrypoint.
                # It was useful for debugging the vLLM server startup,
                # likely more confusion potential than its worth for end user.
                vllm_args_copy.setdefault("uvicorn_log_level", "debug")

            for key, value in vllm_args_copy.items():
                arg_name = f"--{key.replace('_', '-')}"
                if isinstance(value, bool):
                    if value:
                        cmd.append(arg_name)
                elif value is not None:
                    cmd.append(arg_name)
                    cmd.append(str(value))

            # For debugging, log the exact command being run to the status card
            command_str = " ".join(cmd)
            self._log_event("info", f"Launch Command: `{command_str}`")
            if self.debug:
                print(f"[@vllm] Launching vLLM with command: {command_str}")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line-buffered
            )

            # Threads to stream subprocess output
            if self.debug or self.stream_logs_to_card:
                stdout_thread = threading.Thread(
                    target=self._stream_output,
                    args=(process.stdout, "@vllm-server-out"),
                )
                stderr_thread = threading.Thread(
                    target=self._stream_output,
                    args=(process.stderr, "@vllm-server-err"),
                )
                stdout_thread.daemon = True
                stderr_thread.daemon = True
                stdout_thread.start()
                stderr_thread.start()

            self.server_process = process
            self.processes[process.pid] = {
                "p": process,
                "properties": {
                    "type": "vllm-server",
                    "model": self.model,
                    "error_details": None,
                },
                "status": ProcessStatus.RUNNING,
            }

            if self.debug:
                print(f"[@vllm] Started vLLM server process with PID {process.pid}")

            retries = 0
            while (
                not self._is_port_open(self.host, self.port, timeout=2)
                and retries < self.max_retries
            ):
                if retries == 0:
                    print("[@vllm] Waiting for server to be ready...")
                elif retries % self.retry_alert_frequency == 0:
                    print(
                        f"[@vllm] Still waiting for server... ({retries}/{self.max_retries})"
                    )

                returncode = process.poll()
                if returncode is not None:
                    if self.debug or self.stream_logs_to_card:
                        # Threads are handling output, can't use communicate.
                        # The error has already been printed to the log by the thread.
                        if self.stream_logs_to_card:
                            details_msg = "See card for logs."
                        else:
                            details_msg = "See logs from @vllm-server-err for details."
                        error_details = f"Return code: {returncode}. {details_msg}"
                    else:
                        # No threads, so we can and should use communicate to get stderr.
                        stdout, stderr = process.communicate()
                        error_details = f"Return code: {returncode}, stderr: {stderr}"

                    self.processes[process.pid]["properties"][
                        "error_details"
                    ] = error_details
                    self.processes[process.pid]["status"] = ProcessStatus.FAILED
                    self._update_server_status("Failed", error_details=error_details)
                    self._log_event(
                        "error", f"vLLM server failed to start: {error_details}"
                    )
                    raise RuntimeError(f"vLLM server failed to start: {error_details}")

                time.sleep(2)
                retries += 1

            if not self._is_port_open(self.host, self.port, timeout=2):
                error_details = f"vLLM server did not start listening on {self.host}:{self.port} after {self.max_retries*2}s"
                self.processes[process.pid]["properties"][
                    "error_details"
                ] = error_details
                self.processes[process.pid]["status"] = ProcessStatus.FAILED
                self._update_server_status("Failed", error_details=error_details)
                self._log_event("error", f"Server startup timeout: {error_details}")
                raise RuntimeError(f"vLLM server failed to start: {error_details}")

            if not self._verify_server_health():
                error_details = "vLLM server started but failed health check"
                self.processes[process.pid]["status"] = ProcessStatus.FAILED
                self._update_server_status("Failed", error_details=error_details)
                self._log_event("error", error_details)
                raise RuntimeError(error_details)

            self._update_server_status(
                "Running", uptime_start=datetime.now(), model=self.model
            )
            self._log_event("success", "vLLM server is ready and listening")
            print(f"[@vllm] Server ready!")

            self._update_model_status(self.model, status="Ready")

            if self.debug:
                print("[@vllm] Server is ready.")

        except Exception as e:
            if process and process.pid in self.processes:
                self.processes[process.pid]["status"] = ProcessStatus.FAILED
                self.processes[process.pid]["properties"]["error_details"] = str(e)
            self._update_server_status("Failed", error_details=str(e))
            self._log_event("error", f"Error starting vLLM server: {str(e)}")
            raise RuntimeError(f"Error starting vLLM server: {e}") from e

    def _verify_server_health(self):
        try:
            response = requests.get(f"{self.vllm_url}/v1/models", timeout=10)
            if response.status_code == 200:
                if self.debug:
                    models_data = response.json()
                    available_models = [
                        m.get("id", "unknown") for m in models_data.get("data", [])
                    ]
                    print(
                        f"[@vllm] Health check OK. Available models: {available_models}"
                    )
                return True
            else:
                if self.debug:
                    print(
                        f"[@vllm] Health check failed with status {response.status_code}"
                    )
                return False
        except Exception as e:
            if self.debug:
                print(f"[@vllm] Health check exception: {e}")
            return False

    def _collect_version_info(self):
        version_info = {}
        try:
            import vllm

            version_info["vllm"] = getattr(vllm, "__version__", "Unknown")
        except ImportError:
            version_info["vllm"] = "Not installed"
        except Exception as e:
            version_info["vllm"] = "Error detecting"
            if self.debug:
                print(f"[@vllm] Error getting vLLM version: {e}")

        if self.status_card:
            self.status_card.update_status("versions", version_info)
            self._log_event(
                "info", f"vLLM version: {version_info.get('vllm', 'Unknown')}"
            )

    def terminate_models(self):
        shutdown_start_time = time.time()
        self._log_event("info", "Starting vLLM shutdown sequence")
        if self.debug:
            print("[@vllm] Shutting down vLLM server...")

        server_shutdown_cause = "graceful"

        if self.server_process:
            try:
                self._update_server_status("Stopping")
                self._log_event("info", "Stopping vLLM server")

                # Clear model status since server is shutting down
                self._update_model_status(self.model, status="Stopping")

                self.server_process.terminate()
                try:
                    self.server_process.wait(timeout=10)
                    if self.debug:
                        print("[@vllm] Server terminated gracefully")
                except subprocess.TimeoutExpired:
                    server_shutdown_cause = "force_kill"
                    self._log_event(
                        "warning",
                        "vLLM server did not terminate gracefully, killing...",
                    )
                    if self.debug:
                        print("[@vllm] Server did not terminate, killing...")
                    self.server_process.kill()
                    self.server_process.wait()

                if self.server_process.pid in self.processes:
                    self.processes[self.server_process.pid][
                        "status"
                    ] = ProcessStatus.SUCCESSFUL

                self._update_server_status("Stopped")
                if self.status_card:
                    self.status_card.update_status("models", {})

                self._log_event(
                    "success", f"vLLM server stopped ({server_shutdown_cause})"
                )

            except Exception as e:
                server_shutdown_cause = "failed"
                if self.server_process.pid in self.processes:
                    self.processes[self.server_process.pid][
                        "status"
                    ] = ProcessStatus.FAILED
                    self.processes[self.server_process.pid]["properties"][
                        "error_details"
                    ] = str(e)
                self._update_server_status("Failed to stop")
                if self.status_card:
                    self.status_card.update_status("models", {})
                self._log_event("error", f"vLLM server shutdown error: {str(e)}")
                if self.debug:
                    print(f"[@vllm] Warning: Error terminating vLLM server: {e}")

        total_shutdown_time = time.time() - shutdown_start_time
        self._update_performance("total_shutdown_time", total_shutdown_time)
        self._update_performance("shutdown_cause", server_shutdown_cause)

        self._log_event(
            "success", f"vLLM shutdown completed in {total_shutdown_time:.1f}s"
        )
        if self.debug:
            print("[@vllm] vLLM server shutdown complete.")
