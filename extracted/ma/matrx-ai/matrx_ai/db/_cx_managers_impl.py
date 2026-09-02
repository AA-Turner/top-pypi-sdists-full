from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any, Literal
from uuid import uuid4

from matrx_utils import vcprint

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.db._registry import get_base, get_model

CxAgentMemoryBase = get_base("AgentMemoryBase")
CxObservationalMemoryBase = get_base("ObservationalMemoryBase")
CxObservationalMemoryEventBase = get_base("ObservationalMemoryEventBase")
CxRequestBase = get_base("RequestBase")
CxRequestSnapshotBase = get_base("RequestSnapshotBase")
CxToolCallBase = get_base("ToolCallBase")
CxToolTraceBase = get_base("ToolTraceBase")
CxUserRequestBase = get_base("UserRequestBase")
CxMessageBase = get_base("MessageBase")
CxMediaBase = get_base("MediaBase")
CxConversationBase = get_base("ConversationBase")
CxPendingInjectionBase = get_base("PendingInjectionBase")

CxMessage = get_model("Message")
CxToolCall = get_model("ToolCall")
CxToolTrace = get_model("ToolTrace")
CxMedia = get_model("Media")
CxUserRequest = get_model("UserRequest")
CxRequest = get_model("Request")
CxRequestSnapshot = get_model("RequestSnapshot")
CxAgentMemory = get_model("AgentMemory")
CxObservationalMemory = get_model("ObservationalMemory")
CxObservationalMemoryEvent = get_model("ObservationalMemoryEvent")
CxConversation = get_model("Conversation")
CxPendingInjection = get_model("PendingInjection")
from matrx_ai.reports.cost_analysis import ConversationCostSummary, UserRequestCostRollup

from .conversation_rebuild import rebuild_conversation_messages


CONVERSATION_INTEGRITY_ERROR_KIND = "conversation_integrity_incomplete_request"


def _is_incomplete_request(row: Any) -> bool:
    """Identify requests whose terminal persistence never completed."""
    status = str(getattr(row, "status", "") or "").lower()
    if status == "abandoned":
        # The persistence watchdog is the canonical owner of stale rows.  Once
        # its sweep has transitioned a request and stamped the transition
        # metadata, reloading that conversation must not manufacture a fresh
        # system_error on every read.  Unstamped abandonment still represents
        # an independently discovered incomplete turn and is captured here.
        metadata = getattr(row, "metadata", None)
        if isinstance(metadata, dict) and (
            metadata.get("watchdog_at") or metadata.get("watchdog_reason")
        ):
            return False
        return True
    return status == "failed" and getattr(row, "completed_at", None) is None


async def _capture_incomplete_request_integrity(
    *, conversation: Any, incomplete_rows: list[Any]
) -> None:
    """Put reload-detected incomplete turns on the structured repair queue."""
    from matrx_connect.streaming.error_capture import capture_error

    incomplete_ids = [str(getattr(row, "id", "") or "") for row in incomplete_rows]
    first_row = incomplete_rows[0]
    await capture_error(
        RuntimeError(
            "Conversation reload found one or more incomplete persisted requests; "
            "a committed turn may be missing"
        ),
        kind=CONVERSATION_INTEGRITY_ERROR_KIND,
        request_id=incomplete_ids[0] or None,
        user_id=str(getattr(first_row, "user_id", "") or "") or None,
        conversation_id=str(getattr(conversation, "id", "") or "") or None,
        route="matrx_ai.db.cx_managers.get_conversation_data",
        error_type="IncompleteConversationRequest",
        payload={
            "incomplete_request_ids": incomplete_ids[:25],
            "incomplete_request_count": len(incomplete_ids),
            "committed_message_count": getattr(conversation, "message_count", None),
        },
    )


class CxToolCallManager(CxToolCallBase):
    _instance: CxToolCallManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxToolCallManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxToolCall) -> None:
        pass


