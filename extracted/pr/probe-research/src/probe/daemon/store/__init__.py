"""The session's SQLite store: class Store composed of one part per table family, device tokens, Jev.
Front door for the old `probe.daemon.store`: names read live, a patch reaches every piece binding the name."""

from __future__ import annotations
import importlib


from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.daemon.store.conversations",
    "probe.daemon.store.events",
    "probe.daemon.store.files",
    "probe.daemon.store.reader",
    "probe.daemon.store.logbook",
    "probe.daemon.store.queue",
    "probe.daemon.store.requests",
    "probe.daemon.store.device",
    "probe.daemon.store.jev",
    "probe.daemon.store.store",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.daemon.store.conversations
    "KEEP_ENDED_HISTORIES": "probe.daemon.store.conversations",
    "annotations": "probe.daemon.store.conversations",
    "sqlite3": "probe.daemon.store.conversations",
    # probe.daemon.store.events
    "BEFORE_DAEMON_BITE": "probe.daemon.store.events",
    "CHAT_KINDS": "probe.daemon.store.events",
    "Event": "probe.daemon.store.events",
    "Kind": "probe.daemon.store.events",
    "MAX_STORED_CHARS": "probe.daemon.store.events",
    "PEER_TOOL": "probe.daemon.store.events",
    "READER_SOURCE": "probe.daemon.store.events",
    "REQUEST_SOURCE": "probe.daemon.store.events",
    "RUN_SIDE_KINDS": "probe.daemon.store.events",
    "SUMMARY_CHARS": "probe.daemon.store.events",
    "SUMMARY_KEYS": "probe.daemon.store.events",
    "SUMMARY_VALUE_CHARS": "probe.daemon.store.events",
    "StoredEvent": "probe.daemon.store.events",
    "UNRECORDED_BITE": "probe.daemon.store.events",
    "_CONTENT_KEYS": "probe.daemon.store.events",
    "_NOT_BEFORE_DAEMON": "probe.daemon.store.events",
    "_RECORDED": "probe.daemon.store.events",
    "_cap": "probe.daemon.store.events",
    "call_summary": "probe.daemon.store.events",
    "dataclass": "probe.daemon.store.events",
    "json": "probe.daemon.store.events",
    "scrub": "probe.daemon.store.events",
    "secrets": "probe.daemon.store.events",
    # probe.daemon.store.logbook
    "BITE_DONE": "probe.daemon.store.logbook",
    "BITE_PAUSED": "probe.daemon.store.logbook",
    "BITE_SKIPPED": "probe.daemon.store.logbook",
    "CARRY_ON": "probe.daemon.store.logbook",
    "write_target": "probe.daemon.store.logbook",
    # probe.daemon.store.queue
    "WORK_STAMP_WINDOW": "probe.daemon.store.queue",
    "_HISTORY": "probe.daemon.store.queue",
    "_epoch": "probe.daemon.store.queue",
    # probe.daemon.store.device
    "DEVICE_LOCK_WAIT_S": "probe.daemon.store.device",
    "LANE_READ": "probe.daemon.store.device",
    "LANE_WRITE": "probe.daemon.store.device",
    "Path": "probe.daemon.store.device",
    "_LANE_KEYS": "probe.daemon.store.device",
    "_device_today": "probe.daemon.store.device",
    "add_device_tokens": "probe.daemon.store.device",
    "device_path": "probe.daemon.store.device",
    "device_tokens_today": "probe.daemon.store.device",
    "os": "probe.daemon.store.device",
    "tempfile": "probe.daemon.store.device",
    "time": "probe.daemon.store.device",
    "utc_day": "probe.daemon.store.device",
    # probe.daemon.store.jev
    "CUT_SHORT": "probe.daemon.store.jev",
    "FAILED_WHILE_RUNNING": "probe.daemon.store.jev",
    "JEV_ENDINGS": "probe.daemon.store.jev",
    "JevApproved": "probe.daemon.store.jev",
    "field": "probe.daemon.store.jev",
    "jev_approved": "probe.daemon.store.jev",
    "re": "probe.daemon.store.jev",
    # probe.daemon.store.store
    "Callable": "probe.daemon.store.store",
    "FORMAT_VERSION": "probe.daemon.store.store",
    "Iterator": "probe.daemon.store.store",
    "Store": "probe.daemon.store.store",
    "StoreVersionError": "probe.daemon.store.store",
    "_SCHEMA": "probe.daemon.store.store",
    "contextmanager": "probe.daemon.store.store",
    "state_dir": "probe.daemon.store.store",
    "store_path": "probe.daemon.store.store",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=_PIECES)
