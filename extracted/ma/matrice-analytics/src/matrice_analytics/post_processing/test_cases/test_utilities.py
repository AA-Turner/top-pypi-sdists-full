"""
Test utilities and base classes for post processing tests.

This module provides base test classes, assertion helpers, performance monitoring,
and common utilities for testing post processing functionality.
"""

import unittest
import time
import psutil
import os
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import tempfile
import json
import yaml

# Fix imports for proper module resolution
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.matrice_analytics.post_processing import (
    PostProcessor, ProcessingResult, ProcessingContext, ProcessingStatus,
    PeopleCountingConfig, CustomerServiceConfig, BaseConfig
)


@dataclass
class PerformanceMetrics:
    """Container for performance test metrics."""
    execution_time: float
    memory_usage_mb: float
    cpu_usage_percent: float
    peak_memory_mb: float
    
    def is_within_limits(self, max_time: float = 5.0, max_memory_mb: float = 500.0) -> bool:
        """Check if metrics are within acceptable limits."""
        return (self.execution_time <= max_time and 
                self.peak_memory_mb <= max_memory_mb)


class BasePostProcessingTest(unittest.TestCase):
    """Base test class for all post processing tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.processor = PostProcessor()
        self.temp_dir = tempfile.mkdtemp()
        self.start_time = time.time()
        self.process = psutil.Process(os.getpid())
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
    def tearDown(self):
        """Clean up test environment."""
        # Clean up temp files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def measure_performance(self, func, *args, **kwargs) -> tuple[Any, PerformanceMetrics]:
        """Measure performance of a function call."""
        # Record initial state
        start_time = time.time()
        start_memory = self.process.memory_info().rss / 1024 / 1024
        cpu_percent_start = self.process.cpu_percent()
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Record final state
        end_time = time.time()
        end_memory = self.process.memory_info().rss / 1024 / 1024
        cpu_percent_end = self.process.cpu_percent()
        
        # Calculate metrics
        metrics = PerformanceMetrics(
            execution_time=end_time - start_time,
            memory_usage_mb=end_memory - start_memory,
            cpu_usage_percent=(cpu_percent_end + cpu_percent_start) / 2,
            peak_memory_mb=max(start_memory, end_memory)
        )
        
        return result, metrics
    
    def assert_processing_result(self, result: ProcessingResult, 
                                expected_status: ProcessingStatus = ProcessingStatus.SUCCESS,
                                min_insights: int = 0,
                                max_warnings: int = 10,
                                required_metrics: List[str] = None):
        """Assert processing result meets expectations."""
        self.assertIsInstance(result, ProcessingResult)
        self.assertEqual(result.status, expected_status)
        
        if expected_status == ProcessingStatus.SUCCESS:
            self.assertIsNotNone(result.data)
            self.assertGreaterEqual(len(result.insights), min_insights)
            self.assertLessEqual(len(result.warnings), max_warnings)
            
            if required_metrics:
                for metric in required_metrics:
                    self.assertIn(metric, result.metrics)
        
        elif expected_status == ProcessingStatus.ERROR:
            self.assertIsNotNone(result.error_message)
            self.assertIsNotNone(result.error_type)
    
    def assert_config_valid(self, config: BaseConfig):
        """Assert configuration is valid."""
        errors = config.validate()
        self.assertEqual(len(errors), 0, f"Configuration validation failed: {errors}")
    
    def create_temp_config_file(self, config: Dict[str, Any], format: str = "json") -> str:
        """Create temporary configuration file."""
        if format == "json":
            filename = os.path.join(self.temp_dir, "test_config.json")
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
        elif format == "yaml":
            filename = os.path.join(self.temp_dir, "test_config.yaml")
            with open(filename, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filename
    
    def assert_performance_acceptable(self, metrics: PerformanceMetrics,
                                    max_time: float = 5.0,
                                    max_memory_mb: float = 500.0):
        """Assert performance metrics are acceptable."""
        self.assertLessEqual(metrics.execution_time, max_time,
                           f"Execution time {metrics.execution_time:.2f}s exceeds limit {max_time}s")
        self.assertLessEqual(metrics.peak_memory_mb, max_memory_mb,
                           f"Peak memory {metrics.peak_memory_mb:.2f}MB exceeds limit {max_memory_mb}MB")


class StressTestMixin:
    """Mixin for stress testing functionality."""
    
    def run_stress_test(self, test_func, iterations: int = 100, 
                       max_failures: int = 5) -> Dict[str, Any]:
        """Run stress test with multiple iterations."""
        results = {
            "total_iterations": iterations,
            "successful": 0,
            "failed": 0,
            "errors": [],
            "execution_times": [],
            "memory_usage": []
        }
        
        for i in range(iterations):
            try:
                start_time = time.time()
                start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
                
                test_func()
                
                end_time = time.time()
                end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
                
                results["successful"] += 1
                results["execution_times"].append(end_time - start_time)
                results["memory_usage"].append(end_memory - start_memory)
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Iteration {i}: {str(e)}")
                
                if results["failed"] > max_failures:
                    break
        
        # Calculate statistics
        if results["execution_times"]:
            results["avg_execution_time"] = sum(results["execution_times"]) / len(results["execution_times"])
            results["max_execution_time"] = max(results["execution_times"])
            results["min_execution_time"] = min(results["execution_times"])
        
        if results["memory_usage"]:
            results["avg_memory_usage"] = sum(results["memory_usage"]) / len(results["memory_usage"])
            results["max_memory_usage"] = max(results["memory_usage"])
        
        return results


class ValidationHelpers:
    """Helper methods for validation testing."""
    
    @staticmethod
    def create_invalid_bbox() -> List[float]:
        """Create invalid bounding box for testing."""
        return [100, 100, 50, 50]  # x2 < x1, y2 < y1
    
    @staticmethod
    def create_invalid_polygon() -> List[List[float]]:
        """Create invalid polygon for testing."""
        return [[0, 0], [100, 0]]  # Only 2 points
    
    @staticmethod
    def create_invalid_confidence() -> float:
        """Create invalid confidence value for testing."""
        return 1.5  # > 1.0
    
    @staticmethod
    def create_empty_detection_results() -> List[Dict[str, Any]]:
        """Create empty detection results for edge case testing."""
        return []
    
    @staticmethod
    def create_malformed_detection_results() -> List[Dict[str, Any]]:
        """Create malformed detection results for error testing."""
        return [
            {"bbox": [0, 0, 100]},  # Missing coordinate
            {"confidence": 0.8},     # Missing bbox
            {"bbox": [0, 0, 100, 100], "confidence": "high"},  # Wrong type
        ]
    
    @staticmethod
    def create_extreme_values() -> Dict[str, Any]:
        """Create extreme values for boundary testing."""
        return {
            "huge_bbox": [0, 0, 999999, 999999],
            "tiny_bbox": [0, 0, 1, 1],
            "negative_coords": [-100, -100, 100, 100],
            "zero_confidence": 0.0,
            "max_confidence": 1.0,
            "huge_polygon": [[i, i] for i in range(1000)],
            "empty_string": "",
            "none_value": None
        }


class ConcurrencyTestMixin:
    """Mixin for testing concurrent processing."""
    
    def run_concurrent_test(self, test_func, num_threads: int = 5, 
                          iterations_per_thread: int = 10) -> Dict[str, Any]:
        """Run concurrent test with multiple threads."""
        import threading
        import queue
        
        results_queue = queue.Queue()
        threads = []
        
        def worker():
            thread_results = []
            for _ in range(iterations_per_thread):
                try:
                    result = test_func()
                    thread_results.append(("success", result))
                except Exception as e:
                    thread_results.append(("error", str(e)))
            results_queue.put(thread_results)
        
        # Start threads
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Collect results
        all_results = []
        while not results_queue.empty():
            all_results.extend(results_queue.get())
        
        # Analyze results
        successful = sum(1 for status, _ in all_results if status == "success")
        failed = sum(1 for status, _ in all_results if status == "error")
        errors = [result for status, result in all_results if status == "error"]
        
        return {
            "total_operations": len(all_results),
            "successful": successful,
            "failed": failed,
            "success_rate": successful / len(all_results) if all_results else 0,
            "errors": errors[:10]  # Limit error list
        }


class MockDataGenerator:
    """Generate mock data for testing."""
    
    @staticmethod
    def create_detection_batch(batch_size: int = 100) -> List[Dict[str, Any]]:
        """Create batch of detection results."""
        import random
        
        detections = []
        categories = ["person", "car", "bike", "truck", "bus"]
        
        for i in range(batch_size):
            width = random.randint(20, 200)
            height = random.randint(20, 200)
            x1 = random.randint(0, 640 - width)
            y1 = random.randint(0, 480 - height)
            
            detections.append({
                "bbox": [x1, y1, x1 + width, y1 + height],
                "confidence": random.uniform(0.3, 0.95),
                "category": random.choice(categories),
                "detection_id": i
            })
        
        return detections
    
    @staticmethod
    def create_tracking_batch(num_tracks: int = 20, frames: int = 10) -> List[Dict[str, Any]]:
        """Create batch of tracking results."""
        import random
        
        tracks = []
        categories = ["person", "car", "bike"]
        
        for track_id in range(1, num_tracks + 1):
            for frame in range(1, frames + 1):
                # Simulate movement
                base_x = 100 + track_id * 20
                base_y = 100 + track_id * 15
                x = base_x + frame * random.randint(-5, 5)
                y = base_y + frame * random.randint(-5, 5)
                
                tracks.append({
                    "track_id": track_id,
                    "bbox": [x, y, x + 50, y + 80],
                    "confidence": random.uniform(0.5, 0.9),
                    "category": random.choice(categories),
                    "frame": frame,
                    "timestamp": time.time() + frame * 0.033
                })
        
        return tracks


def assert_processing_result(result: ProcessingResult, 
                           expected_status: ProcessingStatus = ProcessingStatus.SUCCESS,
                           min_insights: int = 0,
                           required_data_keys: List[str] = None):
    """Standalone assertion helper for processing results."""
    assert isinstance(result, ProcessingResult)
    assert result.status == expected_status
    
    if expected_status == ProcessingStatus.SUCCESS:
        assert result.data is not None
        assert len(result.insights) >= min_insights
        
        if required_data_keys:
            for key in required_data_keys:
                assert key in result.data
    
    elif expected_status == ProcessingStatus.ERROR:
        assert result.error_message is not None
        assert result.error_type is not None 