class CxToolTraceManager(CxToolTraceBase):
    """Manager for the cx_tool_trace append-only event log. Writes go
    through ``matrx_ai.tools._db_log.db_log_event`` fire-and-forget; reads
    are admin/debug-only (Phase 4 routes)."""

    _instance: CxToolTraceManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxToolTraceManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxToolTrace) -> None:
        pass


class CxConversationManager(CxConversationBase):
    _instance: CxConversationManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxConversationManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxConversation) -> None:
        pass


class CxMediaManager(CxMediaBase):
    _instance: CxMediaManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxMediaManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxMedia) -> None:
        pass


class CxMessageManager(CxMessageBase):
    _instance: CxMessageManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxMessageManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxMessage) -> None:
        pass


@dataclass
class RunClaimResult:
    claimed: bool
    status: str | None = None
    claim_token: str | None = None


# A 'processing' claim older than this is treated as a crashed run and may be
# re-claimed. Must comfortably exceed the orchestrator's per-turn heartbeat
# cadence (last_activity_at is refreshed at every turn commit and before every
# delegated suspend).
RUN_CLAIM_STALE_SECONDS = 180


class CxUserRequestManager(CxUserRequestBase):
    _instance: CxUserRequestManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxUserRequestManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxUserRequest) -> None:
        pass

    async def try_claim_for_run(
        self,
        request_id: str,
        *,
        user_id: str | None = None,
        conversation_id: str | None = None,
        stale_after_seconds: int = RUN_CLAIM_STALE_SECONDS,
    ) -> RunClaimResult:
        """Atomically claim a cx_user_request for a (resume) run.

        Exactly one caller wins: the claim is a conditional UPDATE that flips
        ``status`` to 'processing' only when the row is resumable ('paused')
        or a previous 'processing' claim has gone stale (crashed run —
        ``last_activity_at`` older than ``stale_after_seconds``). Losers get
        ``claimed=False`` plus the row's current status so the caller can
        return a precise conflict (run still live vs. nothing to resume).

        This is the structural fix for the concurrent-resume corruption bug:
        N racing POST /resume calls previously all started loops on the same
        conversation, producing duplicate message positions and repeated
        identical tool calls. (2026-06-09 incident.)

        ``conversation_id`` is NOT a column on cx_user_request (a request spans
        many conversations now). When supplied it is enforced through the
        cx_request bridge: the request must have actually touched that
        conversation, otherwise there is nothing of this conversation to
        resume and we report ``claimed=False, status=None`` (the 404 path).
        """
        from datetime import timedelta

        now = datetime.now(UTC)

        # Conversation scoping via the cx_request bridge (the real request<->
        # conversation link). A resumable request always has ≥1 cx_request for
        # the conversation it paused on (the pause happens after a provider
        # call returns a tool_use), so this never false-negatives a genuine
        # resume.
        if conversation_id and not await CxRequest.exists(
            user_request_id=request_id,
            conversation_id=conversation_id,
        ):
            return RunClaimResult(claimed=False, status=None)

        scope: dict[str, Any] = {"id": request_id}
        if user_id:
            scope["created_by"] = user_id

        existing_rows = await self.filter_items(**scope)
        existing = existing_rows[0] if existing_rows else None
        existing_metadata = (
            dict(existing.metadata)
            if existing is not None and isinstance(existing.metadata, dict)
            else {}
        )
        claim_token = str(uuid4())
        claim_metadata = {**existing_metadata, "run_claim_token": claim_token}

        result = await self.update_where(
            {**scope, "status": "paused"},
            status="processing",
            last_activity_at=now,
            metadata=claim_metadata,
        )
        if result.rows_affected > 0:
            return RunClaimResult(
                claimed=True,
                status="processing",
                claim_token=claim_token,
            )

        # 'processing' = a live claim from this method; 'pending' = a live
        # ORIGINAL run (status is only finalized at persist time). Either may
        # be a crashed run — reclaim only when its heartbeat went stale.
        # last_activity_at is seeded at row creation (conversation_gate) and
        # refreshed every turn commit, so __lt is safe (never NULL).
        stale_cutoff = now - timedelta(seconds=stale_after_seconds)
        result = await self.update_where(
            {
                **scope,
                "status__in": ["processing", "pending"],
                "last_activity_at__lt": stale_cutoff,
            },
            status="processing",
            last_activity_at=now,
            metadata=claim_metadata,
        )
        if result.rows_affected > 0:
            return RunClaimResult(
                claimed=True,
                status="processing",
                claim_token=claim_token,
            )

        rows = await self.filter_items(**scope)
        row = rows[0] if rows else None
        return RunClaimResult(claimed=False, status=row.status if row else None)

    async def release_run_claim(
        self,
        request_id: str,
        *,
        claim_token: str,
    ) -> None:
        """Revert a claim taken by ``try_claim_for_run`` when the run never
        started (prepare failed before the loop ran).

        The UUID stored in metadata is the ownership marker. Matching it
        prevents a stale worker from releasing a newer worker's claim after
        the stale-claim takeover window.
        """
        rows = await self.filter_items(id=request_id, status="processing")
        row = rows[0] if rows else None
        metadata = dict(row.metadata) if row and isinstance(row.metadata, dict) else {}
        if metadata.get("run_claim_token") != claim_token:
            return
        await self.update_where(
            {"id": request_id, "status": "processing", "metadata": metadata},
            status="paused",
        )

    async def renew_run_claim(
        self, request_id: str, *, claim_token: str
    ) -> Literal["owned", "terminal", "lost"]:
        """Heartbeat a claim and distinguish completion from ownership loss."""
        for _ in range(3):
            rows = await self.filter_items(id=request_id)
            row = rows[0] if rows else None
            if row is None:
                return "lost"
            metadata = dict(row.metadata) if isinstance(row.metadata, dict) else {}
            row_token = metadata.get("run_claim_token")
            if row.status != "processing":
                # Same-owner finalization is normal. A legacy/final metadata
                # rewrite may omit the token, which is also terminal-safe. But
                # a different explicit token means a replacement runner won.
                return "lost" if row_token and row_token != claim_token else "terminal"
            if row_token != claim_token:
                return "lost"
            result = await self.update_where(
                {"id": request_id, "status": "processing", "metadata": metadata},
                last_activity_at=datetime.now(UTC),
            )
            if result.rows_affected > 0:
                return "owned"
            # A same-owner metadata enrichment may have raced the CAS. Re-read
            # before deciding ownership was lost.
        return "lost"


