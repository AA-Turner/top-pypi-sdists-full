"""Keep an AI call's history the ONE way, when it did not run through the engine.

Owner ruling (Arman, 2026-10-05): every AI call keeps its history one way —
conversation + messages + cost row + the exact request snapshot — through the
canonical funnel (conversation gate → ``persist_completed_request`` → the
executor's ``_write_request_snapshot``). No parallel writer.

Most calls get that from ``execute_ai_request``. A few spend money WITHOUT the
engine loop:

* a provider Batch API result (``batch_history`` builds its turn, then calls
  :func:`record_turn`);
* a direct ``send_once`` caller — a settings probe, a rejection-fix replay, a
  Hindsight wire replay (:func:`record_sent_call`);
* a realtime socket session — Gemini Live / Lyria — whose turns stream over a
  websocket (:class:`RunConversation`, one ``record`` per completed turn).

Each of them hands this module a ``CompletedRequest`` in exactly the shape a
provider turn comes back in, plus the two snapshot halves (what went on the
wire, and the provider's answer or error). This module only narrows the ambient
AppContext to the run and calls the existing writers inside one standalone
Coordinator.

The ambient AppContext supplies the actor + organization. A call with neither
cannot be recorded; :func:`record_turn` raises, and the callers report the loss
through :func:`report_unrecorded_run` (``run_history_write_failure``) — never a
silent drop.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RunHistoryRecord:
    conversation_id: str
    request_id: str
    message_ids: list[str]
    request_ids: list[str]
    snapshot_id: str


@dataclass
class RunTurn:
    """One completed provider exchange, ready for the funnel.

    ``completed.request.config.messages`` is the conversation INCLUDING this
    turn; ``trigger_position`` is the first message this turn added (the person's
    input), ``assistant_position`` the model's answer (or the last input row
    when the turn produced no answer).
    """

    completed: Any
    provider: str
    model: str
    trigger_position: int
    assistant_position: int
    #: Provider-shape request (``chat.request_snapshot.request_payload``).
    request_payload: Any
    #: ``AIMatrixRequest.to_dict()`` (``unified_payload``), or None.
    unified_payload: Any = None
    #: The provider's answer, or its error envelope (``response_payload``).
    response_payload: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
    #: First message position this turn WRITES (default: ``trigger_position``).
    #: A one-shot call whose whole rendered request is new passes 0 while its
    #: trigger stays the last input message.
    write_from: int | None = None


async def record_turn(
    turn: RunTurn,
    *,
    source_feature: str,
    system_run: bool,
    new_conversation: bool,
    reason: str,
) -> RunHistoryRecord:
    """Write ``turn`` through the canonical funnel. Raises on failure.

    ``new_conversation=True`` opens the conversation through the gate; later
    turns of the same conversation pass False and only append. ``system_run``
    keeps machine calls out of people's chat lists (full history either way).
    """
    # A fresh task gets a COPY of the ambient context, so every override below
    # stays inside this run and never leaks into the caller's context.
    return await asyncio.create_task(
        _record(
            turn,
            source_feature=source_feature,
            system_run=system_run,
            new_conversation=new_conversation,
            reason=reason,
        )
    )


async def _record(
    turn: RunTurn,
    *,
    source_feature: str,
    system_run: bool,
    new_conversation: bool,
    reason: str,
) -> RunHistoryRecord:
    from matrx_ai.context.app_context import get_app_context, set_app_context
    from matrx_ai.db.conversation_gate import (
        create_new_conversation,
        ensure_user_request_exists,
    )
    from matrx_ai.db.persistence import persist_completed_request
    from matrx_ai.orchestrator.execution_state import ExecutionState, ExecutionStateSnapshot
    from matrx_ai.orchestrator.executor import _write_request_snapshot
    from matrx_ai.persistence import standalone_coordinator

    completed = turn.completed
    conversation_id = str(completed.request.conversation_id)
    request_id = str(completed.request.request_id)
    ctx = get_app_context()
    if not getattr(ctx, "user_id", None):
        raise ValueError(
            f"{reason}: the ambient AppContext names no actor — this run's history "
            "cannot be kept (the caller must install the actor + organization)"
        )
    set_app_context(
        ctx.with_overrides(
            conversation_id=conversation_id,
            request_id=request_id,
            store=True,
            system_run=system_run,
            source_feature=source_feature,
            metadata={**dict(ctx.metadata or {}), **dict(turn.metadata or {})},
        )
    )
    run_ctx = get_app_context()
    # The cost row is computed from the catalog price; a cold process (a script,
    # a fresh worker) must load it first or the row records an unknown cost.
    from matrx_ai.config.usage_config import ensure_pricing_lookup

    await ensure_pricing_lookup()
    write_from = turn.trigger_position if turn.write_from is None else turn.write_from
    completed.trigger_message_position = write_from
    has_answer = turn.assistant_position > turn.trigger_position
    completed.result_start_position = (
        turn.assistant_position if has_answer else write_from
    )
    completed.result_end_position = len(completed.request.config.messages.to_list()) - 1

    # The request row id is reserved (persistence INSERTs it under this id).
    # Message ids are NOT: a reserved message id means "a pending row already
    # exists" and persistence would only UPDATE it — here the messages are
    # fresh INSERTs whose ids come back in order.
    state = ExecutionState()
    state.reserved_request_ids[1] = str(uuid.uuid4())

    snapshot_id = str(uuid.uuid4())
    async with standalone_coordinator(
        reason=reason, request_id=request_id, conversation_id=conversation_id
    ):
        if new_conversation:
            await create_new_conversation(conversation_id, str(run_ctx.user_id))
        await ensure_user_request_exists(request_id=request_id, user_id=str(run_ctx.user_id))
        persisted = await persist_completed_request(
            completed, conversation_id=conversation_id, state=state
        )
        message_ids = [str(m) for m in (persisted.get("message_ids") or [])]
        await _write_request_snapshot(
            exec_ctx=run_ctx,
            iteration=1,
            api_response=None,
            error_payload=turn.response_payload if turn.response_payload is not None else {},
            request_payload=turn.request_payload,
            unified_payload=turn.unified_payload,
            trigger_position=turn.trigger_position,
            first_assistant_position=turn.assistant_position,
            state_snapshot=ExecutionStateSnapshot(
                iteration=1,
                reserved_message_ids={
                    write_from + i: mid for i, mid in enumerate(message_ids)
                },
                reserved_request_ids=dict(state.reserved_request_ids),
                last_model=turn.model,
            ),
            provider=turn.provider,
            model=turn.model,
            snapshot_id=snapshot_id,
        )
    return RunHistoryRecord(
        conversation_id=conversation_id,
        request_id=request_id,
        message_ids=message_ids,
        request_ids=[str(r) for r in (persisted.get("request_ids") or [])],
        snapshot_id=snapshot_id,
    )


async def report_unrecorded_run(
    exc: BaseException, *, reason: str, conversation_id: str | None, request_id: str | None
) -> None:
    """The ONE loud door for a run whose history could not be kept. Never raises."""
    from matrx_ai.db.persistence import record_run_history_write_failure

    try:
        from matrx_utils import vcprint

        vcprint(
            f"[run_history] {reason}: history NOT kept for conversation {conversation_id} "
            f"(request {request_id}): {type(exc).__name__}: {exc}",
            color="red",
            log_level="ERROR",
        )
    except Exception:  # noqa: BLE001 — logging never becomes a second failure
        pass
    await record_run_history_write_failure(
        exc, stage=f"record:{reason}", conversation_id=conversation_id, request_id=request_id
    )


# ── one direct send_once call ────────────────────────────────────────────────


def _provider_of(request: Any, response: Any) -> str:
    usage = getattr(response, "usage", None)
    api = str(getattr(usage, "api", "") or "")
    if api:
        return api
    meta = getattr(response, "metadata", None) or {}
    return str(meta.get("provider") or "")


def turn_from_sent_call(
    request: Any,
    *,
    response: Any = None,
    error: BaseException | None = None,
    wire_payload: Any = None,
) -> RunTurn:
    """A ``send_once`` exchange (answer or failure) as a :class:`RunTurn`.

    ``request`` is the canonical ``AIMatrixRequest`` that was sent (its config
    is canonical again after ``send_once``); ``wire_payload`` is what the
    provider's capture seam stashed (``state.snapshot_payload``).
    """
    from matrx_ai.config.unified_config import UnifiedResponse
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    unified = request.to_dict()
    input_count = len(request.config.messages.to_list())
    model = str(
        getattr(request.config, "model", None)
        or getattr(getattr(response, "usage", None), "matrx_model_name", "")
        or ""
    )
    if response is not None:
        usage = getattr(response, "usage", None)
        request.add_usage(usage)
        final = response
        recorded = (
            AIMatrixRequest.add_response(request, response) if response.messages else request
        )
        status = "success"
        response_payload = response.to_dict() if hasattr(response, "to_dict") else response
    else:
        final = UnifiedResponse(
            messages=[], usage=None, finish_reason="error", stop_reason="error", metadata={}
        )
        recorded = request
        status = "failed"
        info = getattr(error, "error_info", None)
        response_payload = {
            "outcome": "error",
            "exception_type": type(error).__name__ if error else None,
            "message": str(getattr(info, "message", None) or error or "")[:2000],
            "error_type": getattr(info, "error_type", None),
        }
    meta: dict[str, Any] = {"status": status, "finish_reason": final.finish_reason}
    if status == "failed":
        meta["error"] = response_payload
    completed = CompletedRequest(
        request=recorded, iterations=1, final_response=final, metadata=meta
    )
    total = len(recorded.config.messages.to_list())
    return RunTurn(
        completed=completed,
        provider=_provider_of(request, response),
        model=model,
        trigger_position=max(0, input_count - 1),
        assistant_position=input_count if total > input_count else max(0, input_count - 1),
        write_from=0,
        request_payload=wire_payload if wire_payload is not None else {},
        unified_payload=unified,
        response_payload=response_payload,
    )


async def record_sent_call(
    request: Any,
    *,
    source_feature: str,
    response: Any = None,
    error: BaseException | None = None,
    wire_payload: Any = None,
) -> RunHistoryRecord | None:
    """Keep ONE direct ``send_once`` call (a probe, a replay) as a system run.

    Never raises: a failure to record is reported through
    :func:`report_unrecorded_run` and the caller's result is untouched.
    """
    conversation_id = str(getattr(request, "conversation_id", "") or "") or None
    request_id = str(getattr(request, "request_id", "") or "") or None
    try:
        turn = turn_from_sent_call(
            request, response=response, error=error, wire_payload=wire_payload
        )
        return await record_turn(
            turn,
            source_feature=source_feature,
            system_run=True,
            new_conversation=True,
            reason=f"sent_call:{source_feature}",
        )
    except Exception as exc:  # noqa: BLE001 — reported loudly, never breaks the caller
        await report_unrecorded_run(
            exc,
            reason=f"sent_call:{source_feature}",
            conversation_id=conversation_id,
            request_id=request_id,
        )
        return None


# ── a multi-turn session (realtime sockets) ──────────────────────────────────


class RunConversation:
    """One conversation whose turns arrive one at a time (a realtime session).

    Holds the session's canonical ``AIMatrixRequest`` (system instruction +
    every turn so far). ``record`` appends one turn — the person's input and
    the model's answer with its usage — and writes it through the funnel; the
    first turn opens the conversation. Turns are recorded in order (one lock).
    """

    def __init__(
        self,
        *,
        provider: str,
        model: str,
        source_feature: str,
        system_instruction: str | None = None,
        session_config: dict[str, Any] | None = None,
        conversation_id: str | None = None,
        system_run: bool = False,
        prior_messages: list[Any] | None = None,
        opened: bool = False,
    ) -> None:
        """``prior_messages`` + ``opened=True`` continue a STORED conversation:
        the history already written (see :meth:`resume`), so the next ``record``
        appends after it instead of opening a new conversation."""
        from matrx_ai.config.message_config import MessageList
        from matrx_ai.config.unified_config import UnifiedConfig
        from matrx_ai.orchestrator.requests import AIMatrixRequest

        self.provider = provider
        self.model = model
        self.source_feature = source_feature
        self.system_run = system_run
        self.session_config = dict(session_config or {})
        self.conversation_id = conversation_id or str(uuid.uuid4())
        config = UnifiedConfig(
            model=model,
            messages=MessageList(_messages=list(prior_messages or [])),
            system_instruction=system_instruction or None,
        )
        self._request = AIMatrixRequest(
            conversation_id=self.conversation_id, config=config, request_id=""
        )
        self._opened = opened
        self._lock = asyncio.Lock()
        self.records: list[RunHistoryRecord] = []

    @property
    def opened(self) -> bool:
        return self._opened

    def messages(self) -> list[Any]:
        """Every message of the conversation so far (stored history + recorded turns)."""
        return list(self._request.config.messages.to_list())

    @classmethod
    async def resume(
        cls,
        conversation_id: str,
        *,
        provider: str,
        model: str,
        source_feature: str,
        system_instruction: str | None = None,
        session_config: dict[str, Any] | None = None,
        system_run: bool = False,
        load: Any = None,
    ) -> RunConversation:
        """The conversation ``conversation_id`` as it is stored, ready to append.

        A turn recorded through a short-lived process (one HTTP request per
        exchange) cannot hold the session in memory, so it rebuilds it from the
        ONE history projection a continuation reads (the resolver's
        ``_load_persisted_messages``). A conversation with no stored messages
        comes back unopened: its first ``record`` opens it through the gate
        (which adopts an unstarted shell row the caller owns).
        """
        if load is None:
            from matrx_ai.agents.resolver import _load_persisted_messages as load
        prior = list(await load(conversation_id) or [])
        return cls(
            provider=provider,
            model=model,
            source_feature=source_feature,
            system_instruction=system_instruction,
            session_config=session_config,
            conversation_id=conversation_id,
            system_run=system_run,
            prior_messages=prior,
            opened=bool(prior),
        )

    async def record(
        self,
        *,
        user_messages: list[Any],
        output_text: str,
        usage: Any = None,
        request_payload: Any = None,
        response_payload: Any = None,
        error: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        answer_metadata: dict[str, Any] | None = None,
    ) -> RunHistoryRecord:
        """Append one turn and write it. Raises on failure (the caller reports).

        ``answer_metadata`` lands on the answer's message row (``chat.message.metadata``),
        as a caller's own ``user_messages`` carry theirs.
        """
        from matrx_ai.config.message_config import UnifiedMessage
        from matrx_ai.config.send_boundary import config_with_messages
        from matrx_ai.config.unified_config import UnifiedResponse
        from matrx_ai.config.unified_content import TextContent
        from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

        async with self._lock:
            prior = self._request.config.messages.to_list()
            trigger = len(prior)
            answer = (
                [
                    UnifiedMessage(
                        role="assistant",
                        content=[TextContent(text=output_text)],
                        metadata=dict(answer_metadata or {}),
                    )
                ]
                if output_text
                else []
            )
            config = config_with_messages(self._request.config, [*prior, *user_messages, *answer])
            request = AIMatrixRequest(
                conversation_id=self.conversation_id,
                config=config,
                request_id=str(uuid.uuid4()),
            )
            request.add_usage(usage)
            status = "success" if (answer and not error) else "failed"
            final = UnifiedResponse(
                messages=answer,
                usage=usage,
                finish_reason="stop" if status == "success" else "error",
                stop_reason="end_turn" if status == "success" else "error",
                metadata={"session": self.source_feature},
            )
            meta: dict[str, Any] = {"status": status, "finish_reason": final.finish_reason}
            if status == "failed":
                meta["error"] = error or {"kind": "no_output"}
            completed = CompletedRequest(
                request=request, iterations=1, final_response=final, metadata=meta
            )
            total = len(config.messages.to_list())
            turn = RunTurn(
                completed=completed,
                provider=self.provider,
                model=self.model,
                trigger_position=trigger,
                assistant_position=total - 1 if answer else max(trigger, total - 1),
                request_payload=request_payload
                if request_payload is not None
                else {"session_config": self.session_config},
                unified_payload=request.to_dict(),
                response_payload=response_payload,
                metadata=dict(metadata or {}),
            )
            record = await record_turn(
                turn,
                source_feature=self.source_feature,
                system_run=self.system_run,
                new_conversation=not self._opened,
                reason=f"session_turn:{self.source_feature}",
            )
            self._opened = True
            # The written rows are this conversation's history now; the next
            # turn appends after them.
            self._request = request
            self.records.append(record)
            return record


__all__ = [
    "RunConversation",
    "RunHistoryRecord",
    "RunTurn",
    "record_sent_call",
    "record_turn",
    "report_unrecorded_run",
    "turn_from_sent_call",
]
