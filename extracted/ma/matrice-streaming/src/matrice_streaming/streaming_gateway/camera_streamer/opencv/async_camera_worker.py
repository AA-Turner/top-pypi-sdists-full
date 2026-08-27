"""Async camera worker process for handling multiple cameras concurrently.

Captures frames via OpenCV, optionally JPEG-encodes them, and publishes to
DataBus SHM ring buffers. Same architecture as the NVDEC path — the only
difference is the decoder (cv2.VideoCapture vs NVDEC hardware). Frame-skip policy
lives behind a pluggable FrameOptimizer (see camera_streamer/frame_optimizer.py).
"""

from __future__ import annotations

import asyncio
import atexit
import logging
import os
import queue
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Deque, Dict, List, Optional, Tuple

import cv2
import psutil
from matrice_common.stream import DataBus
from matrice_common.stream.databus import DataBusProducer

from ..databus_backpressure import BackpressurePublisher
from ..frame_optimizer import build_frame_optimizer
from . import frame_processor
from .video_capture_manager import VideoCaptureManager

# Limit OpenCV/BLAS thread spawning — each worker is a separate process
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["KMP_NUM_THREADS"] = "1"
os.environ["KMP_BLOCKTIME"] = "0"
os.environ["TBB_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
cv2.setNumThreads(1)
cv2.setUseOptimized(True)
cv2.ocl.setUseOpenCL(False)


def _empty_stat() -> Dict[str, float]:
    return {"min": 0, "max": 0, "avg": 0}


class AsyncCameraWorker:
    """Async worker that captures frames via OpenCV and publishes to DataBus.

    Runs an async event loop to handle multiple cameras concurrently. Frames are
    JPEG-encoded (default) and published to POSIX SHM via DataBus, using the same
    address scheme as the NVDEC path: ``/dev/shm/databus__{camera_id}__sg__frames``.
    """

    def __init__(
        self,
        worker_id: int,
        camera_configs: List[Dict[str, Any]],
        stop_event: Any,  # multiprocessing.Event
        health_queue: Any,  # multiprocessing.Queue
        command_queue: Optional[Any] = None,
        response_queue: Optional[Any] = None,
        # Frame encoding
        jpeg_encode: bool = True,
        jpeg_quality: int = 90,
        # DataBus
        num_slots: int = 32,
        max_msg_size: int = 300_000,  # 300KB covers 1080p JPEG at quality 90
        # Frame-skip policy
        optimizer_config: Optional[Dict[str, Any]] = None,
        # MLA-010 OpenCV path optimizations (opt-in; default off per REFACTORING_PLAN §20)
        use_frame_pool: bool = False,
        use_backpressure: bool = False,
        use_executor_publish: bool = False,
    ):
        self.worker_id = worker_id
        self.camera_configs = camera_configs
        self.stop_event = stop_event
        self.health_queue = health_queue
        self.command_queue = command_queue
        self.response_queue = response_queue

        self.logger = logging.getLogger(f"AsyncWorker-{worker_id}")
        self.logger.info(f"Initializing worker {worker_id} with {len(camera_configs)} cameras")

        self.capture_manager = VideoCaptureManager()
        self.optimizer = build_frame_optimizer(optimizer_config)
        self.use_frame_pool = use_frame_pool
        self.use_backpressure = use_backpressure
        self.use_executor_publish = use_executor_publish
        frame_processor.set_use_frame_pool(use_frame_pool)

        # Camera tasks and captures
        self.camera_tasks: Dict[str, asyncio.Task] = {}
        self.captures: Dict[str, cv2.VideoCapture] = {}

        # DataBus producers (one per camera, created lazily)
        self._producers: Dict[str, DataBusProducer] = {}
        self._bp_publishers: Dict[str, BackpressurePublisher] = {}
        self.jpeg_encode = jpeg_encode
        self.jpeg_quality = jpeg_quality
        self.num_slots = num_slots
        self.max_msg_size = max_msg_size

        # ThreadPoolExecutor for I/O-bound frame capture
        num_capture_threads = min(64, max(1, len(camera_configs)))
        self.capture_executor = ThreadPoolExecutor(max_workers=num_capture_threads)
        self.num_capture_threads = num_capture_threads
        self.publish_executor: Optional[ThreadPoolExecutor] = None
        self.num_publish_threads = 0
        if self.use_executor_publish:
            num_publish_threads = min(64, max(1, len(camera_configs)))
            self.publish_executor = ThreadPoolExecutor(max_workers=num_publish_threads)
            self.num_publish_threads = num_publish_threads

        # Metrics tracking
        self._encoding_times: Deque[float] = deque(maxlen=100)
        self._frames_encoded = 0
        self._encoding_errors = 0
        # Per-camera publish counters for real FPS in health reports
        self._cam_frames: Dict[str, int] = {}
        self._cam_started_at: Dict[str, float] = {}
        self._cam_last_bytes: Dict[str, int] = {}
        self._process_info = psutil.Process(os.getpid())

        atexit.register(self._cleanup_producers)

        self.logger.info(
            f"Worker {worker_id}: Created capture pool ({num_capture_threads} threads), "
            f"DataBus mode (jpeg={jpeg_encode}, quality={jpeg_quality}, "
            f"slots={num_slots}, max_msg_size={max_msg_size})"
        )

    def _get_or_create_producer(self, camera_id: str, width: int, height: int) -> DataBusProducer:
        """Get or lazily create a DataBus producer for a camera."""
        if camera_id in self._producers:
            return self._producers[camera_id]

        if self.jpeg_encode:
            producer = DataBus.producer(
                camera_id,
                "sg",
                "frames",
                "bytes",
                num_slots=self.num_slots,
                max_msg_size=self.max_msg_size,
            )
        else:
            # Raw BGR: need enough space for full frame + metadata overhead
            raw_size = width * height * 3 + 1024
            producer = DataBus.producer(
                camera_id,
                "sg",
                "frames",
                "numpy",
                num_slots=self.num_slots,
                max_msg_size=raw_size,
            )

        self._producers[camera_id] = producer
        if self.use_backpressure:
            self._bp_publishers[camera_id] = BackpressurePublisher(producer, camera_id, maxsize=self.num_slots)
        self.logger.info(
            f"Worker {self.worker_id}: Created DataBus producer for {camera_id} "
            f"({'jpeg' if self.jpeg_encode else 'bgr'} {width}x{height})"
        )
        return producer

    def _publish_frame_sync(self, frame, camera_id: str, width: int, height: int):
        """Encode (optionally) and publish a frame to DataBus (blocking)."""
        # monotonic: this measures a duration, so it must not be affected by an NTP
        # step. `_cam_started_at` below stays on the wall clock deliberately -- that is
        # a timestamp reported outward, not an interval.
        encode_start = time.monotonic()

        if self.jpeg_encode:
            ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality])
            if not ok:
                self._encoding_errors += 1
                return
            data = bytes(buf)
            fmt = "jpeg"
        else:
            data = frame  # numpy array
            fmt = "bgr"

        self._encoding_times.append(time.monotonic() - encode_start)
        self._frames_encoded += 1
        self._cam_frames[camera_id] = self._cam_frames.get(camera_id, 0) + 1
        self._cam_started_at.setdefault(camera_id, time.time())
        self._cam_last_bytes[camera_id] = len(data) if isinstance(data, (bytes, bytearray)) else int(frame.nbytes)

        producer = self._get_or_create_producer(camera_id, width, height)
        metadata = {
            "timestamp_ns": int(time.time() * 1e9),
            "width": width,
            "height": height,
            "format": fmt,
        }
        if self.use_backpressure:
            bp = self._bp_publishers.get(camera_id)
            if bp is None:
                bp = BackpressurePublisher(producer, camera_id, maxsize=self.num_slots)
                self._bp_publishers[camera_id] = bp
            if not bp.publish(data, metadata):
                return
        else:
            producer.publish(data, metadata)

    def _publish_frame(self, frame, camera_id: str, width: int, height: int):
        """Sync publish alias kept for unit tests and non-async callers."""
        self._publish_frame_sync(frame, camera_id, width, height)

    async def _await_publish_frame(self, frame, camera_id: str, width: int, height: int):
        """Publish without blocking the asyncio event loop when enabled."""
        if self.use_executor_publish:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                self.publish_executor,
                self._publish_frame_sync,
                frame,
                camera_id,
                width,
                height,
            )
        else:
            self._publish_frame_sync(frame, camera_id, width, height)

    def _cleanup_producers(self):
        """Close all DataBus producers."""
        for camera_id, producer in list(self._producers.items()):
            try:
                producer.close()
                self.logger.info(f"Worker {self.worker_id}: Closed DataBus producer for {camera_id}")
            except Exception as e:
                self.logger.warning(f"Worker {self.worker_id}: Error closing producer {camera_id}: {e}")
        self._producers.clear()

    async def initialize(self):
        """Initialize async resources."""
        self.logger.info(f"Worker {self.worker_id}: Initialized (DataBus mode, no Redis)")

    def _reap_finished_tasks(self):
        """Clean up completed camera tasks and log failures."""
        for stream_key, task in list(self.camera_tasks.items()):
            if task.done():
                try:
                    task.result()
                except Exception as exc:
                    self.logger.error(f"Worker {self.worker_id}: Camera {stream_key} failed: {exc}")
                del self.camera_tasks[stream_key]

    async def run(self):
        """Main worker loop."""
        try:
            await self.initialize()

            for camera_config in self.camera_configs:
                await self._add_camera_internal(camera_config)

            self._report_health("running", len(self.camera_tasks))

            command_task = None
            if self.command_queue:
                command_task = asyncio.create_task(self._command_handler(), name="command-handler")

            while not self.stop_event.is_set():
                self._reap_finished_tasks()
                self._report_health("running", len(self.camera_tasks))
                await asyncio.sleep(1.0)

            self.logger.info(f"Worker {self.worker_id}: Stop event detected, shutting down...")

            if command_task and not command_task.done():
                command_task.cancel()
                try:
                    await command_task
                except asyncio.CancelledError:
                    raise

            await self._shutdown()

        except Exception as exc:
            self.logger.error(f"Worker {self.worker_id}: Fatal error: {exc}", exc_info=True)
            self._report_health("error", error=str(exc))
            raise

    async def _read_frame(self, cap: cv2.VideoCapture) -> Tuple[bool, Optional[Any]]:
        """Read the next frame from a capture (offloaded to the capture pool)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.capture_executor, cap.read)

    async def _camera_handler(self, camera_config: Dict[str, Any]):
        """Handle a single camera with retry logic."""
        stream_key = camera_config["stream_key"]
        camera_id = camera_config.get("camera_id", stream_key)
        source = camera_config["source"]
        fps = camera_config.get("fps", 30)
        width = camera_config.get("width")
        height = camera_config.get("height")
        simulate_video_file_stream = camera_config.get("simulate_video_file_stream", False)

        MIN_RETRY_COOLDOWN = 5
        MAX_RETRY_COOLDOWN = 30
        retry_cycle = 0
        max_frame_failures = 10
        source_type = None

        # OUTER LOOP: Infinite retry for reconnection
        while not self.stop_event.is_set():
            cap = None
            consecutive_failures = 0
            first_video_ms: Optional[float] = None
            first_wall_time: Optional[float] = None
            self.optimizer.reset(stream_key)

            try:
                prepared_source = self.capture_manager.prepare_source(source, stream_key)
                cap, source_type = await asyncio.to_thread(
                    self.capture_manager.open_capture, prepared_source, width, height
                )
                self.captures[stream_key] = cap

                original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                actual_width, actual_height = frame_processor.actual_dimensions(
                    original_width, original_height, width, height
                )

                retry_cycle = 0
                self.logger.info(
                    f"Worker {self.worker_id}: Camera {stream_key} connected - "
                    f"{actual_width}x{actual_height} @ {fps} FPS (type: {source_type})"
                )

                # INNER LOOP: Process frames
                while not self.stop_event.is_set():
                    try:
                        ret, frame = await self._read_frame(cap)

                        if not ret:
                            consecutive_failures += 1
                            if source_type == "video_file":
                                if simulate_video_file_stream:
                                    self.logger.info(f"Worker {self.worker_id}: Video {stream_key} ended, restarting")
                                    await asyncio.sleep(1.0)
                                    break
                                return
                            if consecutive_failures >= max_frame_failures:
                                self.logger.warning(
                                    f"Worker {self.worker_id}: Camera {stream_key} - "
                                    f"{max_frame_failures} failures, reconnecting..."
                                )
                                break
                            await asyncio.sleep(0.1)
                            continue

                        consecutive_failures = 0

                        video_ts_ms = cap.get(cv2.CAP_PROP_POS_MSEC) if source_type == "video_file" else None

                        # Frame-skip policy (FPS decimation by default)
                        frame = self.optimizer.optimize(stream_key, frame)
                        if frame is None:
                            continue

                        if width or height:
                            frame = frame_processor.resize_frame(frame, width, height)

                        await self._await_publish_frame(frame, camera_id, actual_width, actual_height)

                        # PTS-based pacing for video files
                        if source_type == "video_file" and video_ts_ms is not None:
                            if first_video_ms is None:
                                first_video_ms = video_ts_ms
                                first_wall_time = time.time()
                            else:
                                target_wall = first_wall_time + (video_ts_ms - first_video_ms) / 1000.0
                                sleep_time = target_wall - time.time()
                                if sleep_time > 0:
                                    await asyncio.sleep(sleep_time)

                    except asyncio.CancelledError:
                        raise
                    except Exception as exc:
                        self.logger.error(
                            f"Worker {self.worker_id}: Error in camera {stream_key}: {exc}",
                            exc_info=True,
                        )
                        consecutive_failures += 1
                        if consecutive_failures >= max_frame_failures:
                            break
                        await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                raise
            except Exception as exc:
                self.logger.error(
                    f"Worker {self.worker_id}: Camera {stream_key} connection error: {exc}",
                    exc_info=True,
                )
            finally:
                if cap:
                    try:
                        cap.release()
                    except Exception:  # nosec B110
                        pass
                if stream_key in self.captures:
                    del self.captures[stream_key]

            if self.stop_event.is_set():
                break

            if source_type == "video_file" and simulate_video_file_stream:
                continue

            cooldown = min(MAX_RETRY_COOLDOWN, MIN_RETRY_COOLDOWN + retry_cycle)
            self.logger.info(f"Worker {self.worker_id}: Retrying camera {stream_key} in {cooldown}s")
            await asyncio.sleep(cooldown)
            retry_cycle += 1

    # ========================================================================
    # Dynamic Camera Management
    # ========================================================================

    async def _command_handler(self):
        """Handle dynamic camera commands from manager."""
        while not self.stop_event.is_set():
            try:
                command = self._get_command_nonblocking()
                if command:
                    await self._process_command(command)
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                self.logger.error(
                    f"Worker {self.worker_id}: Command handler error: {exc}",
                    exc_info=True,
                )
                await asyncio.sleep(1.0)

    def _get_command_nonblocking(self) -> Optional[Dict[str, Any]]:
        """Get command from queue without blocking."""
        if not self.command_queue:
            return None
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
        except Exception as exc:
            # An empty queue is the expected case (handled above). Anything else
            # (e.g. a broken/closed pipe to the manager) is NOT "no command" —
            # log it instead of silently treating it as empty forever, which is
            # how a wedged worker goes unnoticed.
            self.logger.warning("Worker %s: command queue read failed: %s", self.worker_id, exc)
            return None

    async def _process_command(self, command: Dict[str, Any]):
        """Process a dynamic camera command."""
        cmd_type = command.get("type", "")
        camera_config = command.get("camera_config", {})
        stream_key = command.get("stream_key") or camera_config.get("stream_key", "")

        if cmd_type == "add_camera":
            success = await self._add_camera_internal(camera_config)
            self._send_response(cmd_type, stream_key, success)
        elif cmd_type == "remove_camera":
            success = await self._remove_camera_internal(stream_key)
            self._send_response(cmd_type, stream_key, success)
        elif cmd_type == "update_camera":
            await self._remove_camera_internal(stream_key)
            success = await self._add_camera_internal(camera_config)
            self._send_response(cmd_type, stream_key, success)
        else:
            self.logger.warning(f"Worker {self.worker_id}: Unknown command type: {cmd_type}")

    async def _add_camera_internal(self, camera_config: Dict[str, Any]) -> bool:
        """Add a camera and start its streaming task."""
        stream_key = camera_config.get("stream_key")
        if not stream_key:
            self.logger.error(f"Worker {self.worker_id}: Camera config missing stream_key")
            return False

        if stream_key in self.camera_tasks:
            self.logger.warning(f"Worker {self.worker_id}: Camera {stream_key} already exists")
            return False

        try:
            task = asyncio.create_task(self._camera_handler(camera_config), name=f"camera-{stream_key}")
            self.camera_tasks[stream_key] = task
            self.logger.info(f"Worker {self.worker_id}: Added camera {stream_key}")
            return True
        except Exception as exc:
            self.logger.error(
                f"Worker {self.worker_id}: Failed to add camera {stream_key}: {exc}",
                exc_info=True,
            )
            return False

    async def _remove_camera_internal(self, stream_key: str) -> bool:
        """Remove a camera and stop its streaming task."""
        if stream_key not in self.camera_tasks:
            self.logger.warning(f"Worker {self.worker_id}: Camera {stream_key} not found")
            return False

        try:
            task = self.camera_tasks[stream_key]
            if not task.done():
                task.cancel()
                try:
                    await asyncio.wait_for(task, timeout=5.0)
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    pass

            del self.camera_tasks[stream_key]

            if stream_key in self.captures:
                self.captures[stream_key].release()
                del self.captures[stream_key]

            # stream_key maps to camera_id
            if stream_key in self._producers:
                self._producers[stream_key].close()
                del self._producers[stream_key]

            self.optimizer.reset(stream_key)

            self.logger.info(f"Worker {self.worker_id}: Removed camera {stream_key}")
            return True
        except Exception as exc:
            self.logger.error(
                f"Worker {self.worker_id}: Error removing camera {stream_key}: {exc}",
                exc_info=True,
            )
            return False

    def _send_response(self, cmd_type: str, stream_key: str, success: bool, error: Optional[str] = None):
        """Send response back to manager."""
        if self.response_queue:
            try:
                self.response_queue.put_nowait(
                    {
                        "worker_id": self.worker_id,
                        "command_type": cmd_type,
                        "stream_key": stream_key,
                        "success": success,
                        "error": error,
                        "timestamp": time.time(),
                    }
                )
            except Exception as exc:
                self.logger.warning(f"Worker {self.worker_id}: Failed to send response: {exc}")

    async def _shutdown(self):
        """Gracefully shutdown worker."""
        self.logger.info(f"Worker {self.worker_id}: Starting shutdown")

        for task in self.camera_tasks.values():
            if not task.done():
                task.cancel()

        if self.camera_tasks:
            await asyncio.gather(*self.camera_tasks.values(), return_exceptions=True)

        for cap in list(self.captures.values()):
            cap.release()
        self.captures.clear()

        self._cleanup_producers()

        try:
            self.capture_executor.shutdown(wait=True, cancel_futures=False)
            if self.publish_executor is not None:
                self.publish_executor.shutdown(wait=True, cancel_futures=False)
        except Exception:  # nosec B110
            pass

        # Drive the canonical CUDA teardown so any per-worker CuPy state
        # (kernel cache, memory pool blocks) returns to the driver before
        # the worker process exits. Best-effort; never blocks shutdown.
        try:
            from matrice_common.lifecycle import finalize_cuda  # type: ignore

            finalize_cuda()
        except Exception:  # nosec B110
            pass

        self._report_health("stopped")
        self.logger.info(f"Worker {self.worker_id}: Shutdown complete")

    def _build_per_camera_stats(self) -> Dict[str, Dict[str, Any]]:
        """Build the per-camera stats dict consumed by metrics/manager.py.

        Same minimal shape the NVDEC backend synthesizes (see
        nvdec_worker_manager._synthesize per_camera_stats): real publish FPS plus
        encoding time and last frame size; read/write/process times are not tracked
        on this path and stay zeroed.
        """
        now = time.time()
        avg_encode_ms = (sum(self._encoding_times) / len(self._encoding_times)) * 1000 if self._encoding_times else 0
        stats: Dict[str, Dict[str, Any]] = {}
        for stream_key in self.camera_tasks:
            frames = self._cam_frames.get(stream_key, 0)
            started = self._cam_started_at.get(stream_key)
            fps = frames / (now - started) if started and now > started else 0
            frame_bytes = self._cam_last_bytes.get(stream_key, 0)
            stats[stream_key] = {
                "fps": {"min": fps, "max": fps, "avg": fps},
                "read_time_ms": _empty_stat(),
                "write_time_ms": _empty_stat(),
                "encoding_time_ms": {
                    "min": avg_encode_ms,
                    "max": avg_encode_ms,
                    "avg": avg_encode_ms,
                },
                "frame_size_bytes": {
                    "min": frame_bytes,
                    "max": frame_bytes,
                    "avg": frame_bytes,
                },
            }
        return stats

    def _report_health(self, status: str, active_cameras: int = 0, error: Optional[str] = None):
        """Report health status to main process."""
        try:
            proc_cpu = 0
            proc_memory_mb = 0
            try:
                proc_cpu = self._process_info.cpu_percent(interval=None)
                proc_memory_mb = self._process_info.memory_info().rss / 1024 / 1024
            except Exception:  # nosec B110
                pass

            avg_encoding_ms = 0
            if self._encoding_times:
                avg_encoding_ms = sum(self._encoding_times) / len(self._encoding_times) * 1000

            self.health_queue.put_nowait(
                {
                    "worker_id": self.worker_id,
                    "status": status,
                    "active_cameras": active_cameras,
                    "timestamp": time.time(),
                    "error": error,
                    "metrics": {
                        "cpu_percent": proc_cpu,
                        "memory_mb": proc_memory_mb,
                        "frames_encoded": self._frames_encoded,
                        "encoding_errors": self._encoding_errors,
                        "avg_encoding_ms": avg_encoding_ms,
                        "capture_threads": self.num_capture_threads,
                        "publish_threads": self.num_publish_threads,
                        "executor_publish": self.use_executor_publish,
                        "pool_exhausted_total": frame_processor.pool_exhausted_total() if self.use_frame_pool else 0,
                        "frames_dropped_bp": sum(p.metrics.frames_dropped for p in self._bp_publishers.values())
                        if self.use_backpressure
                        else 0,
                        # Data-plane loss: frames written over a slot the slowest consumer
                        # had not read. Reported beside frames_dropped_bp rather than added
                        # to it -- a refusal and an overwrite are different events, and one
                        # counter cannot carry two meanings. Cumulative, because this whole
                        # metrics block is an absolute snapshot the parent overwrites.
                        "frames_overwritten_bp": sum(p.metrics.frames_overwritten for p in self._bp_publishers.values())
                        if self.use_backpressure
                        else 0,
                    },
                    "per_camera_stats": self._build_per_camera_stats(),
                }
            )
        except queue.Full:
            # Health queue backed up: drop this report (the manager will notice
            # the staleness). Expected under transient pressure, so keep quiet.
            self.logger.debug("Worker %s: health queue full, dropping report", self.worker_id)
        except Exception:
            # Any other failure here (e.g. a bug in stats assembly) must be loud
            # — a silently-swallowed error here is exactly how a worker "dies
            # invisibly" while liveness still looks healthy.
            self.logger.warning("Worker %s: failed to report health", self.worker_id, exc_info=True)


def run_async_worker(
    worker_id: int,
    camera_configs: List[Dict[str, Any]],
    stop_event: Any,
    health_queue: Any,
    command_queue: Optional[Any] = None,
    response_queue: Optional[Any] = None,
    # Frame encoding
    jpeg_encode: bool = True,
    jpeg_quality: int = 90,
    # DataBus
    num_slots: int = 32,
    max_msg_size: int = 300_000,
    # Frame-skip policy
    optimizer_config: Optional[Dict[str, Any]] = None,
    use_frame_pool: bool = False,
    use_backpressure: bool = False,
    use_executor_publish: bool = False,
):
    """Entry point for async worker process (called by multiprocessing.Process)."""
    # Only bootstrap root logging if the deployment hasn't already configured it
    # (basicConfig is a no-op when handlers exist, but be explicit) and take the
    # level from the environment so we don't force INFO over a deployment that
    # deliberately set WARNING. Prevents this worker from clobbering the parent's
    # logging setup — the same class of bug as the LPR "basicConfig kills INFO".
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=os.environ.get("MATRICE_WORKER_LOG_LEVEL", "INFO").upper(),
            format=f"%(asctime)s - Worker-{worker_id} - %(name)s - %(levelname)s - %(message)s",
        )

    logger = logging.getLogger(f"AsyncWorker-{worker_id}")
    logger.info(f"Starting async worker {worker_id}")

    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["KMP_NUM_THREADS"] = "1"
    cv2.setNumThreads(1)
    cv2.setUseOptimized(True)
    cv2.ocl.setUseOpenCL(False)

    try:
        worker = AsyncCameraWorker(
            worker_id=worker_id,
            camera_configs=camera_configs,
            stop_event=stop_event,
            health_queue=health_queue,
            command_queue=command_queue,
            response_queue=response_queue,
            jpeg_encode=jpeg_encode,
            jpeg_quality=jpeg_quality,
            num_slots=num_slots,
            max_msg_size=max_msg_size,
            optimizer_config=optimizer_config,
            use_frame_pool=use_frame_pool,
            use_backpressure=use_backpressure,
            use_executor_publish=use_executor_publish,
        )
        asyncio.run(worker.run())
    except Exception as exc:
        logger.exception(f"Worker {worker_id} failed: {exc}")
        raise