class CxRequestManager(CxRequestBase):
    _instance: CxRequestManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxRequestManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxRequest) -> None:
        pass

    async def sum_costs_by_user_request(
        self,
        user_request_id: str,
    ) -> UserRequestCostRollup:
        """Authoritative cost rollup for one cx_user_request.

        SUMs every committed, non-deleted cx_request row sharing
        ``user_request_id`` — the parent's turns AND every sub-agent's turns
        (they all carry the same inherited user_request_id). This is the
        single source of truth the user confirmed: one user click = one
        cx_user_request = the total of everything it triggered.

        Idempotent and order-independent: re-running recomputes the same sum
        from ground truth, which is what structurally kills the prior in-memory
        last-write-wins clobber (each finalize overwrote the row with only its
        own contribution). Rows of ANY status are summed — a ``failed`` row
        that still carries provider-billed cost MUST count.

        ``filter_*`` reads fresh from the DB (no cache), so it must be called
        AFTER the relevant coordinators have flushed (committed) their rows.
        """
        rows: list[CxRequest] = await self.filter_requests_by_user_request_id(user_request_id)

        request_count = 0
        input_tokens = output_tokens = cached_tokens = total_tokens = 0
        api_duration_ms = tool_duration_ms = total_duration_ms = 0
        total_tool_calls = 0
        total_cost = Decimal("0")

        for r in rows:
            if getattr(r, "deleted_at", None) is not None:
                continue
            request_count += 1
            input_tokens += int(r.input_tokens or 0)
            output_tokens += int(r.output_tokens or 0)
            cached_tokens += int(r.cached_tokens or 0)
            total_tokens += int(r.total_tokens or 0)
            api_duration_ms += int(r.api_duration_ms or 0)
            tool_duration_ms += int(r.tool_duration_ms or 0)
            total_duration_ms += int(r.total_duration_ms or 0)
            total_tool_calls += int(r.tool_calls_count or 0)
            if r.cost is not None:
                total_cost += Decimal(str(r.cost))

        return UserRequestCostRollup(
            user_request_id=user_request_id,
            request_count=request_count,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=cached_tokens,
            total_tokens=total_tokens,
            total_cost=total_cost,
            api_duration_ms=api_duration_ms,
            tool_duration_ms=tool_duration_ms,
            total_duration_ms=total_duration_ms,
            total_tool_calls=total_tool_calls,
        )

    async def get_conversation_cost_summary(
        self,
        conversation_id: str,
    ) -> ConversationCostSummary:
        requests: list[CxRequest] = await self.load_requests_by_conversation_id(conversation_id)

        total_input = total_output = total_cached = total_tokens = 0
        total_cost = Decimal("0")
        total_api_ms = total_wall_ms = 0
        models_used: set[str] = set()
        providers: set[str] = set()

        for r in requests:
            total_input += r.input_tokens or 0
            total_output += r.output_tokens or 0
            total_cached += r.cached_tokens or 0
            total_tokens += r.total_tokens or 0
            total_cost += Decimal(str(r.cost)) if r.cost is not None else Decimal("0")
            total_api_ms += r.api_duration_ms or 0
            total_wall_ms += r.total_duration_ms or 0
            if r.ai_model_id:
                models_used.add(str(r.ai_model_id))
            if r.provider:
                providers.add(r.provider)

        n = len(requests)
        return ConversationCostSummary(
            conversation_id=conversation_id,
            request_count=n,
            input_tokens=total_input,
            output_tokens=total_output,
            cached_tokens=total_cached,
            total_tokens=total_tokens,
            total_cost=total_cost,
            total_api_duration_ms=total_api_ms,
            total_duration_ms=total_wall_ms,
            avg_api_duration_ms=total_api_ms / n if n else 0.0,
            avg_duration_ms=total_wall_ms / n if n else 0.0,
            models_used=list(models_used),
            providers=list(providers),
        )


