"""Test substrate for the WS-6 handoff park/resume protocol (S5 §8).

Two fakes, each backed by a DURABLE dict store passed in from the test — the
same object survives a simulated manager restart, so "kill the process" is
modelled as: throw away the engine + coordinator + scope objects, keep only the
three durable stores (runtime ExecutionStore, the ledger, the handoff rows),
and rebuild. No fake owns continuity in memory.

`FakeHandoffSource` implements the identical `HandoffSource` protocol the real
Browser Manager client implements, and models the two CAS gates it owns
(handoff.state 4.1, controller_revision 4.2). `FakeHandoffLedger` models the
platform's existing `chat.tool_call` exactly-once completion CAS (4.3) plus the
timeout-sweep placeholder + late-answer supersession (S5 §6).

The fakes NEVER simulate Chromium, screenshots, stream tickets, or media
latency (S5 §8.2) — only the browser-manager side of the durable protocol.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from matrx_ai.browser_handoff.models import (
    HandoffOpenRequest,
    HandoffReason,
    HandoffRecord,
    HandoffResolution,
    HandoffResolutionKind,
    HandoffResolutionReceipt,
    HandoffTicket,
    PageFacts,
    PageInventory,
)


class Clock:
    """Injectable, test-driven clock — no wall-clock sleeping (S5 §8.1)."""

    def __init__(self, start: datetime | None = None) -> None:
        self._now = start or datetime(2026, 1, 1, tzinfo=UTC)

    def now(self) -> datetime:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now = self._now + timedelta(seconds=seconds)


class ControllerConflict(Exception):
    """Raised by the source when a controller CAS is lost — the tool maps it to
    `browser_controlled_by_human` (S5 P2 / S6 §5.3)."""

    error_type = "browser_controlled_by_human"


def _inventory(clock: Clock) -> PageInventory:
    return PageInventory(
        context_count=1,
        pages=[
            PageFacts(
                page_id="p1",
                origin="https://accounts.example.com",
                url="https://accounts.example.com/signin/challenge",
                title="Verify it's you",
                is_active=True,
            )
        ],
        active_page_id="p1",
        sanitized_description="A verification page is open.",
        captured_at=clock.now(),
        boundary_artifact_id="file-boundary-1",
    )


class FakeHandoffSource:
    """Durable-row-backed Browser Manager stand-in.

    `handoffs` and `controllers` are the DURABLE stores; passing the SAME dicts
    to a freshly-built source after a "restart" is what proves no continuity
    lives in this object.
    """

    CLAIM_WINDOW_S = 3600.0
    RECONNECT_WINDOW_S = 900.0

    def __init__(
        self,
        clock: Clock,
        *,
        handoffs: dict | None = None,
        controllers: dict | None = None,
    ) -> None:
        self._clock = clock
        self.handoffs: dict[str, dict] = handoffs if handoffs is not None else {}
        # run_id -> {"controller_kind", "controller_revision"}
        self.controllers: dict[str, dict] = (
            controllers if controllers is not None else {}
        )
        self._seq = len(self.handoffs)

    def seed_run(self, run_id: str, *, revision: int = 1) -> None:
        self.controllers[run_id] = {
            "controller_kind": "agent_control",
            "controller_revision": revision,
        }

    # -- P2: open --------------------------------------------------------
    async def open_handoff(self, req: HandoffOpenRequest) -> HandoffTicket:
        ctrl = self.controllers.setdefault(
            req.run_id, {"controller_kind": "agent_control", "controller_revision": 1}
        )
        # Controller CAS (4.2) + unique-active-handoff guard (S1).
        if ctrl["controller_revision"] != req.expected_controller_revision:
            raise ControllerConflict(req.run_id)
        if any(
            h["run_id"] == req.run_id
            and h["state"] in ("requested", "claimed", "returning")
            for h in self.handoffs.values()
        ):
            raise ControllerConflict(req.run_id)
        ctrl["controller_kind"] = "handoff_requested"
        ctrl["controller_revision"] += 1
        self._seq += 1
        handoff_id = f"handoff-{self._seq}"
        rkey = f"{handoff_id}:{req.pending_call_id}"
        now = self._clock.now()
        self.handoffs[handoff_id] = {
            "handoff_id": handoff_id,
            "run_id": req.run_id,
            "profile_id": req.profile_id,
            "reason": req.reason.value,
            "state": "requested",
            "resolution_key": rkey,
            "pending_call_id": req.pending_call_id,
            "pending_execution_id": req.requested_by_execution_id,
            "conversation_id": req.conversation_id,
            "controller_revision": ctrl["controller_revision"],
            "outcome_label": None,
            "requested_at": now,
            "expires_at": now + timedelta(seconds=self.CLAIM_WINDOW_S),
            "reconnect_deadline": None,
            "returning_at": None,
            "returned_at": None,
            "tool_resolved_at": None,
            "resume_dispatched_at": None,
            "claimed_by_user_id": None,
            "returned_by_user_id": None,
            "boundary_artifact_id": req.__dict__.get("boundary_artifact_id"),
            "_resolution": None,
        }
        return HandoffTicket(
            handoff_id=handoff_id,
            run_id=req.run_id,
            resolution_key=rkey,
            controller_revision=ctrl["controller_revision"],
            state="requested",
            expires_at=self.handoffs[handoff_id]["expires_at"],
        )

    def _record(self, handoff_id: str) -> HandoffRecord:
        h = self.handoffs[handoff_id]
        return HandoffRecord(
            handoff_id=h["handoff_id"],
            run_id=h["run_id"],
            profile_id=h["profile_id"],
            reason=HandoffReason(h["reason"]),
            state=h["state"],
            resolution_key=h["resolution_key"],
            pending_call_id=h["pending_call_id"],
            pending_execution_id=h["pending_execution_id"],
            conversation_id=h["conversation_id"],
            controller_revision=h["controller_revision"],
            outcome_label=h["outcome_label"],
            requested_at=h["requested_at"],
            expires_at=h["expires_at"],
            reconnect_deadline=h["reconnect_deadline"],
            returning_at=h["returning_at"],
            returned_at=h["returned_at"],
            tool_resolved_at=h["tool_resolved_at"],
            resume_dispatched_at=h["resume_dispatched_at"],
            claimed_by_user_id=h["claimed_by_user_id"],
            returned_by_user_id=h["returned_by_user_id"],
            boundary_artifact_id=h["boundary_artifact_id"],
        )

    async def get_handoff(self, handoff_id: str) -> HandoffRecord:
        return self._record(handoff_id)

    async def get_handoff_or_none(self, handoff_id):
        if handoff_id is None or handoff_id not in self.handoffs:
            return None
        return self._record(handoff_id)

    async def claim(self, handoff_id: str, *, user_id: str) -> HandoffRecord:
        h = self.handoffs[handoff_id]
        if h["state"] != "requested":
            return self._record(handoff_id)
        ctrl = self.controllers[h["run_id"]]
        h["state"] = "claimed"
        h["claimed_by_user_id"] = user_id
        h["reconnect_deadline"] = self._clock.now() + timedelta(
            seconds=self.RECONNECT_WINDOW_S
        )
        ctrl["controller_kind"] = "human_control"
        ctrl["controller_revision"] += 1
        h["controller_revision"] = ctrl["controller_revision"]
        return self._record(handoff_id)

    # -- R1-R3 + 4.1 CAS -------------------------------------------------
    def _close(
        self,
        handoff_id: str,
        kind: HandoffResolutionKind,
        *,
        user_id: str | None,
        outcome_label: str | None,
    ) -> HandoffResolution:
        h = self.handoffs[handoff_id]
        ctrl = self.controllers[h["run_id"]]
        # R3 — fresh fencing token (agent_control) for COMPLETED; stopped otherwise.
        ctrl["controller_revision"] += 1
        if kind is HandoffResolutionKind.COMPLETED:
            ctrl["controller_kind"] = "agent_control"
        else:
            ctrl["controller_kind"] = "stopped"
        h["controller_revision"] = ctrl["controller_revision"]
        h["state"] = "returning"
        h["returning_at"] = self._clock.now()
        h["outcome_label"] = outcome_label
        h["returned_by_user_id"] = user_id
        inv = _inventory(self._clock) if kind is not HandoffResolutionKind.EXPIRED else None
        resolution = HandoffResolution(
            handoff_id=handoff_id,
            resolution_key=h["resolution_key"],
            kind=kind,
            run_id=h["run_id"],
            profile_id=h["profile_id"],
            pending_call_id=h["pending_call_id"],
            conversation_id=h["conversation_id"],
            execution_id=h["pending_execution_id"],
            controller_revision=ctrl["controller_revision"],
            outcome_label=outcome_label,
            inventory=inv,
            resolved_by_user_id=user_id,
            resolved_at=self._clock.now(),
        )
        h["_resolution"] = resolution
        return resolution

    async def return_control(
        self, handoff_id: str, *, user_id: str, outcome_label: str | None
    ) -> HandoffResolution:
        h = self.handoffs[handoff_id]
        # 4.1 CAS: only a `claimed` episode closes; a duplicate replays the
        # stored resolution idempotently (S5 §4.4).
        if h["state"] in ("returning", "returned") and h["_resolution"] is not None:
            return h["_resolution"]
        if h["state"] != "claimed":
            # cancelled/expired/superseded — replay whatever was stored.
            if h["_resolution"] is not None:
                return h["_resolution"]
            raise RuntimeError(f"handoff {handoff_id} not claimable ({h['state']})")
        return self._close(
            handoff_id, HandoffResolutionKind.COMPLETED, user_id=user_id, outcome_label=outcome_label
        )

    async def cancel(self, handoff_id: str, *, user_id: str) -> HandoffResolution:
        h = self.handoffs[handoff_id]
        if h["_resolution"] is not None:
            return h["_resolution"]
        return self._close(
            handoff_id, HandoffResolutionKind.CANCELLED, user_id=user_id, outcome_label="cancelled"
        )

    async def expire(self, handoff_id: str) -> HandoffResolution:
        h = self.handoffs[handoff_id]
        if h["_resolution"] is not None:
            return h["_resolution"]
        return self._close(
            handoff_id, HandoffResolutionKind.EXPIRED, user_id=None, outcome_label=None
        )

    async def resolution_for(self, handoff_id: str) -> HandoffResolution:
        h = self.handoffs[handoff_id]
        if h["_resolution"] is None:
            raise RuntimeError(f"handoff {handoff_id} has no stored resolution")
        return h["_resolution"]

    async def mark_resume_dispatched(self, handoff_id: str) -> None:
        self.handoffs[handoff_id]["resume_dispatched_at"] = self._clock.now()

    async def mark_tool_resolved(self, handoff_id: str) -> None:
        h = self.handoffs[handoff_id]
        h["tool_resolved_at"] = self._clock.now()
        h["returned_at"] = self._clock.now()
        h["state"] = "returned"

    # -- worker-side fencing check (S2, collapsed) -----------------------
    def command_accepted(self, run_id: str, revision: int) -> bool:
        """A command minted at `revision` is accepted only if it is not stale —
        the fencing-token rule made structural (S5 R3 / §9 #3)."""
        ctrl = self.controllers[run_id]
        return revision >= ctrl["controller_revision"] and ctrl["controller_kind"] == "agent_control"


class LedgerNotFound(Exception):
    error_type = "browser_handoff_call_not_found"


class FakeHandoffLedger:
    """Models the platform `chat.tool_call` durable ledger + its exactly-once
    completion CAS (4.3) and the timeout-sweep placeholder + late supersession
    (S5 §6). `rows` is the DURABLE store."""

    def __init__(self, clock: Clock, *, rows: dict | None = None) -> None:
        self._clock = clock
        self.rows: dict[str, dict] = rows if rows is not None else {}
        self.resolve_calls = 0

    async def delegate(
        self, *, call_id, conversation_id, execution_id, handoff_id, expires_at
    ) -> None:
        self.rows[call_id] = {
            "call_id": call_id,
            "conversation_id": conversation_id,
            "execution_id": execution_id,
            "handoff_id": handoff_id,
            "status": "delegated",
            "resolved_at": None,
            "resolution_source": None,
            "expires_at": expires_at,
        }

    def sweep_timeout(self, call_id: str) -> None:
        """The ledger abandonment sweep writes a placeholder when a pending call
        passes `expires_at` (S5 §6). A later real return SUPERSEDES it."""
        row = self.rows.get(call_id)
        if row is None or row["resolved_at"] is not None:
            return
        if self._clock.now() < row["expires_at"]:
            return
        row["status"] = "abandoned"
        row["resolved_at"] = self._clock.now()
        row["resolution_source"] = "timeout_sweep"

    async def resolve(self, resolution: HandoffResolution) -> HandoffResolutionReceipt:
        self.resolve_calls += 1
        row = self.rows.get(resolution.pending_call_id)
        if row is None:
            return HandoffResolutionReceipt(
                resolved=False, already_resolved=False, not_found=True,
                continuation_needed=False,
            )
        # Winner: still open, OR a timeout placeholder that a genuine return
        # supersedes (late-answer rule, S5 §6).
        can_win = row["resolved_at"] is None or (
            row["resolution_source"] == "timeout_sweep"
            and resolution.kind is HandoffResolutionKind.COMPLETED
        )
        if can_win:
            row["status"] = "resolved"
            row["resolved_at"] = self._clock.now()
            row["resolution_source"] = resolution.kind.value
            return HandoffResolutionReceipt(
                resolved=True, already_resolved=False, not_found=False,
                continuation_needed=True, user_request_id=row["execution_id"],
            )
        # Loser — idempotent success, a no-op (S5 §4.3).
        return HandoffResolutionReceipt(
            resolved=False, already_resolved=True, not_found=False,
            continuation_needed=False, user_request_id=row["execution_id"],
        )
