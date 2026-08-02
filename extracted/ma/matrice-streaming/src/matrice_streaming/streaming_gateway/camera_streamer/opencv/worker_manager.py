"""Worker manager for coordinating multiple async camera workers.

Manages a pool of async worker processes, distributing cameras across them.
Workers publish frames to DataBus SHM (same path as NVDEC: /dev/shm/databus__*__sg__frames).
"""

from __future__ import annotations

import glob
import logging
import multiprocessing
import os
import queue
import signal
import sys
import threading
import time
from typing import Any, Dict, List, Optional

from ...constants import DEFAULT_OPENCV_OPTIMIZATION_MODE
from ..shm_liveness import held_shm_paths, is_shm_path_live
from .async_camera_worker import run_async_worker

_VALID_OPENCV_OPTIM_MODES = frozenset(("none", "frame_pool", "backpressure", "executor_offload", "combined"))


def resolve_opencv_optimization_mode(explicit: Optional[str] = None) -> str:
    """Resolve OpenCV optimization mode (REFACTORING_PLAN §20 — evidence-only, opt-in).

    Default is ``none`` (prior behavior). Override via constructor or
    ``MATRICE_SG_OPENCV_OPTIM``. ``combined`` enables frame_pool + backpressure
    only; ``executor_offload`` is separate (plan excludes added postproc threads
    from combined/default paths).
    """
    if explicit is not None and str(explicit).strip():
        mode = str(explicit).strip().lower()
    else:
        mode = os.getenv("MATRICE_SG_OPENCV_OPTIM", DEFAULT_OPENCV_OPTIMIZATION_MODE).strip().lower()
    if mode not in _VALID_OPENCV_OPTIM_MODES:
        logging.getLogger(__name__).warning("Unknown MATRICE_SG_OPENCV_OPTIM=%r; using none", mode)
        return "none"
    return mode


