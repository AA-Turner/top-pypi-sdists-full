"""Main metrics orchestrator."""

from __future__ import annotations

import logging
import time
from typing import Any, ClassVar, Dict, Optional

from .collector import MetricsCollector
from .config import MetricsConfig
from .reporter import MetricsReporter

logger = logging.getLogger(__name__)


class MetricsManager:
    """Main orchestrator for metrics collection and reporting.

    This class coordinates the collection of metrics from the streaming gateway,
    calculates statistics, and reports them via Kafka.
    """

    # ANSI escape codes for BOLD text in terminal
    BOLD: ClassVar[str] = "\033[1m"
    RESET: ClassVar[str] = "\033[0m"

    def __init__(
        self,
        streaming_gateway,
        session,
        streaming_gateway_id: str,
        action_id: Optional[str] = None,
        config: Optional[MetricsConfig] = None,
    ):
        """Initialize metrics manager.

        Args:
            streaming_gateway: StreamingGateway instance
            session: Session object for API calls
            streaming_gateway_id: ID of the streaming gateway
            action_id: Optional action ID
            config: Optional metrics configuration (uses default if not provided)
        """
        self.streaming_gateway = streaming_gateway
        self.session = session
        self.streaming_gateway_id = streaming_gateway_id
        self.action_id = action_id
        self.config = config or MetricsConfig()

        # Initialize components
        self.collector = MetricsCollector(streaming_gateway, self.config)
        self.reporter = MetricsReporter(session, streaming_gateway_id, self.config)

        # Both backends (NVDEC and WorkerManager) run in subprocesses.
        # active_worker_manager resolves to whichever one is in use.
        self.use_async_workers = getattr(streaming_gateway, "active_worker_manager", None) is not None

        # Tracking
        self.last_report_time = 0
        self.last_log_time = 0
        self._first_report_logged = False
        self.last_metrics_log_time = 0
        self.metrics_log_interval = 60.0
        self.last_aggregate_log_time = 0
        self.aggregate_log_interval = 60.0
        self.enabled = True

        flow_type = "async_workers" if self.use_async_workers else "camera_streamer"
        logger.info(f"Metrics manager initialized (flow: {flow_type})")

    def collect_and_report(self):
        """Collect current metrics and report if interval has elapsed.

        This method should be called periodically (e.g., every 1-30 seconds)
        from the health monitoring loop.
        """
        if not self.enabled:
            return

        try:
            # Always collect current snapshot
            snapshot = self.collector.collect_snapshot()
            if snapshot:
                self.collector.add_to_history(snapshot)

            current_time = time.time()

            # Log metrics summary periodically
            if current_time - self.last_metrics_log_time >= self.metrics_log_interval:
                self._log_metrics_summary(snapshot)
                self.last_metrics_log_time = current_time  # type: ignore[assignment]

            # Log aggregate metrics with BOLD every minute
            if current_time - self.last_aggregate_log_time >= self.aggregate_log_interval:
                self._log_aggregate_metrics_bold()
                self.last_aggregate_log_time = current_time  # type: ignore[assignment]

            # Report if interval has elapsed
            if current_time - self.last_report_time >= self.config.reporting_interval:
                self._generate_and_send_report()
                self.last_report_time = current_time  # type: ignore[assignment]

        except Exception as e:
            logger.exception(f"Error in metrics collect_and_report: {e}")

    def _log_metrics_summary(self, snapshot: Optional[Dict[str, Any]]):
        """Log a summary of current metrics to console."""
        try:
            gateway_stats = self.streaming_gateway.get_statistics()

            if self.use_async_workers:
                self._log_async_worker_metrics(gateway_stats, snapshot)
            else:
                self._log_camera_streamer_metrics(gateway_stats, snapshot)

        except Exception as e:
            logger.warning(f"Error logging metrics summary: {e}")

    def _log_aggregate_metrics_bold(self):
        """Log comprehensive aggregate metrics with BOLD formatting every minute."""
        try:
            gateway_stats = self.streaming_gateway.get_statistics()

            if self.use_async_workers:
                self._log_aggregate_async_workers_bold(gateway_stats)
            else:
                self._log_aggregate_camera_streamer_bold(gateway_stats)

        except Exception as e:
            logger.warning(f"Error logging aggregate metrics: {e}")

    def _log_aggregate_async_workers_bold(self, gateway_stats: Dict[str, Any]):
        """Log aggregate metrics for workers (NVDEC or WorkerManager) with BOLD formatting."""
        worker_stats = gateway_stats.get("worker_stats", {})
        stream_keys = gateway_stats.get("my_stream_keys", [])
        runtime = gateway_stats.get("runtime_seconds", 0)

        num_workers = worker_stats.get("num_workers", 0)
        running_workers = worker_stats.get("running_workers", 0)
        total_cameras = worker_stats.get("total_cameras", len(stream_keys))
        per_camera_stats = worker_stats.get("per_camera_stats", {})

        is_nvdec = getattr(self.streaming_gateway, "use_nvdec", False)
        wm = getattr(self.streaming_gateway, "active_worker_manager", None)

        use_shm = False
        shm_format = "N/A"
        if wm and not is_nvdec:
            use_shm = getattr(wm, "use_shm", False)
            shm_format = getattr(wm, "shm_frame_format", "N/A") if use_shm else "N/A"

        # Aggregate FPS stats (both NVDEC and WorkerManager now provide per_camera_stats)
        total_fps = 0.0
        fps_values = []
        for stream_key, stats in per_camera_stats.items():
            fps_avg = stats.get("fps", {}).get("avg", 0)
            if fps_avg > 0:
                total_fps += fps_avg
                fps_values.append(fps_avg)

        avg_fps = sum(fps_values) / len(fps_values) if fps_values else 0
        min_fps = min(fps_values) if fps_values else 0
        max_fps = max(fps_values) if fps_values else 0

        # Aggregate latency stats (in ms)
        read_times = []
        write_times = []
        encoding_times = []

        for stream_key, stats in per_camera_stats.items():
            read_ms = stats.get("read_time_ms", {}).get("avg", 0)
            write_ms = stats.get("write_time_ms", {}).get("avg", 0)
            encoding_ms = stats.get("encoding_time_ms", {}).get("avg", 0)

            if read_ms > 0:
                read_times.append(read_ms)
            if write_ms > 0:
                write_times.append(write_ms)
            if encoding_ms > 0:
                encoding_times.append(encoding_ms)

        avg_read_ms = sum(read_times) / len(read_times) if read_times else 0
        avg_write_ms = sum(write_times) / len(write_times) if write_times else 0
        avg_encoding_ms = sum(encoding_times) / len(encoding_times) if encoding_times else 0
        total_latency_ms = avg_read_ms + avg_encoding_ms + avg_write_ms

        # Aggregate frame size and throughput
        frame_sizes = []
        for stream_key, stats in per_camera_stats.items():
            frame_size_bytes = stats.get("frame_size_bytes", {}).get("avg", 0)
            if frame_size_bytes > 0:
                frame_sizes.append(frame_size_bytes)

        avg_frame_size_kb = (sum(frame_sizes) / len(frame_sizes) / 1024) if frame_sizes else 0

        total_throughput_kbps = 0.0
        for stream_key, stats in per_camera_stats.items():
            fps_avg = stats.get("fps", {}).get("avg", 0)
            frame_size_bytes = stats.get("frame_size_bytes", {}).get("avg", 0)
            if fps_avg > 0 and frame_size_bytes > 0:
                total_throughput_kbps += (fps_avg * frame_size_bytes) / 1024

        total_throughput_mbps = total_throughput_kbps / 1024

        # Backpressure figures, aggregated by WorkerManager.get_worker_statistics().
        # 0 for NVDEC, which has no per-camera backpressure yet.
        pool_exhausted_total = worker_stats.get("pool_exhausted_total", 0)
        frames_dropped_bp_total = worker_stats.get("frames_dropped_bp_total", 0)
        # Frames the producer DID write over a slot the slowest consumer had not read.
        # Rendered beside frames_dropped rather than added to it: the two are different
        # events, and a panel showing only the first would report a consumer losing every
        # other frame as a healthy gateway.
        frames_overwritten_bp_total = worker_stats.get("frames_overwritten_bp_total", 0)

        B = self.BOLD
        R = self.RESET

        if is_nvdec:
            nvdec_cfg = worker_stats.get("nvdec_config", {})
            mode_str = f"NVDEC ({nvdec_cfg.get('frame_size', 'NV12')})"
            encode_label = "Decode"
        elif use_shm:
            mode_str = f"SHM ({shm_format})"
            encode_label = "Convert"
        else:
            mode_str = "JPEG"
            encode_label = "Encode"

        logger.info(
            f"\n{B}{'=' * 80}{R}\n"
            f"{B}[STREAMING GATEWAY AGGREGATE METRICS - 1 MIN SUMMARY]{R}\n"
            f"{B}{'=' * 80}{R}\n"
            f"{B}Mode:{R} {mode_str} | "
            f"{B}Workers:{R} {running_workers}/{num_workers} active | "
            f"{B}Cameras:{R} {total_cameras} streaming | "
            f"{B}Runtime:{R} {runtime:.0f}s\n"
            f"{B}{'─' * 80}{R}\n"
            f"{B}FPS:{R} avg={avg_fps:.1f} | min={min_fps:.1f} | max={max_fps:.1f} | "
            f"{B}TOTAL={total_fps:.1f} fps{R}\n"
            f"{B}{'─' * 80}{R}\n"
            f"{B}LATENCY BREAKDOWN:{R}\n"
            f"  • Read:     {avg_read_ms:.2f} ms (avg)\n"
            f"  • {encode_label}:   {avg_encoding_ms:.2f} ms (avg)\n"
            f"  • Write:    {avg_write_ms:.2f} ms (avg)\n"
            f"  • {B}TOTAL:    {total_latency_ms:.2f} ms{R}\n"
            f"{B}{'─' * 80}{R}\n"
            f"{B}THROUGHPUT:{R}\n"
            f"  • Avg Frame Size: {avg_frame_size_kb:.1f} KB\n"
            f"  • {B}TOTAL: {total_throughput_mbps:.2f} MB/s ({total_throughput_kbps:.1f} KB/s){R}\n"
            f"{B}{'─' * 80}{R}\n"
            f"{B}BACKPRESSURE:{R} frames_dropped={frames_dropped_bp_total} | "
            f"frames_overwritten={frames_overwritten_bp_total} | "
            f"pool_exhausted={pool_exhausted_total}\n"
            f"{B}{'=' * 80}{R}"
        )

    @staticmethod
    def _collect_stream_timing(cam_stats: Any, stream_keys: list) -> Dict[str, Any]:
        """Collect per-stream timing stats into aggregate lists."""
        fps_values: list = []
        read_times: list = []
        write_times: list = []
        encoding_times: list = []
        frame_sizes: list = []
        total_throughput_kbps = 0.0

        for stream_key in stream_keys:
            timing_stats = cam_stats.get_timing_statistics(stream_key)
            if not timing_stats:
                continue
            fps_avg = timing_stats.get("fps", {}).get("avg", 0)
            if fps_avg > 0:
                fps_values.append(fps_avg)

            read_ms = timing_stats.get("read_time_ms", {}).get("avg", 0)
            write_ms = timing_stats.get("write_time_ms", {}).get("avg", 0)
            encoding_ms = timing_stats.get("encoding_time_ms", {}).get("avg", 0)
            frame_size_bytes = timing_stats.get("frame_size_bytes", {}).get("avg", 0)

            if read_ms > 0:
                read_times.append(read_ms)
            if write_ms > 0:
                write_times.append(write_ms)
            if encoding_ms > 0:
                encoding_times.append(encoding_ms)
            if frame_size_bytes > 0:
                frame_sizes.append(frame_size_bytes)
            if fps_avg > 0 and frame_size_bytes > 0:
                total_throughput_kbps += (fps_avg * frame_size_bytes) / 1024

        _avg = lambda lst: sum(lst) / len(lst) if lst else 0  # noqa: E731
        return {
            "fps_values": fps_values,
            "avg_read_ms": _avg(read_times),
            "avg_write_ms": _avg(write_times),
            "avg_encoding_ms": _avg(encoding_times),
            "avg_frame_size_kb": (_avg(frame_sizes) / 1024) if frame_sizes else 0,
            "total_throughput_kbps": total_throughput_kbps,
        }

    def _log_aggregate_camera_streamer_bold(self, gateway_stats: Dict[str, Any]):
        """Log aggregate metrics for CameraStreamer with BOLD formatting."""
        camera_streamer = getattr(self.streaming_gateway, "camera_manager", None)
        cam_stats = getattr(camera_streamer, "statistics", None)
        if not camera_streamer or cam_stats is None:
            return

        stream_keys = gateway_stats.get("my_stream_keys", [])
        transmission_stats = gateway_stats.get("transmission_stats", {})
        runtime = gateway_stats.get("runtime_seconds", 0)

        s = self._collect_stream_timing(cam_stats, stream_keys)
        fps_values = s["fps_values"]
        total_fps = sum(fps_values)
        avg_fps = sum(fps_values) / len(fps_values) if fps_values else 0
        min_fps = min(fps_values) if fps_values else 0
        max_fps = max(fps_values) if fps_values else 0
        total_latency_ms = s["avg_read_ms"] + s["avg_encoding_ms"] + s["avg_write_ms"]

        frames_sent = transmission_stats.get("frames_sent_full", 0)
        frames_skipped = transmission_stats.get("frames_skipped", 0)

        B = self.BOLD
        R = self.RESET

        logger.info(
            f"\n{B}{'=' * 80}{R}\n"
            f"{B}[STREAMING GATEWAY AGGREGATE METRICS - 1 MIN SUMMARY]{R}\n"
            f"{B}{'=' * 80}{R}\n"
            f"{B}Cameras:{R} {len(stream_keys)} streaming | "
            f"{B}Runtime:{R} {runtime:.0f}s | "
            f"{B}Frames:{R} sent={frames_sent}, skipped={frames_skipped}\n"
            f"{B}{'─' * 80}{R}\n"
            f"{B}FPS:{R} avg={avg_fps:.1f} | min={min_fps:.1f} | max={max_fps:.1f} | "
            f"{B}TOTAL={total_fps:.1f} fps{R}\n"
            f"{B}{'─' * 80}{R}\n"
            f"{B}LATENCY BREAKDOWN:{R}\n"
            f"  • Read:     {s['avg_read_ms']:.2f} ms (avg)\n"
            f"  • Encode:   {s['avg_encoding_ms']:.2f} ms (avg)\n"
            f"  • Write:    {s['avg_write_ms']:.2f} ms (avg)\n"
            f"  • {B}TOTAL:    {total_latency_ms:.2f} ms{R}\n"
            f"{B}{'─' * 80}{R}\n"
            f"{B}THROUGHPUT:{R}\n"
            f"  • Avg Frame Size: {s['avg_frame_size_kb']:.1f} KB\n"
            f"  • {B}TOTAL: {s['total_throughput_kbps'] / 1024:.2f} MB/s ({s['total_throughput_kbps']:.1f} KB/s){R}\n"
            f"{B}{'=' * 80}{R}"
        )

    def _log_camera_streamer_metrics(self, gateway_stats: Dict[str, Any], snapshot: Optional[Dict[str, Any]]):
        """Log metrics summary for CameraStreamer flow."""
        camera_streamer = getattr(self.streaming_gateway, "camera_manager", None)
        cam_stats = getattr(camera_streamer, "statistics", None)
        if not camera_streamer or cam_stats is None:
            return

        stream_keys = gateway_stats.get("my_stream_keys", [])
        transmission_stats = gateway_stats.get("transmission_stats", {})
        runtime = gateway_stats.get("runtime_seconds", 0)

        camera_summaries = []
        total_frame_size_kb = 0
        camera_count_with_size = 0

        for stream_key in stream_keys[:5]:
            timing_stats = cam_stats.get_timing_statistics(stream_key)
            if timing_stats:
                read_ms = timing_stats.get("read_time_ms", {}).get("avg", 0.0)
                write_ms = timing_stats.get("write_time_ms", {}).get("avg", 0.0)
                frame_size_bytes = timing_stats.get("frame_size_bytes", {}).get("avg", 0)
                frame_kb = frame_size_bytes / 1024
                camera_summaries.append(f"{stream_key}(r:{read_ms:.1f}ms,w:{write_ms:.1f}ms,{frame_kb:.1f}KB)")

                if frame_size_bytes > 0:
                    total_frame_size_kb += frame_kb
                    camera_count_with_size += 1

        avg_frame_size_kb = total_frame_size_kb / camera_count_with_size if camera_count_with_size > 0 else 0

        frames_sent = transmission_stats.get("frames_sent_full", 0)
        avg_fps = frames_sent / runtime if runtime > 0 else 0

        logger.info(
            f"[METRICS] CameraStreamer | "
            f"cameras={len(stream_keys)} | "
            f"frames_sent={frames_sent} | "
            f"avg_fps={avg_fps:.1f} | "
            f"avg_frame_size={avg_frame_size_kb:.1f}KB | "
            f"runtime={runtime:.0f}s | "
            f"samples: {', '.join(camera_summaries[:3])}"
        )

    def _log_async_worker_metrics(self, gateway_stats: Dict[str, Any], snapshot: Optional[Dict[str, Any]]):
        """Log metrics summary for worker flow (NVDEC or WorkerManager)."""
        worker_stats = gateway_stats.get("worker_stats", {})
        stream_keys = gateway_stats.get("my_stream_keys", [])
        runtime = gateway_stats.get("runtime_seconds", 0)
        is_nvdec = getattr(self.streaming_gateway, "use_nvdec", False)

        num_workers = worker_stats.get("num_workers", 0)
        running_workers = worker_stats.get("running_workers", 0)
        total_cameras = worker_stats.get("total_cameras", len(stream_keys))
        per_camera_stats = worker_stats.get("per_camera_stats", {})

        # Build worker/GPU load description
        worker_loads = []
        if is_nvdec:
            per_gpu = worker_stats.get("per_gpu_stats", {})
            for gpu_label, gs in per_gpu.items():
                worker_loads.append(f"{gpu_label}:{gs.get('cameras', 0)}cam ({gs.get('fps', 0):.0f}fps)")
        else:
            worker_camera_counts = worker_stats.get("worker_camera_counts", {})
            health_reports = worker_stats.get("health_reports", {})
            for worker_id, count in worker_camera_counts.items():
                health = health_reports.get(worker_id, {})
                status = health.get("status", "unknown")
                worker_loads.append(f"W{worker_id}:{count}({status})")

        # Per-camera frame size (from WorkerManager health reports)
        total_frame_size_kb = 0
        camera_count_with_size = 0
        for stream_key, stats in per_camera_stats.items():
            frame_size_bytes = stats.get("frame_size_bytes", {}).get("avg", 0)
            if frame_size_bytes > 0:
                total_frame_size_kb += frame_size_bytes / 1024
                camera_count_with_size += 1

        avg_frame_size_kb = total_frame_size_kb / camera_count_with_size if camera_count_with_size > 0 else 0

        # FPS: prefer per-camera breakdown, fall back to NVDEC aggregate
        total_fps = 0
        camera_count_with_fps = 0
        for stream_key, stats in per_camera_stats.items():
            fps_avg = stats.get("fps", {}).get("avg", 0)
            if fps_avg > 0:
                total_fps += fps_avg
                camera_count_with_fps += 1

        avg_fps = total_fps / camera_count_with_fps if camera_count_with_fps > 0 else 0

        backend_label = "NVDEC" if is_nvdec else "AsyncWorkers"
        logger.info(
            f"[METRICS] {backend_label} | "
            f"workers={running_workers}/{num_workers} | "
            f"cameras={total_cameras} | "
            f"avg_fps={avg_fps:.1f} | "
            f"avg_frame_size={avg_frame_size_kb:.1f}KB | "
            f"runtime={runtime:.0f}s | "
            f"distribution: {', '.join(worker_loads[:4])}"
        )

    def _generate_and_send_report(self):
        """Generate metrics report and send to Kafka."""
        try:
            per_camera_metrics = self.collector.get_aggregated_metrics()

            if not per_camera_metrics:
                logger.debug("No metrics data available for reporting")
                return

            is_nvdec = getattr(self.streaming_gateway, "use_nvdec", False)
            if is_nvdec:
                flow_type = "nvdec"
            elif self.use_async_workers:
                flow_type = "async_workers"
            else:
                flow_type = "camera_streamer"
            report = {
                "streaming_gateway_id": self.streaming_gateway_id,
                "action_id": self.action_id or "unknown",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "per_camera_metrics": per_camera_metrics,
                "flow_type": flow_type,
            }

            success = self.reporter.send_metrics(report)

            current_time = time.time()
            is_first = not self._first_report_logged
            should_log = is_first or (current_time - self.last_log_time >= self.config.log_interval)

            if success:
                if should_log:
                    logger.info(
                        f"Metrics report sent successfully ({len(per_camera_metrics)} cameras, flow={flow_type})"
                    )
                    self.last_log_time = current_time  # type: ignore[assignment]
                    self._first_report_logged = True

                # Clear timing history after successful reporting
                if not self.use_async_workers:
                    camera_streamer = getattr(self.streaming_gateway, "camera_manager", None)
                    cam_stats = getattr(camera_streamer, "statistics", None)
                    if camera_streamer and cam_stats is not None:
                        cam_stats.clear_timing_history()
                        if should_log:
                            logger.debug("Cleared timing history after successful metrics reporting")
            else:
                if should_log:
                    logger.warning(f"Failed to send metrics report (flow={flow_type})")
                    self.last_log_time = current_time  # type: ignore[assignment]
                    self._first_report_logged = True

        except Exception as e:
            logger.exception(f"Error generating/sending metrics report: {e}")

    def stop(self):
        """Stop metrics collection and close resources."""
        self.enabled = False
        self.reporter.close()
        logger.info("Metrics manager stopped")
