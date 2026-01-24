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
from opentelemetry import trace
from opentelemetry.trace import TracerProvider

# Configuration
VLLM_SERVER = "http://localhost:8004"  # Your vLLM server endpoint
NUM_REQUESTS = 10                     # Number of requests to send
PROMPT = "Write a short poem about AI"  # Prompt to send to vLLM
MAX_TOKENS = 20                       # Max tokens to generate

def setup_otel_collector(server_metric_path):
    """Setup and start the OpenTelemetry Collector"""
    # Create config file
    config = """
receivers:
      otlp:
        protocols:
          grpc: # Use gRPC
            endpoint: 0.0.0.0:4317
        # or use a completely different port if needed:
        # endpoint: localhost:5318

exporters:
  file:
    path: /mnt/personal/honbgo_vllm/graphana/jaeger/jaeger-1.57.0-linux-amd64/tmp/latency_data.json
    format: json
  logging:
    verbosity: detailed # Use detailed for max info

processors:
  batch:
    timeout: 1s

service:
  telemetry: # Keep your telemetry config if you added it
        metrics:
          address: :8889

  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [file, logging]

"""
    
    config_path = Path("/tmp/otel-config.yaml")
    with open(config_path, "w") as f:
        f.write(config)
    
    # Download collector if not exists
    collector_path = Path("/tmp/otelcol-contrib")
    if not collector_path.exists():
        print("Downloading OpenTelemetry Collector...")
        try:
            subprocess.run(
                "curl -L https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.103.1/otelcol-contrib_0.103.1_linux_amd64.tar.gz -o /tmp/otelcol.tar.gz",
                shell=True, check=True
            )
            subprocess.run("tar -xzf /tmp/otelcol.tar.gz -C /tmp", shell=True, check=True)
            
            # Create directory for the output file if it doesn't exist
            subprocess.run("chmod +x /tmp/otelcol-contrib", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error downloading collector: {e}")
            sys.exit(1)
    
    # Start collector
    print("Starting OpenTelemetry Collector...")
    try:
        process = subprocess.Popen(
            ["/tmp/otelcol-contrib", "--config", "/tmp/otel-config.yaml", "--set", f"exporters.file.path={server_metric_path}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it's running
        if process.poll() is not None:
            out, err = process.communicate()
            print(f"Collector failed to start: {err.decode('utf-8')}")
            sys.exit(1)
            
        # Add these lines to capture output in real-time
        def log_output(process):
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                print(f"COLLECTOR: {line.decode().strip()}")
        
        threading.Thread(target=log_output, args=(process,), daemon=True).start()
        
        return process
    except Exception as e:
        print(f"Error starting collector: {e}")
        sys.exit(1)

def send_requests_to_vllm():
    """Send requests to the vLLM server and return completion times"""
    print(f"Sending {NUM_REQUESTS} requests to vLLM server...")
    
    for i in range(NUM_REQUESTS):
        try:
            response = requests.post(
                f"{VLLM_SERVER}/v1/completions",
                json={
                    "model": "/mnt/project/llm/ckpt/stable_ckpts/Llama-3.2-1B/",  # Model name - adjust if needed
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

def calculate_percentiles(service_metric_path):
    """Process the trace data from the specified file and calculate percentiles"""
    print(f"Attempting to read trace data from: {service_metric_path}")
    trace_file = Path(service_metric_path)

    # Give the file system and collector flush interval a bit more time
    time.sleep(7) # Increased wait time slightly after finishing requests

    if not trace_file.exists():
        print(f"Error: Trace data file not found: {service_metric_path}", file=sys.stderr)
        return

    if trace_file.stat().st_size == 0:
        print(f"Error: Trace data file is empty: {service_metric_path}", file=sys.stderr)
        return

    latencies = []
    total_spans_processed = 0
    lines_processed = 0
    trace_data_found = False

    try:
        with open(trace_file, 'r') as f:
            # Try reading as JSON Lines first (more likely with streaming writes)
            print("Attempting to read as JSON Lines...")
            f.seek(0) # Ensure we start at the beginning
            
            # Track multiple latency metrics
            latency_metrics = {
                'gen_ai.latency.time_to_first_token': [],
                'gen_ai.latency.e2e': [],
                'gen_ai.latency.time_in_queue': [],
                'gen_ai.latency.time_in_scheduler': [],
                'gen_ai.latency.time_in_model_forward': [],
                'gen_ai.latency.time_in_model_execute': [],
                'gen_ai.running_batch_size': [],
                'gen_ai.running_batch_size_list': [],
                'gen_ai.latency.time_in_model_forward_list': [],
                'gen_ai.latency.time_in_model_execute_list': []
            }
            
            for line_num, line in enumerate(f):
                lines_processed = line_num + 1
                line = line.strip()
                if not line:
                    continue
                try:
                    # Each line should contain a ResourceSpans object or similar structure
                    data_line = json.loads(line)
                    trace_data_found = True # Mark that we found at least one valid JSON line

                    # Check if the line contains the expected structure
                    if isinstance(data_line, dict):
                        resource_spans_list = data_line.get('resourceSpans', [])
                        # Sometimes the root object itself is the ResourceSpans object
                        if not resource_spans_list and "resource" in data_line and "scopeSpans" in data_line:
                             resource_spans_list = [data_line] # Treat the line object as a single ResourceSpans

                        for resource_span in resource_spans_list:
                            for scope_spans in resource_span.get('scopeSpans', []):
                                for span in scope_spans.get('spans', []):
                                    total_spans_processed += 1
                                    # Check for all latency attributes
                                    for attribute in span.get('attributes', []):
                                        attr_key = attribute.get('key')
                                        if attr_key in latency_metrics:
                                            value_info = attribute.get('value', {})
                                            if 'doubleValue' in value_info:
                                                latency_metrics[attr_key].append(float(value_info['doubleValue']))
                                            elif 'intValue' in value_info: # Handle potential int values too
                                                latency_metrics[attr_key].append(float(value_info['intValue']))
                                            # Handle list values (arrays)
                                            elif 'arrayValue' in value_info:
                                                array_values = value_info.get('arrayValue', {}).get('values', [])
                                                current_array = []
                                                for val in array_values:
                                                    if 'doubleValue' in val:
                                                        current_array.append(float(val['doubleValue']))
                                                    elif 'intValue' in val:
                                                        current_array.append(float(val['intValue']))
                                                if current_array:  # Only append if we have values
                                                    latency_metrics[attr_key].append(current_array)

                except json.JSONDecodeError as line_e:
                    print(f"Warning: Could not decode line {line_num + 1} as JSON: {line_e}. Content: '{line[:100]}...'", file=sys.stderr)
                except Exception as line_e:
                     print(f"Warning: Error processing line {line_num + 1}: {line_e}", file=sys.stderr)

            # If JSON Lines didn't yield data or format seemed wrong, maybe it *is* a single object
            if not trace_data_found and lines_processed <= 1:
                 print("Could not parse as JSON Lines or file was very short, trying as single JSON object...")
                 f.seek(0)
                 try:
                     data = json.load(f)
                     lines_processed = 1
                     if isinstance(data, dict) and 'resourceSpans' in data:
                         resource_spans_list = data.get('resourceSpans', [])
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
                                            # Handle list values (arrays) as 2D array
                                            elif 'arrayValue' in value_info:
                                                array_values = value_info.get('arrayValue', {}).get('values', [])
                                                current_array = []
                                                for val in array_values:
                                                    if 'doubleValue' in val:
                                                        current_array.append(float(val['doubleValue']))
                                                    elif 'intValue' in val:
                                                        current_array.append(float(val['intValue']))
                                                import pdb; pdb.set_trace()
                                                if current_array:  # Only append if we have values
                                                    latency_metrics[attr_key].append(current_array)
                         trace_data_found = True # Mark that we read the single object
                 except json.JSONDecodeError as single_e:
                     print(f"Error: Could not decode file as single JSON object either: {single_e}", file=sys.stderr)
                 except Exception as single_e:
                    print(f"Error processing file as single JSON object: {single_e}", file=sys.stderr)


    except FileNotFoundError:
        print(f"Error: Trace data file disappeared during processing: {service_metric_path}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Error reading or processing trace data file: {e}", file=sys.stderr)
        return

    print(f"Processed {lines_processed} JSON line(s)/object(s). Found {total_spans_processed} total spans.")

    # For backward compatibility
    latencies = latency_metrics['gen_ai.latency.time_to_first_token']

    # Calculate percentiles for all metrics
    try:
        import numpy as np
    except ImportError:
        print("Error: numpy is required for percentile calculations. Please install it (`pip install numpy`).", file=sys.stderr)
        return

    # Print statistics for each latency metric
    for metric_name, values in latency_metrics.items():
        if values:
            print(metric_name, values)
            p50 = np.percentile(values, 50)
            p90 = np.percentile(values, 90)
            p95 = np.percentile(values, 95)
            p99 = np.percentile(values, 99)

            print(f"\n=== {metric_name} Statistics ===")
            print(f"P50: {p50:.6f}s")
            print(f"P90: {p90:.6f}s")
            print(f"P95: {p95:.6f}s")
            print(f"P99: {p99:.6f}s")
            print(f"Min: {min(values):.6f}s")
            print(f"Max: {max(values):.6f}s")
            print(f"Mean: {np.mean(values):.6f}s")
            print(f"Std Dev: {np.std(values):.6f}s")
            print(f"Total samples: {len(values)}")
        elif trace_data_found:
            print(f"Found trace data but no spans contained the '{metric_name}' attribute.")
    
    if not trace_data_found:
        print(f"No valid trace data found in the file to extract metrics from.")

def main():
    # Start collector
    server_metric_path = "/mnt/personal/honbgo_vllm/graphana/latency_data.json"
    collector_process = setup_otel_collector(server_metric_path)
    
    try:
        # Send requests
        send_requests_to_vllm()
        
        # Process results
        calculate_percentiles(server_metric_path)
    finally:
        # Cleanup
        print("Shutting down collector...")
        if collector_process:
            collector_process.terminate()
            collector_process.wait()

if __name__ == "__main__":
    main()
