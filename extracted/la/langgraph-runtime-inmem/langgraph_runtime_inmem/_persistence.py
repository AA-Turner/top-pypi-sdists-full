"""Periodic flushing for all PersistentDict stores."""

from __future__ import annotations

import functools
import logging
import os
import threading
import weakref

from langgraph.checkpoint.memory import PersistentDict

logger = logging.getLogger(__name__)

_stores: dict[str, weakref.ref[PersistentDict]] = {}
# Held while changing _stores and while syncing one entry, so once
# unregister_persistent_dict() returns no sync of that dict is running or will start.
_stores_lock = threading.Lock()
_flush_thread: tuple[threading.Event, threading.Thread] | None = None
_flush_interval: int = 10
DISABLE_FILE_PERSISTENCE = (
    os.getenv("LANGGRAPH_DISABLE_FILE_PERSISTENCE", "false").lower() == "true"
)


def register_persistent_dict(d: PersistentDict) -> None:
    """Register a PersistentDict for periodic flushing."""
    if DISABLE_FILE_PERSISTENCE:
        return
    global _flush_thread
    with _stores_lock:
        _stores[d.filename] = weakref.ref(d)
        if _flush_thread is None:
            logger.info("Starting dev persistence flush loop")
            stop_event = threading.Event()
            _flush_thread = (
                stop_event,
                threading.Thread(
                    target=functools.partial(_flush_loop, stop_event), daemon=True
                ),
            )
            _flush_thread[1].start()


def unregister_persistent_dict(d: PersistentDict) -> None:
    """Stop periodic flushing of ``d`` if it's still the dict registered for its file."""
    with _stores_lock:
        ref = _stores.get(d.filename)
        if ref is not None and ref() is d:
            _stores.pop(d.filename, None)


def stop_flush_loop() -> None:
    """Stop the background flush thread."""
    global _flush_thread
    if _flush_thread is not None:
        logger.info("Stopping dev persistence flush loop")
        _flush_thread[0].set()
        _flush_thread[1].join()
        _flush_thread = None


def _flush_once() -> None:
    with _stores_lock:
        entries = list(_stores.items())
    for filename, ref in entries:
        with _stores_lock:
            # Skip entries unregistered or replaced since the snapshot.
            if _stores.get(filename) is not ref:
                continue
            # Compare to None: an empty dict is falsy but still needs flushing.
            if (store := ref()) is None:
                _stores.pop(filename, None)
                logger.debug(
                    "Dropped garbage-collected dev persistence file %s", filename
                )
                continue
            try:
                store.sync()
            except Exception:
                # One bad file must not stop the others (or later retries) from flushing.
                logger.exception("Failed to flush dev persistence file %s", filename)


def _flush_loop(stop_event: threading.Event) -> None:
    while not stop_event.wait(timeout=_flush_interval):
        _flush_once()
    logger.info("dev persistence flush loop exiting")
