"""Old home of JournalSink (now `QueuedSink` in `sinks/queued.py`) and `queue_only` (now
`delivery/sender/`), kept one release for importers of this module: every other name it
served is forwarded to `sinks/queued.py`."""

# restructure-shim: probe.sdk.delivery.sinks.queued
import importlib

from ..sender import queue_only
from .queued import QueuedSink, _usable_journal

JournalSink = QueuedSink

_moved = importlib.import_module("probe.sdk.delivery.sinks.queued")
__all__ = ["JournalSink", "QueuedSink", "_usable_journal", "queue_only"]


def __getattr__(name):
    return getattr(_moved, name)