class CxRequestSnapshotManager(CxRequestSnapshotBase):
    _instance: CxRequestSnapshotManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxRequestSnapshotManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxRequestSnapshot) -> None:
        pass


class CxAgentMemoryManager(CxAgentMemoryBase):
    _instance: CxAgentMemoryManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxAgentMemoryManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxAgentMemory) -> None:
        pass


class CxObservationalMemoryManager(CxObservationalMemoryBase):
    _instance: CxObservationalMemoryManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxObservationalMemoryManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxObservationalMemory) -> None:
        pass


class CxObservationalMemoryEventManager(CxObservationalMemoryEventBase):
    _instance: CxObservationalMemoryEventManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxObservationalMemoryEventManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxObservationalMemoryEvent) -> None:
        pass

    async def get_conversation_memory_cost(self, conversation_id: Any) -> dict[str, Any]:
        """Aggregate per-event-type cost/token/count rollup for one conversation.

        Lives on the package-level manager rather than the auto-generated base
        so the schema regenerator doesn't strip it.
        """
        rows = await self.filter_items(conversation_id=conversation_id)
        total_cost = Decimal("0")
        total_input = 0
        total_output = 0
        by_event: dict[str, dict[str, Any]] = {}
        for row in rows:
            cost = row.cost if isinstance(row.cost, Decimal) else Decimal(str(row.cost or 0))
            total_cost += cost
            total_input += int(row.input_tokens or 0)
            total_output += int(row.output_tokens or 0)
            bucket = by_event.setdefault(
                row.event_type,
                {"count": 0, "cost": Decimal("0"), "input_tokens": 0, "output_tokens": 0},
            )
            bucket["count"] += 1
            bucket["cost"] += cost
            bucket["input_tokens"] += int(row.input_tokens or 0)
            bucket["output_tokens"] += int(row.output_tokens or 0)
        return {
            "conversation_id": str(conversation_id),
            "total_cost": total_cost,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "event_count": len(rows),
            "by_event_type": by_event,
        }


