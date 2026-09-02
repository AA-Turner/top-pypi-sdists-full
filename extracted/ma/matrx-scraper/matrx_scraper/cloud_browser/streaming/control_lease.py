"""Control-lease CAS and the run registry (S4 §5).

A control lease is the right to inject input into a run. EXACTLY ONE is live per
run — agent or human. It is CAS-guarded and fenced by ``control_revision``; the
worker refuses any input carrying a revision below its current one, so a stale
gateway cannot inject a single keystroke after losing the race.

The real Browser Manager backs this with the ``browser.run`` row and the §5.1
UPDATE. WS-4 ships an in-memory registry with the identical CAS so the
two-controller and revision-fencing proofs run with no DB.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field

from .config import CONTROL_LEASE_TTL_SECONDS
from .errors import (
    BROWSER_CONTROLLED_BY_HUMAN,
    CONTROL_LEASE_LOST,
    RUN_NOT_LIVE,
    StreamError,
)
from .models import ControllerKind

LIVE_STATES = frozenset({"live", "resume_pending"})


@dataclass
class RunState:
    run_id: str
    profile_id: str
    worker_id: str
    state: str = "live"
    # Current controller / lease.
    controller_kind: ControllerKind = "agent"
    controller_user_id: str | None = None
    controller_display_name: str | None = None
    control_revision: int = 1
    control_fencing_token: str = field(default_factory=lambda: uuid.uuid4().hex)
    control_lease_expires_at: float = 0.0
    # Handoff currently open on the run (one at a time), or None.
    active_handoff_id: str | None = None
    handoff_claimant_user_id: str | None = None
    handoff_returned: bool = False
    handoff_cancelled: bool = False
    handoff_expires_at: float = 0.0

    def is_live(self) -> bool:
        return self.state in LIVE_STATES

    def lease_live(self, now: float | None = None) -> bool:
        return self.control_lease_expires_at > (now or time.time())


class RunRegistry:
    """In-memory run + control-lease store with S4 §5.1 CAS semantics."""

    def __init__(self) -> None:
        self._runs: dict[str, RunState] = {}
        self._lock = threading.RLock()

    # --- lifecycle used by the stub / control plane -----------------------
    def create_run(self, *, run_id: str, profile_id: str, worker_id: str) -> RunState:
        with self._lock:
            r = RunState(run_id=run_id, profile_id=profile_id, worker_id=worker_id)
            self._runs[run_id] = r
            return r

    def iter_live(self):
        with self._lock:
            return [r for r in self._runs.values() if r.is_live()]

    def get(self, run_id: str) -> RunState:
        with self._lock:
            r = self._runs.get(run_id)
            if r is None or not r.is_live():
                raise StreamError(RUN_NOT_LIVE, "run is not live")
            return r

    def open_handoff(self, run_id: str, *, ttl_seconds: float = 1800.0) -> str:
        with self._lock:
            r = self.get(run_id)
            r.active_handoff_id = uuid.uuid4().hex
            r.handoff_claimant_user_id = None
            r.handoff_returned = False
            r.handoff_cancelled = False
            r.handoff_expires_at = time.time() + ttl_seconds
            return r.active_handoff_id

    # --- lease CAS (S4 §5.1) ---------------------------------------------
    def claim_control(
        self,
        *,
        run_id: str,
        new_kind: ControllerKind,
        user_id: str | None,
        expected_revision: int | None,
        display_name: str | None = None,
    ) -> RunState:
        """Compare-and-swap the control lease. Matches the SQL WHERE:

            WHERE id = $run_id
              AND (control_lease_expires_at < now() OR control_revision = $expected)

        Zero rows -> the caller does not hold it. Every accepted transition bumps
        ``control_revision`` (PLAN.md fencing) and rotates the fencing token."""
        now = time.time()
        with self._lock:
            r = self.get(run_id)
            expired = not r.lease_live(now)
            revision_matches = (
                expected_revision is not None and r.control_revision == expected_revision
            )
            if not (expired or revision_matches):
                if r.controller_kind == "human":
                    raise StreamError(
                        BROWSER_CONTROLLED_BY_HUMAN,
                        "another person controls this browser",
                        current_controller={
                            "kind": "human",
                            "display_name": r.controller_display_name,
                        },
                    )
                raise StreamError(
                    CONTROL_LEASE_LOST,
                    "control lease is held by someone else",
                    current_control_revision=r.control_revision,
                    current_controller={
                        "kind": r.controller_kind,
                        "display_name": r.controller_display_name,
                    },
                )
            r.controller_kind = new_kind
            r.controller_user_id = user_id
            r.controller_display_name = display_name
            r.control_revision += 1
            r.control_fencing_token = uuid.uuid4().hex
            r.control_lease_expires_at = now + CONTROL_LEASE_TTL_SECONDS
            return r

    def renew_control(self, *, run_id: str, control_revision: int, user_id: str) -> RunState:
        now = time.time()
        with self._lock:
            r = self.get(run_id)
            if (
                r.control_revision != control_revision
                or r.controller_user_id != user_id
                or not r.lease_live(now)
            ):
                raise StreamError(
                    CONTROL_LEASE_LOST,
                    "control lease lost",
                    current_control_revision=r.control_revision,
                    current_controller={
                        "kind": r.controller_kind,
                        "display_name": r.controller_display_name,
                    },
                )
            r.control_lease_expires_at = now + CONTROL_LEASE_TTL_SECONDS
            return r

    def release_control(
        self, *, run_id: str, control_revision: int, to_kind: ControllerKind = "agent"
    ) -> bool:
        """Idempotent (S4 §2.5). Releasing a lease you no longer hold returns
        False (already_released) — never an error."""
        with self._lock:
            r = self._runs.get(run_id)
            if r is None or r.control_revision != control_revision:
                return False
            r.controller_kind = to_kind
            r.controller_user_id = None
            r.controller_display_name = None
            r.control_revision += 1
            r.control_fencing_token = uuid.uuid4().hex
            r.control_lease_expires_at = 0.0
            return True

    def force_revoke(self, *, run_id: str, to_kind: ControllerKind = "agent") -> RunState:
        """Owner/system revoke: reassign, bump revision, void the lease."""
        with self._lock:
            r = self.get(run_id)
            r.controller_kind = to_kind
            r.controller_user_id = None
            r.controller_display_name = None
            r.control_revision += 1
            r.control_fencing_token = uuid.uuid4().hex
            r.control_lease_expires_at = 0.0
            return r
