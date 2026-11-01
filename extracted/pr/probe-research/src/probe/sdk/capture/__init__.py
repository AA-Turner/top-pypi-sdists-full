"""Automatic capture: the producers that feed a run (lineage/, outputs/, code/, logs/) and the capture ledger.
LAZY front door for the old `probe.sdk.capture` (now capture.py): importing a producer never loads the ledger."""

from __future__ import annotations

from ...foundation.front_door.front_door import serve_pieces

#: The old module's pieces: a write through the door reaches these only.
_PIECES = ("probe.sdk.capture.capture",)

#: Every name the old module bound -> the piece that holds it.
_HOMES = {
    "Any": "probe.sdk.capture.capture",
    "CaptureLedger": "probe.sdk.capture.capture",
    "CaptureState": "probe.sdk.capture.capture",
    "Path": "probe.sdk.capture.capture",
    "SCHEMA_VERSION": "probe.sdk.capture.capture",
    "StrEnum": "probe.sdk.capture.capture",
    "_COLLECTED_STATES": "probe.sdk.capture.capture",
    "_FAILURE_STATES": "probe.sdk.capture.capture",
    "_SPAN_NAMESPACE": "probe.sdk.capture.capture",
    "_now": "probe.sdk.capture.capture",
    "annotations": "probe.sdk.capture.capture",
    "json": "probe.sdk.capture.capture",
    "quote": "probe.sdk.capture.capture",
    "stable_external_key": "probe.sdk.capture.capture",
    "stable_span_id": "probe.sdk.capture.capture",
    "uuid": "probe.sdk.capture.capture",
    "write_text_atomic": "probe.sdk.capture.capture",
}
#: `from <old path> import *` takes what the old module's `__all__` named.
__all__ = [
    "CaptureLedger",
    "CaptureState",
    "SCHEMA_VERSION",
    "stable_external_key",
    "stable_span_id",
]

serve_pieces(__name__, _HOMES, pieces=_PIECES, is_lazy=True)
