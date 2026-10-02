"""Background embedding worker: keeps model inference off the frame path.

The video path must never wait. Measured on a laptop RTX 3060, one
OSNet-AIN forward pass costs ~35 ms regardless of batch size -- the network
is 478 modules of small depthwise convolutions, so it is kernel-launch
bound rather than compute bound. That is longer than an entire 30 FPS frame
budget, which makes synchronous embedding a non-starter and this worker the
load-bearing part of the design. (Datacentre GPUs are considerably faster,
but the architecture must not depend on that.)

Shape, modelled on ``license_plate_monitoring._PlateSyncSender``:

* The producer (:meth:`EmbedWorker.offer`) only takes a lock and touches
  dicts -- no inference, no decode, no I/O. It is O(1) and never blocks.
* Jobs coalesce per track id, so a track seen on 30 consecutive frames
  queues once rather than 30 times.
* The pending map is bounded and evicts oldest-first. Full means drop, never
  backpressure: a dropped crop is retried on a later frame.
* Results land in a plain dict the frame path reads on a *later* frame.
  No future, no callback, no join.

Nothing here raises into the caller.
"""

from __future__ import annotations

import logging
import threading
import time
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

__all__ = ["EmbedWorker"]


class EmbedWorker:
    """Single daemon thread turning person crops into embeddings.

    One worker per use-case instance (i.e. per stream). The embedder it
    calls is process-wide and shared, so N streams still cost one model.
    """

    def __init__(
        self,
        embed_fn: Callable[[List[np.ndarray]], Optional[np.ndarray]],
        max_pending: int = 64,
        batch_size: int = 8,
        idle_sleep_s: float = 0.002,
        name: str = "reid-embed",
    ) -> None:
        self._embed_fn = embed_fn
        self._max_pending = int(max_pending)
        self._batch_size = int(batch_size)
        self._idle_sleep_s = float(idle_sleep_s)

        self._lock = threading.Lock()
        # track_id -> crop. OrderedDict gives oldest-first eviction.
        self._pending: "OrderedDict[Any, np.ndarray]" = OrderedDict()
        # track_id -> embedding. Read by the frame path on a later frame.
        self._results: Dict[Any, np.ndarray] = {}
        self._inflight: set = set()

        self._stop = threading.Event()
        self._wake = threading.Event()
        self._dropped = 0
        self._processed = 0
        self._first_queued_at: Optional[float] = None
        self._batches = 0
        self._latency_ms_ema = 0.0
        self._failures = 0

        self._thread = threading.Thread(target=self._run, name=name, daemon=True)
        self._thread.start()

    # -- producer side (frame path; lock + dict ops only) ------------------
    def offer(self, track_id: Any, crop: np.ndarray) -> str:
        """Queue ``crop`` for ``track_id``. Never blocks. Returns a disposition."""
        if self._stop.is_set():
            return "stopped"
        with self._lock:
            if track_id in self._results or track_id in self._inflight:
                return "known"
            if track_id in self._pending:
                self._pending[track_id] = crop  # coalesce: keep the freshest
                self._pending.move_to_end(track_id)
                return "coalesced"
            while len(self._pending) >= self._max_pending:
                self._pending.popitem(last=False)  # drop oldest, never block
                self._dropped += 1
            self._pending[track_id] = crop
            if self._first_queued_at is None:
                self._first_queued_at = time.monotonic()
        self._wake.set()
        return "queued"

    def get_result(self, track_id: Any) -> Optional[np.ndarray]:
        with self._lock:
            return self._results.get(track_id)

    def pop_result(self, track_id: Any) -> Optional[np.ndarray]:
        with self._lock:
            return self._results.pop(track_id, None)

    def has_pending(self, track_id: Any) -> bool:
        with self._lock:
            return track_id in self._pending or track_id in self._inflight

    def starving(self, grace_s: float = 2.0) -> bool:
        """True when work has been queued for ``grace_s`` with nothing completed.

        The frame path calls the use case synchronously, and torch inference
        holds the GIL in bursts, so a caller that never yields between frames
        can starve this thread. Frame-count budgets do not help there: the
        frames tick by while no wall-clock time is given to the worker. This
        is the wall-clock escape hatch -- the caller releases deferred tracks
        under their raw ids rather than holding a count hostage.
        """
        with self._lock:
            if not self._pending and not self._inflight:
                return False
            if self._first_queued_at is None:
                return False
            return (time.monotonic() - self._first_queued_at) > grace_s and self._batches == 0

    def forget(self, track_ids) -> None:
        """Drop state for tracks the caller no longer cares about."""
        with self._lock:
            for tid in track_ids:
                self._pending.pop(tid, None)
                self._results.pop(tid, None)

    # -- consumer side (worker thread) -------------------------------------
    def _take_batch(self) -> List[Tuple[Any, np.ndarray]]:
        with self._lock:
            batch: List[Tuple[Any, np.ndarray]] = []
            while self._pending and len(batch) < self._batch_size:
                tid, crop = self._pending.popitem(last=False)
                batch.append((tid, crop))
                self._inflight.add(tid)
            return batch

    def _run(self) -> None:
        while not self._stop.is_set():
            batch = self._take_batch()
            if not batch:
                self._wake.wait(timeout=0.05)
                self._wake.clear()
                continue
            t0 = time.perf_counter()
            vecs: Optional[np.ndarray] = None
            try:
                vecs = self._embed_fn([c for _, c in batch])
            except Exception as exc:  # noqa: BLE001 - worker must never die
                self._failures += 1
                logger.warning("ReID embed batch failed: %s", exc)
            dt = (time.perf_counter() - t0) * 1000.0

            with self._lock:
                for i, (tid, _) in enumerate(batch):
                    self._inflight.discard(tid)
                    if vecs is not None and i < len(vecs):
                        self._results[tid] = vecs[i]
                        self._processed += 1
                self._batches += 1
                self._latency_ms_ema = (
                    dt if self._latency_ms_ema == 0.0 else 0.9 * self._latency_ms_ema + 0.1 * dt
                )
            # Yield the GIL between batches. `sleep(0)` does not actually
            # release it to a CPU-bound caller on CPython; a tiny non-zero
            # sleep does, and costs nothing next to a ~35 ms forward pass.
            time.sleep(0.001)

    # -- lifecycle ---------------------------------------------------------
    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        self._wake.set()
        try:
            self._thread.join(timeout=timeout)
        except RuntimeError:  # pragma: no cover
            pass

    @property
    def alive(self) -> bool:
        return self._thread.is_alive() and not self._stop.is_set()

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "pending": len(self._pending),
                "inflight": len(self._inflight),
                "results": len(self._results),
                "dropped": self._dropped,
                "processed": self._processed,
                "batches": self._batches,
                "failures": self._failures,
                "latency_ms_ema": round(self._latency_ms_ema, 2),
                "alive": self._thread.is_alive(),
            }
