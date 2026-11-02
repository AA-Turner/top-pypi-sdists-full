"""One ordered background lane for checkpoint uploads owned by a single invocation."""

from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from threading import BoundedSemaphore, Lock

from labqoat.references import CheckpointRef


class CheckpointUploads:
    """Let training continue while earlier snapshots upload, in the order they were taken."""

    def __init__(self, capacity: int = 2) -> None:
        """Bound unfinished snapshots so a slow link fills neither scratch nor memory."""
        self.capacity = capacity
        self._slots = BoundedSemaphore(capacity)
        self._lock = Lock()
        self._executor: ThreadPoolExecutor | None = None
        self._pending: list[Future[CheckpointRef[object]]] = []

    def unfinished(self) -> int:
        """Count snapshots that were accepted and are not retained yet."""
        with self._lock:
            self._pending = [upload for upload in self._pending if not upload.done()]
            return len(self._pending)

    def submit(self, work: Callable[[], CheckpointRef[object]]) -> Future[CheckpointRef[object]]:
        """Queue behind earlier snapshots, waiting only while the lane is full."""
        self._slots.acquire()
        with self._lock:
            if self._executor is None:
                self._executor = ThreadPoolExecutor(1, "labqoat-checkpoint")
            upload = self._executor.submit(work)
            self._pending.append(upload)
        upload.add_done_callback(self._release)
        return upload

    def drain(self) -> None:
        """Wait for every accepted snapshot; their outcomes stay with the handles that own them."""
        with self._lock:
            executor, self._executor = self._executor, None
            self._pending = []
        if executor is not None:
            executor.shutdown(wait=True)

    def _release(self, upload: Future[CheckpointRef[object]]) -> None:
        """Free one place in the lane however the upload ended."""
        del upload
        self._slots.release()
