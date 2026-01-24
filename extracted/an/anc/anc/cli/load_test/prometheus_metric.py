#!/usr/bin/env python3
"""
vLLM Metrics Analyzer

This script collects, analyzes, and calculates percentiles from vLLM's Prometheus metrics.
It can be used either as a standalone script or imported by other modules.
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from typing import Dict, List, Optional, Any, Union, Tuple

import requests
from prometheus_client.parser import text_string_to_metric_families

# Default configuration
DEFAULT_VLLM_SERVER = "http://localhost:8004"
DEFAULT_METRICS_ENDPOINT = "/metrics"
DEFAULT_MODEL_NAME = None  # Will use server's default
DEFAULT_PROMPT = "Write a short poem about artificial intelligence."
DEFAULT_MAX_TOKENS = 20
DEFAULT_NUM_REQUESTS = 10
DEFAULT_PERCENTILES = [1, 25, 50, 75, 99]


def collect_prometheus_metrics(server_url: str = DEFAULT_VLLM_SERVER,
                     metrics_path: str = DEFAULT_METRICS_ENDPOINT,
                     save_raw_path: str = "./raw_prometheus_metrics.txt") -> Optional[str]:
    """
    Collect raw metrics from vLLM's Prometheus metrics endpoint.

    Args:
        server_url: Base URL of the vLLM server
        metrics_path: Path to the metrics endpoint
        save_raw_path: Optional path to save raw metrics text

    Returns:
        Raw metrics text or None if request fails
    """
    metrics_url = f"{server_url.rstrip('/')}{metrics_path}"
    
    try:
        print(f"Fetching metrics from {metrics_url}...")
        response = requests.get(metrics_url, timeout=10)
        response.raise_for_status()
        
        metrics_text = response.text
        
        # Save raw metrics to file if path is specified
        if save_raw_path:
            try:
                with open(save_raw_path, 'w') as f:
                    f.write(metrics_text)
                print(f"Raw metrics saved to {save_raw_path}")
            except Exception as e:
                print(f"Error saving raw metrics: {e}", file=sys.stderr)
        
        return metrics_text
    except requests.RequestException as e:
        print(f"Error fetching metrics: {e}", file=sys.stderr)
        return None


def send_requests_to_vllm(server_url: str = DEFAULT_VLLM_SERVER,
                         num_requests: int = DEFAULT_NUM_REQUESTS,
                         model_name: Optional[str] = DEFAULT_MODEL_NAME,
                         prompt: str = DEFAULT_PROMPT,
                         max_tokens: int = DEFAULT_MAX_TOKENS) -> bool:
    """
    Send test requests to the vLLM server to generate metrics.

    Args:
        server_url: Base URL of the vLLM server
        num_requests: Number of requests to send
        model_name: Model name to use (None for server default)
        prompt: Prompt text to send
        max_tokens: Maximum tokens to generate

    Returns:
        True if all requests were successfully sent, False otherwise
    """
    success_count = 0
    completions_url = f"{server_url.rstrip('/')}/v1/completions"
    
    print(f"Sending {num_requests} test requests to {completions_url}...")
    
    for i in range(num_requests):
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": 0,
                "top_k": 1,
                "ignore_eos": True
            }
            
            # Add model name if specified
            if model_name:
                payload["model"] = model_name
                
            response = requests.post(
                completions_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"Request {i+1}/{num_requests} completed successfully")
                success_count += 1
            else:
                print(f"Request {i+1}/{num_requests} failed: {response.status_code} - {response.text}",
                     file=sys.stderr)
                
        except Exception as e:
            print(f"Error sending request {i+1}/{num_requests}: {e}", file=sys.stderr)
        
        # Small delay between requests
        if i < num_requests - 1:
            time.sleep(0.5)
    
    success_rate = success_count / num_requests if num_requests > 0 else 0
    print(f"Completed {success_count}/{num_requests} requests ({success_rate:.1%} success rate)")
    
    return success_count == num_requests


def analyze_metrics(metrics_text: str, 
                   percentiles: List[int] = DEFAULT_PERCENTILES,
                   save_results_path: str = "./processed_prometheus_metrics.json") -> Dict[str, Dict[str, Any]]:
    """
    Analyze vLLM metrics and calculate specified percentiles.

    Args:
        metrics_text: Raw Prometheus metrics text
        percentiles: List of percentiles to calculate (1-99)
        save_results_path: Optional path to save analysis results as JSON

    Returns:
        Dictionary of analyzed metrics with percentiles
    """
    if not metrics_text:
        return {}
    
    # Organize metrics by type
    metrics_by_type = {
        'histograms': defaultdict(lambda: {'buckets': {}, 'sum': 0, 'count': 0}),
        'counters': {},
        'gauges': {}
    }
    
    # Parse metrics
    for family in text_string_to_metric_families(metrics_text):
        family_name = family.name
        family_type = getattr(family, 'type', 'unknown')
        
        if family_type == 'histogram':
            # Process histogram metrics
            for sample in family.samples:
                sample_name = sample.name
                
                if sample_name.endswith('_sum'):
                    metrics_by_type['histograms'][family_name]['sum'] = sample.value
                elif sample_name.endswith('_count'):
                    metrics_by_type['histograms'][family_name]['count'] = sample.value
                elif sample_name.endswith('_bucket'):
                    if 'le' in sample.labels:
                        try:
                            # Skip +Inf bucket
                            if sample.labels['le'] == '+Inf':
                                continue
                            bucket_value = float(sample.labels['le'])
                            metrics_by_type['histograms'][family_name]['buckets'][bucket_value] = sample.value
                        except (ValueError, TypeError):
                            pass
        
        elif family_type == 'counter':
            # Process counter metrics
            for sample in family.samples:
                metrics_by_type['counters'][sample.name] = sample.value
        
        elif family_type == 'gauge':
            # Process gauge metrics
            for sample in family.samples:
                metrics_by_type['gauges'][sample.name] = sample.value
    
    # Calculate histogram statistics and percentiles
    results = {}
    
    for hist_name, hist_data in metrics_by_type['histograms'].items():
        if hist_data['count'] > 0 and hist_data['buckets']:
            buckets = sorted(hist_data['buckets'].items())
            count = hist_data['count']
            sum_value = hist_data['sum']
            
            stats = {
                'count': count,
                'sum': sum_value,
                'avg': sum_value / count,
                'min': buckets[0][0] if any(v > 0 for _, v in buckets) else None,
                'max': buckets[-1][0]
            }
            # Calculate requested percentiles
            for p in percentiles:
                if p < 1 or p > 99:
                    continue  # Skip invalid percentiles
                
                target_count = count * (p / 100.0)
                percentile_found = False
                
                for i, (upper_bound, cum_count) in enumerate(buckets):
                    if cum_count >= target_count:
                        if i > 0:
                            # Linear interpolation if possible
                            lower_bound, lower_count = buckets[i-1]
                            if cum_count > lower_count:  # Avoid division by zero
                                fraction = (target_count - lower_count) / (cum_count - lower_count)
                                interpolated = lower_bound + fraction * (upper_bound - lower_bound)
                                stats[f'p{p}'] = interpolated
                            else:
                                stats[f'p{p}'] = upper_bound
                        else:
                            stats[f'p{p}'] = upper_bound
                        percentile_found = True
                        break
                
                if not percentile_found:
                    stats[f'p{p}'] = None
            
            results[hist_name] = stats
    
    # Add counter metrics
    for counter_name, value in metrics_by_type['counters'].items():
        results[counter_name] = {'value': value, 'type': 'counter'}
    
    # Add gauge metrics
    for gauge_name, value in metrics_by_type['gauges'].items():
        results[gauge_name] = {'value': value, 'type': 'gauge'}
    
    # Save results to file if path specified
    if save_results_path:
        try:
            with open(save_results_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Analysis results saved to {save_results_path}")
        except Exception as e:
            print(f"Error saving analysis results: {e}", file=sys.stderr)
    print_analysis_results(results)
    return results


def print_analysis_results(results: Dict[str, Dict[str, Any]], 
                          show_histograms: bool = True,
                          show_counters: bool = True,
                          show_gauges: bool = False) -> None:
    """
    Print analysis results in a human-readable format.

    Args:
        results: Analysis results from analyze_metrics()
        show_histograms: Whether to show histogram metrics
        show_counters: Whether to show counter metrics
        show_gauges: Whether to show gauge metrics
    """
    # Organize by metric type
    histograms = {}
    counters = {}
    gauges = {}
    
    for name, data in results.items():
        if 'type' in data:
            if data['type'] == 'counter':
                counters[name] = data
            elif data['type'] == 'gauge':
                gauges[name] = data
        elif 'count' in data and 'avg' in data:
            histograms[name] = data
    
    # Print histograms
    if show_histograms and histograms:
        print("\n=== Prometheus Metrics from vllm ===")
        for name, data in sorted(histograms.items()):
            print(f"\n{name}:")
            print(f"  Count: {data['count']}")
            print(f"  Avg: {data['avg']:.6f}")
            
            # Print all percentiles
            for key in sorted(data.keys()):
                if key.startswith('p') and key[1:].isdigit():
                    value = data[key]
                    if value is not None:
                        print(f"  {key.upper()}: {value:.6f}")
    
    # Print counters
    if show_counters and counters:
        print("\n=== Counter Metrics ===")
        for name, data in sorted(counters.items()):
            print(f"  {name}: {data['value']}")
    
    # Print gauges
    if show_gauges and gauges:
        print("\n=== Gauge Metrics ===")
        for name, data in sorted(gauges.items()):
            print(f"  {name}: {data['value']}")


def main():
    """
    Main function when script is run directly.
    """
    parser = argparse.ArgumentParser(description='Collect and analyze vLLM Prometheus metrics')
    parser.add_argument('--server', default=DEFAULT_VLLM_SERVER, help='vLLM server URL')
    parser.add_argument('--send-requests', action='store_true', help='Send test requests before collecting metrics')
    parser.add_argument('--num-requests', type=int, default=DEFAULT_NUM_REQUESTS, help='Number of test requests to send')
    parser.add_argument('--model',help='Model name to use for requests (server default if not specified)')
    parser.add_argument('--prompt', default=DEFAULT_PROMPT, help='Prompt text to use for requests')
    parser.add_argument('--max-tokens', type=int, default=DEFAULT_MAX_TOKENS, help='Max tokens for generation')
    parser.add_argument('--percentiles', type=str, default='1,25,50,75,99', help='Comma-separated percentiles to calculate')
    parser.add_argument('--output', default = "./processed_prometheus_metrics.json", help='Save analyzed results to JSON file')
    parser.add_argument('--raw-output', default = "./raw_prometheus_metrics.txt", help='Save raw metrics text to file')
    parser.add_argument('--show-gauges', action='store_true', help='Show gauge metrics in output')
    
    args = parser.parse_args()
    if args.send_requests:
        if args.model is None:
            print("Error: --model is required when --send-requests is true", file=sys.stderr)
            return 1
    
    # Parse percentiles
    try:
        percentiles = [int(p.strip()) for p in args.percentiles.split(',')]
    except ValueError:
        print("Error: Percentiles must be comma-separated integers", file=sys.stderr)
        return 1
    
    # Send test requests if requested
    if args.send_requests:
        success = send_requests_to_vllm(
            server_url=args.server,
            num_requests=args.num_requests,
            model_name=args.model,
            prompt=args.prompt,
            max_tokens=args.max_tokens
        )
        if not success:
            print("Warning: Not all requests were successful", file=sys.stderr)
    
    # Collect and analyze metrics
    metrics_text = collect_prometheus_metrics(
        server_url=args.server,
        save_raw_path=args.raw_output
    )
    if not metrics_text:
        print("Error: Failed to collect metrics from vLLM server", file=sys.stderr)
        return 1
    
    analyze_metrics(
        metrics_text, 
        percentiles=percentiles,
        save_results_path=args.output
    )
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
