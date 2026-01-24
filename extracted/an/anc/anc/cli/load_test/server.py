import abc
import subprocess
import time
import requests
from typing import List, Optional
import os

import logging
logger = logging.getLogger("anc")

class BaseServer(abc.ABC):
    """Abstract base class for all server implementations."""
    
    @abc.abstractmethod
    def start(self):
        """Start the server."""
        pass
    
    def check_server_ready(self, host: str, port: int, health_endpoint: str = "/health", 
                          max_retries: int = 300, retry_interval: int = 20) -> bool:
        """
        Check if the server is ready by polling the health endpoint.
        
        Args:
            host: Server host
            port: Server port
            health_endpoint: Health check endpoint
            max_retries: Maximum number of retries
            retry_interval: Time between retries in seconds
            
        Returns:
            bool: True if server is ready, False otherwise
        """
        for retry in range(max_retries):
            try:
                print(f"Checking server health status at {host}:{port}{health_endpoint} (attempt {retry+1}/{max_retries})...")
                # Try to connect to server health check endpoint
                response = requests.get(f"http://{host}:{port}{health_endpoint}")
                if response.status_code == 200:
                    print(f"Server at {host}:{port} is ready")
                    return True
            except requests.exceptions.ConnectionError:
                pass
            
            time.sleep(retry_interval)
        
        print(f"Timed out waiting for server at {host}:{port} to be ready after {max_retries} attempts")
        return False


class ServerFactory:
    """Factory class for creating different types of model serving servers."""
    
    @staticmethod
    def create_server(server_type, **kwargs):
        """
        Create and return a server instance based on the server type.
        
        Args:
            server_type: Type of server to create (vllm, tensorrt-llm, sglang, etc.)
            **kwargs: Arguments specific to the server type
            
        Returns:
            A server instance
        """
        if server_type == "vllm" or server_type == "openai-chat":
            return VLLMServer(**kwargs)
        elif server_type == "tensorrt-llm":
            return TensorRTLLMServer(**kwargs)
        elif server_type == "sglang":
            return SGLangServer(**kwargs)
        elif server_type == "scalellm":
            return ScaleLLMServer(**kwargs)
        else:
            raise ValueError(f"Unsupported server type: {server_type}")


