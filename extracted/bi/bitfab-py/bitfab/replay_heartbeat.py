from __future__ import annotations

import contextlib
import logging
import threading
from collections.abc import Callable, Iterator

logger = logging.getLogger(__name__)

REPLAY_HEARTBEAT_INTERVAL_SECONDS = 60.0
_STOP_WAIT_SECONDS = 10.0

StopHeartbeat = Callable[[], None]


@contextlib.contextmanager
def replay_heartbeat(send: Callable[[], None]) -> Iterator[StopHeartbeat]:
    interval_seconds = REPLAY_HEARTBEAT_INTERVAL_SECONDS
    stopped = threading.Event()

    def beat() -> None:
        while not stopped.wait(interval_seconds):
            try:
                send()
            except Exception:
                logger.debug("Bitfab: replay heartbeat failed", exc_info=True)

    thread = threading.Thread(target=beat, name="bitfab-replay-heartbeat", daemon=True)
    thread.start()

    def stop() -> None:
        stopped.set()
        if thread is not threading.current_thread():
            thread.join(timeout=_STOP_WAIT_SECONDS)

    try:
        yield stop
    finally:
        stop()
