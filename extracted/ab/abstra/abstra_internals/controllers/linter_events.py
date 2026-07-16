import json
import threading
from typing import ClassVar, List, Optional, Protocol

import flask_sock

from abstra_internals.repositories.linter.models import LinterCheck


class DegradedSource(Protocol):
    """Anything exposing the linter repository's `degraded` flag (structural,
    so this module does not import the repository stack)."""

    degraded: bool


class LinterEventController:
    listeners: List[flask_sock.Server] = []
    _lock = threading.Lock()
    # The linter repository, wired at editor boot. When set, every payload
    # reports whether its checks are a fresh run ("ok") or a stale mirror
    # because the linter runner is unavailable ("degraded"). Unwired (e.g.
    # cloud-run editors that never boot linters) always reports "ok".
    _degraded_source: ClassVar[Optional[DegradedSource]] = None

    @classmethod
    def set_degraded_source(cls, source: Optional[DegradedSource]) -> None:
        cls._degraded_source = source

    @classmethod
    def build_payload(cls, checks: List[LinterCheck]) -> str:
        source = cls._degraded_source
        degraded = source is not None and source.degraded
        return json.dumps(
            {
                "checks": [check.to_dict() for check in checks],
                "status": "degraded" if degraded else "ok",
            }
        )

    @classmethod
    def register(cls, listener: flask_sock.Server):
        with cls._lock:
            cls.listeners.append(listener)

    @classmethod
    def unregister(cls, listener: flask_sock.Server):
        with cls._lock:
            try:
                cls.listeners.remove(listener)
            except ValueError:
                pass

    @classmethod
    def broadcast(cls, checks: List[LinterCheck]):
        payload = cls.build_payload(checks)
        with cls._lock:
            listeners = list(cls.listeners)

        failed = []
        for listener in listeners:
            try:
                listener.send(payload)
            except Exception:
                failed.append(listener)

        if failed:
            with cls._lock:
                for listener in failed:
                    try:
                        cls.listeners.remove(listener)
                    except ValueError:
                        pass
