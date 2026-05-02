"""Simple echo gate — mutes mic input while speaker is playing.

Prevents the agent from "hearing itself" through the speakers.
Not a true AEC (acoustic echo cancellation) — just half-duplex gating.

Usage:
    gate = EchoGate()
    gate.set_speaking(True)   # Agent is speaking → mute mic
    gate.set_speaking(False)  # Agent stopped → unmute mic

    if gate.should_forward():
        queue.send_realtime(audio_chunk)
"""

from __future__ import annotations

import threading


class EchoGate:
    """Thread-safe echo gate for half-duplex voice interaction."""

    def __init__(self) -> None:
        self._speaking = False
        self._lock = threading.Lock()

    def set_speaking(self, speaking: bool) -> None:
        """Set whether the agent is currently speaking (outputting audio)."""
        with self._lock:
            self._speaking = speaking

    def should_forward(self) -> bool:
        """Return True if mic audio should be forwarded to the agent."""
        with self._lock:
            return not self._speaking

    @property
    def is_speaking(self) -> bool:
        with self._lock:
            return self._speaking
