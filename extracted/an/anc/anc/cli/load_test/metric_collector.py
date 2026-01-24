#!/usr/bin/env python3
import subprocess
import requests
import json
import numpy as np
import time
import os
import tempfile
from pathlib import Path
import signal
import sys
import threading
import shutil # For shutil.which
from typing import Optional, Dict, Any
import logging
# Configuration
VLLM_SERVER = "http://localhost:8001"  # Your vLLM server endpoint
NUM_REQUESTS = 10                     # Number of requests to send
PROMPT = "Write a short poem about AI"  # Prompt to send to vLLM
MAX_TOKENS = 20                       # Max tokens to generate

# Default path for the collected trace data
DEFAULT_EXPORT_PATH = "/tmp/vllm_otlp_metric.json"
# Default path for the collector config
DEFAULT_CONFIG_PATH = "/tmp/otel-config.yaml"
# Default path for collector binary (if not found in PATH)
DEFAULT_COLLECTOR_BINARY_PATH = "/tmp/otelcol-contrib"

logger = logging.getLogger("anc")
class MetricCollector:
    """
    Manages the OpenTelemetry Collector process for collecting trace data
    and analyzing latency metrics.
    """
    def __init__(self,
                 export_file_path: str = DEFAULT_EXPORT_PATH,
                 config_path: str = DEFAULT_CONFIG_PATH,
                 collector_binary_path: Optional[str] = None):
        """
        Initializes the MetricCollector.

        Args:
            export_file_path: The full path where the collected trace data will be saved.
            config_path: The path to write the OTel collector configuration file.
            collector_binary_path: Explicit path to otelcol-contrib binary.
                                   If None, it tries to find it in PATH or uses DEFAULT_COLLECTOR_BINARY_PATH.
        """
        self.export_file_path = Path(export_file_path)
        self.config_path = Path(config_path)
        self._resolve_collector_binary(collector_binary_path)
        self.collector_process = None
        self._log_thread = None
        self._stderr_pipe_read, self._stderr_pipe_write = os.pipe() # For capturing stderr

    def _resolve_collector_binary(self, explicit_path: Optional[str]):
        """Finds or sets the path to the otelcol-contrib binary."""
        if explicit_path:
            self.collector_binary_path = Path(explicit_path)
            print(f"Using explicit collector binary path: {self.collector_binary_path}")
        else:
            found_path = shutil.which("otelcol-contrib")
            if found_path:
                self.collector_binary_path = Path(found_path)
                print(f"Found collector binary in PATH: {self.collector_binary_path}")
            else:
                self.collector_binary_path = Path(DEFAULT_COLLECTOR_BINARY_PATH)
                print(f"Collector binary not found in PATH, will use default: {self.collector_binary_path}")
                # Note: Download logic will still run if this default path doesn't exist

    def _create_config_file(self):
        """Creates the OTel collector configuration file."""
        # Ensure the export directory exists
        self.export_file_path.parent.mkdir(parents=True, exist_ok=True)

        config = f"""
receivers:
  otlp:
    protocols:
      grpc: # Use gRPC, matching common vLLM config
        endpoint: 0.0.0.0:4317 # Use the default port for otel collector, need to be consistent with the endpoint in the vllm server

processors:
  batch:
    timeout: 1s # Process batches frequently

exporters:
  file:
    path: {str(self.export_file_path)} # Use the instance variable path
    format: json
  logging:
    verbosity: detailed # Log detailed info for debugging

service:
  telemetry:
    metrics:
      address: :8889 # Use a non-default port for internal metrics

  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [file, logging] # Export to both file and logs
"""
        try:
            with open(self.config_path, "w") as f:
                f.write(config)
            print(f"OTel collector configuration written to {self.config_path}")
        except IOError as e:
            print(f"Error writing collector config file: {e}", file=sys.stderr)
            raise

    def _ensure_collector_binary_exists(self):
        """Downloads the collector binary if it doesn't exist."""
        if not self.collector_binary_path.exists():
            print(f"Collector binary not found at {self.collector_binary_path}. Downloading...")
            # Determine target directory based on collector_binary_path
            target_dir = self.collector_binary_path.parent
            target_dir.mkdir(parents=True, exist_ok=True) # Ensure target dir exists
            download_path = target_dir / "otelcol.tar.gz"
            binary_name = self.collector_binary_path.name # e.g., 'otelcol-contrib'

            try:
                # Download command
                download_cmd = f"curl -L https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.103.1/otelcol-contrib_0.103.1_linux_amd64.tar.gz -o {download_path}"
                print(f"Executing: {download_cmd}")
                subprocess.run(download_cmd, shell=True, check=True, capture_output=True)

                # Extract command - extracts directly into target_dir, should contain the binary
                extract_cmd = f"tar -xzf {download_path} -C {target_dir}"
                print(f"Executing: {extract_cmd}")
                subprocess.run(extract_cmd, shell=True, check=True, capture_output=True)

                # Ensure the extracted binary has the expected name (if downloaded name differs)
                extracted_binary = target_dir / "otelcol-contrib" # Default name in tarball
                if extracted_binary.exists() and extracted_binary != self.collector_binary_path:
                    extracted_binary.rename(self.collector_binary_path)
                    print(f"Renamed extracted binary to {self.collector_binary_path}")
                elif not self.collector_binary_path.exists():
                     raise FileNotFoundError(f"Expected binary {self.collector_binary_path.name} not found after extraction.")


                # Make executable command
                chmod_cmd = f"chmod +x {self.collector_binary_path}"
                logger.debug(f"Executing: {chmod_cmd}")
                subprocess.run(chmod_cmd, shell=True, check=True, capture_output=True)

                # Clean up downloaded tarball
                download_path.unlink()
                print("Collector downloaded and prepared successfully.")

            except subprocess.CalledProcessError as e:
                logger.error(f"Error during collector download/setup: {e}", file=sys.stderr)
                logger.error(f"Stdout: {e.stdout.decode()}", file=sys.stderr)
                logger.error(f"Stderr: {e.stderr.decode()}", file=sys.stderr)
                sys.exit(1)
            except FileNotFoundError as e:
                 logger.error(f"Error: {e}", file=sys.stderr)
                 sys.exit(1)
            except Exception as e:
                 logger.error(f"An unexpected error occurred during collector setup: {e}", file=sys.stderr)
                 sys.exit(1)


    def _start_log_thread(self):
        """Starts a thread to read and print the collector's stderr."""
        def log_reader():
            with os.fdopen(self._stderr_pipe_read) as stderr_stream:
                 while True:
                    try:
                        line = stderr_stream.readline()
                        if not line:
                            break
                        logger.debug(f"COLLECTOR: {line.strip()}")
                    except Exception as e:
                        logger.error(f"Log reader thread error: {e}", file=sys.stderr)
                        break
            logger.info("Collector log reader thread finished.")

        self._log_thread = threading.Thread(target=log_reader, daemon=True)
        self._log_thread.start()

    def start(self):
        """Creates config, ensures binary exists, and starts the collector process."""
        if self.collector_process and self.collector_process.poll() is None:
            print("Collector process already running.")
            return

        try:
            self._create_config_file()
            self._ensure_collector_binary_exists()

            print(f"Starting OpenTelemetry Collector using binary: {self.collector_binary_path}...")
            # Use os.setsid to start collector in a new session, making it easier to kill group later
            self.collector_process = subprocess.Popen(
                [str(self.collector_binary_path), "--config", str(self.config_path)],
                stdout=subprocess.PIPE, # Capture stdout if needed, or DEVNULL
                stderr=self._stderr_pipe_write, # Redirect stderr to the pipe
                preexec_fn=os.setsid # Start in new session
            )
            print(f"Collector process started with PID: {self.collector_process.pid}")

            self._start_log_thread()

            # Brief wait for initialization and check for immediate failure
            time.sleep(5) # Increased sleep
            if self.collector_process.poll() is not None:
                # Process already exited, read remaining stderr
                os.close(self._stderr_pipe_write) # Close write end so reader thread exits
                self._log_thread.join(timeout=2) # Wait briefly for reader thread
                raise RuntimeError("Collector failed to start or exited immediately.")

            logger.info("Collector seems to have started successfully.")

        except Exception as e:
            logger.error(f"Error starting collector: {e}", file=sys.stderr)
            # Ensure cleanup if process started but failed later
            if self.collector_process and self.collector_process.poll() is None:
                self.stop() # Attempt cleanup
            self.collector_process = None # Mark as not running
            raise # Re-raise the exception


    def stop(self):
        """Stops the collector process."""
        if self.collector_process and self.collector_process.poll() is None:
            print(f"Shutting down collector process (PID: {self.collector_process.pid})...")
            try:
                # Send SIGTERM to the process group (due to os.setsid)
                os.killpg(os.getpgid(self.collector_process.pid), signal.SIGTERM)
                # Wait for termination with a timeout
                self.collector_process.wait(timeout=10)
                logger.info("Collector process terminated.")
            except ProcessLookupError:
                 logger.info("Collector process already exited.")
            except subprocess.TimeoutExpired:
                logger.info("Collector did not terminate gracefully, sending SIGKILL...", file=sys.stderr)
                try:
                     os.killpg(os.getpgid(self.collector_process.pid), signal.SIGKILL)
                     self.collector_process.wait(timeout=5) # Wait briefly after kill
                     logger.info("Collector process killed.")
                except ProcessLookupError:
                    logger.info("Collector process exited after SIGKILL attempt.")
                except Exception as kill_e:
                    logger.error(f"Error during SIGKILL: {kill_e}", file=sys.stderr)
            except Exception as e:
                logger.error(f"Error terminating collector: {e}", file=sys.stderr)

            # Clean up stderr pipe and thread
            try:
                os.close(self._stderr_pipe_write)
            except OSError:
                 pass # Ignore errors if already closed
            if self._log_thread and self._log_thread.is_alive():
                self._log_thread.join(timeout=2)

            self.collector_process = None
        else:
            logger.info("Collector process not running or already stopped.")

    def _analyze(self) -> Dict[str, Any]:
        return self.analyze(self.export_file_path)

    @staticmethod
    def analyze(export_file_path: str = DEFAULT_EXPORT_PATH) -> Dict[str, Any]:
        """
        Processes the trace data file and calculates latency percentiles.

        Returns:
            A dictionary containing the calculated statistics, or None if analysis fails.
        """
        logger.info(f"Attempting to read trace data from: {export_file_path}")


        if not Path(export_file_path).exists():
            logger.error(f"Error: Trace data file not found: {export_file_path}", file=sys.stderr)
            return None
        if Path(export_file_path).stat().st_size == 0:
            logger.error(f"Error: Trace data file is empty: {export_file_path}", file=sys.stderr)
            return None

        latency_metrics = {
            'gen_ai.latency.time_to_first_token': [],
            'gen_ai.latency.e2e': [],
            'gen_ai.latency.time_in_queue': [],
            'gen_ai.latency.time_in_scheduler': [],
            'gen_ai.latency.time_in_model_forward': [],
            'gen_ai.latency.time_in_model_execute': [],
            # Add more single-value metrics if needed
        }
        total_spans_processed = 0
        lines_processed = 0
        trace_data_found = False

        try:
            with open(export_file_path, 'r') as f:
                print("Attempting to read as JSON Lines...")
                f.seek(0)
                for line_num, line in enumerate(f):
                    lines_processed = line_num + 1
                    line = line.strip()
                    if not line: continue
                    try:
                        data_line = json.loads(line)
                        trace_data_found = True
                        if isinstance(data_line, dict):
                            resource_spans_list = data_line.get('resourceSpans', [])
                            if not resource_spans_list and "resource" in data_line and "scopeSpans" in data_line:
                                resource_spans_list = [data_line]

                            for resource_span in resource_spans_list:
                                for scope_spans in resource_span.get('scopeSpans', []):
                                    for span in scope_spans.get('spans', []):
                                        total_spans_processed += 1
                                        for attribute in span.get('attributes', []):
                                            attr_key = attribute.get('key')
                                            if attr_key in latency_metrics:
                                                value_info = attribute.get('value', {})
                                                if 'doubleValue' in value_info:
                                                    latency_metrics[attr_key].append(float(value_info['doubleValue']))
                                                elif 'intValue' in value_info:
                                                    latency_metrics[attr_key].append(float(value_info['intValue']))
                    except json.JSONDecodeError as line_e:
                        logger.warning(f"Warning: Could not decode line {line_num + 1} as JSON: {line_e}.", file=sys.stderr)
                    except Exception as line_e:
                        logger.warning(f"Warning: Error processing line {line_num + 1}: {line_e}", file=sys.stderr)

                # Simplified fallback for single object (less likely with file exporter)
                if not trace_data_found and lines_processed <= 1:
                    logger.error("Could not parse as JSON Lines or file was very short. Check collector config/output.", file=sys.stderr)


        except Exception as e:
            logger.error(f"Error reading or processing trace data file: {e}", file=sys.stderr)
            return None

        print(f"Processed {lines_processed} JSON line(s). Found {total_spans_processed} total spans.")

        results = {}
        logger.info("\n=== OTLP Latency Statistics ===")
        try:
            import numpy as np # Import here in case not installed globally
        except ImportError:
             logger.error("Error: numpy is required for percentile calculations. Please install it (`pip install numpy`).", file=sys.stderr)
             return None

        for metric_name, values in latency_metrics.items():
            if values:
                p50 = np.percentile(values, 50)
                p90 = np.percentile(values, 90)
                p95 = np.percentile(values, 95)
                p99 = np.percentile(values, 99)
                mean = np.mean(values)
                std_dev = np.std(values)
                min_val = min(values)
                max_val = max(values)
                count = len(values)

                print(f"--- {metric_name} ({count} samples) ---")
                print(f"  Min: {min_val:.6f}s")
                print(f"  P50: {p50:.6f}s")
                print(f"  P90: {p90:.6f}s")
                print(f"  P95: {p95:.6f}s")
                print(f"  P99: {p99:.6f}s")
                print(f"  Max: {max_val:.6f}s")
                print(f"  Mean: {mean:.6f}s")
                print(f"  Std Dev: {std_dev:.6f}s")

                # Store results
                metric_key_base = metric_name.replace('.', '_').replace('-', '_')
                results[f"{metric_key_base}_count"] = count
                results[f"{metric_key_base}_min"] = min_val
                results[f"{metric_key_base}_p50"] = p50
                results[f"{metric_key_base}_p90"] = p90
                results[f"{metric_key_base}_p95"] = p95
                results[f"{metric_key_base}_p99"] = p99
                results[f"{metric_key_base}_max"] = max_val
                results[f"{metric_key_base}_mean"] = mean
                results[f"{metric_key_base}_stddev"] = std_dev
            else:
                print(f"--- {metric_name} ---")
                print("  No data found for this metric.")

        if not results:
            logger.warning("No valid latency metrics found in the trace data.")
            return None

        return results

def send_requests_to_vllm():
    """Send requests to the vLLM server and return completion times"""
    print(f"Sending {NUM_REQUESTS} requests to vLLM server...")
    
    for i in range(NUM_REQUESTS):
        try:
            response = requests.post(
                f"{VLLM_SERVER}/v1/completions",
                json={
                    "model": "facebook/opt-125m",  # Model name - adjust if needed
                    "prompt": PROMPT,
                    "max_tokens": MAX_TOKENS,
                    "temperature": 0.7
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"Request {i+1}/{NUM_REQUESTS} completed successfully")
            else:
                print(f"Request {i+1}/{NUM_REQUESTS} failed: {response.status_code} - {response.text}")
                
            # After your request code
            print(response.json())
            
        except Exception as e:
            print(f"Error sending request: {e}")
        
        # Small delay between requests
        time.sleep(0.5)

    # Add this cleanup code

def main():
    # Start collector
    server_metric_path = DEFAULT_EXPORT_PATH
    metric_collector = MetricCollector(export_file_path=server_metric_path)
    metric_collector.start()
    
    # Send requests
    send_requests_to_vllm()
    MetricCollector.analyze()
    metric_collector.stop()

if __name__ == "__main__":
    main()
