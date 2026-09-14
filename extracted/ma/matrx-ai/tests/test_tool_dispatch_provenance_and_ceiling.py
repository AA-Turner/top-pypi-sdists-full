"""An agent-tier write made by a TOOL names the system that made it — and a
tool that cannot finish inside its ceiling says so honestly.

Live failure, 2026-09-12 (conversation 2050e02b-c663-4b6d-99f8-7996eff7cd81).
A non-technical Expert asked the Masterwork Conductor to change how her desk's
Writer thinks. Both attempts died in the ``workflow_plan`` tool:

* 23:23:42Z — cancelled at 120s, the unturnable literal on
  ``ToolDefinition.timeout_seconds``, while the agent-builder meta-agent ran;
* 23:24:08Z — ``Matrx ORM IntegrityError … "This write declares actor_tier=code,
  but names no actor_system … x-matrx-actor-system on the client channel, or the
  app.actor_system GUC on a server channel" … Table: agent.definition``.

Nothing on the agent-tool lane declared an actor and nothing on it sets
``app.user_id`` (a durable run has no request identity at all), so the DB
resolver fell back to tier ``code`` with a NULL system — the exact pair
``wf_051`` refuses. And the Conductor, reading that text through an envelope
that added "try with different parameters", told the Expert she was *"blocked by
system policy … edits to any agent's contract must come from an authorized human
channel"*. Nothing about her request was disallowed.

These tests drive the REAL ``ToolExecutor._dispatch`` with the REAL provider
wiring (``configure_session_context(declared_actor_gucs)`` — what
``package_integration`` does at startup) and a tool whose implementation refuses
its write exactly as the database would (the ``wf_051`` predicate, transcribed
from the migration). Remove the declaration from ``_dispatch`` and the write
fails with the live message again.

Breaks these tests name:
* an agent-tier tool write reaching Postgres without naming its system;
* the dispatch ceiling going back to a literal no admin can turn;
* a timeout that does not say what it was doing, or that reads as a refusal;
* a provenance refusal reaching a model without its cause and remedy.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from matrx_orm import (
    configure_session_context,
    current_actor,
    declared_actor,
    declared_actor_gucs,
    session_context_gucs,
)

from matrx_ai.tools import knobs as knobs_mod
from matrx_ai.tools.error_remedy import UNDECLARED_ACTOR_SYSTEM, error_remedy_for
from matrx_ai.tools.executor import (
    ToolExecutor,
    _dispatch_timeout_seconds,
    timeout_tool_error,
)
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry

# The live message, verbatim from chat.tool_trace (2026-09-12 23:24:08Z).
LIVE_REFUSAL = (
    "This write declares actor_tier=code, but names no actor_system. An agent or "
    "automated write must say WHICH agent/system it is (x-matrx-actor-system on the "
    "client channel, or the app.actor_system GUC on a server channel) — a person's "
    'write needs no system at all, but "an AI did it" with no name is not provenance. '
    "Table: agent.definition"
)


class _RefusedByTheDatabase(RuntimeError):
    """What matrx-orm raises when the wf_051 CHECK rejects the row."""


def _would_the_database_refuse(gucs: dict[str, str]) -> bool:
    """``platform._stamp_actor_tier()``'s refusal clause, transcribed from
    ``db/migrations/wf_051_dd131_an_agent_names_its_system.sql``:

        IF tier IN ('ai', 'code') AND sys IS NULL THEN RAISE EXCEPTION …

    An unset GUC and an empty-string GUC are both NULL to
    ``platform.actor_system()``; a declaration that never reached the transaction
    is the ``code`` default.
    """
    tier = gucs.get("app.actor_tier") or "code"
    system = (gucs.get("app.actor_system") or "").strip() or None
    return tier in ("ai", "code") and system is None


async def _write_an_agent_definition(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """A tool implementation that writes ``agent.definition`` — the build_agent
    shape. The write opens a transaction, so it sees exactly the GUCs matrx-orm
    would emit at that BEGIN."""
    gucs = session_context_gucs()
    if _would_the_database_refuse(gucs):
        raise _RefusedByTheDatabase(LIVE_REFUSAL)
    actor = current_actor()
    return ToolResult(
        success=True,
        output={
            "agent_id": "6e60ad30-9e8b-4bc6-a3de-f05a6bb5a2e1",
            "actor_tier": actor.tier if actor else None,
            "actor_system": actor.system if actor else None,
        },
        tool_name=ctx.tool_name if hasattr(ctx, "tool_name") else "",
        call_id=ctx.call_id,
    )


@pytest.fixture(autouse=True)
def _host_provider_wired() -> Any:
    """The startup wiring, for the duration of one test (package_integration)."""
    configure_session_context(declared_actor_gucs)
    try:
        yield
    finally:
        configure_session_context(None)


@pytest.fixture(autouse=True)
def _no_host_knobs() -> Any:
    """Standalone posture: the package's announced mirrors, no host bound."""
    knobs_mod.configure_tool_dispatch_knobs(None)
    yield
    knobs_mod.configure_tool_dispatch_knobs(None)


