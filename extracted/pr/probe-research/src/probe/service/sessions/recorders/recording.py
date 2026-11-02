"""one recorded session: its record, and the steps it goes through."""

from __future__ import annotations
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
#: A session's record says it ended while off and is not finished yet.
DEFERRED_KEY = "capture_deferred"
#: `RecorderHost._hold`'s answers.
RECORD_STEP = "record"
PAUSED_STEP = "paused"
ENDED_STEP = "ended"


@dataclass
class Recording:
    sid: str
    params: dict
    controls: Any
    thread: threading.Thread | None = None
    started_at: float = field(default_factory=time.time)
    last: str = ""
    failures: int = 0
    #: Inside `hosted.record` now (not waiting to try again), since this
    #: (monotonic): a beat older than its start is a previous run's (the
    #: watch's `stalled`, crash-report plan B2).
    in_record: bool = False
    record_since: float = 0.0
    #: Set by a `session.record` for this session while its recorder waits
    #: after stepping back (another recorder held the claim): it tries again
    #: at once instead of after STOPPED_RETRIES first waits (a `tap watch`
    #: that has just let go of the session: `hooks/tap_handover.py`).
    wake: threading.Event = field(default_factory=threading.Event)
    #: Its switch reads `off` (or a gap waits to be settled): its tap loop does
    #: not run, the gate holds it (`RecorderHost._hold`).
    held: bool = False
    #: The switch was seen `off` while its loop ran: the loop was told to leave
    #: (`controls.pause`), and the guard holds the session instead of pausing it.
    hold_asked: bool = False
    #: Wakes a held recorder at once (`session.recording` saw the switch move).
    gate_wake: threading.Event = field(default_factory=threading.Event)
    #: A held session that ended is being finished (settled to its end and
    #: finalized): the service stays up for that, as for any recorder's end.
    finishing: bool = False
    #: Its transcript file, once known (a Codex session names only a folder).
    transcript: Path | None = None
    #: A held session that ended could not be finished (the server did not
    #: answer): it is retried, slowly, by this service and every later one, and
    #: keeps no service alive meanwhile.
    deferred: bool = False
    #: A `session.record` came for it (a `tap watch` offering it): a held
    #: recorder looks for the session's claim again at once.
    claim_now: bool = False
    #: Its gap file is behind its record: written off the shared lock and off
    #: the service's loop, by its recorder thread or the monitor
    #: (`RecorderHost._flush_gap_file`).
    gap_file_due: bool = False
    #: It ended while off and was refused for good (no login here, or the
    #: Probe gateway's own 401/403/404/422): no later service retries it; its
    #: gap file stays.
    dropped: bool = False
    #: Its gap file was read and merged into its record (`_gate`). Until then
    #: it is held, its gap file decides for every drain here (it is not `live`),
    #: and its gap file is never rewritten from its record.
    file_merged: bool = False
    #: Its gap file could not be written: said once, and once it can again.
    gap_file_failing: bool = False
    #: Its gap file's signature when this recording last wrote or read it
    #: (`()`: not yet). One that differs was written by another writer since
    #: (from tap 0.10.19 a `tap watch` of the session records its own off
    #: stretches there): merged into the record before it is written again.
    file_sig: Any = ()
    #: The gaps this recording settled (dropped from its record): never taken
    #: back from a gap file another writer wrote before it saw them go.
    settled_gaps: set = field(default_factory=set)