class WorkerManager:
    """Manages multiple async camera worker processes with dynamic scaling.

    Each worker handles multiple cameras concurrently using async I/O.
    Frames are published to DataBus SHM ring buffers, matching the NVDEC
    architecture — the only difference is the decoder (OpenCV vs NVDEC).
    """

    def __init__(
        self,
        camera_configs: List[Dict[str, Any]],
        num_workers: Optional[int] = None,
        cpu_percentage: float = 0.9,
        max_cameras_per_worker: int = 100,
        # Frame encoding
        jpeg_encode: bool = True,
        jpeg_quality: int = 90,
        # DataBus
        num_slots: int = 32,
        max_msg_size: int = 300_000,
        # Frame-skip policy (see camera_streamer/frame_optimizer.py)
        optimizer_config: Optional[Dict[str, Any]] = None,
        # MLA-010 / REFACTORING_PLAN §20: opt-in; default none preserves behavior
        optimization_mode: Optional[str] = None,
    ):
        self.camera_configs = camera_configs
        self.jpeg_encode = jpeg_encode
        self.jpeg_quality = jpeg_quality
        self.num_slots = num_slots
        self.max_msg_size = max_msg_size
        self.optimizer_config = optimizer_config
        optimization_mode = resolve_opencv_optimization_mode(optimization_mode)
        self.optimization_mode = optimization_mode
        self.use_frame_pool = optimization_mode in ("frame_pool", "combined")
        self.use_backpressure = optimization_mode in ("backpressure", "combined")
        # Executor publish is opt-in only — REFACTORING_PLAN §20 excludes added
        # post-processing threads from default/combined production paths.
        self.use_executor_publish = optimization_mode == "executor_offload"

        self.logger = logging.getLogger(__name__)

        # Calculate worker count
        if num_workers is None:
            cpu_count = os.cpu_count() or 4
            num_cameras = len(camera_configs)

            if num_cameras == 0:
                calculated_workers = 2
            elif num_cameras <= 10:
                calculated_workers = max(1, num_cameras)
            elif cpu_count >= 16 or num_cameras >= 100:
                target_cameras_per_worker = 25
                calculated_workers = max(4, min(num_cameras // target_cameras_per_worker, 50))
            else:
                calculated_workers = max(4, int(cpu_count * cpu_percentage))

            self.num_workers = min(calculated_workers, num_cameras) if num_cameras > 0 else calculated_workers
        else:
            self.num_workers = num_workers

        self.max_cameras_per_worker = max_cameras_per_worker

        self.logger.info(
            f"WorkerManager: {self.num_workers} workers for {len(camera_configs)} cameras "
            f"(jpeg={jpeg_encode}, quality={jpeg_quality}, slots={num_slots}, "
            f"optimization={optimization_mode})"
        )

        # Multiprocessing primitives
        self.stop_event = multiprocessing.Event()
        self.health_queue = multiprocessing.Queue()
        self.workers: List[multiprocessing.Process] = []
        self.worker_camera_assignments: Dict[int, List[Dict[str, Any]]] = {}

        # Health monitoring
        self.last_health_reports: Dict[int, Dict[str, Any]] = {}

        # Dynamic camera support (protected by _camera_lock — accessed from
        # the camera manager thread and the metrics/monitoring thread)
        self._camera_lock = threading.Lock()
        self.command_queues: Dict[int, multiprocessing.Queue] = {}
        self.response_queue = multiprocessing.Queue()
        self.camera_to_worker: Dict[str, int] = {}
        self.worker_camera_count: Dict[int, int] = {}
        # Live per-camera config, kept in sync on add/update/remove so a no-op
        # UPDATE can be short-circuited before it tears down + recreates the
        # DataBus producer (new SHM segment, reset counters, consumer churn).
        self._live_camera_configs: Dict[str, Dict[str, Any]] = {}

    def start(self):
        """Start all workers and begin streaming."""
        try:
            # Clean stale SHM files from previous runs
            self._clean_stale_shm()

            # GpuCameraMap removed (decoupled decode/inference): the IE reads the
            # producer GPU from each ring-buffer header, so no map is published.

            # Distribute cameras across workers
            self._distribute_cameras()

            # Start worker processes
            self.logger.info(f"Starting {self.num_workers} worker processes...")
            for worker_id in range(self.num_workers):
                self._start_worker(worker_id)

            self.logger.info(
                f"All workers started! {len(self.camera_configs)} cameras across {self.num_workers} workers"
            )
        except Exception as exc:
            self.logger.error(f"Failed to start workers: {exc}")
            self.stop()
            raise

    def _clean_stale_shm(self):
        """Remove stale SHM files from previous runs.

        Only genuinely orphaned files. A segment a live process still holds open
        is not stale, and unlinking it strands that producer's consumers with
        ENOENT while frames still flow — the same defect fixed on the NVDEC path
        (``nvdec_worker_manager._clean_stale_shm_for``). These patterns are
        fleet-wide (``databus__*``), so the blast radius is every camera on the
        host, not just this manager's.
        """
        patterns = [  # nosec B108 - SHM cleanup is intentional
            "/dev/shm/databus__*",
            "/dev/shm/databus_status__*",
            "/dev/shm/gpu_camera_map",
        ]
        removed = 0
        skipped = 0
        # One /proc walk for the whole sweep rather than one per candidate path.
        held = held_shm_paths()
        for pattern in patterns:
            for path in glob.glob(pattern):
                if is_shm_path_live(path, held):
                    skipped += 1
                    continue
                try:
                    os.unlink(path)
                    removed += 1
                except OSError:
                    pass
        if removed:
            self.logger.info(f"Cleaned {removed} stale SHM files")
        if skipped:
            self.logger.warning(f"Left {skipped} SHM file(s) in place — still held open by a live process")

    def _distribute_cameras(self):
        """Distribute cameras across workers using static partitioning."""
        total_cameras = len(self.camera_configs)
        cameras_per_worker = total_cameras // self.num_workers if self.num_workers > 0 else 0
        remainder = total_cameras % self.num_workers if self.num_workers > 0 else 0

        camera_idx = 0
        for worker_id in range(self.num_workers):
            num_cameras = cameras_per_worker + (1 if worker_id < remainder else 0)
            worker_cameras = self.camera_configs[camera_idx : camera_idx + num_cameras]
            self.worker_camera_assignments[worker_id] = worker_cameras
            camera_idx += num_cameras

    def _start_worker(self, worker_id: int):
        """Start a single worker process."""
        worker_cameras = self.worker_camera_assignments.get(worker_id, [])

        command_queue = multiprocessing.Queue()
        self.command_queues[worker_id] = command_queue
        self.worker_camera_count[worker_id] = len(worker_cameras)

        for cam_config in worker_cameras:
            stream_key = cam_config.get("stream_key")
            if stream_key:
                self.camera_to_worker[stream_key] = worker_id

        if sys.platform == "win32":
            ctx = multiprocessing.get_context("spawn")
        else:
            ctx = multiprocessing.get_context("fork")

        worker = ctx.Process(
            target=run_async_worker,
            args=(
                worker_id,
                worker_cameras,
                self.stop_event,
                self.health_queue,
                command_queue,
                self.response_queue,
                self.jpeg_encode,
                self.jpeg_quality,
                self.num_slots,
                self.max_msg_size,
                self.optimizer_config,
                self.use_frame_pool,
                self.use_backpressure,
                self.use_executor_publish,
            ),
            name=f"AsyncWorker-{worker_id}",
            daemon=False,
        )
        worker.start()

        if worker_id < len(self.workers):
            self.workers[worker_id] = worker
        else:
            self.workers.append(worker)

        self.logger.info(f"Started worker {worker_id} (PID: {worker.pid}) with {len(worker_cameras)} cameras")

    def _drain_health_queue(self):
        """Drain health reports from workers."""
        while not self.health_queue.empty():
            try:
                report = self.health_queue.get_nowait()
            except queue.Empty:
                break
            try:
                self.last_health_reports[report["worker_id"]] = report
            except (KeyError, TypeError):
                self.logger.warning("Discarding malformed worker health report: %r", report)

    def _check_worker_liveness(self):
        """Log errors for any dead workers."""
        for i, worker in enumerate(self.workers):
            if not worker.is_alive() and not self.stop_event.is_set():
                self.logger.error(f"Worker {i} died (exit code: {worker.exitcode})")

    def monitor(self, duration: Optional[float] = None):
        """Monitor workers and collect health reports."""
        start_time = time.time()
        last_summary_time = start_time

        try:
            while not self.stop_event.is_set():
                if duration and (time.time() - start_time) >= duration:
                    break

                self._drain_health_queue()
                self._check_worker_liveness()

                if time.time() - last_summary_time >= 10.0:
                    running = sum(1 for w in self.workers if w.is_alive())
                    self.logger.info(f"Health: {running}/{len(self.workers)} workers alive")
                    last_summary_time = time.time()

                time.sleep(0.5)
        except KeyboardInterrupt:
            pass

    def stop(self, timeout: float = 15.0):
        """Stop all workers gracefully."""
        self.logger.info("Stopping all workers...")
        self.stop_event.set()

        for i, worker in enumerate(self.workers):
            if worker.is_alive():
                worker.join(timeout=timeout)
                if worker.is_alive():
                    self.logger.warning(f"Worker {i} did not stop, terminating...")
                    worker.terminate()
                    worker.join(timeout=5.0)

        self.logger.info("All workers stopped")

    def run(self, duration: Optional[float] = None):
        """Start workers and monitor until stopped."""
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            self.start()
            self.monitor(duration=duration)
        except Exception as exc:
            self.logger.error(f"Error in run loop: {exc}", exc_info=True)
        finally:
            self.stop()

    def _signal_handler(self, signum, frame):
        self.stop_event.set()

    # ========================================================================
    # Dynamic Camera Management
    # ========================================================================

    def add_camera(self, camera_config: Dict[str, Any]) -> bool:
        """Add a camera to the least-loaded worker at runtime."""
        stream_key = camera_config.get("stream_key")
        if not stream_key:
            return False

        with self._camera_lock:
            if stream_key in self.camera_to_worker:
                return False

            target = self._find_least_loaded_worker()
            if target is None:
                respawned = self._respawn_dead_workers()
                if respawned > 0:
                    time.sleep(1.0)
                    target = self._find_least_loaded_worker()

            if target is None:
                self.logger.error("All workers at capacity or dead")
                return False

            try:
                self.command_queues[target].put({"type": "add_camera", "camera_config": camera_config}, timeout=5.0)
                self.camera_to_worker[stream_key] = target
                self.worker_camera_count[target] += 1
                self._live_camera_configs[stream_key] = dict(camera_config)
            except Exception as exc:
                self.logger.error(f"Failed to add camera: {exc}")
                return False

        # GpuCameraMap removed (decoupled decode/inference) — no map to update.

        return True

    def remove_camera(self, stream_key: str) -> bool:
        """Remove a camera from its assigned worker."""
        with self._camera_lock:
            if stream_key not in self.camera_to_worker:
                return False

            worker_id = self.camera_to_worker[stream_key]
            try:
                self.command_queues[worker_id].put({"type": "remove_camera", "stream_key": stream_key}, timeout=5.0)
                del self.camera_to_worker[stream_key]
                self.worker_camera_count[worker_id] -= 1
                self._live_camera_configs.pop(stream_key, None)

                # GpuCameraMap removed (decoupled decode/inference) — nothing to evict.

                return True
            except Exception as exc:
                self.logger.error(f"Failed to remove camera: {exc}")
                return False

    @staticmethod
    def _camera_config_materially_equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        """True if two camera configs are equivalent for decoding/publishing, so
        an UPDATE between them needs no producer teardown/recreate. Compares only
        decode/producer-relevant fields; metadata-only changes are no-ops."""
        for k in (
            "url",
            "rtsp_url",
            "video_path",
            "source",
            "input_topic",
            "output_topic",
            "width",
            "height",
            "fps",
            "target_fps",
            "codec",
        ):
            if a.get(k) != b.get(k):
                return False
        return True

    def update_camera(self, camera_config: Dict[str, Any]) -> bool:
        """Update a camera's configuration."""
        stream_key = camera_config.get("stream_key")
        if not stream_key:
            return False

        with self._camera_lock:
            if stream_key not in self.camera_to_worker:
                # Release lock before calling add_camera (which acquires it)
                pass
            else:
                worker_id = self.camera_to_worker[stream_key]
                # No-op guard (fail-safe: only skips when we have a cached prior
                # config that is materially identical; otherwise proceeds as
                # before). Avoids a needless remove+add that recreates the SHM
                # producer and forces every consumer to reconnect.
                prev = self._live_camera_configs.get(stream_key)
                if prev is not None and self._camera_config_materially_equal(prev, camera_config):
                    self.logger.info(
                        f"Camera {stream_key}: UPDATE is a no-op "
                        f"(source/geometry/codec unchanged) — keeping existing "
                        f"producer, no respawn"
                    )
                    return True
                try:
                    self.command_queues[worker_id].put(
                        {
                            "type": "update_camera",
                            "camera_config": camera_config,
                            "stream_key": stream_key,
                        },
                        timeout=5.0,
                    )
                    self._live_camera_configs[stream_key] = dict(camera_config)
                    return True
                except Exception as exc:
                    self.logger.error(f"Failed to update camera: {exc}")
                    return False

        # Camera not found — add it
        return self.add_camera(camera_config)

    def _find_least_loaded_worker(self) -> Optional[int]:
        """Find the worker with the least cameras that's not at capacity."""
        available = []
        for worker_id, count in self.worker_camera_count.items():
            if worker_id not in self.command_queues:
                continue
            if count >= self.max_cameras_per_worker:
                continue
            if worker_id < len(self.workers) and self.workers[worker_id].is_alive():
                available.append((worker_id, count))

        if not available:
            return None
        return min(available, key=lambda x: x[1])[0]

    def _respawn_dead_workers(self) -> int:
        """Detect and respawn dead worker processes.

        Note: Caller must hold self._camera_lock.
        """
        respawned = 0
        for worker_id in list(self.worker_camera_count.keys()):
            if worker_id >= len(self.workers) or self.workers[worker_id].is_alive():
                continue

            self.logger.warning(f"Worker {worker_id} is dead, respawning...")
            stale_keys = [sk for sk, wid in self.camera_to_worker.items() if wid == worker_id]
            for sk in stale_keys:
                del self.camera_to_worker[sk]

            self.worker_camera_count[worker_id] = 0
            self.worker_camera_assignments[worker_id] = []

            old_queue = self.command_queues.pop(worker_id, None)
            if old_queue:
                try:
                    old_queue.close()
                except Exception:  # nosec B110
                    pass

            try:
                self._start_worker(worker_id)
                respawned += 1
            except Exception as exc:
                self.logger.error(f"Failed to respawn worker {worker_id}: {exc}")
        return respawned

    def get_camera_assignments(self) -> Dict[str, int]:
        with self._camera_lock:
            return self.camera_to_worker.copy()

    def get_worker_statistics(self) -> Dict[str, Any]:
        """Return the last cached health snapshot without draining the queue."""
        per_camera_stats = {}
        for report in self.last_health_reports.values():
            per_camera_stats.update(report.get("per_camera_stats", {}))

        with self._camera_lock:
            total_cameras = sum(self.worker_camera_count.values())
            camera_assignments = self.camera_to_worker.copy()
            worker_camera_counts = self.worker_camera_count.copy()

        return {
            "num_workers": len(self.workers),
            "running_workers": sum(1 for w in self.workers if w.is_alive()),
            "total_cameras": total_cameras,
            "camera_assignments": camera_assignments,
            "worker_camera_counts": worker_camera_counts,
            "health_reports": {
                wid: {
                    "status": r.get("status", "unknown"),
                    "active_cameras": r.get("active_cameras", 0),
                    "timestamp": r.get("timestamp", 0),
                }
                for wid, r in self.last_health_reports.items()
            },
            "per_camera_stats": per_camera_stats,
        }

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