class VLLMServer(BaseServer):
    """VLLM server implementation."""
    
    def __init__(self, model=None, host=None, port=None, 
                **kwargs):
        self.model = model
        self.host = host
        self.port = port
        self.kwargs = kwargs
        self.process = None  # Add this line to store process handle
        
    def start(self, dry_run, server_log_dir, start_otlp_server=False):
        """Start the VLLM server."""
        try:
            # Construct command to start vLLM server
            cmd = [
                "python3", "-m", "vllm.entrypoints.openai.api_server",
                "--model", self.model,
                "--host", self.host,
                "--port", str(self.port),
                "--tensor-parallel-size", str(self.kwargs.get('tensor_parallel_size', 4)),
                # "--enable-chunked-prefill", str(self.kwargs.get('enable_chunked_prefill', "True")),
                "--gpu-memory-utilization", str(self.kwargs.get('gpu_memory_utilization', 0.95)),
                "--max-model-len", str(self.kwargs.get('max-model-len', 8000)),
                # "--multi-step-stream-outputs", str(self.kwargs.get('multi_step_stream_outputs', "True")),
            ]
            if self.kwargs.get('use_v2_block_manager'):
                cmd.append("--use-v2-block-manager")
            if self.kwargs.get('max-num-seqs'):
                cmd.append("--max-num-seqs")
                cmd.append(self.kwargs.get('max-num-seqs'))
            
            if self.kwargs.get('enable_prefix_caching') and self.kwargs.get('enable_prefix_caching') == "True":
                cmd.append("--enable-prefix-caching")
            
            if self.kwargs.get('speculative-model'):
                cmd.append("--speculative-model")
                cmd.append(self.kwargs.get('speculative-model'))
                cmd.append("--speculative-draft-tensor-parallel-size")
                cmd.append(self.kwargs.get('speculative-draft-tensor-parallel-size'))
                cmd.append("--num-speculative-tokens")
                cmd.append(self.kwargs.get('num-speculative-tokens'))
                cmd.append("--speculative-disable-by-batch-size")
                cmd.append(self.kwargs.get('speculative_disable_by_batchsize'))
            
            if start_otlp_server:
                os.environ["OTEL_SERVICE_NAME"] = "vllm-server"
                os.environ["OTEL_EXPORTER_OTLP_TRACES_INSECURE"] = "true"
                cmd.append("--collect-detailed-traces")
                cmd.append("all")
                cmd.append("--otlp-traces-endpoint")
                cmd.append("grpc://localhost:4317")
            if self.kwargs.get('extra_vllm_args'):
                # Split the extra args by space and add each part individually
                extra_args = self.kwargs.get('extra_vllm_args').split()
                cmd.extend(extra_args)
            # Check if port is already in use and kill the process
            self.release_port
            kill_gpu_processes()
                
            logger.info(f"Starting vLLM server with command: {' '.join(cmd)}")
            logger.debug(f"env: {os.environ}")
            if dry_run:
                return
            # Start server as a background process
            # If start_server_only is specified, run server in foreground
            log_file_path = f"{server_log_dir}/vllm_server_{int(time.time())}.log"
            with open(log_file_path, "w") as log_file:
                print(f"\n{'-'*100}")
                print(f"\n{'-'*100}")
                print(f"Server logs will be saved to {log_file_path}")
                print(f"{'-'*100}\n")
                print(f"{'-'*100}\n")
                if self.kwargs.get('start_server_only'):
                    # Run server in foreground with output to both log file and screen
                    self.process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1
                    )
                    
                    # Print output to both log file and screen
                    for line in self.process.stdout:
                        print(line, end='')
                        log_file.write(line)
                        log_file.flush()
                    
                    self.process.wait()
                    return self.process.returncode == 0
                else:
                    # Run server in background
                    self.process = subprocess.Popen(
                        cmd,
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        text=True
                )
                
                # Check if server is ready
                server_ready = self.check_server_ready(self.host, self.port)
                if not server_ready:
                    raise Exception("vLLM server failed to start")
        except Exception as e:
            print(f"Error starting vLLM server: {e}")
            raise e

    def release_port(self):
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
                
            if result == 0:  # Port is in use
                print(f"Port {self.port} is already in use. Attempting to free it...")
                # Propagate the exception to the caller
                raise Exception(f"Port {self.port} is already in use. not able to release it. try to kill the process manually with lsof -ti :{self.port} | xargs kill -9")

        except ImportError:
            print("Warning: psutil not installed. Cannot automatically free port.")
            print("If the server fails to start, manually kill the process using the port.")
        except Exception as e:
            print(f"Error releasing port: {e}")
            raise e

    def stop(self):
        """Stop the VLLM server gracefully."""
        if self.process:
            print("Stopping vLLM server...")
            self.process.terminate()  # Send SIGTERM
            try:
                self.process.wait(timeout=30)  # Wait up to 30 seconds
            except subprocess.TimeoutExpired:
                print("Server didn't terminate gracefully, forcing shutdown...")
                self.process.kill()  # Send SIGKILL
                kill_gpu_processes()  # Kill any remaining GPU processes
            self.process = None


class TensorRTLLMServer(BaseServer):
    """TensorRT-LLM server implementation."""
    
    def __init__(self, host=None, port=None, **kwargs):
        self.host = host
        self.port = port
        self.kwargs = kwargs
        
    def start(self):
        """Start the TensorRT-LLM server."""
        print("Starting TensorRT-LLM server (not yet implemented)")
        # When implemented, should check if server is ready
        # self.check_server_ready(self.host, self.port)
        return False


class SGLangServer(BaseServer):
    """SGLang server implementation."""
    
    def __init__(self, host=None, port=None, **kwargs):
        self.host = host
        self.port = port
        self.kwargs = kwargs
        
    def start(self):
        """Start the SGLang server."""
        print("Starting SGLang server (not yet implemented)")
        # When implemented, should check if server is ready
        # self.check_server_ready(self.host, self.port)
        return False


class ScaleLLMServer(BaseServer):
    """ScaleLLM server implementation."""
    
    def __init__(self, host=None, port=None, **kwargs):
        self.host = host
        self.port = port
        self.kwargs = kwargs
        
    def start(self):
        """Start the ScaleLLM server."""
        print("Starting ScaleLLM server (not yet implemented)")
        # When implemented, should check if server is ready
        # self.check_server_ready(self.host, self.port)
        return False

def kill_gpu_processes():
    """Kill all Python processes using GPU."""
    try:
        # Get all GPU processes
        nvidia_smi = "nvidia-smi"
        process = subprocess.run([nvidia_smi, "--query-compute-apps=pid", "--format=csv,noheader"], 
                               capture_output=True, text=True)
        
        # Extract PIDs
        pids = process.stdout.strip().split('\n')
        
        # Kill each process
        for pid in pids:
            if pid:  # Skip empty lines
                try:
                    subprocess.run(['kill', '-9', pid.strip()])
                    print(f"Killed GPU process {pid}")
                except subprocess.CalledProcessError:
                    print(f"Failed to kill process {pid}")
                    
    except subprocess.CalledProcessError as e:
        print(f"Error getting GPU processes: {e}")
