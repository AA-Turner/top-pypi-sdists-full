"""Old home of OfflineClient and OfflineTransport (now `offline/client.py`) and LINEAGE_ROUTES
(now `offline/lineage.py`), kept one release for importers of this module. OfflineSink is gone
with no alias: an offline run's writes land in `QueuedSink`, which every async client uses, so an
alias would make `isinstance(sink, OfflineSink)` true for online runs; ask
`delivery.is_offline_client(client)` instead."""

# restructure-shim: probe.sdk.delivery.offline.client
import importlib

from ..offline.client import OfflineClient, OfflineTransport
from ..offline.lineage import LINEAGE_ROUTES
from ..sink import SinkKind  # noqa: F401 -- the old module served it
from .queued import QueuedSink

JournalSink = QueuedSink

_moved = importlib.import_module("probe.sdk.delivery.offline.client")
__all__ = ["LINEAGE_ROUTES", "OfflineClient", "OfflineTransport"]


def __getattr__(name):
    return getattr(_moved, name)
