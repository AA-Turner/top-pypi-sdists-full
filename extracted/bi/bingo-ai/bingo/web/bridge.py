"""Bridge the unchanged pentest engine (AgentLoop) into the Textual UI.

AgentLoop runs blocking in a worker thread and publishes progress through an
EventBus (loop_start / stream_chunk / tool_result / finding / session_done).
We subscribe to that bus and forward every event to a UI callback. User input
during a run is injected via push_hint(); when idle it starts a fresh loop.

The engine and EventBus are reused verbatim — nothing here mutates them.
"""
from __future__ import annotations

import io
import json
import re
import threading
from typing import Callable

_URL_RE = re.compile(r"https?://[^\s]+")


def extract_target(text: str) -> str:
    """Pull the first URL out of a message (same rule as the classic CLI)."""
    m = _URL_RE.search(text)
    return m.group(0).rstrip(".,;") if m else ""


class PentestSession:
    """Owns one AgentLoop run + an event-drain thread feeding the web session.

    on_event(event_type: str, data: dict) is invoked from a background thread,
    so the caller must marshal to its own loop (WebSession: call_soon_threadsafe).
    """

    def __init__(self, config, on_event: Callable[[str, dict], None]) -> None:
        self._config = config
        self._on_event = on_event
        self._bus = None
        self._loop_thread: threading.Thread | None = None
        self._drain_thread: threading.Thread | None = None
        self._stop = threading.Event()
        self.target: str = ""

    @property
    def running(self) -> bool:
        return bool(self._loop_thread and self._loop_thread.is_alive())

    def send_hint(self, text: str) -> None:
        """Inject user input into the already-running loop."""
        if self._bus is not None:
            self._bus.push_hint(text)

    def start(self, target: str, user_message: str) -> None:
        """Launch AgentLoop(target) in a worker thread; stream events out."""
        from .event_bus import EventBus
        from ..engine.loop import AgentLoop
        from rich.console import Console

        self.target = target
        self._stop.clear()
        self._bus = EventBus()
        q = self._bus.subscribe()

        # AgentLoop writes rich console output too; keep it off the Textual
        # screen by handing it a quiet console. All progress still arrives
        # through the event bus, which is what the UI consumes.
        quiet = Console(file=io.StringIO(), force_terminal=False)

        def _run_loop() -> None:
            try:
                loop = AgentLoop(
                    target=target, config=self._config,
                    console=quiet, event_bus=self._bus,
                )
                loop.run(user_message)
            except Exception as exc:  # surface engine errors into chat
                self._bus.push_event("engine_error", {"error": str(exc)})
            finally:
                self._bus.push_event("_loop_exit", {})

        def _drain() -> None:
            while not self._stop.is_set():
                try:
                    msg = q.get(timeout=0.25)
                except Exception:
                    continue
                try:
                    payload = json.loads(msg)
                except Exception:
                    continue
                etype = payload.get("type", "")
                if etype == "_loop_exit":
                    self._on_event("_loop_exit", {})
                    break
                self._on_event(etype, payload.get("data", {}))
            self._bus.unsubscribe(q)

        self._loop_thread = threading.Thread(target=_run_loop, daemon=True, name="bingo-agentloop")
        self._drain_thread = threading.Thread(target=_drain, daemon=True, name="bingo-drain")
        self._loop_thread.start()
        self._drain_thread.start()

    def stop(self) -> None:
        self._stop.set()
