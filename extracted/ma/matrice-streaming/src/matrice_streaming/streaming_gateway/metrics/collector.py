"""Metrics collection from streaming gateway."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Dict, List, Optional

from .config import MetricsConfig


class MetricsCollector:
    """Collects and aggregates streaming gateway metrics."""

    def __init__(self, streaming_gateway, config: MetricsConfig):
        """Initialize metrics collector.

        Args:
            streaming_gateway: StreamingGateway instance
            config: Metrics configuration
        """
        self.streaming_gateway = streaming_gateway
        self.config = config

        # Thread safety
        self._lock = threading.RLock()

        # Time-series history
        self.metrics_history: List[Dict[str, Any]] = []

        # Track frame counts for FPS calculation
        self.camera_frame_counts: Dict[str, List[tuple]] = {}  # camera_id -> [(timestamp, count)]

        # Both backends (NVDEC and WorkerManager) run in worker subprocesses and
        # expose metrics via get_statistics()["worker_stats"]. The active_worker_manager
        # property on the gateway resolves to whichever one is in use.
        self.use_async_workers = getattr(streaming_gateway, "active_worker_manager", None) is not None

    def collect_snapshot(self) -> Dict[str, Any]:
        """Collect current metrics snapshot from streaming gateway.

        Returns:
            Dictionary containing current metrics state
        """
        with self._lock:
            try:
                # Get overall statistics from streaming gateway
                gateway_stats = self.streaming_gateway.get_statistics()

                # Route to appropriate collection method based on flow
                if self.use_async_workers:
                    return self._collect_async_worker_snapshot(gateway_stats)  # type: ignore[return-value]
                return self._collect_camera_streamer_snapshot(gateway_stats)  # type: ignore[return-value]

            except Exception as e:
                logging.exception(f"Error collecting metrics snapshot: {e}")
                return None  # type: ignore[return-value]

    def _collect_camera_streamer_snapshot(self, gateway_stats: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Collect metrics from original CameraStreamer flow."""
        # Get camera streamer for detailed metrics
        camera_streamer = getattr(self.streaming_gateway, "camera_manager", None)
        cam_stats = getattr(camera_streamer, "statistics", None)
        if not camera_streamer or cam_stats is None:
            return None

        # Collect per-camera metrics
        camera_metrics = {}

        # Get active stream keys
        stream_keys = gateway_stats.get("my_stream_keys", [])

        for stream_key in stream_keys:
            # Get timing statistics for this stream
            timing = cam_stats.get_timing_stats(stream_key)

            if timing:
                # Get camera_id from the streaming gateway mapping
                camera_id = self.streaming_gateway.get_camera_id_for_stream_key(stream_key)
                if not camera_id:
                    # Fallback: try to extract from stream_key if mapping not available
                    camera_id = stream_key.split("_")[0] if "_" in stream_key else stream_key

                camera_metrics[camera_id] = {
                    "stream_key": stream_key,
                    "read_time": timing.get("last_read_time_sec", 0.0),  # Camera reading latency
                    "write_time": timing.get("last_write_time_sec", 0.0),  # Gateway sending latency
                    "process_time": timing.get("last_process_time_sec", 0.0),  # Total processing time
                    "frame_size": timing.get("last_frame_size_bytes", 0),  # ACG frame size in bytes
                }

        # Get transmission stats for frame counts
        transmission_stats = gateway_stats.get("transmission_stats", {})

        snapshot = {
            "timestamp": time.time(),
            "cameras": camera_metrics,
            "frames_sent": transmission_stats.get("frames_sent_full", 0),
            "total_frames_processed": transmission_stats.get("total_frames_processed", 0),
            "flow_type": "camera_streamer",
        }

        return snapshot

    def _collect_async_worker_snapshot(self, gateway_stats: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Collect metrics from worker flow (NVDEC or WorkerManager)."""
        worker_manager = getattr(self.streaming_gateway, "active_worker_manager", None)
        if not worker_manager:
            return None

        # Collect per-camera metrics from worker statistics
        camera_metrics = {}

        # Get active stream keys
        stream_keys = gateway_stats.get("my_stream_keys", [])

        # Get worker statistics
        worker_stats = gateway_stats.get("worker_stats", {})

        for stream_key in stream_keys:
            # Get camera_id from the streaming gateway mapping
            camera_id = self.streaming_gateway.get_camera_id_for_stream_key(stream_key)
            if not camera_id:
                camera_id = stream_key.split("_")[0] if "_" in stream_key else stream_key

            # For async workers, we track basic info (detailed timing not yet available)
            camera_metrics[camera_id] = {
                "stream_key": stream_key,
                "read_time": 0.0,  # Not tracked per-camera in async flow yet
                "write_time": 0.0,  # Not tracked per-camera in async flow yet
                "process_time": 0.0,  # Not tracked per-camera in async flow yet
                "frame_size": 0,  # Not tracked per-camera in async flow yet
            }

        # Calculate aggregate stats from worker health reports
        total_cameras = worker_stats.get("total_cameras", len(stream_keys))
        running_workers = worker_stats.get("running_workers", 0)

        snapshot = {
            "timestamp": time.time(),
            "cameras": camera_metrics,
            "frames_sent": 0,  # Not tracked in async flow yet
            "total_frames_processed": 0,  # Not tracked in async flow yet
            "flow_type": "async_workers",
            "worker_stats": {
                "num_workers": worker_stats.get("num_workers", 0),
                "running_workers": running_workers,
                "total_cameras": total_cameras,
            },
        }

        return snapshot

    def add_to_history(self, snapshot: Dict[str, Any]):
        """Add snapshot to rolling history window.

        Args:
            snapshot: Metrics snapshot to add
        """
        if not snapshot:
            return

        with self._lock:
            self.metrics_history.append(snapshot)

            # Prune old data outside the window
            cutoff_time = time.time() - self.config.history_window
            self.metrics_history = [m for m in self.metrics_history if m["timestamp"] > cutoff_time]

    def get_aggregated_metrics(self) -> Optional[Dict[str, Any]]:
        """Calculate aggregated metrics from accumulated timing history.

        Returns:
            Dictionary with aggregated per-camera metrics
        """
        with self._lock:
            if not self.metrics_history:
                return None

            try:
                # Route to appropriate aggregation method based on flow
                if self.use_async_workers:
                    return self._get_async_worker_aggregated_metrics()  # type: ignore[return-value]
                return self._get_camera_streamer_aggregated_metrics()  # type: ignore[return-value]

            except Exception as e:
                logging.exception(f"Error calculating aggregated metrics: {e}")
                return None

    def _get_camera_streamer_aggregated_metrics(self) -> Optional[List[Dict[str, Any]]]:
        """Get aggregated metrics for CameraStreamer flow."""
        camera_streamer = getattr(self.streaming_gateway, "camera_manager", None)
        cam_stats = getattr(camera_streamer, "statistics", None)
        if not camera_streamer or cam_stats is None:
            return None

        # Get active stream keys from the most recent snapshot
        stream_keys = set()
        for snapshot in self.metrics_history:
            for camera_id, metrics in snapshot.get("cameras", {}).items():
                stream_keys.add(metrics.get("stream_key"))

        # Calculate statistics for each stream using accumulated history
        per_camera_metrics = []

        for stream_key in stream_keys:
            if not stream_key:
                continue

            # Get real statistics from accumulated timing history
            stats = cam_stats.get_timing_statistics(stream_key)

            if not stats:
                continue

            # Get camera_id from the streaming gateway mapping
            camera_id = self.streaming_gateway.get_camera_id_for_stream_key(stream_key)
            if not camera_id:
                camera_id = stream_key.split("_")[0] if "_" in stream_key else stream_key

            # Get read time statistics (already in milliseconds)
            read_time_ms = stats.get("read_time_ms", {})
            read_stats = {
                "min": read_time_ms.get("min", 0.0),
                "max": read_time_ms.get("max", 0.0),
                "avg": read_time_ms.get("avg", 0.0),
                "p0": read_time_ms.get("min", 0.0),
                "p50": read_time_ms.get("avg", 0.0),
                "p100": read_time_ms.get("max", 0.0),
                "unit": "ms",
            }

            # Get write time statistics (already in milliseconds)
            write_time_ms = stats.get("write_time_ms", {})
            write_stats = {
                "min": write_time_ms.get("min", 0.0),
                "max": write_time_ms.get("max", 0.0),
                "avg": write_time_ms.get("avg", 0.0),
                "p0": write_time_ms.get("min", 0.0),
                "p50": write_time_ms.get("avg", 0.0),
                "p100": write_time_ms.get("max", 0.0),
                "unit": "ms",
            }

            # Get FPS statistics (real calculations from timestamps)
            fps_data = stats.get("fps", {})
            fps_stats = {
                "min": fps_data.get("min", 0.0),
                "max": fps_data.get("max", 0.0),
                "avg": fps_data.get("avg", 0.0),
                "p0": fps_data.get("min", 0.0),
                "p50": fps_data.get("avg", 0.0),
                "p100": fps_data.get("max", 0.0),
                "unit": "fps",
            }

            # Get frame size statistics
            frame_size_data = stats.get("frame_size_bytes", {})
            frame_size_stats = {
                "min": frame_size_data.get("min", 0.0),
                "max": frame_size_data.get("max", 0.0),
                "avg": frame_size_data.get("avg", 0.0),
                "p0": frame_size_data.get("min", 0.0),
                "p50": frame_size_data.get("avg", 0.0),
                "p100": frame_size_data.get("max", 0.0),
                "unit": "bytes",
            }

            camera_metric = {
                "camera_id": camera_id,
                "camera_reading": {"throughput": fps_stats, "latency": read_stats},
                "gateway_sending": {"throughput": fps_stats, "latency": write_stats},
                "frame_size_stats": frame_size_stats,
            }

            per_camera_metrics.append(camera_metric)

        return per_camera_metrics

    def _get_async_worker_aggregated_metrics(self) -> Optional[List[Dict[str, Any]]]:
        """Get aggregated metrics for worker flow (NVDEC or WorkerManager)."""
        worker_manager = getattr(self.streaming_gateway, "active_worker_manager", None)
        if not worker_manager:
            return None

        # Get active stream keys from the most recent snapshot
        stream_keys = set()
        for snapshot in self.metrics_history:
            for camera_id, metrics in snapshot.get("cameras", {}).items():
                stream_keys.add(metrics.get("stream_key"))

        # Get worker statistics (includes per_camera_stats from health reports)
        gateway_stats = self.streaming_gateway.get_statistics()
        worker_stats = gateway_stats.get("worker_stats", {})
        per_camera_stats = worker_stats.get("per_camera_stats", {})

        per_camera_metrics = []

        for stream_key in stream_keys:
            if not stream_key:
                continue

            camera_id = self.streaming_gateway.get_camera_id_for_stream_key(stream_key)
            if not camera_id:
                camera_id = stream_key.split("_")[0] if "_" in stream_key else stream_key

            camera_stats = per_camera_stats.get(stream_key, {})

            fps_data = camera_stats.get("fps", {})
            fps_stats = {
                "min": fps_data.get("min", 0.0),
                "max": fps_data.get("max", 0.0),
                "avg": fps_data.get("avg", 0.0),
                "p0": fps_data.get("min", 0.0),
                "p50": fps_data.get("avg", 0.0),
                "p100": fps_data.get("max", 0.0),
                "unit": "fps",
            }

            read_time_ms = camera_stats.get("read_time_ms", {})
            read_stats = {
                "min": read_time_ms.get("min", 0.0),
                "max": read_time_ms.get("max", 0.0),
                "avg": read_time_ms.get("avg", 0.0),
                "p0": read_time_ms.get("min", 0.0),
                "p50": read_time_ms.get("avg", 0.0),
                "p100": read_time_ms.get("max", 0.0),
                "unit": "ms",
            }

            write_time_ms = camera_stats.get("write_time_ms", {})
            write_stats = {
                "min": write_time_ms.get("min", 0.0),
                "max": write_time_ms.get("max", 0.0),
                "avg": write_time_ms.get("avg", 0.0),
                "p0": write_time_ms.get("min", 0.0),
                "p50": write_time_ms.get("avg", 0.0),
                "p100": write_time_ms.get("max", 0.0),
                "unit": "ms",
            }

            frame_size_data = camera_stats.get("frame_size_bytes", {})
            frame_size_stats = {
                "min": frame_size_data.get("min", 0.0),
                "max": frame_size_data.get("max", 0.0),
                "avg": frame_size_data.get("avg", 0.0),
                "p0": frame_size_data.get("min", 0.0),
                "p50": frame_size_data.get("avg", 0.0),
                "p100": frame_size_data.get("max", 0.0),
                "unit": "bytes",
            }

            camera_metric = {
                "camera_id": camera_id,
                "camera_reading": {"throughput": fps_stats, "latency": read_stats},
                "gateway_sending": {"throughput": fps_stats, "latency": write_stats},
                "frame_size_stats": frame_size_stats,
                "flow_type": "async_workers",
            }

            per_camera_metrics.append(camera_metric)

        return per_camera_metrics
