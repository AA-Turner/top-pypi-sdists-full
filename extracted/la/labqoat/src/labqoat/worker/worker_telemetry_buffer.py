"""Assignment-owned telemetry batching with one-shot deadlines and explicit delivery barriers."""

from threading import RLock, Timer

from labqoat.json_document import JsonValue
from labqoat.worker.telemetry_frames import TelemetryFrames
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.worker_telemetry_stream import WorkerTelemetryStream


class WorkerTelemetryBuffer:
    """Buffer for at most one second normally, with bounded memory and acknowledged backpressure.

    Producers wait for the network only when a window is full or an earlier delivery failed; a deadline
    delivery in flight never holds the lock they append under. The window holds a second of output from a
    loop that logs several hundred times a second, so the deadline, not the producer, normally delivers it.
    """

    WINDOW_FRAMES = 1024
    WINDOW_BYTES = 262_144
    REPLAY_FRAMES = 128

    def __init__(self, stream: WorkerTelemetryStream) -> None:
        """Bind one transport without starting a thread or opening a connection."""
        self._stream = stream
        self._frames: list[bytes] = []
        self._bytes = 0
        self._lock = RLock()
        self._delivery = RLock()
        self._timer: Timer | None = None
        self._generation = 0
        self._closed = False
        self._failed = False

    def add(self, kind: str, entries: list[JsonValue]) -> None:
        """Accept a snapshot; recover prior failed delivery before accepting any new evidence."""
        frame = TelemetryFrames.encode(kind, entries)
        while not self._accept(frame):
            self.flush()

    def _accept(self, frame: bytes) -> bool:
        """Append under the short lock, or ask the caller to deliver first when the window cannot take the frame."""
        with self._lock:
            if self._closed:
                raise RuntimeError("Worker telemetry is closed")
            full = len(self._frames) >= self.WINDOW_FRAMES or self._bytes + len(frame) > self.WINDOW_BYTES
            if self._failed or (self._frames and full):
                return False
            self._schedule()
            self._frames.append(frame)
            self._bytes += len(frame)
            return True

    def _schedule(self) -> None:
        """Start a deadline before accepting evidence so thread creation failure cannot claim ownership."""
        if self._timer is None:
            timer = Timer(1.0, self._deliver, args=(self._generation,))
            timer.daemon = True
            timer.start()
            self._timer = timer

    def flush(self) -> None:
        """Require durable acknowledgement of every accepted entry, including prior failed uploads."""
        with self._delivery:
            self._stage()
            self._stream.flush()
            self._failed = False

    def send(self, kind: str, entries: list[JsonValue]) -> None:
        """Keep immediate callers synchronous and ordered after any buffered evidence."""
        with self._delivery:
            if self._frames:
                self.flush()
            self._stream.send(kind, entries)

    def close(self) -> None:
        """Stop accepting evidence and close the transport even when final delivery fails."""
        with self._delivery:
            with self._lock:
                if self._closed:
                    return
                self._closed = True
            try:
                self._stage()
            finally:
                self._stream.close()

    def _stage(self) -> None:
        """Transfer a compacted window to the replay owner without losing failed evidence."""
        with self._lock:
            self._cancel()
            waiting = bool(self._frames)
        if waiting:
            self._stream.flush()
            with self._lock:
                frames, self._frames, self._bytes = self._frames, [], 0
            combined = TelemetryFrames.combine(frames)
            for start in range(0, len(combined), self.REPLAY_FRAMES):
                self._stream.stage(combined[start : start + self.REPLAY_FRAMES])

    def _cancel(self) -> None:
        """Invalidate callbacks that raced with cancellation without waiting under their lock."""
        self._generation += 1
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _deliver(self, generation: int) -> None:
        """Attempt one deadline flush; failed frames remain owned by the replay transport."""
        with self._lock:
            if generation != self._generation:
                return
        try:
            self.flush()
        except WorkerApiError:
            self._failed = True