def _row_seq(row: Any) -> int:
    """FIFO key for claim results — RETURNING rows may be raw dicts."""
    val = (
        row.get("enqueued_seq")
        if isinstance(row, dict)
        else getattr(row, "enqueued_seq", 0)
    )
    return int(val or 0)


class CxPendingInjectionManager(CxPendingInjectionBase):
    """The Turn-Boundary Inbox manager. Producers (the enqueue endpoint, and
    later the reactive-injection system) write rows; the orchestrator loop
    drains them at the natural turn boundary via ``claim_pending`` (atomic
    UPDATE … RETURNING so concurrent drains can't double-deliver)."""

    _instance: CxPendingInjectionManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxPendingInjectionManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: CxPendingInjection) -> None:
        pass

    async def enqueue(
        self,
        *,
        injection_id: str,
        conversation_id: str,
        created_by: str,
        kind: str,
        content: dict[str, Any],
        source: str,
        is_visible_to_user: bool,
        is_visible_to_model: bool,
        delivery: str = "next_boundary",
        metadata: dict[str, Any] | None = None,
    ) -> CxPendingInjection:
        return await self.create_item(
            id=injection_id,
            conversation_id=conversation_id,
            created_by=created_by,
            kind=kind,
            content=content,
            source=source,
            status="pending",
            delivery=delivery,
            is_visible_to_user=is_visible_to_user,
            is_visible_to_model=is_visible_to_model,
            metadata=metadata or {},
        )

    async def has_pending(self, conversation_id: str) -> bool:
        return await self.count(conversation_id=conversation_id, status="pending") > 0

    async def claim_pending(
        self, conversation_id: str, *, request_id: str | None = None
    ) -> list[CxPendingInjection]:
        """Atomically claim every pending STEER row (``delivery='next_boundary'``)
        for a conversation (pending → consumed) in ONE ``UPDATE … RETURNING``
        and return them in strict FIFO order. Two concurrent drains cannot both
        claim a row; a row enqueued after the snapshot simply waits for the next
        turn. QUEUE rows (``delivery='turn_end'``) are NEVER claimed here — they
        wait for the run's final boundary (``claim_next_turn_end``)."""
        from datetime import UTC, datetime

        result = await self.update_where(
            {
                "conversation_id": conversation_id,
                "status": "pending",
                "delivery": "next_boundary",
            },
            status="consumed",
            consumed_at=datetime.now(UTC),
            consumed_by_request_id=request_id,
        )
        rows = result.updated_rows or []
        return sorted(rows, key=_row_seq)

    async def claim_next_turn_end(
        self, conversation_id: str, *, request_id: str | None = None
    ) -> list[CxPendingInjection]:
        """Atomically claim the SINGLE oldest QUEUE row (``delivery='turn_end'``)
        — one queued message per turn, per the three-send-modes ruling ("when we
        are DONE, THE NEXT QUEUED MESSAGE submits"). The conditional
        ``UPDATE … WHERE id … AND status='pending'`` makes the two-step
        read-then-claim race-safe: a concurrent winner leaves this claim with
        zero rows and the item is simply gone (already claimed)."""
        from datetime import UTC, datetime

        candidates = await self.filter_items(
            conversation_id=conversation_id,
            status="pending",
            delivery="turn_end",
        )
        # A run NEVER delivers a turn_end item it enqueued itself (matched via
        # metadata.enqueued_by_request_id, stamped by every producer). Without
        # this, an in-run producer (agent_call's remember write-back to the
        # caller's own conversation) is claimed at the SAME run's final
        # boundary — an extra paid turn re-answering output the model already
        # holds. The item waits for the next run, as the contract promises.
        if request_id:
            candidates = [
                r
                for r in candidates
                if str((r.metadata or {}).get("enqueued_by_request_id") or "")
                != str(request_id)
            ]
        if not candidates:
            return []
        head = min(candidates, key=lambda r: int(r.enqueued_seq or 0))
        result = await self.update_where(
            {"id": str(head.id), "status": "pending"},
            status="consumed",
            consumed_at=datetime.now(UTC),
            consumed_by_request_id=request_id,
        )
        return list(result.updated_rows or [])

    async def list_for_conversation(
        self, conversation_id: str, created_by: str, *, status: str = "pending"
    ) -> list[CxPendingInjection]:
        """Items the user has in a conversation's inbox, FIFO. Ownership-scoped
        by created_by (only the conversation owner ever enqueues)."""
        rows = await self.filter_items(
            conversation_id=conversation_id, created_by=created_by, status=status
        )
        return sorted(rows, key=lambda r: int(r.enqueued_seq or 0))

    async def cancel_pending(
        self, injection_id: str, conversation_id: str, created_by: str
    ) -> str:
        """Cancel a still-pending item atomically. Returns one of:
        'cancelled' | 'already_drained' | 'not_found'. The status flip races
        the drain's claim safely — whoever flips first wins."""
        result = await self.update_where(
            {
                "id": injection_id,
                "conversation_id": conversation_id,
                "created_by": created_by,
                "status": "pending",
            },
            status="cancelled",
        )
        if (result.rows_affected or 0) > 0:
            return "cancelled"
        exists = await self.count(
            id=injection_id, conversation_id=conversation_id, created_by=created_by
        )
        return "already_drained" if exists else "not_found"

    async def edit_pending(
        self, injection_id: str, conversation_id: str, created_by: str, text: str
    ) -> str:
        """Replace a still-pending item's text. Returns 'updated' |
        'already_drained' | 'not_found'."""
        result = await self.update_where(
            {
                "id": injection_id,
                "conversation_id": conversation_id,
                "created_by": created_by,
                "status": "pending",
            },
            content={"text": text},
        )
        if (result.rows_affected or 0) > 0:
            return "updated"
        exists = await self.count(
            id=injection_id, conversation_id=conversation_id, created_by=created_by
        )
        return "already_drained" if exists else "not_found"


