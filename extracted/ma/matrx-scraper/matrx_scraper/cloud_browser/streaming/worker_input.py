"""The worker-side input channel — the ONE input path and its kill switch.

On the real worker this is Selkies translating WebRTC DataChannel input into
XTEST events against the private Xvfb display. WS-4 models it as an in-process
channel with the exact security properties that must hold on the real worker, so
the "input is demonstrably dead the instant control is revoked" proof runs with
no Selkies:

1. **Exactly one input path exists per run.** Enabling input for a session
   disables any prior one. There are never two writable paths (S4 §7.2).
2. **A ticket lacking ``input:xtest`` can never inject** — enforced HERE, at the
   worker, not merely by the gateway declining to forward (S4 §9, the two-layer
   rule). A `view` session is refused input by the worker itself.
3. **Revision fencing.** The worker records the current ``control_revision`` and
   refuses any input carrying a lower one. A stale gateway that lost the CAS race
   cannot land a single keystroke (S4 §5.1).
4. **Input dies FIRST, synchronously.** ``kill_input`` is what every revocation
   path calls before tearing down media or closing the session (S4 §5.2). After
   it returns, ``inject`` raises.

This is the security contract the real Selkies deployment must honour; the
in-memory form is the executable spec.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field

from .config import SCOPE_INPUT
from .errors import INPUT_NOT_PERMITTED, StreamError


@dataclass
class _InputBinding:
    stream_session_id: str
    control_revision: int
    scopes: frozenset[str]
    live: bool = True


class WorkerInputChannel:
    """One input channel per worker/run. Thread-safe."""

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self._binding: _InputBinding | None = None
        self._injected: list[dict] = []  # observable proof surface for tests
        self._lock = threading.Lock()

    def enable_input(
        self, *, stream_session_id: str, control_revision: int, scopes: frozenset[str]
    ) -> None:
        """Bind THE input path to one session. Any prior binding is dropped —
        there is only ever one writable path. A session whose ticket lacked
        ``input:xtest`` is refused here, at the worker."""
        if SCOPE_INPUT not in scopes:
            raise StreamError(
                INPUT_NOT_PERMITTED,
                "session ticket does not carry input:xtest; worker refuses input",
            )
        with self._lock:
            # Replacing the binding IS the "one input path" guarantee.
            self._binding = _InputBinding(
                stream_session_id=stream_session_id,
                control_revision=control_revision,
                scopes=frozenset(scopes),
                live=True,
            )

    def kill_input(self) -> None:
        """Synchronously make the input path dead. Called FIRST on every
        revocation, before media teardown or session close. Idempotent."""
        with self._lock:
            if self._binding is not None:
                self._binding.live = False
                self._binding = None

    def inject(self, *, stream_session_id: str, control_revision: int, event: dict) -> None:
        """Inject one input event. Raises the instant control is revoked, or when
        the session/revision does not match the live binding, or the revision is
        stale (fencing)."""
        with self._lock:
            b = self._binding
            if b is None or not b.live:
                raise StreamError(INPUT_NOT_PERMITTED, "input path is dead")
            if b.stream_session_id != stream_session_id:
                raise StreamError(INPUT_NOT_PERMITTED, "not the active input session")
            if control_revision < b.control_revision:
                # Stale gateway that lost the CAS race.
                raise StreamError(INPUT_NOT_PERMITTED, "stale control revision refused by worker")
            self._injected.append(event)

    # --- test/proof surface ----------------------------------------------
    @property
    def input_live(self) -> bool:
        with self._lock:
            return bool(self._binding and self._binding.live)

    @property
    def injected_count(self) -> int:
        with self._lock:
            return len(self._injected)


class WorkerInputRegistry:
    """One :class:`WorkerInputChannel` per run."""

    def __init__(self) -> None:
        self._channels: dict[str, WorkerInputChannel] = {}
        self._lock = threading.Lock()

    def channel(self, run_id: str) -> WorkerInputChannel:
        with self._lock:
            ch = self._channels.get(run_id)
            if ch is None:
                ch = WorkerInputChannel(run_id)
                self._channels[run_id] = ch
            return ch
