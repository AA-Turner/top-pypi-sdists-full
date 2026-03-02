import logging
import threading
import time
import json
from typing import Dict, Any, Optional, List, Tuple
from collections import defaultdict, deque
from datetime import datetime, timezone
from statistics import mean, median, stdev

from matrice_common.session import Session
from confluent_kafka import Producer
import base64


class LatencyTracker:
    """
    Tracks and analyzes latency metrics from multiple deployments in real-time.
    
    Provides detailed timing analysis including:
    - Model inference times
    - Post-processing times  
    - End-to-end latencies
    - Client-side timings
    - Server-side breakdown
    - Cross-deployment comparisons
    """

    def __init__(
        self,
        session: Session,
        inference_pipeline_id: str,
        flush_interval_seconds: int = 60,
        max_samples: int = 1000,
    ) -> None:
        """Initialize latency tracker.
        
        Args:
            session: Session object for authentication
            inference_pipeline_id: ID of the inference pipeline
            flush_interval_seconds: Interval for publishing latency reports
            max_samples: Maximum number of samples to keep per metric
        """
        self.session = session
        self.inference_pipeline_id = inference_pipeline_id
        self.flush_interval_seconds = flush_interval_seconds
        self.max_samples = max_samples

        self.kafka_producer = self._setup_kafka_producer()

        # Threading
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._is_running = False
        self._lock = threading.Lock()

        # Latency data storage
        # Structure: {deployment_id: {metric_name: deque([values])}}
        self._latency_data: Dict[str, Dict[str, deque]] = defaultdict(
            lambda: defaultdict(lambda: deque(maxlen=max_samples))
        )
        
        # Per-stream latency tracking
        # Structure: {(deployment_id, stream_key): {metric_name: deque([values])}}
        self._stream_latency_data: Dict[Tuple[str, str], Dict[str, deque]] = defaultdict(
            lambda: defaultdict(lambda: deque(maxlen=max_samples))
        )

        # Cross-deployment analysis
        self._deployment_summary: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Stats
        self.stats = {
            "start_time": None,
            "messages_processed": 0,
            "latency_reports_published": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
            "last_flush_time": None,
        }

    def _setup_kafka_producer(self):
        """Setup Kafka producer for publishing latency reports."""
        try:
            path = "/v1/actions/get_kafka_info"
            response = self.session.rpc.get(path=path, raise_exception=True)

            if not response or not response.get("success"):
                raise ValueError(f"Failed to fetch Kafka config: {response.get('message', 'No response')}")

            # Decode base64 fields
            encoded_ip = response["data"]["ip"]
            encoded_port = response["data"]["port"]
            ip = base64.b64decode(encoded_ip).decode("utf-8")
            port = base64.b64decode(encoded_port).decode("utf-8")
            bootstrap_servers = f"{ip}:{port}"
            
            kafka_producer = Producer({
                "bootstrap.servers": bootstrap_servers,
                "acks": "all",
                "retries": 3,
                "retry.backoff.ms": 1000,
                "request.timeout.ms": 30000,
                "max.in.flight.requests.per.connection": 1,
                "linger.ms": 10,
                "batch.size": 4096,
                "queue.buffering.max.ms": 50,
                "log_level": 0,
            })
            return kafka_producer
        except Exception as exc:
            logging.error(f"Failed to setup Kafka producer for latency tracker: {exc}")
            return None

    def start(self) -> bool:
        """Start the latency tracker."""
        if self._is_running:
            logging.warning("Latency tracker already running")
            return True
        
        try:
            self._stop.clear()
            self._is_running = True
            self.stats["start_time"] = time.time()
            self.stats["last_flush_time"] = time.time()
            
            self._thread = threading.Thread(
                target=self._run, 
                name=f"LatencyTracker-{self.inference_pipeline_id}", 
                daemon=True
            )
            self._thread.start()
            
            logging.info("Latency tracker started")
            return True
        except Exception as exc:
            self._record_error(f"Failed to start latency tracker: {exc}")
            self.stop()
            return False

    def stop(self) -> None:
        """Stop the latency tracker."""
        if not self._is_running:
            logging.info("Latency tracker not running")
            return
        
        logging.info("Stopping latency tracker...")
        self._is_running = False
        self._stop.set()
        
        try:
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=5.0)
        except Exception as exc:
            logging.error(f"Error joining latency tracker thread: {exc}")
        
        self._thread = None
        logging.info("Latency tracker stopped")

    def ingest_result(self, deployment_id: str, aggregated_result: Dict[str, Any]) -> None:
        """Ingest a result for latency analysis.
        
        Args:
            deployment_id: ID of the deployment that produced this result
            aggregated_result: Result payload containing latency data
        """
        try:
            with self._lock:
                self._extract_and_store_latency_data(deployment_id, aggregated_result)
                self.stats["messages_processed"] += 1
        except Exception as exc:
            self._record_error(f"Failed to ingest latency data: {exc}")

    def _extract_and_store_latency_data(self, deployment_id: str, result: Dict[str, Any]) -> None:
        """Extract latency data from result and store it."""
        # Extract stream key for per-stream tracking
        camera_info = result.get("camera_info", {}) or {}
        stream_key = camera_info.get("camera_name", "unknown")
        stream_tuple = (deployment_id, stream_key)
        
        # Extract latency stats from agg_apps
        agg_apps = result.get("agg_apps", []) or []
        current_time = time.time()
        
        for app in agg_apps:
            # Extract timing data from separated inference and post-processing workers
            # Look for inference timing (from inference worker message)
            inference_timing = app.get("inference_timing", {}) or {}
            
            # Look for post-processing timing (from post-processing worker message)
            post_processing_timing = app.get("post_processing_timing", {}) or {}
            
            # Legacy server timing fallback (for backward compatibility)
            server_timing = app.get("server_timing", {}) or {}
            
            # Extract client timing data from input stream metadata  
            input_streams = app.get("input_streams", []) or []
            client_timing = {}
            if input_streams:
                first_input_stream = input_streams[0].get("input_stream", {}) or {}
                client_timing = {
                    "last_read_time_sec": first_input_stream.get("last_read_time_sec", 0.0),
                    "last_write_time_sec": first_input_stream.get("last_write_time_sec", 0.0), 
                    "last_process_time_sec": first_input_stream.get("last_process_time_sec", 0.0),
                }
            
            # Legacy latency stats fallback
            latency_stats = app.get("latency_stats", {}) or {}
            server_breakdown = latency_stats.get("server_processing_breakdown", {}) or {}
            client_breakdown = latency_stats.get("client_timing_breakdown", {}) or {}
            
            # Extract all timing metrics from separated workers
            timing_metrics = {
                # Model inference timing (from inference worker)
                "model_inference_time_sec": (
                    inference_timing.get("model_inference_time_sec") or
                    server_timing.get("model_inference_time_sec") or
                    server_breakdown.get("model_inference_time_sec", 0.0)
                ),
                
                # Post-processing timing (from post-processing worker)
                "post_processing_time_sec": (
                    post_processing_timing.get("post_processing_time_sec") or
                    server_timing.get("post_processing_time_sec") or
                    server_breakdown.get("post_processing_time_sec", 0.0)
                ),
                
                # Combined inference total time
                "inference_total_time_sec": (
                    inference_timing.get("inference_total_time_sec") or
                    server_timing.get("inference_total_time_sec") or
                    server_breakdown.get("inference_total_time_sec", 0.0)
                ),
                
                # Individual worker times
                "inference_worker_time_sec": inference_timing.get("total_worker_time_sec", 0.0),
                "post_processing_worker_time_sec": post_processing_timing.get("total_worker_time_sec", 0.0),
                
                # Legacy total worker time (for backward compatibility)
                "total_worker_time_sec": server_timing.get("total_worker_time_sec", server_breakdown.get("total_worker_time_sec", 0.0)),
                
                # Client timing breakdown
                "client_read_time_sec": client_timing.get("last_read_time_sec", client_breakdown.get("last_read_time_sec", 0.0)),
                "client_write_time_sec": client_timing.get("last_write_time_sec", client_breakdown.get("last_write_time_sec", 0.0)),
                "client_process_time_sec": client_timing.get("last_process_time_sec", client_breakdown.get("last_process_time_sec", 0.0)),
                
                # Legacy/extended server timing fields
                "kafka_consume_time_sec": server_breakdown.get("kafka_consume_time_sec", 0.0),
                "kafka_produce_time_sec": server_breakdown.get("kafka_produce_time_sec", 0.0),
                "output_construct_time_sec": server_breakdown.get("output_construct_time_sec", 0.0),
                
                # Application-level latency (legacy format)
                "app_e2e_sec": latency_stats.get("app_e2e_sec", 0.0),
                "last_input_feed_sec": latency_stats.get("last_input_feed_sec", 0.0),
                "last_output_sec": latency_stats.get("last_output_sec", 0.0),
                
                # Model-specific latency (from model streams)
                "model_latency_sec": 0.0,
                "post_processing_latency_sec": 0.0,
                "inference_total_latency_sec": 0.0,
                
                # Calculate total end-to-end pipeline time (inference + post-processing)
                "total_e2e_pipeline_time_sec": 0.0,
            }
            
            # Calculate total end-to-end pipeline time
            inference_worker_time = timing_metrics["inference_worker_time_sec"]
            post_processing_worker_time = timing_metrics["post_processing_worker_time_sec"]
            
            if inference_worker_time > 0 or post_processing_worker_time > 0:
                timing_metrics["total_e2e_pipeline_time_sec"] = inference_worker_time + post_processing_worker_time
            elif timing_metrics["model_inference_time_sec"] > 0 or timing_metrics["post_processing_time_sec"] > 0:
                # Fallback to individual step times if worker times aren't available
                timing_metrics["total_e2e_pipeline_time_sec"] = (
                    timing_metrics["model_inference_time_sec"] + 
                    timing_metrics["post_processing_time_sec"]
                )
            
            # Extract model stream latency data
            model_streams = app.get("model_streams", []) or []
            for model_stream in model_streams:
                model_latency_stats = model_stream.get("model_stream", {}).get("latency_stats", {}) or {}
                timing_metrics.update({
                    "model_latency_sec": model_latency_stats.get("model_latency_sec", 0.0),
                    "post_processing_latency_sec": model_latency_stats.get("post_processing_latency_sec", 0.0),
                    "inference_total_latency_sec": model_latency_stats.get("inference_total_latency_sec", 0.0),
                })
                break  # Take first model stream
            
            # Store per-deployment metrics
            for metric_name, value in timing_metrics.items():
                if isinstance(value, (int, float)) and value > 0:
                    self._latency_data[deployment_id][metric_name].append((current_time, value))
                    self._stream_latency_data[stream_tuple][metric_name].append((current_time, value))
            
            # Send individual latency metrics to Kafka
            self._send_latency_metrics(deployment_id, stream_key, timing_metrics, current_time)

    def _send_latency_metrics(self, deployment_id: str, stream_key: str, metrics: Dict[str, float], timestamp: float) -> None:
        """Send individual latency metrics to Kafka."""
        if not self.kafka_producer:
            return
        
        latency_data = {
            "deployment_id": deployment_id,
            "stream_key": stream_key,
            "timestamp": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
            "pipeline_id": self.inference_pipeline_id,
            "metrics": {k: v for k, v in metrics.items() if isinstance(v, (int, float)) and v > 0}
        }
        
        try:
            self.kafka_producer.produce(
                topic="Latency-Metrics",
                key=f"{deployment_id}-{stream_key}".encode("utf-8"),
                value=json.dumps(latency_data, separators=(",", ":")).encode("utf-8"),
            )
        except Exception as exc:
            logging.error(f"Failed to send latency metrics: {exc}")

    def _run(self) -> None:
        """Main tracker loop."""
        logging.info("Latency tracker worker started")
        
        while not self._stop.is_set():
            try:
                current_time = time.time()
                last_flush = self.stats.get("last_flush_time") or current_time
                
                if current_time - last_flush >= self.flush_interval_seconds:
                    self._flush_latency_report(current_time)
                    self.stats["last_flush_time"] = current_time
                
                time.sleep(1.0)  # Check every second
                
            except Exception as exc:
                if not self._stop.is_set():
                    self._record_error(f"Error in latency tracker loop: {exc}")
                    time.sleep(1.0)
        
        # Final flush on stop
        try:
            self._flush_latency_report(time.time())
        except Exception as exc:
            logging.error(f"Error during final latency flush: {exc}")
        
        logging.info("Latency tracker worker stopped")

    def _flush_latency_report(self, end_time: float) -> None:
        """Generate and publish comprehensive latency report."""
        with self._lock:
            if not self._latency_data:
                return  # No data to report
            
            # Generate deployment-level statistics
            deployment_stats = {}
            for deployment_id, metrics in self._latency_data.items():
                deployment_stats[deployment_id] = self._calculate_deployment_stats(metrics)
            
            # Generate cross-deployment analysis
            cross_deployment_analysis = self._analyze_cross_deployment_performance(deployment_stats)
            
            # Generate stream-level analysis
            stream_analysis = self._analyze_stream_performance()
            
            # Create comprehensive report
            latency_report = {
                "report_type": "latency_analysis",
                "pipeline_id": self.inference_pipeline_id,
                "report_timestamp": datetime.now(timezone.utc).isoformat(),
                "report_period_seconds": self.flush_interval_seconds,
                "deployment_statistics": deployment_stats,
                "cross_deployment_analysis": cross_deployment_analysis,
                "stream_analysis": stream_analysis,
                "summary": {
                    "total_deployments": len(deployment_stats),
                    "total_streams": len(self._stream_latency_data),
                    "messages_processed": self.stats["messages_processed"],
                },
                "metadata": {
                    "tracker_version": "1.0",
                    "max_samples": self.max_samples,
                },
            }
            
            # Publish report
            if self.kafka_producer:
                try:
                    self.kafka_producer.produce(
                        topic="Latency-Analytics",
                        key=str(self.inference_pipeline_id).encode("utf-8"),
                        value=json.dumps(latency_report, separators=(",", ":")).encode("utf-8"),
                    )
                    self.kafka_producer.poll(0)
                    self.stats["latency_reports_published"] += 1
                    
                    logging.info(
                        f"Published latency report: {len(deployment_stats)} deployments, "
                        f"{self.stats['messages_processed']} messages processed"
                    )
                except Exception as exc:
                    self._record_error(f"Failed to publish latency report: {exc}")
            
            # Reset message counter
            self.stats["messages_processed"] = 0

    def _calculate_deployment_stats(self, metrics: Dict[str, deque]) -> Dict[str, Any]:
        """Calculate statistics for a single deployment."""
        stats = {}
        
        for metric_name, samples in metrics.items():
            if not samples:
                continue
            
            # Extract values (samples are (timestamp, value) tuples)
            values = [sample[1] for sample in samples]
            
            if values:
                stats[metric_name] = {
                    "count": len(values),
                    "mean": mean(values),
                    "median": median(values),
                    "min": min(values),
                    "max": max(values),
                    "std": stdev(values) if len(values) > 1 else 0.0,
                    "p95": self._percentile(values, 95),
                    "p99": self._percentile(values, 99),
                }
        
        return stats

    def _analyze_cross_deployment_performance(self, deployment_stats: Dict[str, Dict]) -> Dict[str, Any]:
        """Analyze performance across all deployments."""
        analysis = {
            "performance_comparison": {},
            "outlier_detection": {},
            "recommendations": [],
        }
        
        # Compare key metrics across deployments (updated for separated worker architecture)
        key_metrics = [
            "model_inference_time_sec", 
            "post_processing_time_sec", 
            "inference_worker_time_sec",
            "post_processing_worker_time_sec",
            "total_e2e_pipeline_time_sec",
            "app_e2e_sec"  # Legacy metric
        ]
        
        for metric in key_metrics:
            metric_values = {}
            for deployment_id, stats in deployment_stats.items():
                if metric in stats:
                    metric_values[deployment_id] = stats[metric]["mean"]
            
            if len(metric_values) > 1:
                values = list(metric_values.values())
                analysis["performance_comparison"][metric] = {
                    "deployment_means": metric_values,
                    "overall_mean": mean(values),
                    "overall_std": stdev(values) if len(values) > 1 else 0.0,
                    "fastest_deployment": min(metric_values.keys(), key=lambda k: metric_values[k]),
                    "slowest_deployment": max(metric_values.keys(), key=lambda k: metric_values[k]),
                    "performance_spread": max(values) - min(values),
                }
                
                # Detect outliers (deployments with >2 std deviations from mean)
                overall_mean = mean(values)
                overall_std = stdev(values) if len(values) > 1 else 0.0
                
                if overall_std > 0:
                    outliers = []
                    for deployment_id, value in metric_values.items():
                        z_score = abs(value - overall_mean) / overall_std
                        if z_score > 2.0:
                            outliers.append({
                                "deployment_id": deployment_id,
                                "value": value,
                                "z_score": z_score,
                            })
                    
                    if outliers:
                        analysis["outlier_detection"][metric] = outliers
        
        return analysis

    def _analyze_stream_performance(self) -> Dict[str, Any]:
        """Analyze performance per stream across deployments."""
        stream_analysis = {}
        
        # Group by stream key
        streams = defaultdict(list)
        for (deployment_id, stream_key), metrics in self._stream_latency_data.items():
            streams[stream_key].append((deployment_id, metrics))
        
        for stream_key, deployment_metrics in streams.items():
            if len(deployment_metrics) > 1:  # Only analyze streams with multiple deployments
                stream_stats = {}
                
                for deployment_id, metrics in deployment_metrics:
                    stream_stats[deployment_id] = self._calculate_deployment_stats(metrics)
                
                stream_analysis[stream_key] = {
                    "deployment_count": len(deployment_metrics),
                    "deployment_stats": stream_stats,
                }
        
        return stream_analysis

    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of a list of values."""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = (percentile / 100.0) * (len(sorted_values) - 1)
        
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower = sorted_values[int(index)]
            upper = sorted_values[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))

    def _record_error(self, error_message: str) -> None:
        """Record an error in statistics."""
        with self._lock:
            self.stats["errors"] += 1
            self.stats["last_error"] = error_message
            self.stats["last_error_time"] = time.time()
        logging.error(f"Latency tracker error: {error_message}")

    def get_stats(self) -> Dict[str, Any]:
        """Get current tracker statistics."""
        with self._lock:
            stats = dict(self.stats)
        
        if stats.get("start_time"):
            stats["uptime_seconds"] = time.time() - stats["start_time"]
        
        # Add data size information
        stats["deployment_count"] = len(self._latency_data)
        stats["stream_count"] = len(self._stream_latency_data)
        
        total_samples = sum(
            sum(len(metric_queue) for metric_queue in deployment_metrics.values())
            for deployment_metrics in self._latency_data.values()
        )
        stats["total_samples"] = total_samples
        
        return stats

    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the latency tracker."""
        health = {
            "status": "healthy",
            "is_running": self._is_running,
            "errors": self.stats["errors"],
            "reports_published": self.stats["latency_reports_published"],
            "messages_processed": self.stats["messages_processed"],
        }
        
        # Check for recent errors
        if (
            self.stats.get("last_error_time")
            and (time.time() - self.stats["last_error_time"]) < 60
        ):
            health["status"] = "degraded"
            health["reason"] = f"Recent error: {self.stats.get('last_error')}"
        
        # Check if not running
        if not self._is_running:
            health["status"] = "unhealthy"
            health["reason"] = "Latency tracker is not running"
        
        return health

    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.stop()
        except Exception:
            pass
        
        with self._lock:
            self._latency_data.clear()
            self._stream_latency_data.clear()
            self._deployment_summary.clear()
        
        try:
            if hasattr(self, "kafka_producer") and self.kafka_producer is not None:
                self.kafka_producer.flush(5)
        except Exception as exc:
            logging.error(f"Error flushing latency tracker kafka producer: {exc}")
        
        logging.info("Latency tracker cleanup completed")

