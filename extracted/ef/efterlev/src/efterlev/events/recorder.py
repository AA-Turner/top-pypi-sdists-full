"""Record the live event stream to a JSONL file — the `studio --live` transport.

`efterlev studio --live` spawns the real pipeline (`report run`) as a
subprocess so the scan + gap agent run exactly as they do on the CLI, with
the user's configured LLM backend. That subprocess sets
`EFTERLEV_STUDIO_EVENT_LOG`; the Typer root callback then calls
`record_events_to(path)`, which binds a process-global bus that appends each
emitted event as one JSON line. The Studio server tails the file and streams
the lines to the browser over SSE. One event per line, flushed immediately so
the browser sees it as it happens.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.events.bus import EventBus, set_active_bus
from efterlev.events.schema import StudioEvent

# Keep the open file handle alive for the life of the process — the bus
# subscriber closes over it, and we never want it garbage-collected mid-run.
_sink_file = None


def record_events_to(path: Path) -> EventBus:
    """Bind a process-global bus that writes each event to `path` as JSONL.

    Returns the bus (mostly for tests). The handle stays open for the life of
    the process; the OS closes it on exit. Each line is flushed so a tailing
    reader sees events in real time.
    """
    global _sink_file
    path.parent.mkdir(parents=True, exist_ok=True)
    _sink_file = path.open("a", encoding="utf-8")
    f = _sink_file

    def _write(event: StudioEvent) -> None:
        f.write(event.model_dump_json() + "\n")
        f.flush()

    bus = EventBus()
    bus.subscribe(_write)
    set_active_bus(bus)
    return bus