def _tool_def(
    name: str = "workflow_plan",
    *,
    callable_: Any = _write_an_agent_definition,
    timeout_seconds: float | None = None,
) -> ToolDefinition:
    tool_def = ToolDefinition(
        name=name,
        description="Work a plan (the Plan Steward's hands).",
        tool_type=ToolType.LOCAL,
        timeout_seconds=timeout_seconds,
    )
    tool_def._callable = callable_
    return tool_def


class _SilentStream:
    def __getattr__(self, _name: str) -> Any:
        async def _noop(*a: Any, **k: Any) -> None:
            return None

        return _noop


def _executor() -> ToolExecutor:
    return ToolExecutor(registry=ToolRegistry())


def _ctx() -> ToolContext:
    return ToolContext(call_id="call-1", conversation_id="2050e02b-c663-4b6d-99f8-7996eff7cd81")


# ---------------------------------------------------------------------------
# 1. An agent-tier write names itself
# ---------------------------------------------------------------------------


def test_the_predicate_can_fail_it_is_the_live_failure() -> None:
    """The forcing half: an undeclared write is what the database refuses."""
    assert _would_the_database_refuse({}) is True
    assert _would_the_database_refuse({"app.actor_tier": "code"}) is True
    assert _would_the_database_refuse({"app.actor_tier": "ai", "app.actor_system": ""}) is True
    # A person's write is exempt on purpose (the chair's DD-131 ruling).
    assert _would_the_database_refuse({"app.actor_tier": "human"}) is False


@pytest.mark.asyncio
async def test_an_undeclared_dispatch_is_refused_exactly_as_live() -> None:
    """Without the declaration the tool's write dies with the live message."""
    tool_def = _tool_def()
    with pytest.raises(_RefusedByTheDatabase) as excinfo:
        # ``_dispatch_declared`` is ``_dispatch`` MINUS the declaration — the
        # code as it stood when the Conductor failed.
        await _executor()._dispatch_declared(tool_def, {}, _ctx(), _SilentStream())
    assert "names no actor_system" in str(excinfo.value)


@pytest.mark.asyncio
async def test_dispatch_declares_the_tool_as_the_actor_system() -> None:
    """The fix: one edge, so every tool's write names itself."""
    result = await _executor()._dispatch(_tool_def(), {}, _ctx(), _SilentStream())

    assert isinstance(result, ToolResult)
    assert result.success, result.error
    assert result.output["actor_tier"] == "ai"
    assert result.output["actor_system"] == "tool:workflow_plan"
    assert current_actor() is None, "the declaration must not outlive the tool call"


@pytest.mark.asyncio
async def test_every_tool_inherits_it_not_just_the_one_that_broke() -> None:
    """The class, not the instance: the edge names whatever tool is dispatched."""
    for name in ("agent_author", "rulebook", "workflow_author", "kind_instance_create"):
        result = await _executor()._dispatch(_tool_def(name), {}, _ctx(), _SilentStream())
        assert result.success, result.error
        assert result.output["actor_system"] == f"tool:{name}"


