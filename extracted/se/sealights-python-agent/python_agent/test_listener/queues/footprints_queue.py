import json
import logging
import threading

from queue import Queue

from python_agent.packages.blinker import signal

log = logging.getLogger(__name__)


class FootprintsQueue(Queue, object):
    def __init__(self, maxsize=0, config_data=None):
        super(FootprintsQueue, self).__init__(maxsize=maxsize)
        # SLDEV-26009: accumulated byte count of items currently in the queue.
        # Accessed under the queue's own mutex so increments stay consistent
        # with the underlying ``deque`` operations.
        self._config_data = config_data
        self._bytes_in_queue = 0
        self._threshold_signal_pending = False
        self._size_lock = threading.Lock()

    def _threshold_bytes(self):
        if self._config_data is None:
            return 0
        mb = getattr(self._config_data, "footprintsBufferThresholdMB", None)
        if mb is None:
            return 0
        try:
            mb = int(mb)
        except (TypeError, ValueError):
            return 0
        if mb <= 0:
            return 0
        return mb * 1024 * 1024

    @staticmethod
    def _estimate_bytes(item):
        try:
            return len(json.dumps(item, default=str).encode("utf-8"))
        except Exception:
            return 0

    def put(self, item, block=True, timeout=None):
        super(FootprintsQueue, self).put(item, block=block, timeout=timeout)
        item_bytes = self._estimate_bytes(item)
        threshold = self._threshold_bytes()
        should_signal_full = self.full()
        should_signal_threshold = False
        with self._size_lock:
            self._bytes_in_queue += item_bytes
            if (
                threshold
                and self._bytes_in_queue >= threshold
                and not self._threshold_signal_pending
            ):
                self._threshold_signal_pending = True
                should_signal_threshold = True
        if should_signal_full:
            footprints_queue_full = signal("footprints_queue_full")
            log.info("Footprints Queue is Full. Signaling...")
            footprints_queue_full.send()
        elif should_signal_threshold:
            # Reuse the existing queue-full signal so downstream listeners
            # (FootprintsManager.send_footprints_task) treat both events
            # identically — an early flush.
            log.info(
                "Footprints Queue crossed byte threshold (%d bytes). Signaling...",
                self._bytes_in_queue,
            )
            signal("footprints_queue_full").send()

    def get_all(self):
        test_coverage_items = []
        while not self.empty():
            test_coverage_item = self.get()
            test_coverage_items.append(test_coverage_item)
        with self._size_lock:
            self._bytes_in_queue = 0
            self._threshold_signal_pending = False
        return test_coverage_items

    def put_all(self, footprint_items):
        for footprint_item in footprint_items:
            self.put(footprint_item)