cx_conversation_manager_instance = CxConversationManager()
cx_media_manager_instance = CxMediaManager()
cx_message_manager_instance = CxMessageManager()
cx_user_request_manager_instance = CxUserRequestManager()
cx_request_manager_instance = CxRequestManager()
cx_request_snapshot_manager_instance = CxRequestSnapshotManager()
cx_agent_memory_manager_instance = CxAgentMemoryManager()
cx_observational_memory_manager_instance = CxObservationalMemoryManager()
cx_observational_memory_event_manager_instance = CxObservationalMemoryEventManager()
cx_tool_call_manager_instance = CxToolCallManager()
cx_tool_trace_manager_instance = CxToolTraceManager()
cx_pending_injection_manager_instance = CxPendingInjectionManager()


class CxManagers:
    _instance: CxManagers | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> CxManagers:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.conversation: CxConversationManager = cx_conversation_manager_instance
        self.message: CxMessageManager = cx_message_manager_instance
        self.tool_call: CxToolCallManager = cx_tool_call_manager_instance
        self.tool_trace: CxToolTraceManager = cx_tool_trace_manager_instance
        self.media: CxMediaManager = cx_media_manager_instance
        self.user_request: CxUserRequestManager = cx_user_request_manager_instance
        self.request: CxRequestManager = cx_request_manager_instance
        self.request_snapshot: CxRequestSnapshotManager = cx_request_snapshot_manager_instance
        self.agent_memory: CxAgentMemoryManager = cx_agent_memory_manager_instance
        self.om_memory: CxObservationalMemoryManager = cx_observational_memory_manager_instance
        self.om_event: CxObservationalMemoryEventManager = (
            cx_observational_memory_event_manager_instance
        )
        self.pending_injection: CxPendingInjectionManager = cx_pending_injection_manager_instance

    async def get_conversation_data(self, conversation_id: str) -> dict[str, Any]:
        item, all_related = await self.conversation.get_conversation_with_all_related(
            conversation_id
        )
        # vcprint(item, "[CX MANAGERS] Item", color="green")
        # vcprint(all_related, "[CX MANAGERS] All Related", color="cyan")
        conversation = item
        foreign_keys = all_related.foreign_keys
        inverse_fks = all_related.inverse_foreign_keys

        requests = inverse_fks.get("request") or []
        messages = inverse_fks.get("message") or []
        tool_calls = inverse_fks.get("tool_call") or []
        media = inverse_fks.get("media") or []

        # cx_user_request has NO conversation_id — it is one backend API call
        # that can span many conversations. Resolve the user_requests that
        # touched THIS conversation through the cx_request bridge (the real
        # request<->conversation link). A request that died before making any
        # provider call has zero cx_request rows and produced zero messages
        # here, so it correctly does not surface against this conversation.
        user_request_ids = sorted(
            {
                str(getattr(r, "user_request_id", "") or "")
                for r in requests
                if getattr(r, "user_request_id", None)
            }
        )
        user_requests: list[Any] = []
        if user_request_ids:
            user_requests = await self.user_request.filter_items(id__in=user_request_ids)

        # PERSISTENCE-INTEGRITY (reload detection) — an abandoned request, or a
        # failed request that never reached its completed_at finalization stamp,
        # means the turn did not commit cleanly and some messages may be missing.
        # A failed row WITH completed_at is a legitimate, fully persisted failed
        # turn and must not permanently re-alert on every conversation reload.
        # cx_conversation.message_count is the committed
        # high-water-mark (advanced atomically with each turn's messages in
        # persist_completed_request), so a reload SURFACES a possible lost turn
        # loudly instead of silently showing a short conversation. This is the
        # 2026-05-23 detector. (Persistence contract — CLAUDE.md.)
        incomplete_rows = [
            r
            for r in user_requests
            if _is_incomplete_request(r)
        ]
        incomplete_requests = [str(getattr(r, "id", "")) for r in incomplete_rows]
        if incomplete_requests:
            vcprint(
                f"[CX INTEGRITY] conversation {conversation_id}: "
                f"{len(incomplete_requests)} incomplete request(s) "
                f"[{', '.join(s[:8] for s in incomplete_requests[:5])}] — a turn may "
                f"be missing (committed message_count="
                f"{getattr(conversation, 'message_count', '?')}). Surfaced on reload.",
                color="red",
            )
            await _capture_incomplete_request_integrity(
                conversation=conversation,
                incomplete_rows=incomplete_rows,
            )

        return {
            "conversation": conversation,
            "foreign_keys": foreign_keys,
            "user_requests": user_requests,
            "requests": requests,
            "messages": messages,
            "tool_calls": tool_calls,
            "media": media,
            "incomplete_requests": incomplete_requests,
        }

    async def conversation_has_active_run(
        self, conversation_id: str, *, max_staleness_seconds: float | None = None
    ) -> bool:
        """True if a non-terminal (pending/processing) cx_user_request has
        touched this conversation.

        cx_user_request has NO conversation_id — the link is the cx_request
        bridge. There is a sub-second window right after a run starts but
        before its first cx_request lands where this returns False even though
        a run is live; the live stream itself signals the client in that
        window, so it is acceptable.

        ``max_staleness_seconds`` additionally requires ``last_activity_at``
        within the window. Callers that BLOCK on this signal (the turn lock)
        MUST pass it: a crashed run stuck 'processing' forever must never lock
        a user out of their own conversation (over-tightening is a defect —
        THE SECURITY PHILOSOPHY). Informational callers omit it.
        """
        request_ids = sorted(
            {
                str(getattr(r, "user_request_id", "") or "")
                for r in await self.request.filter_items(conversation_id=conversation_id)
                if getattr(r, "user_request_id", None)
            }
        )
        if not request_ids:
            return False
        filters: dict[str, Any] = {
            "id__in": request_ids,
            "status__in": ["pending", "processing"],
        }
        if max_staleness_seconds is not None:
            filters["last_activity_at__gte"] = datetime.now(UTC) - timedelta(
                seconds=max_staleness_seconds
            )
        return await self.user_request.exists(**filters)

    async def get_unified_config(self, flat_data: dict[str, Any]) -> UnifiedConfig:
        conversation = flat_data["conversation"]
        messages = flat_data["messages"]
        tool_calls = flat_data["tool_calls"]
        media = flat_data["media"]

        messages_rebuilt = await rebuild_conversation_messages(messages, tool_calls, media)
        # vcprint(messages_rebuilt, "[CX MANAGERS] Messages Rebuilt", color="green")

        config_dict = {
            "model": conversation.last_model_id,
            "system_instruction": conversation.system_instruction,
            "system_prompt_frozen": bool(conversation.system_instruction),
            "messages": messages_rebuilt,
            **conversation.config,
        }

        unified_config = UnifiedConfig.from_dict(config_dict)
        vcprint(unified_config, "[CX MANAGERS] Unified Config", color="cyan")

        return unified_config

    async def get_conversation_unified_config(self, conversation_id: str) -> UnifiedConfig:
        conversation_data = await self.get_conversation_data(conversation_id)

        # vcprint(conversation_data, "[CX MANAGERS] Conversation Data", color="cyan")
        conversation: CxConversation = conversation_data["conversation"]
        messages: list[CxMessage] = conversation_data["messages"]
        tool_calls: list[CxToolCall] = conversation_data["tool_calls"]
        media: list[CxMedia] = conversation_data["media"]

        messages_rebuilt = await rebuild_conversation_messages(messages, tool_calls, media)

        # Precedence: last_model_id (set after the FIRST successful turn) wins
        # when present. Otherwise we fall back to whatever is in the
        # conversation.config JSONB blob — typically the agent's default model
        # written at row creation time. The previous unconditional overwrite
        # destroyed that fallback, producing "Model not found: None" on any
        # conversation whose first turn never persisted.
        config_dict = dict(conversation.config)

        if conversation.last_model_id is not None:
            config_dict["model"] = conversation.last_model_id
        if conversation.system_instruction is not None:
            config_dict["system_instruction"] = conversation.system_instruction
            config_dict["system_prompt_frozen"] = True
        config_dict["messages"] = messages_rebuilt

        return UnifiedConfig.from_dict(config_dict)

    async def get_full_conversation(self, conversation_id: str) -> dict[str, Any]:
        conversation_data = await self.get_conversation_data(conversation_id)
        unified_config: UnifiedConfig = await self.get_unified_config(conversation_data)
        conversation: CxConversation = conversation_data["conversation"]
        user_requests: list[CxUserRequest] = conversation_data["user_requests"]
        requests: list[CxRequest] = conversation_data["requests"]

        result = {
            "conversation_id": conversation.id,
            "variables": conversation.variables,
            "overrides": conversation.overrides,
            "unified_config": unified_config,
            "user_requests": user_requests,
            "requests": requests,
        }

        return result

    async def get_conversation_cost_summary(self, conversation_id: str) -> ConversationCostSummary:
        return await self.request.get_conversation_cost_summary(conversation_id)


cxm = CxManagers()