@pytest.mark.asyncio
async def test_a_tool_that_knows_a_better_system_name_still_wins() -> None:
    """Innermost declaration first — the nested per-tool declarations stay valid."""

    async def writes_under_its_own_name(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
        async with declared_actor("ai", "tool:instance_create"):
            return await _write_an_agent_definition(args, ctx)

    result = await _executor()._dispatch(
        _tool_def("kind_instance", callable_=writes_under_its_own_name),
        {},
        _ctx(),
        _SilentStream(),
    )
    assert result.output["actor_system"] == "tool:instance_create"


# ---------------------------------------------------------------------------
# 2. The ceiling is a knob
# ---------------------------------------------------------------------------


def test_the_dispatch_ceiling_comes_from_the_knob_not_a_literal() -> None:
    seen: list[str] = []

    def reader(key: str) -> Any:
        seen.append(key)
        return {"default_timeout_seconds": 90, "per_tool_timeout_seconds": {"workflow_plan": 450}}[
            key
        ]

    knobs_mod.configure_tool_dispatch_knobs(reader)

    assert _dispatch_timeout_seconds(_tool_def("workflow_plan"), {}, is_delegated=False) == 450.0
    assert _dispatch_timeout_seconds(_tool_def("rulebook"), {}, is_delegated=False) == 90.0
    assert "per_tool_timeout_seconds" in seen and "default_timeout_seconds" in seen


def test_a_tool_row_that_declares_its_own_ceiling_keeps_it() -> None:
    knobs_mod.configure_tool_dispatch_knobs(lambda key: {"default_timeout_seconds": 90}.get(key))
    tool_def = _tool_def("rulebook", timeout_seconds=15.0)
    assert _dispatch_timeout_seconds(tool_def, {}, is_delegated=False) == 15.0


def test_the_starting_values_are_the_seeded_rows() -> None:
    """Standalone, the announced mirrors are what migration 0673 recorded."""
    assert knobs_mod.DEFAULT_TIMEOUT_SECONDS_MIRROR == 120.0
    assert knobs_mod.PER_TOOL_TIMEOUT_SECONDS_MIRROR["workflow_plan"] == 300.0
    assert _dispatch_timeout_seconds(_tool_def("workflow_plan"), {}, is_delegated=False) == 300.0
    assert _dispatch_timeout_seconds(_tool_def("anything_else"), {}, is_delegated=False) == 120.0


def test_an_unreadable_knob_never_fails_the_tool_call() -> None:
    def angry(_key: str) -> Any:
        raise RuntimeError("no knob snapshot in this process")

    knobs_mod.configure_tool_dispatch_knobs(angry)
    assert _dispatch_timeout_seconds(_tool_def("rulebook"), {}, is_delegated=False) == 120.0


# ---------------------------------------------------------------------------
# 3. A timeout is honest, and a refusal reaches the person with its remedy
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_deadline_really_cancels_the_call() -> None:
    """The dispatch is bounded by the resolved ceiling, knob and all."""
    tool_def = _tool_def("workflow_plan", timeout_seconds=0.05)

    async def never_finishes(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
        await asyncio.sleep(10)
        raise AssertionError("unreachable — the deadline arrives first")

    tool_def._callable = never_finishes
    dispatch_timeout = _dispatch_timeout_seconds(tool_def, {}, is_delegated=False)
    assert dispatch_timeout == 0.05

    with pytest.raises(TimeoutError):
        await asyncio.wait_for(
            _executor()._dispatch(tool_def, {}, _ctx(), _SilentStream()),
            timeout=dispatch_timeout,
        )


def test_a_timeout_names_the_work_and_what_to_retry() -> None:
    """THE envelope the executor's timeout branch returns — the real function,
    driven directly (never `inspect.getsource`, which can read a different
    function than it names when a concurrent commit lands mid-run)."""
    error = timeout_tool_error(
        tool_name="workflow_plan",
        dispatch_timeout=120.0,
        user_message='building "Writer (v2026-09-12T2215)"',
    )

    assert error.error_type == "timeout"
    assert error.is_retryable is True
    # What it was doing, and that nothing unfinished was written.
    assert 'building "Writer (v2026-09-12T2215)"' in error.message
    assert "The call was cancelled and its work abandoned" in error.message
    assert "nothing it had not already finished was written" in error.message
    # The ceiling is a knob an admin can raise, and this is NOT a refusal.
    assert error.suggested_action is not None
    assert "agents.tool_dispatch" in error.suggested_action
    assert "default_timeout_seconds" in error.suggested_action
    assert "it is not a refusal of the request" in error.suggested_action
    # The old advice, which is what made a ceiling read as a rejected request.
    assert "different parameters" not in (error.suggested_action or "")


def test_the_provenance_refusal_carries_its_cause_and_remedy() -> None:
    remedy = error_remedy_for(LIVE_REFUSAL)
    assert remedy is UNDECLARED_ACTOR_SYSTEM

    envelope = remedy.prefix(LIVE_REFUSAL)
    # What the Conductor got wrong, said right — and the raw text still there.
    assert "PLATFORM DEFECT" in envelope
    assert "no approval, human channel or extra authorization is required" in envelope
    assert "Retry the identical call once" in remedy.remedy
    assert LIVE_REFUSAL in envelope


def test_an_ordinary_failure_gets_no_invented_diagnosis() -> None:
    assert error_remedy_for("Plan 1c45a4a4 not found.") is None
    assert error_remedy_for(None) is None


def test_the_classifier_reads_the_bounded_text_never_the_payload() -> None:
    """A caller's own document must not be able to trip the ladder
    (``matrx_utils.error_text.classification_text``)."""
    payload_says_it = (
        "Database integrity error: duplicate key value violates unique constraint\n"
        "Args: ['the complaint alleges the app.actor_system GUC names no actor_system']"
    )
    assert error_remedy_for(payload_says_it) is None
