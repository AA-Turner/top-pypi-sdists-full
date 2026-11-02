"""Old home of DirectSink (now `delivery/sender/`: `Sender`) and `queue_only` (now `delivery/sender/`),
kept one release for importers of this module. The NAMES only: `land` now takes `policy=`
(a `SendPolicy`) instead of strict/sync/raise_permanent, and `send_instead_of_queueing` is
`QueuedSink`'s (`sinks/queued.py`)."""

from __future__ import annotations

from ..sender import Sender as DirectSink
from ..sender import queue_only

__all__ = ["DirectSink", "queue_only"]
