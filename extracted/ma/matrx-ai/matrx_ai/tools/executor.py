from __future__ import annotations

import asyncio
import difflib
import json
import logging
import time
import traceback as tb
from collections.abc import Awaitable, Iterable, Sequence
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any, get_args
from uuid import uuid4

from matrx_utils import detached_task, vcprint
from pydantic import BaseModel, ValidationError
from pydantic_core.core_schema import ErrorType

from ._db_log import db_log_event as _db_log
from ._debug_log import is_verbose as _debug_verbose
from ._debug_log import log_event as _debug_log
from .error_remedy import annotate_tool_error, known_outcome_notices
from .guardrails import GuardrailEngine
from .knobs import (
    delegated_call_abandon_seconds,
    dispatch_timeout_ceiling,
    process_tool_deadline_grace_seconds,
)
from .lifecycle import ToolLifecycleManager
from .logger import ToolExecutionLogger
from .models import ToolContext, ToolDefinition, ToolError, ToolResult, ToolType
from .registry import ToolRegistry
from .result_gate import apply_size_gate_async, tool_kind_label
from .streaming import ToolStreamManager

logger = logging.getLogger(__name__)

TOOL_INPUT_CONTRACT_DRIFT_KIND = "tool_input_contract_drift"
TOOL_OUTPUT_CONTRACT_DRIFT_KIND = "tool_output_contract_drift"
CONTEXT_PATCH_NO_MATCH_KIND = "context_patch_no_match"
TOOL_EXECUTION_FAILED_KIND = "tool_execution_failed"
TOOL_RESULT_KIND_MISSING_KIND = "tool_result_kind_missing"
TOOL_RESULT_KIND_UNAVAILABLE_KIND = "tool_result_kind_unavailable"
TOOL_RESULT_SIZE_UNMANAGED_KIND = "tool_result_size_unmanaged"
TOOL_BATCH_CANCELLED_KIND = "tool_batch_cancelled"

# These tools validate a caller-selected process deadline themselves. The
# executor's registry default is a dispatch fallback, not a second shorter
# process limit: otherwise a valid 121–300s shell request is canceled before
# its own implementation can enforce the declared deadline.
_CALLER_BOUNDED_PROCESS_TOOLS = frozenset({"shell_execute", "shell_python"})
#: Seconds the dispatch deadline of a caller-bounded process tool waits PAST the timeout the
#: caller asked for. Equal deadlines raced: a 120s (or 300s) request was canceled at exactly
#: 120s (300s) by this executor before the box's own timeout answer could arrive, so the agent
#: got "canceled, work abandoned" instead of the command's exit code and output so far
#: (tool_execution_failed, 2026-11-18). A knob: ``agents.tool_dispatch.process_tool_deadline_grace_seconds``
#: (``matrx_ai.tools.knobs.process_tool_deadline_grace_seconds``, always above the transport grace).

# These are terminal facts about a Cloud Browser session, not failures of the
# executor.  The next model turn can start/attach a fresh session; an ERROR
# log or ``tool_execution_failed`` record would instead page operations for a
# normal lifecycle race.  Keep real worker reachability and command failures
# outside this set so they still scream and capture exactly once.
_CLOUD_BROWSER_EXPECTED_LIFECYCLE_OUTCOMES = frozenset(
    {
        "run_state_conflict",
        "worker_shutting_down",
        "unknown_page",
        # "This browser is still starting. Retry this same action in a few seconds": the typed,
        # retryable answer while a session activates (cloud_browser/errors.py); the model retries
        # it on its next step. Filed as a tool_execution_failed system_error 2026-11-16.
        "activation_in_progress",
        # The person's own state, not a platform fault (live 2026-11-16 guided-setup rows): someone else is
        # driving this browser right now (the model waits or asks), and this person has no Cloud Computer
        # yet (the refusal carries the set-up link; cloud_browser/errors.py). A worker that cannot be reached
        # or an action that failed stays filed.
        "controlled_by_other",
        "cloud_computer_required",
        # The person's own browser is open on another of their Cloud Computers (manager.py
        # ``_require_same_machine``): the sentence tells them to close it there. Filed as
        # tool_execution_failed until 2026-11-21 (a64d4454, 78461556).
        "browser_open_on_other_machine",
    }
)


#: The fixed sentence the browser readiness pre-gate answers when a selector matches nothing.
_CLOUD_BROWSER_SELECTOR_ABSENT_PREFIX = "Nothing on this page matches "


def _candidate_stopped_content(result: ToolResult, stop: dict[str, Any]) -> dict[str, Any]:
    """The content slot for a candidate-stopped call.

    It exists only because ``execute`` returns a pair; it is NEVER a tool result
    for the model — ``handle_tool_calls_v2`` drops every ``candidate_stopped``
    call and the orchestrator ends the run. The flag rides the dict too, so any
    other caller that reads only the content can still tell.
    """
    return {
        "tool_use_id": result.call_id,
        "call_id": result.call_id,
        "name": result.tool_name,
        "content": "",
        "is_error": False,
        "candidate_stopped": True,
        "stopped_at": stop,
    }


def _dispatch_timeout_seconds(
    tool_def: ToolDefinition,
    arguments: dict[str, Any],
    *,
    is_delegated: bool,
) -> float:
    """Return the executor deadline without undercutting process-tool input contracts.

    A tool row that declares its own ``guardrail_config.timeout_seconds`` keeps it.
    Everything else resolves the ceiling from ``platform.feature_knob``
    (``agents.tool_dispatch``) — the limit is a knob an admin turns, never the
    literal that killed the Conductor's ``workflow_plan build_agent`` at 120s
    (2026-09-12). See ``matrx_ai.tools.knobs``.
    """
    if is_delegated:
        return _DELEGATED_DISPATCH_TIMEOUT_SECONDS

    configured_timeout = (
        float(tool_def.timeout_seconds)
        if tool_def.timeout_seconds is not None
        else dispatch_timeout_ceiling(tool_def.name)
    )
    if tool_def.name not in _CALLER_BOUNDED_PROCESS_TOOLS:
        return configured_timeout

    requested_timeout = arguments.get("timeout_seconds")
    if not isinstance(requested_timeout, (int, float)) or isinstance(requested_timeout, bool):
        return configured_timeout
    return max(configured_timeout, float(requested_timeout) + process_tool_deadline_grace_seconds())


def _timeout_safe_to_repeat(tool_def: Any) -> bool:
    from matrx_ai.tools.mcp_resilience import safe_to_repeat

    if getattr(tool_def, "tool_type", None) == ToolType.EXTERNAL_MCP:
        return safe_to_repeat(tool_def)
    return not getattr(tool_def, "annotations", None) or safe_to_repeat(tool_def)


def timeout_tool_error(
    *,
    tool_name: str,
    dispatch_timeout: float,
    user_message: str,
    safe_to_repeat: bool = True,
    exc: BaseException | None = None,
) -> ToolError:
    """THE HONEST TIMEOUT (2026-09-12).

    The Conductor's `workflow_plan build_agent` died on "timed out after 120s"
    with no word of what it had been doing, so neither the agent nor the Expert
    could tell whether the agent it was building now half-existed — and the
    generic "try with different parameters" that rode with it reads as a refusal
    of the request. So the envelope names the work, says the call was canceled
    and nothing unfinished was written, and names the ceiling as the knob an
    admin can raise. A function, not an inline literal, so a test can drive the
    real envelope instead of reading the executor's source.
    """
    return ToolError.declared(
        exc=exc,
        reported_failure=None if exc is not None else f"the {dispatch_timeout:.0f}s dispatch ceiling",
        error_type="timeout",
        message=(
            f"Tool '{tool_name}' timed out after {dispatch_timeout:.0f}s "
            f"while: {user_message}. The call was canceled and its work "
            "abandoned — nothing it had not already finished was written."
        ),
        is_retryable=safe_to_repeat,
        suggested_action=(
            ("Retry the same call (it is safe to repeat), or break the work into " if safe_to_repeat else
             "Do NOT simply repeat it: it may already have been done on the other side. Check whether it was, "
             "then repeat only what is missing, or break the work into ")
            + "smaller steps. If this tool legitimately needs longer, the ceiling is "
            "the platform.feature_knob 'agents.tool_dispatch' "
            "(default_timeout_seconds / per_tool_timeout_seconds) an admin can "
            "raise — it is not a refusal of the request."
        ),
    )


#: The records store's DELIBERATE refusals, by SQLSTATE (matrx_records.errors names each):
#: a stale write, a missing argument, a malformed payload, a wall (check), a duplicate, the
#: store's own raise and a row that is not there. The ``records*`` tools carry them as
#: ``store_<sqlstate>`` with the store's sentence, so the model can fix its call — they are
#: never an operational fault. A lock collision (55P03), an aborted transaction (25P02) or any
#: other code stays a fault. 2026-11-04: 78 open rows were these refusals, e.g. "You already
#: have a column called \"Patient\"." (store_23505).
#: ``22P02`` (a value that is not the column's type, e.g. "`records[0].to` must be an id such as …") and
#: ``23503`` (a reference to a row that is not there, e.g. "There is no such form in this organization.")
#: are the caller's own values too: 3 records rows 2026-11-16/17 were these.
_STORE_REFUSAL_SQLSTATES = frozenset({"PT409", "02000", "22004", "22023", "22P02", "23514", "23503", "23505", "P0001"})
#: ``42501`` is the store's door refusing this reader ("You do not have access to this
#: record.") — unless Postgres itself worded it "permission denied for <object>", which is a
#: connection carrying the wrong role: a fault (matrx_records.errors.is_deliberate_unavailability).
_STORE_DOOR_CLOSED = "42501"


def _is_store_refusal(error_type: str, message: str | None) -> bool:
    if not error_type.startswith("store_"):
        return False
    sqlstate = error_type[len("store_"):].upper()
    if sqlstate in _STORE_REFUSAL_SQLSTATES:
        return True
    if sqlstate == _STORE_DOOR_CLOSED:
        return not (message or "").strip().lower().startswith("permission denied")
    return False


def _missing_traceback_line(tool_name: str, error: Any, *, expected: bool) -> str:
    """The failure banner's traceback line when the error carries no stack.

    An expected domain conflict and a declared refusal (``ToolError.refusal``) never had an
    exception, so the banner says that. Anything else with no stack is named as the tool's
    defect: it caught an exception and stringified it (PB-08 B10 kept that claim off a deliberate
    refusal, app_log c7500692)."""
    if expected:
        return (
            "  traceback:  <not applicable — expected domain conflict; "
            "handled by the tool's expected-domain-failure contract.>"
        )
    reported = getattr(error, "reported_failure", None)
    if reported:
        return (
            f"  traceback:  <none — the tool reported a failure from {reported}; "
            "no Python exception was raised.>"
        )
    if getattr(error, "refusal", False):
        return (
            "  traceback:  <not applicable — a refusal by the tool (the caller's input, a "
            "permission, an absent record or a policy); no exception was raised.>"
        )
    return (
        "  traceback:  <none — the tool swallowed its exception and "
        f"stringified it. Fix '{tool_name}' to let the exception reach the "
        "executor, or set ToolError.traceback.>"
    )


def _is_expected_domain_failure(*, tool_name: str, error_type: str, message: str | None = None) -> bool:
    """Return true for deliberate tool refusals that are not operational errors."""
    if _is_store_refusal(error_type, message):
        return True
    from matrx_ai.providers.caller_refusal import EXPECTED_HOLD_CODES

    # A run held by a limit or approval someone set (agent_call / mandate_call carry the child's
    # hold code): expected, with its own human path, never a tool failure.
    if error_type in EXPECTED_HOLD_CODES:
        return True
    normalized_error_type = error_type.lower()
    if normalized_error_type in {
        "auth_required",
        "invalid_arguments",
        "missing_context",
        "not_allowed",
        "not_found",
        "validation",
        # The on-screen write guard (on_screen_write_guard.py): a deliberate
        # refusal that names the right door, never an operational error.
        "record_on_screen",
        "person_declined_this_change",
        # A store/service refusal in its own words (tables_*, drill, attention,
        # spend desk): the caller's arguments were wrong and the sentence says
        # how — the agent's to fix, never an operational error.
        "refused",
        # NOT "recursion_limit": the agent nesting limit stays a red failure (owner ruling
        # 2026-11-08; guard test_a_nesting_refusal_is_never_called_a_swallowed_exception).
        # A tool the server added read-only for this run refusing a write in words
        # (scope_system: "read-only in this run … Nothing was written").
        "read_only",
        # A client-delegated tool (matrx-desktop) refusing the model's arguments.
        "invalid_params",
        # A tool refusing an actor its own policy does not admit (kindcomp_patch_code).
        "forbidden",
        # The same refusal under its other name: a tool or Action whose own policy does not let this
        # caller do this, answered with what to do instead (mail agent_gate "An agent may send mail
        # only from a named inbox it can open", via actions_run, filed 2026-11-18). A database fault
        # is typed ``database`` / ``execution`` by its tool, never ``permission``, and stays filed.
        "permission",
        # A child agent call with no message (agents/child_turn.py): nothing ran, nothing was
        # spent, and the sentence tells the calling model what to send (PB-03 r2/r3, 2026-11-08).
        "missing_user_input",
        # A child agent refused because the caller left a declared-required input empty
        # (agents/required_variables.py): nothing ran, and the sentence names the inputs.
        "required_variables_missing",
        # The person's own setup, not a fault: a computer tool with no computer connected to
        # this chat (desktop.py ``_no_computer``), and memory asked for inside a temporary chat
        # (memory.py ``person_memory_off``). The sentence tells the model what to tell them.
        "no_computer",
        "person_memory_off",
        # A person's own connector that is not connected yet (cerbo.py ``cerbo_not_connected``,
        # connection_tools.py): the sentence tells the model to send them to Settings → Connectors.
        "not_connected",
        # The same for a chat bundle loaded through use_tool (tool_catalog/discovery.py
        # ``bundle_not_connected``: "The person has not connected Linear…"), filed until 2026-11-20.
        "bundle_not_connected",
        # The database refused the caller's own values — a check/foreign-key/unique/not-null
        # violation or bad enum text (db_hints.is_constraint_refusal). The refusal sentence
        # names the allowed values; the model corrects it on its next step.
        "constraint_violation",
        # A person's own MCP connection credential refused on discovery (401/403): the model tells
        # them to reconnect (bundle_lister.py). A 5xx / network failure stays ``mcp_no_tools``, filed.
        "mcp_unauthorized",
        # A person's own connector credential refused by the provider (cerbo ``cerbo_keys_refused``,
        # graph_actions/cerbo.py): the sentence sends them to reconnect in Settings → Connectors.
        # Cerbo unreachable or failing on its side stays ``execution``, filed (live 2026-11-13).
        "connection_credentials_refused",
        # A paid call refused at zero cost by the caller's OWN spend arguments (aidream spend desk,
        # action_requests/spend_ask.py): the estimate is above the max_cost_usd the model passed, or
        # the spend_approval_id it passed was not issued to this caller. The sentence names the value
        # to send (four seo_domain rows filed 2026-11-21). ``configuration`` stays filed.
        "over_max_cost",
        "spend_approval_not_yours",
        # An optimistic edit whose anchor text matched nowhere or in several places (fs_edit,
        # notes, CMS, kind components, context_patch, db patch): nothing was written and the
        # sentence names the lines; the model re-reads and re-anchors. Filed for fs_edit as
        # tool_execution_failed until 2026-11-21 (fa3b500f). context_patch keeps its own
        # context_patch_no_match capture, which does not read this set.
        "patch_no_match",
        "patch_ambiguous",
    } or normalized_error_type.endswith("_not_found"):
        return True
    if tool_name == "cloud_browser" and error_type in _CLOUD_BROWSER_EXPECTED_LIFECYCLE_OUTCOMES:
        return True
    # A selector the readiness pre-gate positively found absent (matrx_scraper ai_browser/actions.py
    # ``_UNUSABLE_TARGET_MESSAGE["absent"]``): the model aimed at nothing and picks another selector
    # (filed as system errors until 2026-11-19, guided-setup). Every other action failure stays filed.
    if (
        tool_name == "cloud_browser"
        and error_type == "browser_action_failed"
        and (message or "").startswith(_CLOUD_BROWSER_SELECTOR_ABSENT_PREFIX)
    ):
        return True
    return (tool_name, error_type) in {
        ("code_execute_python", "python_error"),
        ("context", "context_not_attached"),
        # The model's ask payload missing a field of its kind (action_requests.payload_refusal): the
        # refusal names the field and an example, nothing was sent (live 2026-11-09). ``configuration``
        # (ask_person offered where it cannot park) stays filed: that is the platform's wiring.
        ("ask_person", "payload_invalid"),
        ("context", "context_create_disabled"),
        ("shell_execute", "exit_code"),
        ("shell_python", "exit_code"),
        # The sql tool and its read-only sibling refusing a schema/relation that is not application
        # data, a credential table, or a privilege / RLS denial (42501) — by design, answered to
        # the model with guidance (db_read's were filed as system_errors until 2026-11-17).
        ("sql", "permission"),
        ("db_read", "permission"),
        # The background-helper cap (agent_harness/children.py ``_background_cap_refusal``): a limit by
        # design whose sentence tells the model to wait or task_stop one; the sealed real test expects
        # starts past the cap to end here (filed as system errors until 2026-11-19).
        ("agent", "limit_reached"),
        ("send_message", "limit_reached"),
        # A wake-up refused by its own limits (agent_harness/wakeups.py ``schedule``: too far ahead,
        # unclear time, bad repeat, daily budget, pending cap): each sentence tells the model what to do
        # instead (filed as system errors until 2026-11-19, a voice agent asking for 2028).
        ("schedule_wakeup", "limit_reached"),
        # git_ingest given a folder path while the turn is bound to a box (code_ingest.py): the tool runs
        # on the server and cannot see the box's disk; the sentence sends the model to fs_* / shell
        # (filed as tool_execution_failed until 2026-11-21, 662ec5a4).
        ("git_ingest", "local_path_on_bound_box"),
    }


async def _capture_context_patch_no_match(*, ctx: ToolContext) -> None:
    """Capture a failed optimistic context edit without retaining document text."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError("Context patch could not find its requested anchor")
    await capture_error(
        exc,
        kind=CONTEXT_PATCH_NO_MATCH_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.context_patch",
        error_type="PatchNoMatch",
        context={"tool_name": "context_patch", "call_id": ctx.call_id, "retryable": True},
    )


def _note_tool_argument_refusal(
    *,
    ctx: ToolContext,
    tool_name: str,
    validation_error: ValidationError,
) -> None:
    """A refused tool call is the MODEL's mistake, never a platform error.

    The refusal goes back to the model as a normal tool result it corrects on its
    next step (PB-08, 2026-10-19: the lead left out ``agent_id``, was refused, and
    called again correctly 1 s later — and the same refusal was ALSO filed as a
    system_error, paging operations for a mistake the loop had already handled).
    So: one WARNING line naming the tool and the pydantic error CODES, never what
    the model sent, and nothing on the errors surface. A server fault behind a
    tool still files ``tool_execution_failed`` from the dispatch path.
    Guard: tools/tests/test_a_model_correctable_refusal_is_never_a_platform_error.py.
    """
    allowed_codes = frozenset(get_args(ErrorType))
    errors = validation_error.errors(include_url=False, include_context=False, include_input=False)
    codes = sorted(
        {e["type"] if e["type"] in allowed_codes else "custom_validation" for e in errors}
    )
    vcprint(
        f"[ToolExecutor] {tool_name} call refused for its arguments (the model corrects it): "
        f"{validation_error.error_count()} error(s), codes {codes[:20]}, call {ctx.call_id}",
        color="yellow",
    )


def typed_result_inside_preview_envelope(output: Any) -> dict[str, Any] | None:
    """The typed result a preview envelope carries, or None when ``output`` is not one.

    ``kind_component._with_auto_preview`` hands a save back in one of two envelopes so the
    model sees its screenshots: an ``image_ref_list`` whose ``details.save`` is the save, or
    ``{"save": <save>, "preview": <findings>}``. The save is the result the tool's contracts
    describe; the envelope is transport. Only a ``save`` that is itself an object counts.
    """
    if not isinstance(output, dict):
        return None
    if output.get("kind") == "image_ref_list" and isinstance(output.get("items"), list):
        details = output.get("details")
        save = details.get("save") if isinstance(details, dict) else None
        return save if isinstance(save, dict) else None
    if set(output) == {"save", "preview"} and isinstance(output["save"], dict):
        return output["save"]
    return None


def arguments_as_meant(arguments: dict[str, Any], args_model: Any) -> dict[str, Any] | None:
    """The arguments as the tool's own input model reads them, or ``None`` when it refuses them.

    A tool whose input model repairs a call before the body runs (ask_person's ``repair_ask``:
    an empty ``message`` is filled from the first question) runs the REPAIRED arguments. The
    Content IR shadow check judges what the tool ran, so a call the model's own repair settled
    is the model's mistake corrected by the tool's declared repair — never contract drift
    (live 2026-11-14: ask_person with ``message: ''`` filed tool_input_contract_drift four
    times while the tool accepted the repaired call). Only fields the model set (or the repair
    filled) are kept, so defaults the model never sent do not change the verdict.
    """
    if args_model is None or not hasattr(args_model, "model_validate"):
        return None
    # Only a DECLARED repair (a ``mode="before"`` model validator) counts: a model that merely
    # ignores a key the contract forbids is still drift (contract and code disagree).
    decorators = getattr(args_model, "__pydantic_decorators__", None)
    validators = getattr(decorators, "model_validators", {}) or {}
    if not any(getattr(getattr(d, "info", None), "mode", None) == "before" for d in validators.values()):
        return None
    try:
        parsed = args_model.model_validate(arguments or {})
        meant = parsed.model_dump(mode="json", exclude_unset=True)
    except Exception:  # noqa: BLE001 — a refused call keeps the raw verdict
        return None
    return meant if isinstance(meant, dict) else None


async def _capture_tool_input_contract_drift(
    *,
    ctx: ToolContext,
    tool_name: str,
    input_kind: str,
    error_count: int,
    errors: Sequence[str] = (),
) -> None:
    """Durably capture a shadow-contract mismatch without retaining tool input."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError(
        f"Tool input disagreed with its Content IR contract: {tool_name} "
        f"({error_count} validation error(s))"
    )
    await capture_error(
        exc,
        kind=TOOL_INPUT_CONTRACT_DRIFT_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.content_ir_input",
        error_type="ToolInputContractDrift",
        context={
            "tool_name": tool_name,
            "input_kind": input_kind,
            "error_count": error_count,
            # Which field disagreed: the validator's own sentences (path + rule), capped.
            "validation_errors": [str(e)[:200] for e in list(errors)[:5]],
        },
    )


#: Status receipts a catalog Tool hands back INSTEAD of its answer (nothing found, still
#: running, awaiting approval). They are successful calls whose payload is, by design, not
#: the Tool's success shape; each validates against its own registered kind.
CATALOG_STATUS_RECEIPT_KINDS = frozenset(
    {"catalog_tool_empty", "catalog_tool_pending", "catalog_tool_approval"}
)


def is_catalog_status_receipt(curated_kind: str | None, drift_sources: Sequence[str]) -> bool:
    """True when a result is a catalog status receipt that passed its OWN kind check.

    Judging it against the Tool's success-output schema filed a false drift row for
    every empty/pending catalog call (``current_time_in_zone``, 2026-11-15).
    """
    return curated_kind in CATALOG_STATUS_RECEIPT_KINDS and "declared_kind" not in drift_sources


async def _capture_tool_output_contract_drift(
    *,
    ctx: ToolContext,
    tool_name: str,
    output_kind: str,
    error_count: int,
    validation_sources: tuple[str, ...],
    errors: Sequence[str] = (),
) -> None:
    """Durably capture a successful result that violates its output contract."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError(
        f"Tool output disagreed with its Content IR contract: {tool_name} "
        f"({error_count} validation error(s))"
    )
    await capture_error(
        exc,
        kind=TOOL_OUTPUT_CONTRACT_DRIFT_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.content_ir_output",
        error_type="ToolOutputContractDrift",
        context={
            "tool_name": tool_name,
            "output_kind": output_kind,
            "error_count": error_count,
            "validation_sources": list(validation_sources),
            "validation_errors": [str(e)[:200] for e in list(errors)[:5]],
        },
    )


async def _capture_tool_result_kind_missing(
    *, ctx: ToolContext, tool_name: str, output_kind: str
) -> None:
    """Capture a successful declared-kind result that omitted its discriminator."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        RuntimeError(f"Declared tool result kind was missing: {tool_name}"),
        kind=TOOL_RESULT_KIND_MISSING_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.content_ir_output",
        error_type="ToolResultKindMissing",
        context={"tool_name": tool_name, "output_kind": output_kind},
    )


async def _capture_tool_result_kind_unavailable(
    *, ctx: ToolContext, tool_name: str, output_kind: str, degraded_reason: str
) -> None:
    """Capture a successful kinded result whose registry contract was unavailable."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        RuntimeError(f"Declared tool result kind was unavailable: {tool_name}"),
        kind=TOOL_RESULT_KIND_UNAVAILABLE_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.content_ir_output",
        error_type="ToolResultKindUnavailable",
        context={
            "tool_name": tool_name,
            "output_kind": output_kind,
            "degraded_reason": degraded_reason,
        },
    )


# ---------------------------------------------------------------------------
# Watch AI raw capture (matrx_utils.raw_capture) — the RAW tier and cut trail of one tool call.
# ---------------------------------------------------------------------------


def _content_chars(content: Any) -> int:
    if content is None:
        return 0
    if isinstance(content, str):
        return len(content)
    try:
        return len(json.dumps(content, ensure_ascii=False, default=str))
    except (TypeError, ValueError):
        return len(str(content))


def _note_gate_cut(before: Any, after: Any, *, truncated: bool) -> None:
    """The size gate's cut on the call's capture scope, plus what was sent. Never raises."""
    from matrx_utils import raw_capture

    scope = raw_capture.current_scope()
    if scope is None:
        return
    try:
        sent = _content_chars(after)
        scope.facts["sent_chars"] = sent
        scope.facts["gate_truncated"] = bool(truncated)
        if truncated:
            from .output_caps import TOOL_RESULT_SOFT_CAP_CHARS

            raw_capture.record_cut(
                where="size gate",
                before=_content_chars(before),
                after=sent,
                limit_name="TOOL_RESULT_SOFT_CAP_CHARS",
                limit=TOOL_RESULT_SOFT_CAP_CHARS,
                original=before if isinstance(before, str) else None,
            )
    except Exception as exc:  # noqa: BLE001 — watching never changes the call
        logger.warning("[ToolExecutor] raw capture: gate cut not recorded (%s: %s)", type(exc).__name__, exc)


def tool_capture_facts(result: ToolResult, scope: Any) -> None:
    """Fill ``scope`` with the call's own sizes and its whole result when anything was cut.

    RAW for a tool call is what its source returned: a transport body a feeder recorded, the pre-cut
    value a cut primitive kept, or — when no cut happened at all — the stored ``chat.tool_call.output``
    itself (a pointer, nothing copied). When the result was shortened for storage (100,000 chars) or
    by the size gate, the whole result is kept as its own raw item."""
    from matrx_utils import raw_capture

    if result.output is None:
        full, output_type = "", "text"
    else:
        from .models import tool_output_text

        full, output_type = tool_output_text(result.output)
    limit = ToolExecutionLogger._MAX_OUTPUT_CHARS
    scope.facts.update(
        {
            "tool_name": result.tool_name,
            "success": bool(result.success),
            "result_chars": len(full),
            "stored_chars": min(len(full), limit),
            "output_self_capped": bool(result.output_self_capped),
        }
    )
    stored_cut = len(full) > limit
    if stored_cut:
        scope.cuts.append(
            raw_capture.CutRecord(
                where="storage (chat.tool_call.output)",
                before=len(full),
                after=limit,
                limit_name="ToolExecutionLogger._MAX_OUTPUT_CHARS",
                limit=limit,
            )
        )
    gate_cut = bool(scope.facts.get("gate_truncated"))
    if stored_cut or gate_cut:
        scope.items.append(
            raw_capture.RawItem(
                label="Tool result as returned",
                source="tool_result",
                data=full.encode("utf-8"),
                content_type="application/json" if output_type == "json" else "text/plain; charset=utf-8",
            )
        )
    else:
        scope.items.append(
            raw_capture.RawItem(
                label="Tool result as returned",
                source="tool_result",
                ref={"table": "chat.tool_call", "column": "output", "chars": len(full)},
            )
        )



async def _capture_tool_result_size_unmanaged(*, ctx: ToolContext, tool_name: str) -> None:
    """Capture an owned tool that reached the universal blunt size gate."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        RuntimeError(f"Owned tool result exceeded its unmanaged size limit: {tool_name}"),
        kind=TOOL_RESULT_SIZE_UNMANAGED_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.result_gate",
        error_type="ToolResultSizeUnmanaged",
        context={"tool_name": tool_name, "call_id": ctx.call_id},
    )


_CAPTURED_FAILURE_MESSAGE_CHARS = 1000


async def _capture_tool_execution_failed(
    *,
    ctx: ToolContext,
    tool_name: str,
    error_type: str,
    message: str | None = None,
    traceback_text: str | None = None,
) -> None:
    """Capture an unexpected failed tool result: the tool's own error sentence and traceback,
    never its args or output. A row that only said "Tool execution failed: <tool>" left every
    triage to a join against chat.tool_call (28 tables_automation rows, 2026-11-02)."""
    from matrx_connect.streaming.error_capture import capture_error

    said = (message or "").strip()[:_CAPTURED_FAILURE_MESSAGE_CHARS] or "no error message"
    await capture_error(
        RuntimeError(f"Tool execution failed: {tool_name} ({error_type}): {said}"),
        kind=TOOL_EXECUTION_FAILED_KIND,
        traceback_text=traceback_text or None,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.execution",
        error_type=error_type,
        context={"tool_name": tool_name, "call_id": ctx.call_id},
    )


# ── Client-delegated tool timing — the canonical durable contract ──────────────
# These two numbers govern client delegation and are the SINGLE SOURCE OF TRUTH;
# no UI surface defines its own answer deadline. A delegated call's honest state
# is ``cx_tool_call.status='delegated'`` + ``cx_user_request.status='paused'`` —
# a user may sit in it for seconds, minutes, hours, or weeks, and the platform
# does NOT try to control that. The only role of a timeout here is far-future
# cleanup of genuinely-abandoned conversations; a late answer ALWAYS resumes
# (see ``submit_tool_results``' timeout_sweep supersession).
#
# DELEGATED_CALL_ABANDON_AFTER_SECONDS — the durable ledger TTL stamped on
#   ``cx_tool_call.expires_at``. The lifecycle sweep flips a row past this to a
#   timeout terminal state purely so an abandoned conversation doesn't keep a
#   'delegated' row outstanding forever. It is NOT a user-facing answer deadline.
#   Override per-tool via the ``tools.max_client_wait_seconds`` column when a
#   specific tool legitimately needs a tighter bound.
# The live window is ``persistence.paused_request_abandon_days`` (tools/knobs.py
# ``delegated_call_abandon_seconds``); this constant is only its 30-day standalone mirror.
DELEGATED_CALL_ABANDON_AFTER_SECONDS: int = 30 * 24 * 60 * 60  # 30 days

# _DELEGATED_DISPATCH_TIMEOUT_SECONDS — pure HANG-backstop for the delegated
#   DISPATCH itself (queue the 'delegated' UPDATE + ``coordinator.finalize()`` +
#   ``tool_delegated`` emit). It returns in milliseconds normally and NEVER waits
#   for the user. It must sit comfortably ABOVE ``finalize()``'s own internal
#   worst case — ``finalize`` drains each in-flight commit serially at
#   ``_DRAIN_TIMEOUT_SECONDS`` (30s) plus a ``_COMMIT_HARD_DEADLINE_SECONDS``
#   (60s) current flush, so a slow-but-SUCCESSFUL finalize must not be killed
#   here (that would overwrite the durable 'delegated' row with an error and
#   reopen the delegation loop). 1h matches the prior known-good value; it only
#   ever fires if the emit/commit genuinely deadlocks. DECOUPLED from the
#   abandonment TTL so a long per-tool wait can never hold the request task open.
_DELEGATED_DISPATCH_TIMEOUT_SECONDS: float = 60.0 * 60.0  # 1 hour
# A held stream's wait (tools/delegated_hold.py) runs INSIDE this dispatch, so it must end before the
# backstop does: the margin is finalize()'s own worst case above (30 s drain + 60 s flush) with room.
_DELEGATED_HOLD_BACKSTOP_MARGIN_SECONDS: float = 5 * 60.0  # protocol-constant: derived invariant, finalize()'s worst case (30 s drain + 60 s flush) with room; a smaller value lets the backstop cut a held wait mid-finalize

# ── Unknown-tool hint bounds — always on, tune here (never a flag) ─────────────
# The db_hints pattern applied to tool names: a miss returns did-you-mean +
# a bounded option list, never an unbounded registry dump (context bloat).
UNKNOWN_TOOL_LIST_CAP = 25  # max tool names listed in the error message
_CONFIDENT_SUGGESTION_RATIO = 0.85  # difflib ratio for a "Retry with tool 'X'" action


async def _await_must_complete(
    operation: Awaitable[ToolResult],
    *,
    timeout_seconds: float,
    stream: ToolStreamManager,
    tool_name: str,
) -> tuple[ToolResult, asyncio.CancelledError | None]:
    task = asyncio.create_task(operation, name=f"must_complete_tool:{tool_name}")
    cancellation: asyncio.CancelledError | None = None
    try:
        result = await asyncio.wait_for(
            asyncio.shield(task),
            timeout=timeout_seconds,
        )
        return result, None
    except TimeoutError:
        vcprint(
            f"[ToolExecutor] Tool '{tool_name}' crossed its {timeout_seconds:.0f}s "
            "soft timeout, but must_complete=True — waiting for the real result. "
            "The execution was NOT canceled and MUST NOT be retried.",
            color="yellow",
        )
        detached_task(
            stream.progress(
                "Still running — this paid operation will continue until the "
                "provider returns a terminal result.",
                data={
                    "soft_timeout_seconds": timeout_seconds,
                    "must_complete": True,
                    "retry_allowed": False,
                },
            ),
            name=f"must_complete_progress:{tool_name}",
        )
    except asyncio.CancelledError as exc:
        if task.done():
            return task.result(), None
        cancellation = exc
        vcprint(
            f"[ToolExecutor] Cancellation reached must-complete tool '{tool_name}'. "
            "Finishing the in-flight operation before propagating cancellation.",
            color="yellow",
        )

    while True:
        try:
            result = await asyncio.shield(task)
            return result, cancellation
        except asyncio.CancelledError as exc:
            if task.done():
                return task.result(), cancellation
            cancellation = cancellation or exc
            vcprint(
                f"[ToolExecutor] Repeated cancellation ignored while must-complete "
                f"tool '{tool_name}' is still in flight.",
                color="red",
            )


def build_unknown_tool_hint(
    called: str,
    *,
    vocabulary: Iterable[str],
    active_tools: Iterable[str] | None = None,
    cap: int = UNKNOWN_TOOL_LIST_CAP,
) -> tuple[str, str]:
    """Build ``(message, suggested_action)`` for an unregistered tool name.

    Fuzzy-matches ``called`` against every internal name in ``vocabulary`` AND
    its wire spelling (``:`` → ``__`` — the model may only ever have seen wire
    names), mapping matches back to internal names. Lists ``active_tools``
    (bounded, closest-first) so the model has a real vocabulary to pick from.
    Pure function — unit-testable without an executor.
    """
    from matrx_utils import did_you_mean, format_options

    from matrx_ai.config.wire_names import to_wire_name

    # wire/internal spelling → internal name (identity for colon-free names).
    spelling_to_internal: dict[str, str] = {}
    for name in vocabulary:
        spelling_to_internal.setdefault(name, name)
        spelling_to_internal.setdefault(to_wire_name(name), name)

    matched_spellings = did_you_mean(called, spelling_to_internal.keys())
    # Present suggestions in WIRE form — that is the spelling the model saw
    # declared and the only one it should call (wire-name seam rules).
    suggestions: list[str] = []
    for spelling in matched_spellings:
        wire = to_wire_name(spelling_to_internal[spelling])
        if wire not in suggestions:
            suggestions.append(wire)

    lines = [f"Tool '{called}' is not registered."]
    confident: str | None = None
    if suggestions:
        if len(suggestions) == 1:
            lines.append(f"Did you mean '{suggestions[0]}'?")
        else:
            lines.append(f"Did you mean one of: {format_options(suggestions, 5)}?")
        top_ratio = difflib.SequenceMatcher(None, called, suggestions[0]).ratio()
        if len(suggestions) == 1 or top_ratio >= _CONFIDENT_SUGGESTION_RATIO:
            confident = suggestions[0]

    active = sorted({to_wire_name(n) for n in active_tools}) if active_tools is not None else []
    if active:
        # Closest-first so a truncated list still leads with the likely target.
        active.sort(
            key=lambda n: difflib.SequenceMatcher(None, called, n).ratio(),
            reverse=True,
        )
        lines.append(f"Available tools: {format_options(active, cap)}.")

    if confident:
        action = f"Retry with tool '{confident}'."
    elif active:
        action = "Pick a tool from the available list and retry with its exact name."
    else:
        action = "Check the tool name and try again. Use a valid tool from the available set."
    return " ".join(lines), action


async def warn_member_depth_exhausted(
    ctx: ToolContext, tool_def: ToolDefinition, tool_name: str
) -> None:
    """Emit a loud `member_depth_exhausted` warning for a depth-refused agent tool.

    D-39: a projected member refused at recursion depth is TRUNCATED DELEGATION —
    the calling orchestrator answers WITHOUT this member and may quietly absorb
    the refusal ToolResult. That result is the model's signal; this warning is
    the HUMAN's, so the truncation is never silent on the wire. Additive only —
    a failure to emit never breaks the run (it screams to the console instead).
    """
    try:
        emitter = ctx.emitter
        if emitter is None:
            return
        from matrx_connect.context.events import WarningPayload

        await emitter.send_warning(
            WarningPayload(
                code="member_depth_exhausted",
                system_message=(
                    f"Projected agent tool '{tool_name}' (agent "
                    f"{tool_def.prompt_id}) refused: agent-nesting depth "
                    f"{ctx.recursion_depth} has reached its ceiling of "
                    f"{tool_def.max_recursion_depth}."
                ),
                user_message=(
                    "A team member couldn't be called because the delegation "
                    f"chain is already {ctx.recursion_depth} levels deep "
                    f"(limit {tool_def.max_recursion_depth}). The answer may "
                    "be missing that member's contribution."
                ),
                level="medium",
                recoverable=True,
                metadata={
                    "tool_name": tool_name,
                    "agent_id": tool_def.prompt_id,
                    "depth": ctx.recursion_depth,
                    "ceiling": tool_def.max_recursion_depth,
                },
            )
        )
    except Exception as warn_exc:
        vcprint(
            f"[executor] member_depth_exhausted warning failed to emit: {warn_exc}",
            color="red",
        )


#: ``tool_step`` name that carries a notice the model was shown on a result.
MODEL_NOTICE_STEP = "model_notice"


def _chosen_variant_schema(tool_def: ToolDefinition, args: dict[str, Any]) -> dict[str, Any] | None:
    """The provider-dialect JSON Schema of the action ``args`` chose, or ``None``.

    ``None`` when the tool has no ``$variants``, no recognizable discriminator,
    or the call names no known action (the flattened check already refused an
    unknown action through the discriminator's enum).
    """
    discriminator = tool_def._variant_discriminator()
    if discriminator is None:
        return None
    variant = tool_def.parameters["$variants"].get(args.get(discriminator))
    if not isinstance(variant, dict):
        return None
    if isinstance(variant.get("properties"), dict):
        required = variant.get("required")
        action_def = ToolDefinition(
            name=tool_def.name,
            parameters=variant["properties"],
            required_params=[str(k) for k in required] if isinstance(required, list) else [],
        )
    else:
        action_def = ToolDefinition(name=tool_def.name, parameters=variant)
    schema = dict(action_def._build_json_schema())
    schema.pop("additionalProperties", None)
    return schema


def _validate_against_declared_schema(tool_def: ToolDefinition, args: dict[str, Any]) -> str | None:
    """Return a human-readable schema violation for ``args``, or ``None``.

    Uses the exact provider-facing JSON Schema the model was shown
    (``ToolDefinition._build_json_schema``), so "valid here" == "valid for
    the model" == "valid for the client dispatcher" — one contract.
    ``jsonschema`` is an optional dependency of matrx-ai (the host installs
    it); when it is absent this is a no-op, never a failure. Validation itself
    never raises: an unexpected schema shape is logged and treated as valid so
    a bad ROW can never block a tool call.
    """
    try:
        import jsonschema
    except Exception:
        return None
    try:
        # The CONTRACT shape: an envelope row's call has already been unwrapped to
        # the flat per-action form, which is what the full contract describes.
        schema = dict(tool_def._build_json_schema(contract=True))
        # Extra top-level keys are the CLIENT's call (zod objects strip unknown
        # keys; the alias recovery upstream already canonicalised the known
        # ones). This check exists to catch constraint violations the client
        # would REJECT — lengths, enums, ranges, required fields, item shapes —
        # not to add a stricter door than the client has.
        schema.pop("additionalProperties", None)
        validator_cls = jsonschema.validators.validator_for(schema)
        validator = validator_cls(schema)
        errors = sorted(validator.iter_errors(args or {}), key=lambda e: list(e.path))
        if not errors:
            # The flattened schema offers every action's choices (a shared
            # field carries their union), so it cannot see "valid for SOME
            # action but not this one" — local_media format=zip with
            # action=office_generate. The chosen action's own $variants
            # contract can; check it too, still without the extra-keys door.
            variant_schema = _chosen_variant_schema(tool_def, args or {})
            if variant_schema is not None:
                variant_validator = jsonschema.validators.validator_for(variant_schema)(
                    variant_schema
                )
                errors = sorted(
                    variant_validator.iter_errors(args or {}), key=lambda e: list(e.path)
                )
    except Exception as exc:  # a malformed declared schema must not block execution
        logger.warning(
            "[ToolExecutor] could not validate args for %r against its declared schema: %s",
            tool_def.name,
            exc,
        )
        return None
    if not errors:
        return None
    parts: list[str] = []
    for err in errors[:5]:
        path = ".".join(str(p) for p in err.absolute_path) or "<root>"
        parts.append(f"{path}: {err.message}")
    if len(errors) > 5:
        parts.append(f"(+{len(errors) - 5} more)")
    return "; ".join(parts)


#: Tools that REPORT state named sibling tools change, mapped to those tools. In a batch, a reporter
#: runs after its named siblings finish and never waits on any other call: real test PB-08k r19
#: (2026-11-09) emitted ``list_agents`` then ``task_stop`` in one batch, the two ran concurrently,
#: and the list read the helper ``running`` 1 ms before the stop landed. A long foreground agent
#: call in the same batch does not hold the list back. A host registers with
#: :func:`reads_after_its_batch`.
_READS_AFTER_ITS_BATCH: dict[str, frozenset[str]] = {}

#: Write tools whose calls in one batch each touch their own target, so they run side by side
#: instead of in emission order (``task_stop``: each stop waits for its own helper to wind down,
#: and N stops in one batch must not cost N waits). A host registers with :func:`writes_independently`.
_INDEPENDENT_WRITES: set[str] = set()


def reads_after_its_batch(name: str, *, after: frozenset[str] | set[str]) -> None:
    """Declare ``name`` a reporter that, in one batch, runs after its ``after`` siblings."""
    if name:
        _READS_AFTER_ITS_BATCH[name] = frozenset(after)


def writes_independently(*names: str) -> None:
    """Declare write tools whose calls in one batch never need to run in emission order."""
    _INDEPENDENT_WRITES.update(n for n in names if n)


class ToolExecutor:
    """The single entry point for all tool executions.

    Replaces:
      - tool_registry.execute_tool_call()
      - tool_registry.execute_tool()
      - All thin wrapper functions in mcp_server/tools/

    Every tool — local, external MCP, agent — goes through the same pipeline:
      1. Resolve tool definition from registry
      2. Build ToolContext
      3. Validate arguments
      4. Check guardrails
      5. Stream "started" to client
      6. Execute (dispatch by tool type)
      7. Stream "completed" or "error" to client
      8. Log execution (fire-and-forget)
      9. Persist output if flagged
      10. Return result
    """

    def __init__(
        self,
        registry: ToolRegistry,
        guardrails: GuardrailEngine | None = None,
        execution_logger: ToolExecutionLogger | None = None,
        lifecycle: ToolLifecycleManager | None = None,
    ):
        self.registry = registry
        self.guardrails = guardrails or GuardrailEngine()
        self.execution_logger = execution_logger or ToolExecutionLogger()
        self.lifecycle = lifecycle or ToolLifecycleManager.get_instance()

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------

    @staticmethod
    def build_context(
        *,
        call_id: str,
        tool_name: str,
        iteration: int = 0,
        recursion_depth: int = 0,
        cost_budget_remaining: float | None = None,
        calls_remaining: int | None = None,
    ) -> ToolContext:
        return ToolContext(
            call_id=call_id,
            tool_name=tool_name,
            iteration=iteration,
            recursion_depth=recursion_depth,
            cost_budget_remaining=cost_budget_remaining,
            calls_remaining_this_conversation=calls_remaining,
        )

    # ------------------------------------------------------------------
    # Inbound wire-name normalization
    # ------------------------------------------------------------------

    def _normalize_called_name(self, called: str) -> str:
        """Map a model-called (wire) tool name back to its internal name.

        Providers reject ':' in tool names, so colon-namespaced internal
        names (``bundle:list_supabase``) are declared to the model in wire
        form (``bundle__list_supabase`` — see ``matrx_ai.config.wire_names``).
        This reverses that transform for dispatch.

        A name that resolves as-is (projected tool, alias-map entry, or
        registry hit) is returned unchanged — direct identity always wins,
        so plain names containing ``__`` can never be corrupted. Only when
        direct resolution fails do we look for an internal name whose wire
        form matches what the model said.
        """
        from matrx_ai.config.wire_names import WIRE_SEP, resolve_wire_name
        from matrx_ai.tools.agent_projection import lookup_projected_tool
        from matrx_ai.tools.tool_aliases import get_alias_map, lookup_canonical

        if WIRE_SEP not in called:
            return called
        if (
            lookup_projected_tool(called) is not None
            or lookup_canonical(called) is not None
            or self.registry.get(called) is not None
        ):
            return called
        matched = resolve_wire_name(called, get_alias_map().keys())
        if matched is None:
            matched = resolve_wire_name(called, self.registry.list_tool_names())
        return matched if matched is not None else called

    # ------------------------------------------------------------------
    # Pre-dispatch rejection recorder
    # ------------------------------------------------------------------

    async def _record_rejected(
        self,
        ctx: ToolContext,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        result: ToolResult,
        tool_type: str = "local",
        canonical_name: str | None = None,
    ) -> None:
        """Persist a terminal cx_tool_call row for a call rejected before
        dispatch. Best-effort — telemetry must never block dispatch, so a
        failure here is logged inside the logger and swallowed here."""
        try:
            await self.execution_logger.log_rejected(
                ctx,
                tool_name=tool_name,
                arguments=arguments,
                result=result,
                tool_type=tool_type,
                canonical_name=canonical_name,
            )
        except Exception as exc:
            vcprint(
                f"[ToolExecutor] Failed to record rejected tool call "
                f"'{tool_name}' ({getattr(result.error, 'error_type', '?')}): {exc}",
                color="red",
            )

    async def _reject_invalid_arguments(
        self,
        *,
        ctx: ToolContext,
        tool_name: str,
        as_called: str,
        canonical_name: str,
        tool_def: ToolDefinition,
        arguments: dict[str, Any],
        msg: str,
        validation_error: ValidationError | None,
        dispatch_kind: str,
        started_at: float,
        suggested_action: str = (
            "Re-read the tool's input schema and call it again with "
            "exactly the documented arguments (no extra keys)."
        ),
    ) -> tuple[dict[str, Any], ToolResult]:
        """Terminal reject for a pre-dispatch argument-validation failure —
        error_type='invalid_arguments' (fault_domain model_error), recorded to
        both trace sinks with the full args (forensics: 'what did the model
        actually send?') and streamed to the client."""
        if validation_error is not None:
            _note_tool_argument_refusal(
                ctx=ctx,
                tool_name=canonical_name,
                validation_error=validation_error,
            )
        else:
            vcprint(
                f"[ToolExecutor] {canonical_name} call refused for its arguments "
                f"(the model corrects it): {msg[:160]}, call {ctx.call_id}",
                color="yellow",
            )
        result = ToolResult(
            success=False,
            error=ToolError(
                refusal=True,
                error_type="invalid_arguments",
                message=f"Invalid arguments for '{tool_name}': {msg}",
                suggested_action=suggested_action,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )
        _conv_full = getattr(ctx, "conversation_id", None)
        try:
            _args_str = json.dumps(arguments, default=str)
        except Exception:
            _args_str = str(arguments)
        _debug_log(
            "FAIL",
            tool=tool_name,
            kind=dispatch_kind,
            ms=int((time.time() - started_at) * 1000),
            args=_args_str,
            err_type="invalid_arguments",
            err_msg=msg,
            conv=(_conv_full or "")[:8],
            call=ctx.call_id,
        )
        detached_task(
            _db_log(
                "FAIL",
                tool_name=tool_name,
                kind=dispatch_kind,
                args=arguments,
                err_type="invalid_arguments",
                err_msg=msg,
                conversation_id=_conv_full,
                call_id=ctx.call_id,
                user_id=getattr(ctx, "user_id", None),
            ),
            name="tool_db_log_invalid_args",
        )
        result.compute_duration()
        await self._record_rejected(
            ctx,
            tool_name=as_called,
            arguments=arguments,
            result=result,
            tool_type=tool_def.tool_type.value,
            canonical_name=canonical_name,
        )
        stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
        await stream.error(
            f"Invalid arguments for '{tool_name}': {msg}",
            error_type="invalid_arguments",
        )
        return result.to_tool_result_content(), result

    # ------------------------------------------------------------------
    # Completion-log persistence (coordinator-aware)
    # ------------------------------------------------------------------

    async def _persist_tool_outcome(self, coro: Any, *, coordinator: Any, name: str) -> None:
        """Persist a tool-completion log write (log_completed / log_error).

        WHEN A REQUEST COORDINATOR IS PRESENT (the in-request path) the write
        is a purely IN-MEMORY ``coordinator.queue()`` (Session.defer_update) —
        it does NO database I/O. So we run it INLINE and synchronously, which
        deterministically lands the UPDATE in the coordinator's current Session
        BEFORE the tool returns to the loop. It then coalesces with the row's
        INSERT and flushes at the turn barrier exactly like any normal tool.

        This replaces a fire-and-forget ``detached_task``. That detached write
        raced the request's final drain + ``seal()``: for a child-agent-forking
        tool (``agent_call``) — whose ``child_agent_context`` force-finalizes the
        parent coordinator (``pre_fan_out``) and thereby splits the row's INSERT
        off from its UPDATE into separate flush cycles — the late, untracked
        completion write landed AFTER ``seal()`` as a one-shot that request
        teardown never ran. The row stayed ``status='running'`` and the watchdog
        later flipped it to ``error`` (the observed 2026-06-20 agent_call bug).
        The detached_task was only ever needed to keep a REAL DB write off the
        parent's transaction connection — but with a coordinator there is no DB
        write here, just an in-memory defer, so the isolation is moot.

        WITH NO COORDINATOR (a true out-of-request background dispatch) the write
        IS a real DB UPDATE (``update_item_fields``) that must run in a fresh
        contextvars Context so it doesn't dispatch onto a parent transaction
        connection. ``detached_task`` provides that isolation, but the task is
        awaited: a short-lived CLI must not exit after a successful tool result
        while its ledger row is still ``running``.
        """
        if coordinator is not None:
            try:
                await coro
            except Exception as exc:  # noqa: BLE001 — telemetry must never break dispatch
                vcprint(
                    f"[ToolExecutor] inline completion-log write failed: "
                    f"{type(exc).__name__}: {exc}",
                    color="red",
                )
        else:
            try:
                await detached_task(coro, name=name)
            except Exception as exc:  # noqa: BLE001 — telemetry must never break dispatch
                vcprint(
                    f"[ToolExecutor] isolated completion-log write failed: "
                    f"{type(exc).__name__}: {exc}",
                    color="red",
                )

    # ------------------------------------------------------------------
    # Single execution
    # ------------------------------------------------------------------

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        ctx: ToolContext,
        client_tools: frozenset[str] | None = None,
        allowed_tools: frozenset[str] | None = None,
    ) -> tuple[dict[str, Any], ToolResult]:
        """Execute one tool call inside its Watch AI capture scope (``matrx_utils.raw_capture``).

        Everything the call's source returned (transport bodies, values a cut primitive shortened, the
        size gate's pre-cut text) is collected on the scope; when the call ends the scope goes to the
        host's sink with the call's sizes, which stores it and indexes it on the ``chat.tool_call``
        row (``metadata.raw_capture``). No sink → nothing kept, the call is unchanged."""
        from matrx_utils import raw_capture

        from matrx_ai.providers.keys import platform_keys_only

        # A tool is OUR work: any model it calls runs on our key and charges, even
        # inside a turn on the person's own key (owner ruling 2026-10-15 #6).
        with raw_capture.capture_scope({"target": "tool_call"}) as scope, platform_keys_only():
            content_dict, result = await self._execute_pipeline(
                tool_name, arguments, ctx, client_tools=client_tools, allowed_tools=allowed_tools
            )
        if raw_capture.has_raw_capture_sink():
            try:
                from matrx_ai.context.app_context import try_get_app_context

                _app = try_get_app_context()
                scope.target.update(
                    {
                        "row_id": self.execution_logger.row_id_for_call(ctx) or None,
                        "call_id": ctx.call_id,
                        "conversation_id": str(getattr(_app, "conversation_id", "") or "") or None,
                        "user_id": str(getattr(_app, "user_id", "") or "") or None,
                        # Carried verbatim, never defaulted: an empty organization is
                        # refused BY NAME at the sink (it files nothing), not stored as None.
                        "organization_id": str(getattr(_app, "organization_id", "") or ""),
                    }
                )
                tool_capture_facts(result, scope)
            except Exception as exc:  # noqa: BLE001 — watching never changes the call
                logger.warning("[ToolExecutor] raw capture facts failed (%s: %s)", type(exc).__name__, exc)
            raw_capture.deliver(scope)
        return content_dict, result

    async def _execute_pipeline(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        ctx: ToolContext,
        client_tools: frozenset[str] | None = None,
        allowed_tools: frozenset[str] | None = None,
    ) -> tuple[dict[str, Any], ToolResult]:
        """Execute a single tool call through the full pipeline.

        Two-phase logging:
          1. INSERT cx_tool_call with status='running' immediately
          2. UPDATE with output/error when done

        Parameters
        ----------
        allowed_tools:
            When provided, the tool_name must be in this set or execution is
            rejected.  ``None`` means no restriction.  Resolved from the tools
            that were actually sent to the model in the current API call.

        Returns ``(tool_result_content_dict, full_result)``.
        """
        started_at = time.time()

        # --- Wire-name normalization (inbound seam) ---
        # Providers reject ':' in tool names, so declarations go out in wire
        # form (':' → '__', see matrx_ai.config.wire_names) and the model
        # calls the wire name (e.g. 'bundle__list_supabase'). Reverse the
        # transform ONCE, here, so the allowlist, alias map, registry lookup,
        # guardrails and persistence all operate on the internal name. The
        # as-called (wire) spelling is preserved for the trace columns.
        as_called = tool_name
        tool_name = self._normalize_called_name(tool_name)
        if tool_name != as_called:
            vcprint(
                f"[ToolExecutor] wire-name normalized: {as_called!r} → {tool_name!r}",
                color="cyan",
            )
            # Handlers read ctx.tool_name (e.g. the bundle lister parses its
            # bundle from it) — it must carry the internal name.
            ctx = ctx.model_copy(update={"tool_name": tool_name})

        # --- Per-call routing ---
        # A tool a live client implements on purpose still runs on the server when THIS
        # call carries an argument its declaration reserves for the server (e.g. a Cloud
        # Browser session_id). Decided once, here, so every later delegation check agrees.
        from matrx_ai.tools.declared import client_tools_for_call

        client_tools = client_tools_for_call(tool_name, arguments, client_tools)

        # --- Allowlist guard ---
        # Reject any tool the model was not explicitly given in this request.
        # This prevents the model from invoking arbitrary registered tools by
        # guessing their names (accidental or adversarial).
        from matrx_ai.tools.declaration_ledger import retained_reason

        if (
            allowed_tools is not None
            and tool_name not in allowed_tools
            and as_called not in allowed_tools
        ) or (
            # No allowlist this request (no registered tools left): a tool the
            # conversation still declares but withdrew must not run either.
            allowed_tools is None and retained_reason(tool_name, as_called) is not None
        ):
            vcprint(
                {
                    "tool_name": tool_name,
                    "call_id": ctx.call_id,
                    "allowed_tools": sorted(allowed_tools or ()),
                },
                f"[ToolExecutor] Tool '{tool_name}' was not in the allowed set for this request",
                color="yellow",
            )
            # A tool this conversation still DECLARES (the provider tools array
            # never shrinks mid-conversation, declaration_ledger.py) but no
            # longer offers is refused by name, with why, never as "not provided".
            _withdrawn = retained_reason(tool_name, as_called)
            if _withdrawn is not None:
                _err_type = "tool_unavailable"
                _message = (
                    f"Tool '{tool_name}' cannot be used: {_withdrawn}. It is still listed "
                    "so the conversation's prompt cache survives, but calling it does nothing."
                )
                _action = "Continue with your other tools, and tell the user if the job needs this one."
            else:
                _err_type = "not_allowed"
                _message = (
                    f"Tool '{tool_name}' was not provided to the model for this request "
                    "and cannot be executed."
                )
                # A late tool (``providers/late_tools.py``) is defined in turn context and may stay defined on an earlier
                # turn after it is no longer offered; the newest turn's context names the ones that are.
                _action = (
                    "Only call a tool from your tools list, or one this turn's context names as available now; "
                    "a tool defined only on an earlier turn and not named there cannot be called."
                )
            result = ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type=_err_type,
                    message=_message,
                    suggested_action=_action,
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
            result.compute_duration()
            await self._record_rejected(
                ctx,
                tool_name=as_called,
                arguments=arguments,
                result=result,
                canonical_name=tool_name,
            )
            stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
            await stream.error(
                _message if _withdrawn is not None
                else f"Tool '{tool_name}' is not in the allowed set for this request.",
                error_type=_err_type,
            )
            return result.to_tool_result_content(), result

        # The run's allowed set rides on the context so a gateway (``use_tool``) can run a tool
        # the run holds — late tools (providers/late_tools.py) — and refuse any other.
        if allowed_tools is not None and ctx.allowed_tools != allowed_tools:
            ctx = ctx.model_copy(update={"allowed_tools": allowed_tools})

        # --- Resolve tool ---
        # Lookup precedence (Step 2 of the redesign):
        #   1. Projected agent tools — synthetic ``custom_tool_N`` definitions
        #      live on AppContext.metadata['projected_agent_tools'] and never
        #      have a real DB row. Highest priority so concurrent requests
        #      don't collide on the same opaque name.
        #   2. tool_aliases map — bundle aliasing exposes a canonical tool
        #      under a bundle-prefixed name (e.g. 'cool_stuff:scrape_page' →
        #      'scraper:scrape_page'). Resolve through the map, then fetch
        #      the canonical from the registry.
        #   3. Direct registry lookup — back-compat for code paths that haven't
        #      populated the alias map, plus the identity case where exposed
        #      name equals canonical.
        from matrx_ai.tools.agent_projection import lookup_projected_tool
        from matrx_ai.tools.tool_aliases import lookup_canonical

        tool_def = lookup_projected_tool(tool_name)
        canonical_name: str = tool_name
        if tool_def is None:
            aliased = lookup_canonical(tool_name)
            if aliased is not None and aliased != tool_name:
                canonical_name = aliased
            tool_def = self.registry.get(canonical_name)
        if tool_def is None:
            # Catalog Tools are never preloaded: resolve this one name at the
            # executor's edge and pin it to the request (CONTRACT §4).
            from matrx_ai.tools.catalog_seam import resolve_lazy_tools

            lazy = await resolve_lazy_tools([canonical_name])
            if lazy:
                tool_def = lazy[0]
        if tool_def is None:
            vcprint(
                {
                    "tool_name": tool_name,
                    "call_id": ctx.call_id,
                    "registry_loaded": self.registry.loaded,
                    "registry_count": self.registry.count,
                    "available_tools": self.registry.list_tool_names()[:20],
                },
                f"[ToolExecutor] Tool '{tool_name}' not found in registry",
                color="red",
            )
            hint_message, hint_action = self._unknown_tool_hint(tool_name, allowed_tools)
            result = self._unknown_tool_result(
                tool_name,
                ctx.call_id,
                started_at,
                message=hint_message,
                suggested_action=hint_action,
            )
            result.compute_duration()
            await self._record_rejected(
                ctx,
                tool_name=as_called,
                arguments=arguments,
                result=result,
                canonical_name=tool_name,
            )
            stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
            await stream.error(hint_message, error_type="not_found")
            return result.to_tool_result_content(), result

        # --- Pre-flight: viable executor check ---
        # Detects tools that have no live executor for the current request
        # context — the bug class where an agent has a tool whose only
        # client surface isn't connected, AND the server-side fallback
        # function_path is empty (handler not yet implemented). Without
        # this check the dispatch would either silently run on the wrong
        # executor (the original incident) or fail with a generic import
        # error mid-run.
        is_delegated_pre = bool(client_tools and tool_name in client_tools)
        # Captured for the single OK/FAIL line emitted at completion —
        # cheaper than re-deriving from client_tools at result time.
        _dispatch_kind = "DELEGATE" if is_delegated_pre else "SERVER"

        # Schema-proven discriminator alias recovery runs before the durable
        # tool row and delegated event are written, so every client receives
        # the canonical shape. This is generic (not a `user`-tool special
        # case): it fires only when the published type.enum accepts the value
        # and the schema does not own an `action` field. Loud on every fire.
        from matrx_ai.tools._dispatch_util import (
            recover_action_type_alias,
            unwrap_args_envelope,
        )

        # A lean dispatcher row (``$envelope``) shows the model only ``action`` +
        # one arguments object; lift that object back into the flat call here, so
        # the durable row, every guard and the declared-model validation below see
        # exactly the shape a flat caller sends. A call that is already flat is
        # unchanged. An envelope that cannot be lifted honestly is left in place
        # and refused below with ``_envelope_problem`` — never silently chosen.
        _envelope = tool_def.args_envelope
        # THE SAME ENVELOPE ON A FLAT TOOL (2026-11-02, Company Setup efficiency loop). A model
        # that drives one lean dispatcher (`records`: action + `args`) carries that habit to its
        # flat siblings: `html_page(action="create", args={}, …)` and
        # `tables_template(action="list", args={…})` were refused 8 times in 13 runs, each
        # costing a turn. A flat tool that declares no `args` parameter has no other meaning
        # for one, so it is lifted the same honest way (clashes still refused, never chosen).
        if (
            _envelope is None
            and isinstance(arguments, dict)
            and "args" in arguments
            and "args" not in (tool_def.parameters or {})
        ):
            _envelope = "args"
        arguments, _envelope_problem = unwrap_args_envelope(arguments or {}, _envelope)

        _alias_recovered = recover_action_type_alias(arguments, tool_def.parameters)
        if _alias_recovered is not None:
            arguments = _alias_recovered
            logger.warning(
                "[ToolExecutor] recovered discriminator alias action→type for tool %r",
                tool_name,
            )
            vcprint(
                f"[ToolExecutor] RECOVERED {tool_name}: `action` was accepted as "
                "the schema-proven `type` alias.",
                color="yellow",
            )
            _debug_log(
                "ALIAS_RECOVERED",
                tool=tool_name,
                alias="action_to_type",
                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "ALIAS_RECOVERED",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    args=arguments,
                    conversation_id=getattr(ctx, "conversation_id", None),
                    call_id=ctx.call_id,
                    user_id=getattr(ctx, "user_id", None),
                    metadata={"alias": "action_to_type"},
                ),
                name="tool_db_log_alias_recovered",
            )

        # ── A JSON STRING where the schema publishes an object/array is decoded FIRST ──
        # Before the durable row, every guard, the tool's own input repair and the
        # contract check: a tool whose model repairs its input never raises the
        # ValidationError the later coercion waits for, and ask_person's repair then
        # threw the real questions away and showed its lead-in as the only question
        # (review 12 C1, 2/2; both filed as tool_input_contract_drift). A string that
        # does not read as one container is left as sent and refused by name.
        from matrx_ai.tools._dispatch_util import decode_stringified_by_schema

        _schema_decoded: list[str] = []
        # Decoded by the CONTRACT schema (the flattened per-action map the model is shown
        # and the Content IR check judges), never the raw row root: a $variants row's root
        # map can omit ``items`` the per-action contract declares (video_clone gestures).
        _decoded = decode_stringified_by_schema(
            arguments or {}, tool_def._build_json_schema(contract=True)
        )
        if _decoded is not None:
            arguments, _schema_decoded = _decoded
            _decoded_str = ", ".join(_schema_decoded)
            logger.warning(
                "[ToolExecutor] decoded JSON-string arg(s) for tool %r: %s",
                tool_name,
                _decoded_str,
            )
            vcprint(
                f"[ToolExecutor] COERCED {tool_name}: field(s) [{_decoded_str}] were "
                "strings where the schema publishes an object/array/number/boolean — decoded.",
                color="yellow",
            )
            _debug_log(
                "COERCED",
                tool=tool_name,
                fields=_decoded_str,
                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "COERCED",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    args=arguments,
                    conversation_id=getattr(ctx, "conversation_id", None),
                    call_id=ctx.call_id,
                    user_id=getattr(ctx, "user_id", None),
                    metadata={"coerced_fields": _schema_decoded},
                ),
                name="tool_db_log_schema_decoded",
            )

        # --- Pinned arguments (the person's per-request limit, arg_pins.py) ---
        # Applied before the durable row, the trace and validation, so every record of
        # the call carries what actually ran. Loud on every fire; told to the model below.
        from matrx_ai.context.app_context import try_get_app_context as _try_app
        from matrx_ai.tools.arg_pins import apply_arg_pins, pins_for

        _pin_app = _try_app()
        arguments, pinned_changes = apply_arg_pins(
            arguments, pins_for(canonical_name, getattr(_pin_app, "metadata", None) if _pin_app else None)
        )
        if pinned_changes:
            vcprint(f"[ToolExecutor] PINNED {tool_name}: {'; '.join(pinned_changes)}", color="cyan")
            _debug_log(
                "ARGS_PINNED",
                tool=tool_name,
                pinned="; ".join(pinned_changes),
                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "ARGS_PINNED",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    args=arguments,
                    conversation_id=getattr(ctx, "conversation_id", None),
                    call_id=ctx.call_id,
                    user_id=getattr(ctx, "user_id", None),
                    metadata={"pinned": pinned_changes},
                ),
                name="tool_db_log_args_pinned",
            )

        # --- Admin-only gate (defense-in-depth, the hard runtime boundary) ---
        # A tool marked admin_only (e.g. the cross-user `sql` tool) must NEVER execute
        # for a non-admin caller, no matter how it entered the toolset. The injection
        # funnel filters these out for non-admins, but this backstop guarantees it even
        # if a misconfigured agent or a path that bypasses the funnel slips one through.
        if getattr(tool_def, "admin_only", False):
            # An admin tool is a capability the admin put on their own agent: it runs
            # for an admin from ANY chat (Arman, 2026-10-07). The admin lane governs
            # what a normal PAGE shows an admin, never a tool they chose.
            from matrx_connect import admin_tool_authorized, admin_tool_refusal_message

            try:
                _is_admin = admin_tool_authorized()
            except Exception:
                _is_admin = False
            if not _is_admin:
                # Honest about WHICH no: "not an admin" vs "this run did not carry your reach".
                _admin_msg = admin_tool_refusal_message(tool_name)
                result = ToolResult(
                    success=False,
                    error=ToolError(refusal=True, error_type="admin_only", message=_admin_msg),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name=tool_name,
                    call_id=ctx.call_id,
                )
                _conv_full = getattr(ctx, "conversation_id", None)
                _debug_log(
                    "FAIL",
                    tool=tool_name,
                    kind=_dispatch_kind,
                    ms=int((time.time() - started_at) * 1000),
                    err_type="admin_only",
                    err_msg="non-admin caller",
                    conv=(_conv_full or "")[:8],
                    call=ctx.call_id,
                )
                detached_task(
                    _db_log(
                        "FAIL",
                        tool_name=tool_name,
                        kind=_dispatch_kind,
                        args=arguments,
                        err_type="admin_only",
                        err_msg="non-admin caller",
                        conversation_id=_conv_full,
                        call_id=ctx.call_id,
                        user_id=getattr(ctx, "user_id", None),
                    ),
                    name="tool_db_log_admin_only",
                )
                result.compute_duration()
                await self._record_rejected(
                    ctx,
                    tool_name=as_called,
                    arguments=arguments,
                    result=result,
                    tool_type=tool_def.tool_type.value,
                    canonical_name=canonical_name,
                )
                stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
                await stream.error(_admin_msg, error_type="admin_only")
                return result.to_tool_result_content(), result

        # --- Compliance gate (rule H runtime backstop; host-injected, compliance_gate.py) ---
        # The funnel already removed a regulated run's disallowed tools; this refuses any that
        # arrived another way (use_tool, a mid-run queue, a nested agent), delegated ones too.
        from matrx_ai.tools.compliance_gate import (
            COMPLIANCE_REFUSAL_ERROR_TYPE,
            tool_compliance_gate_configured,
            tool_compliance_refusal,
        )

        if tool_compliance_gate_configured():
            from matrx_ai.context.app_context import try_get_app_context as _try_gate_app

            _compliance_msg = await tool_compliance_refusal(canonical_name, _try_gate_app())
            if _compliance_msg:
                vcprint(f"[ToolExecutor] COMPLIANCE REFUSED {tool_name}: {_compliance_msg}", color="yellow")
                result = ToolResult(
                    success=False,
                    error=ToolError(
                        refusal=True,
                        error_type=COMPLIANCE_REFUSAL_ERROR_TYPE,
                        message=_compliance_msg,
                        suggested_action="Do not retry this tool; answer without it.",
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name=tool_name,
                    call_id=ctx.call_id,
                )
                detached_task(
                    _db_log(
                        "FAIL",
                        tool_name=tool_name,
                        kind=_dispatch_kind,
                        args=arguments,
                        err_type=COMPLIANCE_REFUSAL_ERROR_TYPE,
                        err_msg=_compliance_msg,
                        conversation_id=getattr(ctx, "conversation_id", None),
                        call_id=ctx.call_id,
                        user_id=getattr(ctx, "user_id", None),
                    ),
                    name="tool_db_log_compliance_refused",
                )
                result.compute_duration()
                await self._record_rejected(
                    ctx,
                    tool_name=as_called,
                    arguments=arguments,
                    result=result,
                    tool_type=tool_def.tool_type.value,
                    canonical_name=canonical_name,
                )
                stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
                await stream.error(_compliance_msg, error_type=COMPLIANCE_REFUSAL_ERROR_TYPE)
                return result.to_tool_result_content(), result

        on_screen_redirect: dict[str, Any] | None = None
        # --- On-screen write guard (W-60) ---
        # A record the person has open on a page with a live write target is
        # changed only through that page's approval (apply_surface_write) —
        # never by a server writer the model picks instead, and never after the
        # person declined it this turn. See matrx_ai/tools/on_screen_write_guard.py.
        if not is_delegated_pre:
            from matrx_ai.context.app_context import try_get_app_context
            from matrx_ai.tools.on_screen_write_guard import (
                ON_SCREEN_ERROR_TYPE,
                ON_SCREEN_SUGGESTED_ACTION,
                SURFACE_WRITE_DOOR,
                guarded_write_refusal,
                on_screen_surface_redirect,
                writer_key,
            )

            _app = try_get_app_context()
            _app_md = getattr(_app, "metadata", None) if _app else None
            # Q-05 (2026-11-10): a right edit on the record open on screen IS the
            # approval card — the same edit goes to the page's apply_surface_write
            # under this call id, instead of coming back as a failed tool call.
            _redirect = (
                on_screen_surface_redirect(canonical_name, arguments, _app_md)
                if client_tools and SURFACE_WRITE_DOOR in client_tools
                else None
            )
            _door_def = self.registry.get(SURFACE_WRITE_DOOR) if _redirect is not None else None
            _refusal = (
                None
                if _door_def is not None
                else guarded_write_refusal(canonical_name, arguments, _app_md)
            )
            if _door_def is not None and _redirect is not None:
                on_screen_redirect = {
                    "from_tool": writer_key(canonical_name, arguments) or canonical_name,
                    # The model called ``as_called``: the rebuilt result answers that name
                    # (Gemini pairs functionResponse to functionCall by name).
                    "answers_name": as_called,
                    "from_arguments": dict(arguments),
                }
                logger.warning(
                    "[ToolExecutor] on-screen write %s sent to the person as %s (call %s)",
                    on_screen_redirect["from_tool"],
                    SURFACE_WRITE_DOOR,
                    ctx.call_id,
                )
                tool_name = canonical_name = SURFACE_WRITE_DOOR
                tool_def = _door_def
                arguments = _redirect
                is_delegated_pre = True
                _dispatch_kind = "DELEGATE"
                ctx = ctx.model_copy(update={"tool_name": SURFACE_WRITE_DOOR})
            if _refusal is not None:
                _err_type, _msg = _refusal
                result = ToolResult(
                    success=False,
                    error=ToolError(
                        refusal=True,
                        error_type=_err_type,
                        message=_msg,
                        # A redirect, not a dead end: "or tell the person" read as
                        # permission to stop (Q-05, 2026-11-09).
                        suggested_action=(
                            ON_SCREEN_SUGGESTED_ACTION
                            if _err_type == ON_SCREEN_ERROR_TYPE
                            else "Tell the person the change was left as it was."
                        ),
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name=tool_name,
                    call_id=ctx.call_id,
                )
                logger.warning(
                    "[ToolExecutor] on-screen write guard refused %s (%s)", tool_name, _err_type
                )
                result.compute_duration()
                await self._record_rejected(
                    ctx,
                    tool_name=as_called,
                    arguments=arguments,
                    result=result,
                    tool_type=tool_def.tool_type.value,
                    canonical_name=canonical_name,
                )
                stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
                await stream.error(_msg, error_type=_err_type)
                return result.to_tool_result_content(), result

        # --- Pre-flight: validate arguments against the declared schema ---
        # When a tool declares a Pydantic args model in code
        # (matrx_ai.tools.declared, populated by @tool / the generated
        # declarations), validate the model-supplied arguments BEFORE dispatch.
        # A failure here is the MODEL's fault — wrong / extra / missing /
        # mistyped args — and is reported as error_type="invalid_arguments"
        # (fault_domain "model_error"), cleanly distinct from a tool body that
        # throws (a "tool_defect"). Only server-executed, validate-enabled
        # declared tools are checked; client-delegated tools validate on the
        # client, and tools without a declared model are left untouched.
        coerced_fields: list[str] = list(_schema_decoded)
        respelled_choices: list[tuple[str, Any, Any]] = []
        inferred_discriminator: tuple[str, str] | None = None
        # (discriminator, action, removed fields) when pre-flight stripped
        # arguments another action owns — told to the model on the result.
        removed_variant_fields: tuple[str, str, list[str]] | None = None

        # ── Copied context-trim text is never run ─────────────────────────
        # Old calls in the model's context are trimmed in their own shape, each
        # cut value ending in a note (config/context_trim.py). A NEW call that
        # carries the note copied history: running it would send a truncated
        # value. Refuse it so the model writes the full value (2026-10-21,
        # conversation 9b224bf5: three calls sent a trim stub as arguments).
        from matrx_ai.config.context_trim import arguments_carry_trim_marker

        _copied_marker = arguments_carry_trim_marker(arguments or {})
        if _copied_marker is not None:
            return await self._reject_invalid_arguments(
                ctx=ctx,
                tool_name=tool_name,
                as_called=as_called,
                canonical_name=canonical_name,
                tool_def=tool_def,
                arguments=arguments or {},
                msg=(
                    "these arguments contain text copied from an earlier call that was "
                    f"trimmed from your context ({_copied_marker!r})."
                ),
                validation_error=None,
                dispatch_kind=_dispatch_kind,
                started_at=started_at,
                suggested_action=(
                    "Write every argument out in full for this call; earlier calls in "
                    "your context are shortened and must never be copied."
                ),
            )

        if not is_delegated_pre:
            from matrx_ai.tools._dispatch_util import (
                coerce_stringified_containers,
                format_args_error,
                infer_missing_discriminator,
                remove_flattened_variant_extras,
            )
            from matrx_ai.tools.declared import get_effective_declared

            _declared = get_effective_declared(canonical_name)
            # A lean row's `guide` is answered from the row at the dispatch edge
            # (``lean_envelope.row_guide``); the code's union has no such action,
            # so it is not validated against it.
            from matrx_ai.tools.lean_envelope import serves_row_guide

            if (
                _declared is not None
                and _declared.validate
                and not serves_row_guide(tool_def, arguments)
            ):
                # ── Missing action/command inference (before validate) ───────
                # A rejected call still costs a full provider turn. When the
                # discriminator is omitted but variant-unique fields uniquely
                # identify the action, fill it in. Loud on every fire.
                _infer = infer_missing_discriminator(arguments or {}, _declared.args_model)
                if _infer.kind == "inferred" and _infer.args is not None:
                    arguments = _infer.args
                    inferred_discriminator = (
                        _infer.discriminator or "action",
                        _infer.tag or "",
                    )
                    _disc_f, _disc_t = inferred_discriminator
                    logger.warning(
                        "[ToolExecutor] inferred missing %s=%r for tool %r "
                        "from variant-unique fields",
                        _disc_f,
                        _disc_t,
                        tool_name,
                    )
                    vcprint(
                        f"[ToolExecutor] INFERRED {tool_name}: missing "
                        f"{_disc_f}={_disc_t!r} recovered from supplied fields.",
                        color="yellow",
                    )
                    _debug_log(
                        "INFERRED",
                        tool=tool_name,
                        field=_disc_f,
                        tag=_disc_t,
                        conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                        call=ctx.call_id,
                    )
                    detached_task(
                        _db_log(
                            "INFERRED",
                            tool_name=tool_name,
                            kind=_dispatch_kind,
                            args=arguments,
                            conversation_id=getattr(ctx, "conversation_id", None),
                            call_id=ctx.call_id,
                            user_id=getattr(ctx, "user_id", None),
                            metadata={
                                "inferred_discriminator": _disc_f,
                                "inferred_tag": _disc_t,
                            },
                        ),
                        name="tool_db_log_inferred",
                    )

                try:
                    _declared.args_model.model_validate(arguments or {})
                except Exception as _ve:
                    # ── Flattened dispatcher-schema recovery ──────────────
                    # Provider schemas expose the superset of dispatcher
                    # fields, while the selected Pydantic action correctly
                    # forbids fields owned by another variant. Remove only
                    # those provably cross-variant extras, revalidate once,
                    # and scream in every trace sink when recovery fires.
                    _healed = False
                    _variant_recovery = remove_flattened_variant_extras(
                        arguments or {},
                        _declared.args_model,
                        _ve,
                    )
                    if _variant_recovery is not None:
                        _cand_args, _removed_fields = _variant_recovery
                        try:
                            _declared.args_model.model_validate(_cand_args)
                            _healed = True
                        except Exception:
                            _healed = False
                        if _healed:
                            arguments = _cand_args
                            from matrx_ai.tools.validation.schema import (
                                discriminated_union_members,
                            )

                            _union = discriminated_union_members(_declared.args_model)
                            _disc_name = _union[0] if _union else "action"
                            removed_variant_fields = (
                                _disc_name,
                                str((arguments or {}).get(_disc_name, "")),
                                list(_removed_fields),
                            )
                            _fields_str = ", ".join(_removed_fields)
                            logger.warning(
                                "[ToolExecutor] removed flattened-schema "
                                "variant field(s) for tool %r: %s",
                                tool_name,
                                _fields_str,
                            )
                            vcprint(
                                f"[ToolExecutor] VARIANT-RECOVERED {tool_name}: "
                                f"removed field(s) [{_fields_str}] advertised "
                                "by another action and re-validated OK.",
                                color="yellow",
                            )
                            _debug_log(
                                "VARIANT_RECOVERED",
                                tool=tool_name,
                                fields=_fields_str,
                                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                                call=ctx.call_id,
                            )
                            detached_task(
                                _db_log(
                                    "VARIANT_RECOVERED",
                                    tool_name=tool_name,
                                    kind=_dispatch_kind,
                                    args=arguments,
                                    conversation_id=getattr(ctx, "conversation_id", None),
                                    call_id=ctx.call_id,
                                    user_id=getattr(ctx, "user_id", None),
                                    metadata={"removed_variant_fields": _removed_fields},
                                ),
                                name="tool_db_log_variant_recovered",
                            )

                    # ── Stringified-JSON auto-coercion (one pass) ─────────────
                    # The dominant arg-shape failure: the model sent a JSON
                    # STRING where a dict/list is required (8x-in-one-conversation
                    # class). Nothing has executed yet, so decoding the string
                    # and re-validating once is an encoding fix, not a semantic
                    # guess. Loud on every fire — the model gets a notice on the
                    # result, both trace sinks record a COERCED event.
                    _coerce = (
                        None if _healed else coerce_stringified_containers(arguments or {}, _ve)
                    )
                    if _coerce is not None:
                        _cand_args, _cand_fields = _coerce
                        # After decoding containers, retry discriminator
                        # inference once (e.g. requests='[...]' then action=batch).
                        _infer2 = infer_missing_discriminator(_cand_args, _declared.args_model)
                        if _infer2.kind == "inferred" and _infer2.args is not None:
                            _cand_args = _infer2.args
                            if inferred_discriminator is None:
                                inferred_discriminator = (
                                    _infer2.discriminator or "action",
                                    _infer2.tag or "",
                                )
                        try:
                            _declared.args_model.model_validate(_cand_args)
                            _healed = True
                        except Exception:
                            _healed = False
                        if _healed:
                            arguments = _cand_args
                            coerced_fields = sorted({*coerced_fields, *_cand_fields})
                            _fields_str = ", ".join(coerced_fields)
                            logger.warning(
                                "[ToolExecutor] auto-coerced JSON-string arg(s) "
                                "for tool %r: %s (model sent a JSON-encoded "
                                "string where a dict/list is required)",
                                tool_name,
                                _fields_str,
                            )
                            vcprint(
                                f"[ToolExecutor] COERCED {tool_name}: field(s) "
                                f"[{_fields_str}] were JSON-encoded strings — "
                                f"decoded to native containers and re-validated OK.",
                                color="yellow",
                            )
                            _debug_log(
                                "COERCED",
                                tool=tool_name,
                                fields=_fields_str,
                                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                                call=ctx.call_id,
                            )
                            detached_task(
                                _db_log(
                                    "COERCED",
                                    tool_name=tool_name,
                                    kind=_dispatch_kind,
                                    args=arguments,
                                    conversation_id=getattr(ctx, "conversation_id", None),
                                    call_id=ctx.call_id,
                                    user_id=getattr(ctx, "user_id", None),
                                    metadata={"coerced_fields": coerced_fields},
                                ),
                                name="tool_db_log_coerced",
                            )
                    # ── Out-of-range number clamp (one pass) ─────────────────
                    # "Validation offers, never blocks": a number past a
                    # declared ge/le bound has one nearest lawful value. Clamp
                    # it, re-validate once, and say so on every sink.
                    if not _healed:
                        from matrx_ai.tools._dispatch_util import clamp_out_of_range_numbers

                        _clamp = clamp_out_of_range_numbers(arguments or {}, _ve)
                        if _clamp is not None:
                            _cand_args, _clamp_changes = _clamp
                            try:
                                _declared.args_model.model_validate(_cand_args)
                                _healed = True
                            except Exception:
                                _healed = False
                            if _healed:
                                arguments = _cand_args
                                _clamp_desc = ", ".join(
                                    f"{f}={s!r}->{v!r}" for f, s, v in _clamp_changes
                                )
                                logger.warning(
                                    "[ToolExecutor] clamped out-of-range arg(s) for tool %r: %s",
                                    tool_name,
                                    _clamp_desc,
                                )
                                vcprint(
                                    f"[ToolExecutor] CLAMPED {tool_name}: [{_clamp_desc}] "
                                    "was outside the declared bound — moved to the "
                                    "nearest allowed value and re-validated OK.",
                                    color="yellow",
                                )
                                _debug_log(
                                    "CLAMPED",
                                    tool=tool_name,
                                    fields=_clamp_desc,
                                    conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                                    call=ctx.call_id,
                                )
                                detached_task(
                                    _db_log(
                                        "CLAMPED",
                                        tool_name=tool_name,
                                        kind=_dispatch_kind,
                                        args=arguments,
                                        conversation_id=getattr(ctx, "conversation_id", None),
                                        call_id=ctx.call_id,
                                        user_id=getattr(ctx, "user_id", None),
                                        metadata={
                                            "clamped_fields": [
                                                {"field": f, "supplied": s, "clamped": v}
                                                for f, s, v in _clamp_changes
                                            ]
                                        },
                                    ),
                                    name="tool_db_log_clamped",
                                )
                    # ── Enum spelling (one pass) ─────────────────────────────
                    # 'Choice' for 'choice', 'choice-many' for 'choice_many', at
                    # any depth. Spelling only; a synonym is the tool's own call.
                    if not _healed:
                        from matrx_ai.tools._dispatch_util import heal_choice_spelling

                        _spelled = heal_choice_spelling(arguments or {}, _ve)
                        if _spelled is not None:
                            _cand_args, _spell_changes = _spelled
                            try:
                                _declared.args_model.model_validate(_cand_args)
                                _healed = True
                            except Exception:
                                _healed = False
                            if _healed:
                                arguments = _cand_args
                                respelled_choices = _spell_changes
                                _spell_desc = ", ".join(
                                    f"{f}={s!r}->{v!r}" for f, s, v in _spell_changes
                                )
                                logger.warning(
                                    "[ToolExecutor] respelled enum value(s) for tool %r: %s",
                                    tool_name,
                                    _spell_desc,
                                )
                                vcprint(
                                    f"[ToolExecutor] COERCED {tool_name}: [{_spell_desc}] "
                                    "differed from a declared value only in spelling.",
                                    color="yellow",
                                )
                                _debug_log(
                                    "COERCED",
                                    tool=tool_name,
                                    fields=_spell_desc,
                                    conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                                    call=ctx.call_id,
                                )
                                detached_task(
                                    _db_log(
                                        "COERCED",
                                        tool_name=tool_name,
                                        kind=_dispatch_kind,
                                        args=arguments,
                                        conversation_id=getattr(ctx, "conversation_id", None),
                                        call_id=ctx.call_id,
                                        user_id=getattr(ctx, "user_id", None),
                                        metadata={
                                            "respelled_choices": [
                                                {"field": f, "supplied": s, "value": v}
                                                for f, s, v in _spell_changes
                                            ]
                                        },
                                    ),
                                    name="tool_db_log_respelled",
                                )
                    if not _healed:
                        # Prefer the action-menu error over Pydantic's
                        # "Unable to extract tag using discriminator …".
                        if _infer.kind in ("ambiguous", "uninferable") and _infer.error:
                            _msg = _infer.error[:800]
                        else:
                            _retry_infer = infer_missing_discriminator(
                                arguments or {}, _declared.args_model
                            )
                            if (
                                _retry_infer.kind in ("ambiguous", "uninferable")
                                and _retry_infer.error
                            ):
                                _msg = _retry_infer.error[:800]
                            else:
                                _msg = format_args_error(_ve)[:800]
                        if _envelope is not None:
                            # The model was shown no per-action field names, so the
                            # refusal carries them — a plain sentence, never a bare
                            # pydantic location.
                            from matrx_ai.tools._dispatch_util import (
                                expected_fields_sentence,
                            )

                            _expected = expected_fields_sentence(
                                arguments or {}, _declared.args_model, envelope=_envelope
                            )
                            _msg = " ".join(
                                part for part in (_envelope_problem, _msg, _expected) if part
                            )[:1200]
                        else:
                            from matrx_ai.tools._dispatch_util import (
                                flat_required_sentence,
                                other_action_fields_sentence,
                            )

                            _flat = flat_required_sentence(
                                arguments or {}, _declared.args_model, _ve
                            )
                            if _flat:
                                _msg = f"{_msg} {_flat}"[:1200]
                            _owned = other_action_fields_sentence(
                                arguments or {}, _declared.args_model, _ve
                            )
                            if _owned:
                                _msg = f"{_msg} {_owned}"[:1200]
                        return await self._reject_invalid_arguments(
                            ctx=ctx,
                            tool_name=tool_name,
                            as_called=as_called,
                            canonical_name=canonical_name,
                            tool_def=tool_def,
                            arguments=arguments,
                            msg=_msg,
                            validation_error=_ve,
                            dispatch_kind=_dispatch_kind,
                            started_at=started_at,
                        )

        from matrx_ai.tools.implementations.legacy_local import routes_to_matrx2

        if (
            tool_def.tool_type == ToolType.LOCAL
            and not is_delegated_pre
            and not (tool_def.function_path or "").strip()
            and tool_def._callable is None
            and not self._has_external_handler(tool_def)
            # An old local_* name on a Matrx 2 computer: its successor runs it (legacy_local.py).
            and not routes_to_matrx2(tool_def.name)
        ):
            _debug_log(
                "NO_EXECUTOR",
                tool=tool_name,
                canonical=canonical_name,
                reason="LOCAL+empty_fn+not_delegated",
                call_id=ctx.call_id,
            )
            vcprint(
                {
                    "tool_name": tool_name,
                    "canonical_name": canonical_name,
                    "call_id": ctx.call_id,
                    "client_tools": sorted(client_tools or []),
                    "tool_type": tool_def.tool_type.value,
                },
                f"[ToolExecutor] Tool '{tool_name}' has no viable executor "
                f"for this request — not delegated to a live client surface "
                f"AND no server-side function_path is configured.",
                color="red",
            )
            result = ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type="no_viable_executor",
                    message=(
                        f"Tool {tool_name!r} (canonical {canonical_name!r}) "
                        f"has no executor available for this request. The "
                        f"client surface that runs this tool isn't active "
                        f"in the request envelope, and no server-side "
                        f"fallback handler is configured."
                    ),
                    suggested_action=(
                        "Either run from a client that supports this tool, "
                        "or implement the server-side handler."
                    ),
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
            result.compute_duration()
            await self._record_rejected(
                ctx,
                tool_name=as_called,
                arguments=arguments,
                result=result,
                tool_type=tool_def.tool_type.value,
                canonical_name=canonical_name,
            )
            stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
            await stream.error(
                f"Tool '{tool_name}' has no viable executor for this request.",
                error_type="no_viable_executor",
            )
            return result.to_tool_result_content(), result

        # Content IR shadow input check. This runs only after wire-name and
        # alias resolution plus all safe argument coercions, against the same
        # normalized schema sent to providers. It never blocks dispatch.
        from matrx_graph.content_ir.model import kind_of
        from matrx_graph.contract_kinds import check_schema
        from matrx_graph.kinds import KindDegradedReason, check_against_kind

        from matrx_ai.tools.kinds import result_kind_slug

        input_contract, output_contract = tool_def.content_ir_contracts()
        input_kind_verdict = check_schema(arguments, input_contract.json_schema)
        if input_kind_verdict.errors and not is_delegated_pre:
            # The tool runs what its own input model reads (a declared repair included);
            # judge THAT, so a call the tool's repair settled is never filed as drift.
            from matrx_ai.tools.declared import get_effective_declared as _declared_of

            _decl = _declared_of(canonical_name)
            _meant = arguments_as_meant(arguments or {}, getattr(_decl, "args_model", None)) if _decl else None
            if _meant is not None and _meant != arguments:
                _meant_verdict = check_schema(_meant, input_contract.json_schema)
                if not _meant_verdict.errors:
                    input_kind_verdict = _meant_verdict
        # The contract checked here IS the schema the model was shown, so a refusal
        # alone says only that the model sent what it was not offered. It is DRIFT
        # (contract and code disagree) when the tool then ACCEPTS those arguments;
        # when the server-run tool refuses them too, the model got the refusal and
        # corrects it — a model mistake, never a platform error (live:
        # hub_page_go_live with confirm_opens, refused by PageGoLiveInput too,
        # 2026-11-05). Paths that never learn the tool's verdict (delegated,
        # contained, guardrail-stopped) still file at once.
        pending_input_drift = bool(input_kind_verdict.errors)

        async def _file_input_drift() -> None:
            nonlocal pending_input_drift
            if not pending_input_drift:
                return
            pending_input_drift = False
            logger.error(
                "[Content IR] tool input drift for %s (%s): %s",
                canonical_name,
                input_contract.kind,
                input_kind_verdict.errors,
            )
            await _capture_tool_input_contract_drift(
                ctx=ctx,
                tool_name=canonical_name,
                input_kind=input_contract.kind,
                error_count=len(input_kind_verdict.errors),
                errors=input_kind_verdict.errors,
            )

        # --- Phase 1: log attempt (fire-and-forget INSERT) ---
        from matrx_ai.tools.execution_authorization import evaluate_tool_authorization

        authorization = await evaluate_tool_authorization(tool_def, arguments, ctx)
        delegated_authorization: dict[str, Any] | None = authorization.metadata or None
        if on_screen_redirect:
            # Q-05 (REVIEW-C105): a server write sent to the page as its approval card is
            # ALWAYS approved by the person, whatever the target's apply policy ("auto"
            # included). The tool_delegated event and the stored row carry the mark; the
            # page's apply_surface_write reads it and shows the card.
            delegated_authorization = {
                **(delegated_authorization or {}),
                "on_screen_redirect": True,
                "requires_person": True,
            }
        if authorization.requires_confirmation:
            client_tools = frozenset({*(client_tools or frozenset()), tool_name})
            is_delegated_pre = True
            _dispatch_kind = "DELEGATE"

        # --- Mandate-candidate containment (PLAN.md P3) ---
        # Decided HERE — after the delegation set is final, before the row, the
        # guardrails, the stream and any dispatch — so a candidate call cannot
        # act before it is judged. None ⇒ no marker in scope ⇒ nothing changes.
        from matrx_ai.tools.candidate_containment import (
            DISPATCHED_DISPOSITIONS as _CANDIDATE_DISPATCHED,
        )
        from matrx_ai.tools.candidate_containment import (
            candidate_stop as _candidate_stop,
        )
        from matrx_ai.tools.candidate_containment import decide as _candidate_decide

        containment = await _candidate_decide(
            tool_def,
            arguments,
            call_id=ctx.call_id,
            is_delegated=bool(
                client_tools and (tool_name in client_tools or tool_def.name in client_tools)
            ),
        )
        # ``real`` and ``contained`` dispatch; ``borrowed`` / ``stopped`` never do.
        if containment is not None and containment.disposition not in _CANDIDATE_DISPATCHED:
            await _file_input_drift()
            return await self._contain_candidate_call(
                ctx,
                tool_def,
                arguments,
                containment,
                tool_name=tool_name,
                as_called=as_called,
                started_at=started_at,
            )
        # A nested run (agent-as-tool, a child agent) that stops records the
        # stop in the SHARED ledger; sampled here so the parent call can end too.
        candidate_stop_before = _candidate_stop() if containment is not None else None

        # ``as_called`` is the literal (wire) name the model used;
        # ``tool_def.name`` is the *canonical* identity. Pass both so the
        # logger records each in its own column (analytics defaults to
        # canonical; trace UIs can show what the model actually called it).
        row_id = await self.execution_logger.log_started(
            ctx,
            tool_def,
            arguments,
            exposed_name=as_called,
            authorization_metadata=delegated_authorization,
            candidate_disposition=containment.as_record() if containment is not None else None,
            **({"on_screen_redirect": on_screen_redirect} if on_screen_redirect else {}),
        )

        stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name, row_id=str(row_id) if row_id else None)

        # --- Guardrails ---
        guardrail_result = await self.guardrails.check(tool_name, arguments, ctx, tool_def)
        if guardrail_result.blocked:
            error_result = ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type=guardrail_result.error_type,
                    message=guardrail_result.reason or "Blocked by guardrail",
                    suggested_action=guardrail_result.suggested_action,
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
            error_result.compute_duration()
            await stream.error(guardrail_result.reason or "Blocked", guardrail_result.error_type)
            if (
                guardrail_result.error_type == "recursion_depth"
                and tool_def.tool_type == ToolType.AGENT
            ):
                await warn_member_depth_exhausted(ctx, tool_def, tool_name)
            self.execution_logger.prepare_metadata(error_result)
            events = stream.get_events_for_persistence()
            # Phase F: detached_task so this log write doesn't inherit the
            # request's transaction connection (would cause asyncpg
            # InterfaceError when the parent flush is mid-statement). Capture
            # the coordinator in the live context and hand it through so the
            # UPDATE is queued onto the INSERT's Session instead of racing it
            # as a context-less direct write (see _update_row).
            from matrx_ai.persistence.queue_helpers import get_coordinator as _get_coord

            _gr_coord = _get_coord()
            await self._persist_tool_outcome(
                self.execution_logger.log_error(
                    row_id, error_result, events, coordinator=_gr_coord
                ),
                coordinator=_gr_coord,
                name="tool_log_error_guardrail",
            )
            await _file_input_drift()
            return error_result.to_tool_result_content(), error_result

        self.guardrails.record_call(tool_name, arguments, ctx, tool_def)

        # --- Stream started (with full arguments — non-negotiable) ---
        user_message = tool_def.format_user_message(arguments)
        await stream.started(
            user_message, arguments=arguments, display_name=tool_def.display_name, category=tool_def.category
        )

        # Touch lifecycle
        self.lifecycle.touch(ctx.conversation_id)

        # --- Execute ---
        # Client-delegated tools follow a different cancellation contract:
        # their row is the durable ledger entry for "awaiting client POST",
        # so an SSE disconnect MUST leave the row in 'delegated' (not flip
        # it to 'error/abandoned') so a later POST or the expiry sweep can
        # resolve it. The delegated dispatch RETURNS IMMEDIATELY — it commits
        # the ledger row + emits ``tool_delegated`` and then suspends; it never
        # blocks on the user. So its timeout only guards that commit/emit and is
        # deliberately SHORT and decoupled from the user's answer window, which
        # is durable (cx_tool_call.expires_at + /resume), not a held request task.
        is_delegated = bool(client_tools and tool_name in client_tools)
        dispatch_timeout = _dispatch_timeout_seconds(
            tool_def,
            arguments,
            is_delegated=is_delegated,
        )
        cancellation_after_completion: asyncio.CancelledError | None = None
        # the connection layer counts its budget from HERE (the dispatch), so its own words always beat this ceiling
        from matrx_ai.tools.mcp_resilience import DISPATCH_ENDS_AT

        _ends_token = DISPATCH_ENDS_AT.set(time.monotonic() + dispatch_timeout)
        try:
            dispatch = self._dispatch(
                tool_def,
                arguments,
                ctx,
                stream,
                client_tools,
                row_id,
                authorization_metadata=delegated_authorization,
            )
            if tool_def.must_complete and not is_delegated:
                result, cancellation_after_completion = await _await_must_complete(
                    dispatch,
                    timeout_seconds=dispatch_timeout,
                    stream=stream,
                    tool_name=tool_name,
                )
            else:
                result = await asyncio.wait_for(
                    dispatch,
                    timeout=dispatch_timeout,
                )
        except asyncio.CancelledError:
            # Server-side tools: flip 'running' → 'error/abandoned' synchronously
            # (shielded) to avoid orphan rows. Client-delegated tools: LEAVE the
            # row alone — status='delegated' is durable and expected to outlive
            # the request.
            if row_id and not is_delegated:
                try:
                    # Cancellation cleanup runs under ``shield()``, which may
                    # execute in a copied context after request teardown has
                    # begun. Carry the coordinator explicitly, just like the
                    # normal completion funnel, so the terminal UPDATE cannot
                    # miss the deferred INSERT or strand a running row.
                    from matrx_ai.persistence.queue_helpers import (
                        get_coordinator as _get_cancel_coord,
                    )

                    _cancel_coord = _get_cancel_coord()
                    await asyncio.shield(
                        self.execution_logger.log_abandoned(
                            row_id,
                            reason="client_disconnected",
                            error_message=(
                                f"Tool '{tool_name}' was abandoned — the request "
                                "was canceled (client disconnected) before the "
                                "tool finished."
                            ),
                            execution_events=stream.get_events_for_persistence(),
                            coordinator=_cancel_coord,
                        )
                    )
                except Exception as cleanup_exc:
                    vcprint(
                        f"[ToolExecutor] Failed to mark row abandoned on cancel: {cleanup_exc}",
                        color="red",
                    )
            raise
        except TimeoutError as timeout_exc:
            result = ToolResult(
                success=False,
                error=timeout_tool_error(
                    exc=timeout_exc,
                    tool_name=tool_name,
                    dispatch_timeout=dispatch_timeout,
                    user_message=user_message,
                    # honest about a repeat: a tool that declares its hints is safe to repeat only when it says so
                    # a connected (MCP) tool is safe to repeat only when it SAYS so — most declare nothing, and a
                    # write that may already have happened must never be invited twice (re-review R-C1b)
                    safe_to_repeat=_timeout_safe_to_repeat(tool_def),
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
        except Exception as exc:
            result = ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution",
                    message=str(exc),
                    traceback=tb.format_exc(),
                    is_retryable=False,
                    suggested_action="Check the error details and try with different parameters.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
        finally:
            DISPATCH_ENDS_AT.reset(_ends_token)

        result.compute_duration()

        # --- Held stream for a PERSON (RESUME-AND-RECOVERY 1b rule P4): a call parked on an ask waits here,
        # outside the dispatch's timeout and cancel branch, when the client keeps reading for the answer.
        if result.delegated_pending and not is_delegated and row_id:
            held_for_person = await self._hold_for_person(tool_def, ctx, row_id, started_at)
            if held_for_person is not None:
                result = held_for_person
                result.compute_duration()

        # --- Held stream: the client's result landed while this turn waited for it ---
        # The result POST wrote the row (status, output, kind, trace). Nothing below may write it again,
        # and the model gets exactly what a rebuild of the stored row gives (RESUME-AND-RECOVERY 1a).
        if result.client_resolved_content is not None:
            _debug_log(
                "DELEGATED_HELD",
                tool=tool_name,
                kind=_dispatch_kind,
                conv=(ctx.conversation_id or "")[:8],
                call=ctx.call_id,
            )
            await _file_input_drift()
            return result.client_resolved_content, result

        # --- Mandate-candidate: a nested run stopped under this call ---
        # The child's stop is terminal for the whole candidate: this call's
        # result (e.g. an agent tool's "child answered") is never handed to the
        # model. The row closes as a candidate stop, like the child's own.
        if containment is not None and candidate_stop_before is None:
            nested_stop = _candidate_stop()
            if nested_stop is not None:
                from matrx_ai.persistence.queue_helpers import get_coordinator as _get_coord

                _ns_coord = _get_coord()
                await self._persist_tool_outcome(
                    self.execution_logger.log_abandoned(
                        row_id,
                        reason="candidate_stopped",
                        error_message=(
                            "Candidate run stopped inside this call at step "
                            f"{nested_stop.get('step')} ({nested_stop.get('tool')}); its "
                            "result was not returned to the model."
                        ),
                        execution_events=stream.get_events_for_persistence(),
                        coordinator=_ns_coord,
                    ),
                    coordinator=_ns_coord,
                    name="tool_log_candidate_stopped_nested",
                )
                stopped = ToolResult(
                    success=False,
                    candidate_stopped=True,
                    candidate_disposition=containment.as_record(),
                    tool_name=tool_name,
                    call_id=ctx.call_id,
                    started_at=started_at,
                    completed_at=time.time(),
                )
                stopped.compute_duration()
                await _file_input_drift()
                return _candidate_stopped_content(stopped, nested_stop), stopped
            result.candidate_disposition = containment.as_record()

        # THE REFUSAL REACHES THE PERSON HONESTLY. One place, after every
        # dispatch path: a failure class we can NAME carries its cause and its
        # remedy in front of the raw text, whether the tool RAISED (the branches
        # above) or built its own failed envelope (`workflow_plan` and most host
        # tools do). Without this the model paraphrases a database CHECK as
        # policy — live 2026-09-12, a missing `app.actor_system` declaration
        # became "edits to any agent's contract must come from an authorized
        # human channel" for a non-technical Expert. See `error_remedy`.
        if not result.success and result.error is not None:
            annotate_tool_error(result.error)

        # The generated I/O contracts (``content_ir_contracts``) are machine contracts
        # that live in ``content_ir.io_contract`` (rule 6). They are checked above for
        # drift, but their slugs are never stamped as the call's kind (rule 28).

        # --- Client-delegated suspension: record DELEGATED, skip OK/FAIL ---
        # A delegated call produced no result here — it suspended. The cx_tool_call
        # row is already 'delegated' (set in _execute_delegated) and is the
        # durable ledger for the client's POST /tool_results + /resume. Running
        # the completed/error stream events or log_completed/log_error below would
        # overwrite that 'delegated' status and emit a misleading OK/FAIL trace —
        # skip those. (docs/tool_delegation/DELEGATION_LOOP_BUGS.md)
        #
        # But the DISPATCH itself must still reach both trace sinks: before
        # 2026-08-12 this early return skipped ALL logging, so delegated tools
        # (executor matrx-user — apply_surface_write, war_room_*, matrx-local
        # tools) left ZERO rows in chat.tool_trace and were invisible to
        # /admin/debug-traces. The completion is recorded by the /tool_results
        # resolver (aidream/services/ai_execution/tool_results.py) as OK/FAIL
        # with kind=DELEGATE when the client posts the result back.
        if result.delegated_pending:
            try:
                _dl_conv_id = ctx.conversation_id or None
            except Exception:
                _dl_conv_id = None
            try:
                _dl_user_id: str | None = ctx.user_id or None
            except Exception:
                _dl_user_id = None
            _debug_log(
                "DELEGATED",
                tool=tool_name,
                kind=_dispatch_kind,
                conv=(_dl_conv_id or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "DELEGATED",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    args=arguments,
                    conversation_id=_dl_conv_id,
                    call_id=ctx.call_id,
                    user_id=_dl_user_id,
                    metadata={"disposition": "suspended_for_client"},
                ),
                name="tool_db_log_delegated",
            )
            await _file_input_drift()
            return result.to_tool_result_content(), result

        # --- Defense-in-depth: embedded-error-envelope detection ---
        # Some legacy tools (and any new ones written under the same
        # anti-pattern) return ``ToolResult(success=True, output={"success":
        # False, "error": "..."})`` — the outer flag says OK but the
        # payload says the underlying operation failed. The Pydantic
        # validator on ToolResult.output catches the str()-ed-dict variant;
        # this catches the native-dict variant. When detected, flip the
        # ToolResult to a structured failure BEFORE downstream consumers
        # (stream.error, log_error, _debug_log FAIL) read it, so all three
        # telemetry sinks record the truth instead of the outer lie.
        if (
            result.success
            and isinstance(result.output, dict)
            and result.output.get("success") is False
        ):
            embedded_err = (
                result.output.get("error")
                or result.output.get("message")
                or "Tool returned success=False inside its output payload."
            )
            result.success = False
            result.error = ToolError(
                error_type="embedded_error_envelope",
                message=str(embedded_err),
                is_retryable=False,
                suggested_action=(
                    "The tool wrapped a failure as a success envelope. "
                    "Inspect the original output and fix the tool to "
                    "raise or return ToolResult(success=False, ...) directly."
                ),
            )

        # --- Content IR: the tool's RESULT kind (KINDS_EVERYWHERE_PLAN §10d-C) ---
        # Two different things, and conflating them is what kept tools opaque:
        #
        #   * the GENERATED CONTRACT (`tool_io_<name>_<digest>_output`, derived
        #     from the row's hand-written `output_schema`) is an ABI fingerprint
        #     — it detects DRIFT. It is not an identity, it renders nowhere, and
        #     it is nobody's declaration.
        #   * the CURATED KIND is the result's identity, and — exactly as
        #     everywhere else in the platform — the payload SAYS SO ITSELF via
        #     its `__kind` field. A tool declares its result kind by RETURNING a
        #     KindModel; there is no second registry and no new column.
        #
        # So the payload's own declaration wins, verified against the live
        # catalog just like a workflow node's (scheduler.py runtime propagation:
        # "output kind = the kind of what actually flowed"). A payload lying
        # about itself screams exactly like author drift; a payload carrying no
        # `__kind` changes nothing and the generated contract still governs.
        # Both schemas describe the JSON wire value, never an in-memory
        # Pydantic object. Keep one serialization seam for the curated kind
        # check and the generated output-contract drift check. Passing a
        # BaseModel directly to ``check_schema`` makes every valid kinded tool
        # result look like a non-object and creates a false drift row.
        serialized_output = (
            result.output.model_dump(mode="json")
            if isinstance(result.output, BaseModel)
            else result.output
        )
        # A save that carries an automatic preview (kindcomp_* after a save) is handed
        # back as a media envelope so the model SEES the screenshots; the typed result
        # rides inside it. Every contract below judges that typed result, never the
        # envelope — judging the envelope filed ~650 false drift rows a day.
        enveloped_result = typed_result_inside_preview_envelope(serialized_output)
        if enveloped_result is not None:
            serialized_output = enveloped_result
        curated_kind = kind_of(serialized_output)
        output_drift_sources: list[str] = []
        output_drift_error_count = 0
        output_drift_errors: list[str] = []
        output_drift_kind: str | None = None
        if curated_kind == "json":
            # 'json' is a format word, never an identity — the same refusal the
            # scheduler makes when adopting a kind from a payload.
            curated_kind = None
        if curated_kind is not None:
            # Validate the SERIALIZED form: a tool may hand back the KindModel
            # itself, and the registered schema describes the wire shape.
            kind_check = await check_against_kind(serialized_output, curated_kind)
            if (
                kind_check.degraded_reason is not KindDegradedReason.KIND_NOT_REGISTERED
                and enveloped_result is None
            ):
                # Only a registered kind is stamped (content-ir rule 28); an
                # unregistered __kind is still screamed below.
                result.output_kind = curated_kind
                result.output_kind_version = kind_check.kind_version
                result.output_kind_checked = kind_check.checked
                result.output_kind_errors = list(kind_check.errors)
            if kind_check.errors:
                logger.error(
                    "[Content IR] tool result violates its self-described kind for %s (%s): %s",
                    canonical_name,
                    curated_kind,
                    kind_check.errors,
                )
                output_drift_sources.append("declared_kind")
                output_drift_error_count += len(kind_check.errors)
                output_drift_errors.extend(kind_check.errors)
                output_drift_kind = curated_kind
            elif not kind_check.checked:
                degraded_reason = (
                    kind_check.degraded_reason.value
                    if kind_check.degraded_reason is not None
                    else "unknown"
                )
                logger.warning(
                    "[Content IR] tool result kind check SKIPPED for %s (%s): %s "
                    "— a skipped check is never a pass.",
                    canonical_name,
                    curated_kind,
                    degraded_reason,
                )
                await _capture_tool_result_kind_unavailable(
                    ctx=ctx,
                    tool_name=canonical_name,
                    output_kind=curated_kind,
                    degraded_reason=degraded_reason,
                )

        if result.success:
            await _file_input_drift()  # the tool accepted what its contract refused: drift
        elif pending_input_drift:
            vcprint(
                f"[ToolExecutor] {canonical_name}: arguments outside its contract were refused "
                f"by the tool too (the model corrects it), call {ctx.call_id}",
                color="yellow",
            )

        # Failed tools have no successful output to validate. Their ToolError
        # is the contract; checking ``None`` against the success schema creates
        # a second false drift event that hides the actual failure.
        if (
            result.success
            and output_contract is not None
            and not is_catalog_status_receipt(curated_kind, output_drift_sources)
        ):
            output_kind_verdict = check_schema(serialized_output, output_contract.json_schema)
            if output_kind_verdict.errors:
                logger.error(
                    "[Content IR] tool output drift for %s (%s): %s",
                    canonical_name,
                    output_contract.kind,
                    output_kind_verdict.errors,
                )
                output_drift_sources.append("generated_output_contract")
                output_drift_error_count += len(output_kind_verdict.errors)
                output_drift_errors.extend(output_kind_verdict.errors)
                output_drift_kind = output_drift_kind or output_contract.kind

        # One successful tool result may violate both its self-described kind
        # and its generated output schema. They are distinct diagnostics, but
        # one durable repair signal must describe the one bad result rather
        # than creating duplicate queue work.
        if result.success and output_drift_sources and output_drift_kind is not None:
            await _capture_tool_output_contract_drift(
                ctx=ctx,
                tool_name=canonical_name,
                output_kind=output_drift_kind,
                error_count=output_drift_error_count,
                validation_sources=tuple(output_drift_sources),
                errors=output_drift_errors,
            )

        # The RUNTIME half of the reconciled tool measure (§10g GAP 3). A tool
        # listed in ``TOOL_RESULT_KINDS`` has a stored ``output_schema`` derived
        # from that model, so every reader that never runs the tool has been
        # told what comes back. If the implementation stops returning the model
        # — a branch nobody converted, a dict slipped in on an error path — that
        # promise is silently false. Scream instead: same loud-but-open posture
        # as everywhere else, the call still succeeds.
        declared_slug = result_kind_slug(canonical_name)
        if result.success and declared_slug is not None and curated_kind != declared_slug:
            logger.error(
                "[Content IR] DECLARED tool result kind missing for %s: expected "
                "%r from the returned KindModel, payload carries %r. The stored "
                "output_schema promises a shape this branch does not return — "
                "convert the branch (matrx_ai/tools/kinds/__init__.py names the "
                "declaration) or remove the declaration.",
                canonical_name,
                declared_slug,
                curated_kind,
            )
            result.output_kind_errors = [
                *result.output_kind_errors,
                f"declared result kind {declared_slug!r} not carried by the payload",
            ]
            await _capture_tool_result_kind_missing(
                ctx=ctx,
                tool_name=canonical_name,
                output_kind=declared_slug,
            )

        # --- Surface the arg-coercion / inference notice to the MODEL ---
        # When the pre-flight healed JSON-string args or inferred a missing
        # action/command, the model must LEARN the correct shape, not just get
        # away with it: inject a notice key into a dict output so it rides the
        # tool result into context. Non-dict outputs fall back to the log +
        # COERCED/INFERRED trace events only.
        # A non-dict output carries the same notice as a model notice (rendered
        # after the content by ToolResult.to_tool_result_content) — the log +
        # trace events alone would leave the model repeating the mistake.
        if coerced_fields:
            _coerce_notice = (
                f"NOTICE: argument(s) {', '.join(repr(f) for f in coerced_fields)} "
                "were sent as JSON-encoded strings; the server decoded them to "
                "native JSON this time. Next call, pass the raw JSON "
                "object/array itself — not a quoted string."
            )
            if isinstance(result.output, dict):
                result.output.setdefault("arg_coercion_notice", _coerce_notice)
            else:
                result.model_notices.append(_coerce_notice)
        if inferred_discriminator:
            _idf, _idt = inferred_discriminator
            _infer_notice = (
                f"NOTICE: {_idf!r} was omitted; inferred {_idf}={_idt!r} from "
                f"the other fields. Next call, set {_idf}={_idt!r} explicitly."
            )
            if isinstance(result.output, dict):
                result.output.setdefault("arg_inference_notice", _infer_notice)
            else:
                result.model_notices.append(_infer_notice)
        if respelled_choices:
            result.model_notices.append(
                "NOTICE: accepted "
                + ", ".join(f"{f}={v!r} (you sent {s!r})" for f, s, v in respelled_choices)
                + ". Next call, use that exact spelling."
            )
        if pinned_changes:
            result.model_notices.append(
                f"NOTICE: this chat pins {tool_name}: {'; '.join(pinned_changes)}. "
                "The call ran with the pinned value."
            )
        if removed_variant_fields is not None:
            # The call ran WITHOUT these arguments: a model that sent, say,
            # categories to the wrong action got a different answer than it
            # asked for, so it is told — on every result shape, success or not.
            _rdisc, _raction, _rfields = removed_variant_fields
            result.model_notices.append(
                f"NOTICE: ignored argument(s) for {_rdisc}={_raction!r}: "
                f"{', '.join(_rfields)} — not accepted by this {_rdisc}, so the call "
                "ran without them. Send them only with the "
                f"{_rdisc} that takes them."
            )
        # Each model notice is also a tool_step: streamed live (the person sees
        # it) and persisted in execution_events, which is where a rebuilt turn
        # reads it back (``_conversation_rebuild_impl``) — cx_tool_call.output
        # stays the tool's own output.
        # Known outcomes (a bot wall in a "successful" fetch, …) — every tool, one
        # ladder: `error_remedy.known_outcome_notices`. A hint never masks the result.
        try:
            result.model_notices.extend(
                known_outcome_notices(result, active_tools=allowed_tools)
            )
        except Exception as exc:  # noqa: BLE001
            vcprint(f"[ToolExecutor] known-outcome scan failed: {exc}", color="yellow")
        for _notice in result.model_notices:
            await stream.step(MODEL_NOTICE_STEP, _notice)

        # --- Contract repair: failure with no structured error ---
        # If a tool returns success=False but leaves ToolResult.error unset,
        # we used to surface a useless "Unknown error" to the model, the FE,
        # and all three telemetry sinks. Synthesise an error from result.output
        # instead so the failure detail is always visible — and stamp it with a
        # dedicated error_type so the tool author can find and fix the leak.
        if not result.success and result.error is None:
            try:
                output_preview = json.dumps(result.output, default=str)[:4000]
            except Exception:
                output_preview = str(result.output)[:4000]
            result.error = ToolError(
                reported_failure=f"tool {tool_name!r} itself (success=False with no ToolError)",
                error_type="missing_error_field",
                message=(
                    f"Tool {tool_name!r} returned success=False but did not "
                    f"populate ToolResult.error. Synthesised from output: "
                    f"{output_preview}"
                ),
                is_retryable=False,
                suggested_action=(
                    "Fix the tool to populate ToolResult.error when returning "
                    "success=False. Per-item failure details (if any) are in "
                    "the message above and in the original output payload."
                ),
            )

        if (
            not result.success
            and canonical_name == "context_patch"
            and result.error is not None
            and result.error.error_type == "patch_no_match"
        ):
            await _capture_context_patch_no_match(ctx=ctx)

        # Normalize result metadata before the completion event snapshots the
        # output.  ToolStreamManager stores a validated copy, so mutating the
        # ToolResult afterward cannot repair NUL bytes already captured in
        # execution_events.
        self.execution_logger.prepare_metadata(result)

        # --- Stream completed / error (with full result — non-negotiable) ---
        if result.success:
            # The surface-write receipt rides ONE tool_step just before
            # completion: streamed live, persisted in execution_events, never in
            # the model's tool result (matrx_ai.tools.surface_write).
            if result.surface_write is not None:
                from matrx_ai.tools.surface_write import SURFACE_WRITE_STEP

                await stream.step(
                    SURFACE_WRITE_STEP,
                    "Recorded the change",
                    data=result.surface_write.model_dump(),
                )
            if result.site_icons:
                from matrx_ai.tools.site_icons import SITE_ICONS_STEP

                await stream.step(
                    SITE_ICONS_STEP,
                    "Site icons",
                    data={"icons": result.site_icons},
                )
            # Self-corrected slips: earlier failed calls this success recovers ride the completion
            # event (`supersedes`) so a client's failed count is right while the turn runs; the same
            # ids are stamped on those rows (`metadata.superseded_by`) below.
            from matrx_ai.tools.turn_ledger import claim_superseded

            _superseded = claim_superseded(ctx.call_id or str(row_id or ""))
            await stream.completed(
                "Done",
                result=result,
                supersedes=[e.key for e in _superseded],
            )
        else:
            _superseded = []
            await stream.error(result.error.message, result.error.error_type)

        # --- Phase 2: log result (fire-and-forget UPDATE) ---
        events = stream.get_events_for_persistence()
        events.append(
            {
                "event": "content_ir_contract",
                "input": {
                    "kind": result.input_kind,
                    "version": result.input_kind_version,
                    "checked": result.input_kind_checked,
                    "errors": result.input_kind_errors,
                },
                "output": {
                    "kind": result.output_kind,
                    "version": result.output_kind_version,
                    "checked": result.output_kind_checked,
                    "errors": result.output_kind_errors,
                },
            }
        )
        # Capture the request-scoped WriteCoordinator NOW, while we are still in
        # the live request context. detached_task runs the completion write in a
        # FRESH contextvars Context (to isolate the asyncpg connection), which
        # also hides the coordinator ContextVar — without this hand-off the
        # UPDATE would fall back to a direct DB write that races the row's
        # deferred INSERT and gets silently lost (the status='error'+success=true
        # phantom-row bug). Passing the object in keeps the UPDATE on the same
        # Session as the INSERT, ordered after it. None outside a request scope.
        from matrx_ai.persistence.queue_helpers import get_coordinator as _get_coord

        _log_coord = _get_coord()
        # In-request: queue the UPDATE INLINE onto the coordinator (in-memory,
        # no DB I/O) so it deterministically coalesces with the row's INSERT and
        # flushes at the turn barrier. Out-of-request: detached_task isolates the
        # real DB write. See _persist_tool_outcome for the full rationale (this
        # is the fix for agent_call's lost completion write → watchdog phantom).
        if result.success:
            await self._persist_tool_outcome(
                self.execution_logger.log_completed(row_id, result, events, coordinator=_log_coord),
                coordinator=_log_coord,
                name="tool_log_completed",
            )
        else:
            await self._persist_tool_outcome(
                self.execution_logger.log_error(row_id, result, events, coordinator=_log_coord),
                coordinator=_log_coord,
                name="tool_log_error",
            )

        if _superseded:
            await self._persist_tool_outcome(
                self.execution_logger.mark_superseded(
                    _superseded, ctx.call_id or str(row_id or ""), coordinator=_log_coord
                ),
                coordinator=_log_coord,
                name="tool_mark_superseded",
            )

        if cancellation_after_completion is not None:
            vcprint(
                f"[ToolExecutor] Must-complete tool '{tool_name}' reached a terminal "
                "result and its outcome was persisted; propagating the deferred "
                "request cancellation now.",
                color="yellow",
            )
            raise cancellation_after_completion

        # User-id capture for the DB sink. ctx.user_id is a property that
        # reads from AppContext and may raise when called outside a request;
        # swallow so telemetry never blocks dispatch.
        try:
            _trace_user_id: str | None = ctx.user_id or None
        except Exception:
            _trace_user_id = None
        # ctx.conversation_id also reads AppContext and RAISES out of request — wrap
        # it identically (the size gate now depends on this for the overflow key).
        try:
            _trace_conv_id_full = ctx.conversation_id or None
        except Exception:
            _trace_conv_id_full = None

        if result.success:
            # Verbose mode (the host's `verbose` trace switch) adds args + a
            # truncated result preview to OK events. Use this when chasing
            # a silent-success bug — the trace file grows much faster, but
            # you get forensic detail without joining cx_tool_call.
            verbose_extra: dict[str, Any] = {}
            if _debug_verbose():
                try:
                    verbose_extra["args"] = json.dumps(arguments, default=str)
                except Exception:
                    verbose_extra["args"] = str(arguments)
                if result.output is not None:
                    try:
                        verbose_extra["result"] = json.dumps(result.output, default=str)
                    except Exception:
                        verbose_extra["result"] = str(result.output)
            _debug_log(
                "OK",
                tool=tool_name,
                kind=_dispatch_kind,
                ms=result.duration_ms,
                conv=(_trace_conv_id_full or "")[:8],
                call=ctx.call_id,
                **verbose_extra,
            )
            # DB sink — always retain the bounded result preview. Downstream
            # review/audit consumers must be able to fact-check successful
            # calls; _db_log caps the serialized value at 4 KiB.
            detached_task(
                _db_log(
                    "OK",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    duration_ms=result.duration_ms,
                    args=arguments,
                    result_preview=result.output,
                    conversation_id=_trace_conv_id_full,
                    call_id=ctx.call_id,
                    user_id=_trace_user_id,
                ),
                name="tool_db_log_OK",
            )
        else:
            # Failures get the full forensic detail: args (truncated),
            # error type, error message. This is the data the operator
            # actually needs to triage — don't make them join against
            # the DB to find it.
            try:
                args_blob = json.dumps(arguments, default=str)
            except Exception:
                args_blob = str(arguments)
            _err_type = result.error.error_type if result.error else "unknown"
            _err_msg = result.error.message if result.error else "no error message"
            _err_tb = result.error.traceback if result.error else None
            _expected_domain_failure = _is_expected_domain_failure(
                tool_name=canonical_name,
                error_type=_err_type,
                message=_err_msg,
            )
            if not _expected_domain_failure:
                await _capture_tool_execution_failed(
                    ctx=ctx,
                    tool_name=canonical_name,
                    error_type=_err_type,
                    message=_err_msg,
                    traceback_text=_err_tb,
                )

            # SCREAM. A tool failure is a REAL failure and it goes to the
            # console, always — the two sinks below are durable but SILENT
            # (a file under .matrx-debug/ and a chat.tool_trace row), so for
            # years a tool could fail every single call and the terminal
            # showed nothing but a happy stream. Whoever is watching the
            # server MUST see this without opening a log file or a DB.
            #
            # The traceback is printed when we have one. We often DON'T,
            # because the tool caught its own exception and stringified it
            # (`message=f"... {exc}"`) — that destroys the stack before it can
            # ever reach here. That is a defect in the tool, not here; the
            # `no traceback` line below names it so the tool gets fixed.
            vcprint(
                "\n"
                "╔══════════════════════════════════════════════════════════════════╗\n"
                "║  TOOL CALL FAILED                                                ║\n"
                "╚══════════════════════════════════════════════════════════════════╝\n"
                f"  tool:       {tool_name}  (kind={_dispatch_kind}, {result.duration_ms}ms)\n"
                f"  error_type: {_err_type}\n"
                f"  message:    {_err_msg}\n"
                f"  conv:       {_trace_conv_id_full or '-'}\n"
                f"  call_id:    {ctx.call_id}\n"
                f"  args:       {args_blob[:2000]}\n"
                + (
                    f"  traceback:\n{_err_tb}"
                    if _err_tb
                    else _missing_traceback_line(
                        tool_name, result.error, expected=_expected_domain_failure
                    )
                ),
                color="yellow" if _expected_domain_failure else "red",
            )

            _debug_log(
                "FAIL",
                tool=tool_name,
                kind=_dispatch_kind,
                ms=result.duration_ms,
                args=args_blob,
                err_type=_err_type,
                err_msg=_err_msg,
                tb=_err_tb,
                conv=(_trace_conv_id_full or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "FAIL",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    duration_ms=result.duration_ms,
                    args=arguments,
                    err_type=_err_type,
                    err_msg=_err_msg,
                    # No schema change needed — chat.tool_trace.metadata is jsonb.
                    # Without this the durable row recorded the error MESSAGE but
                    # threw the stack away, so /admin/debug-traces could tell you
                    # THAT a tool broke but never WHERE.
                    metadata={"traceback": _err_tb} if _err_tb else None,
                    conversation_id=_trace_conv_id_full,
                    call_id=ctx.call_id,
                    user_id=_trace_user_id,
                ),
                name="tool_db_log_FAIL",
            )

        # --- Layer 1: universal tool-result size gate (source-aware, graceful) ---
        # Cap what the model SEES from this result so a runaway payload (the 1.8 MB
        # note dump) can't be re-billed on every loop iteration. A tool that
        # self-managed (output_self_capped) is trusted; everything else over the
        # soft cap is truncated-with-notice, its full payload cached for
        # fetch_tool_result, and the firing recorded (a defect for tools we own, an
        # expected event for external/MCP). Runs on EVERY output-carrying result —
        # the single convergence point all tool kinds reach.
        #
        # WHICH PART reaches the agent is decided here too (2026-09-20). The cut
        # used to be purely positional — keep the first 50,000 characters — and
        # position is not relevance: the answer is as likely to be at character
        # 300,000 as at character 300. Deciding by relevance needs to know what
        # the agent is currently pursuing, which is exactly what this seam never
        # had. The orchestrator now hands that down on ctx.gate_context, and the
        # tool's OWN arguments (in scope right here, dropped before the gate
        # until now) are merged in. With no Holder bound to the deciding
        # mandate, the positional cut stays and the notice says so.
        content_dict = result.to_tool_result_content()
        _tool_kind = tool_kind_label(tool_def.tool_type)
        _gate_context = getattr(ctx, "gate_context", None)
        if _gate_context is not None and isinstance(arguments, dict) and arguments:
            _gate_context = replace(_gate_context, tool_input=arguments, iteration=ctx.iteration)
        _pre_gate_content = content_dict.get("content")
        content_dict, _gate_truncated = await apply_size_gate_async(
            content_dict,
            output_self_capped=result.output_self_capped,
            tool_name=tool_name,
            tool_kind=_tool_kind,
            conversation_id=_trace_conv_id_full,
            user_id=_trace_user_id,
            gate_context=_gate_context,
        )
        # Watch AI's cut trail (matrx_utils.raw_capture): what the gate cut, with the pre-cut text kept.
        _note_gate_cut(_pre_gate_content, content_dict.get("content"), truncated=_gate_truncated)
        if _gate_truncated:
            if _tool_kind in ("native", "agent"):
                await _capture_tool_result_size_unmanaged(ctx=ctx, tool_name=tool_name)
            # Inject-on-truncation: make fetch_tool_result available on the NEXT
            # turn so the notice's promise ("call fetch_tool_result …") is real,
            # without bloating the default toolset. Idempotent — the merge dedups
            # by name, so repeated truncations don't pile up. Best-effort.
            #
            # The notice names fetch_tool_result, so it must be a step the model
            # can actually take: the tool must exist in this registry and there
            # must be a request context for the queued addition to land in (a
            # direct/MCP/workflow dispatch has none). Otherwise the pointer is
            # rewritten to a step the model CAN take — call this tool again,
            # narrower — and the miss is logged.
            _offered = False
            if self.registry.get("fetch_tool_result") is not None:
                from matrx_ai.context.app_context import try_get_app_context

                if try_get_app_context() is not None:
                    try:
                        ctx.queue_tool_changes(
                            add=[{"kind": "registered", "name": "fetch_tool_result"}]
                        )
                        _offered = True
                    except Exception as inj_exc:  # noqa: BLE001 — never break dispatch
                        vcprint(
                            f"[ToolExecutor] fetch_tool_result injection failed: {inj_exc}",
                            color="yellow",
                        )
            if not _offered and isinstance(content_dict.get("content"), str):
                logger.warning(
                    "[ToolExecutor] %r result was shortened but fetch_tool_result cannot be "
                    "offered in this run; the notice names a re-call instead",
                    tool_name,
                )
                from matrx_ai.tools.output_caps import without_fetch_pointer

                content_dict["content"] = without_fetch_pointer(
                    content_dict["content"], tool_name=tool_name
                )
                content_dict["output_chars"] = len(content_dict["content"])
        return content_dict, result

    # ------------------------------------------------------------------
    # Batch execution
    # ------------------------------------------------------------------

    def _write_chain_key(
        self,
        called: str,
        arguments: Any,
        client_tools: frozenset[str] | None,
    ) -> str | None:
        """The tool a call WRITES through, or None when it may run concurrently.

        Read through the destructive-operations register: a call whose
        invocation class is read-only (or a paid read) is None. Anything else —
        including an unclassified or unresolvable tool, read fail-closed as the
        most destructive class — is keyed by its canonical tool name, so every
        write to that tool in one batch runs in emission order.
        """
        from matrx_ai.tools.agent_projection import lookup_projected_tool
        from matrx_ai.tools.side_effect_class import (
            PAID_READ,
            READ_ONLY,
            effective_invocation_side_effect_class,
        )
        from matrx_ai.tools.tool_aliases import lookup_canonical

        if not called or (client_tools and called in client_tools):
            return None
        try:
            name = self._normalize_called_name(called)
            if (client_tools and name in client_tools) or name in _INDEPENDENT_WRITES:
                return None
            tool_def = lookup_projected_tool(name)
            canonical = name
            if tool_def is None:
                aliased = lookup_canonical(name)
                if aliased is not None:
                    canonical = aliased
                tool_def = self.registry.get(canonical)
            if tool_def is not None and tool_def.tool_type == ToolType.AGENT:
                # A sub-agent fan-out is parallel on purpose; its own tool
                # calls are batched — and ordered — inside the child run.
                return None
            effect = effective_invocation_side_effect_class(
                tool_def, arguments, tool_name=canonical
            )
        except Exception:  # noqa: BLE001 — ordering is never a reason to fail dispatch
            return called
        if effect in (READ_ONLY, PAID_READ):
            return None
        return canonical

    async def execute_batch(
        self,
        tool_calls: list[dict[str, Any]],
        ctx_base: ToolContext,
        client_tools: frozenset[str] | None = None,
        allowed_tools: frozenset[str] | None = None,
    ) -> tuple[list[dict[str, Any]], list[ToolResult]]:
        """Execute multiple tool calls concurrently — except that the writes
        to one tool run in the order the model emitted them (``_write_chain_key``).

        Each item in ``tool_calls`` must have:
          - ``name``: tool name
          - ``arguments``: dict of arguments
          - ``call_id`` or ``id``: the tool call id
        """
        child_contexts: list[ToolContext] = []
        # 🚨 WRITES TO ONE TOOL RUN IN THE ORDER THE MODEL EMITTED THEM.
        # A model that says "create the sections, then file these rules under
        # them" emits both calls in one response. Running them concurrently let
        # the second read the record before the first had written it (walk 24:
        # `rulebook` update_meta started 2.5 ms before add_rules; add_rules
        # read "Its sections are: `G`" and was refused, and the model's retry
        # narration leaked to the Expert). Each write chain runs its calls one
        # after another, each in its OWN child task (so per-task ContextVar
        # isolation is unchanged); read-only calls and different tools still
        # run concurrently. Client-delegated tools are not chained — the
        # client owns their execution.
        chains: dict[str, list[int]] = {}
        chain_of: list[str | None] = []
        for idx, tc in enumerate(tool_calls):
            name = tc.get("name", "")
            arguments = tc.get("arguments", {})
            call_id = tc.get("call_id") or tc.get("id") or str(uuid4())

            child_ctx = ctx_base.model_copy(
                update={
                    "call_id": call_id,
                    "tool_name": name,
                }
            )
            child_contexts.append(child_ctx)
            key = self._write_chain_key(name, arguments, client_tools)
            chain_of.append(key)
            if key is not None:
                chains.setdefault(key, []).append(idx)

        def _run(idx: int) -> Awaitable[tuple[dict[str, Any], ToolResult]]:
            tc = tool_calls[idx]
            return self.execute(
                tc.get("name", ""),
                tc.get("arguments", {}),
                child_contexts[idx],
                client_tools,
                allowed_tools,
            )

        slots: list[Any] = [None] * len(tool_calls)

        def _batch_cancelled() -> bool:
            task = asyncio.current_task()
            return bool(task and task.cancelling())

        # Every call's outcome lands in its own slot, exactly as the previous
        # gather(return_exceptions=True) recorded it — a call canceled on its
        # own (not the batch) is that call's result, never a sibling's loss.
        async def _run_chain(indices: list[int]) -> None:
            for idx in indices:
                try:
                    slots[idx] = await asyncio.create_task(_run(idx))
                except asyncio.CancelledError as exc:
                    if _batch_cancelled():
                        raise
                    slots[idx] = exc
                except Exception as exc:  # noqa: BLE001 — mirrors gather(return_exceptions=True)
                    slots[idx] = exc

        async def _run_one(idx: int) -> None:
            try:
                slots[idx] = await _run(idx)
            except asyncio.CancelledError as exc:
                if _batch_cancelled():
                    raise
                slots[idx] = exc
            except Exception as exc:  # noqa: BLE001 — mirrors gather(return_exceptions=True)
                slots[idx] = exc

        # Reporters (``_READS_AFTER_ITS_BATCH``) wait only for the siblings they report on.
        names = [self._normalize_called_name(str(tc.get("name", "") or "")) for tc in tool_calls]
        done = [asyncio.Event() for _ in tool_calls]
        waits: dict[int, list[int]] = {}
        if len(tool_calls) > 1 and _READS_AFTER_ITS_BATCH:
            for idx, name in enumerate(names):
                after = _READS_AFTER_ITS_BATCH.get(name)
                if after and chain_of[idx] is None:
                    siblings = [j for j, other in enumerate(names) if j != idx and other in after]
                    if siblings:
                        waits[idx] = siblings

        async def _then(idx: int, unit: Awaitable[None]) -> None:
            try:
                await unit
            finally:
                done[idx].set()

        async def _chain_then(indices: list[int]) -> None:
            try:
                await _run_chain(indices)
            finally:
                for idx in indices:
                    done[idx].set()

        async def _report_after(idx: int) -> None:
            await asyncio.gather(*(done[j].wait() for j in waits[idx]))
            await _run_one(idx)

        units: list[Awaitable[None]] = [
            _report_after(idx) if idx in waits else _then(idx, _run_one(idx))
            for idx, key in enumerate(chain_of)
            if key is None
        ]
        units.extend(_chain_then(indices) for indices in chains.values())

        from matrx_ai.tools.host_park import tool_batch_scope

        try:
            # ONE STEP, ONE ASK: the step's calls share a batch scope, so a host that asks the
            # person about several of them (the apply gate) asks once (``host_park.ToolBatch``).
            with tool_batch_scope(ctx.call_id for ctx in child_contexts):
                await asyncio.gather(*units)
        except asyncio.CancelledError:
            # The BATCH was cancelled (client disconnect, shutdown, parent run
            # stopped). Every call without an outcome ends recorded — never
            # silent — and then the cancellation propagates unchanged.
            await asyncio.shield(
                self._record_cancelled_batch(
                    tool_calls, child_contexts, slots, ctx_base, client_tools
                )
            )
            raise
        raw_results = slots

        content_results: list[dict[str, Any]] = []
        full_results: list[ToolResult] = []

        for idx, r in enumerate(raw_results):
            if isinstance(r, BaseException):
                tc = tool_calls[idx]
                child_ctx = child_contexts[idx]
                call_id = child_ctx.call_id
                tool_name_str = tc.get("name", "")
                error_traceback = "".join(tb.format_exception(type(r), r, r.__traceback__))
                err_result = ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="unhandled",
                        message=str(r),
                        traceback=error_traceback,
                    ),
                    started_at=time.time(),
                    completed_at=time.time(),
                    tool_name=tool_name_str,
                    call_id=call_id,
                )
                # Stream the unhandled exception as a tool_error so the client
                # knows this specific call failed rather than seeing silence.
                stream = ToolStreamManager(ctx_base.emitter, call_id, tool_name_str)
                await stream.error(str(r), error_type="unhandled")
                self.execution_logger.prepare_metadata(err_result)
                row_id = self.execution_logger.row_id_for_call(child_ctx)
                if row_id:
                    from matrx_ai.persistence.queue_helpers import (
                        get_coordinator as _get_coord,
                    )

                    coordinator = _get_coord()
                    await self._persist_tool_outcome(
                        self.execution_logger.log_error(
                            row_id,
                            err_result,
                            stream.get_events_for_persistence(),
                            coordinator=coordinator,
                        ),
                        coordinator=coordinator,
                        name="tool_log_unhandled_error",
                    )
                content_results.append(err_result.to_tool_result_content())
                full_results.append(err_result)
            else:
                content_dict, full_result = r
                content_results.append(content_dict)
                full_results.append(full_result)

        return content_results, full_results

    async def _record_cancelled_batch(
        self,
        tool_calls: list[dict[str, Any]],
        child_contexts: list[ToolContext],
        slots: list[Any],
        ctx_base: ToolContext,
        client_tools: frozenset[str] | None,
    ) -> None:
        """Record a terminal ``cancelled`` outcome for every unfinished call.

        2026-11-07: a cancelled archestra batch left no FAIL row and no error.
        In-flight server calls close their own ledger row inside ``execute``
        (``log_abandoned``); a call still queued behind a write chain, or
        cancelled before it reached dispatch, had no row at all and vanished.
        Here every unfinished call gets a FAIL trace, a call with no ledger row
        gets a born-terminal ``cancelled`` row, and the batch is captured once.
        Best-effort: never raises (the caller re-raises the cancellation).
        Guard: tests/test_cancelled_batch_records_every_call.py.
        """
        unfinished: list[str] = []
        for idx, slot in enumerate(slots):
            if slot is not None:
                continue
            child_ctx = child_contexts[idx]
            tc = tool_calls[idx]
            name = tc.get("name", "")
            call_id = child_ctx.call_id
            unfinished.append(call_id)
            message = (
                f"Tool '{name}' was cancelled with its batch before it returned a "
                "result (the request was cancelled)."
            )
            try:
                is_delegated = bool(client_tools and name in client_tools)
                row_id = self.execution_logger.row_id_for_call(child_ctx)
                if is_delegated and row_id:
                    # A delegated row stays 'delegated': the client owns it.
                    continue
                detached_task(
                    _db_log(
                        "FAIL",
                        tool_name=name,
                        kind="SERVER",
                        duration_ms=None,
                        args=tc.get("arguments", {}),
                        err_type="cancelled",
                        err_msg=message,
                        conversation_id=child_ctx.conversation_id or None,
                        call_id=call_id,
                        user_id=child_ctx.user_id or None,
                    ),
                    name="tool_db_log_batch_cancelled",
                )
                if not row_id:
                    now = time.time()
                    await self.execution_logger.log_rejected(
                        child_ctx,
                        tool_name=name,
                        arguments=tc.get("arguments", {}) or {},
                        result=ToolResult(
                            success=False,
                            error=ToolError(refusal=True, error_type="cancelled", message=message),
                            started_at=now,
                            completed_at=now,
                            tool_name=name,
                            call_id=call_id,
                        ),
                    )
            except Exception as exc:  # noqa: BLE001 — recording must never mask the cancel
                vcprint(
                    f"[ToolExecutor] Failed to record cancelled call {call_id} ({name}): {exc}",
                    color="red",
                )
        if not unfinished:
            return
        from matrx_connect.streaming.run_tracking import host_is_shutting_down

        if host_is_shutting_down():
            # A deploy drain cut the batch: the calls are recorded above, and the cut belongs to the
            # layer that owns the turn — the stream files ``stream_cancelled`` when nothing resumes it,
            # and a durable run is the run reaper's to judge (``runtime_execution_abandoned`` only when
            # nothing resumes it). Filing here too alarmed every deploy-cut batch twice, resumed or not
            # (2026-11-16, 2026-11-19: both ``tool_batch_cancelled`` rows were deploy drains).
            vcprint(
                f"[ToolExecutor] Tool batch cut by a server shutdown with {len(unfinished)} unfinished "
                "call(s); the stream or the run reaper judges the cut",
                color="yellow",
            )
            return
        try:
            from matrx_connect.streaming import error_capture as _error_capture

            await _error_capture.capture_error(
                asyncio.CancelledError(
                    f"Tool batch cancelled with {len(unfinished)} unfinished call(s)"
                ),
                kind=TOOL_BATCH_CANCELLED_KIND,
                request_id=ctx_base.request_id or None,
                user_id=ctx_base.user_id or None,
                conversation_id=ctx_base.conversation_id or None,
                route="tool_executor.execute_batch",
                error_type="CancelledError",
                context={
                    "unfinished_call_ids": unfinished,
                    "tool_names": sorted(
                        {
                            tool_calls[i].get("name", "")
                            for i, slot in enumerate(slots)
                            if slot is None
                        }
                    ),
                    "batch_size": len(tool_calls),
                },
            )
        except Exception as exc:  # noqa: BLE001 — capture is best-effort
            vcprint(f"[ToolExecutor] Failed to capture cancelled batch: {exc}", color="red")

    # ------------------------------------------------------------------
    # Mandate-candidate containment — borrowed / stopped calls never dispatch
    # ------------------------------------------------------------------

    async def _contain_candidate_call(
        self,
        ctx: ToolContext,
        tool_def: ToolDefinition,
        arguments: dict[str, Any],
        containment: Any,
        *,
        tool_name: str,
        as_called: str,
        started_at: float,
    ) -> tuple[dict[str, Any], ToolResult]:
        """Record a ``borrowed`` or ``stopped`` call; nothing is dispatched.

        borrowed — the model receives the live run's model-facing content
        exactly as the live model saw it (no result gate, no re-serialisation).
        stopped — the row closes as ``candidate_stopped``; the returned result
        carries ``candidate_stopped=True`` and ``handle_tool_calls_v2`` never
        hands it to the model. The run ends at the orchestrator's next check.
        """
        from matrx_ai.persistence.queue_helpers import get_coordinator as _get_coord

        record = containment.as_record()
        row_id = await self.execution_logger.log_started(
            ctx,
            tool_def,
            arguments,
            exposed_name=as_called,
            candidate_disposition=record,
        )
        coordinator = _get_coord()

        if containment.disposition == "borrowed":
            borrowed = containment.borrowed
            content = borrowed.content
            chars = len(content) if isinstance(content, str) else len(str(content))
            preview = {"chars": chars, "borrowed_from_call_id": borrowed.live_call_id}
            result = ToolResult(
                success=not borrowed.is_error,
                provider_content=content,
                error=(
                    ToolError(
                        reported_failure="the earlier identical call whose error this borrows",
                        error_type="candidate_borrowed_error",
                        message=(content if isinstance(content, str) else str(content)),
                    )
                    if borrowed.is_error
                    else None
                ),
                output_chars=chars,
                output_preview=preview,
                candidate_disposition=record,
                tool_name=tool_name,
                call_id=ctx.call_id,
                started_at=started_at,
                completed_at=time.time(),
            )
            result.compute_duration()
            log = (
                self.execution_logger.log_error(row_id, result, [], coordinator=coordinator)
                if borrowed.is_error
                else self.execution_logger.log_completed(
                    row_id, result, [], coordinator=coordinator
                )
            )
            await self._persist_tool_outcome(
                log, coordinator=coordinator, name="tool_log_candidate_borrowed"
            )
            content_dict: dict[str, Any] = {
                "tool_use_id": ctx.call_id,
                "call_id": ctx.call_id,
                "name": tool_name,
                "content": content,
                "is_error": bool(borrowed.is_error),
                "output_chars": chars,
                "output_preview": preview,
                "approved_max_chars": None,
            }
            return content_dict, result

        stop = {
            "step": containment.seq,
            "tool": tool_def.name,
            "class": containment.side_effect_class,
        }
        await self._persist_tool_outcome(
            self.execution_logger.log_abandoned(
                row_id,
                reason="candidate_stopped",
                error_message=(
                    f"Candidate run stopped before this call at step {containment.seq}: "
                    f"{containment.stopped_reason}. Nothing was executed."
                ),
                coordinator=coordinator,
            ),
            coordinator=coordinator,
            name="tool_log_candidate_stopped",
        )
        result = ToolResult(
            success=False,
            candidate_stopped=True,
            candidate_disposition=record,
            tool_name=tool_name,
            call_id=ctx.call_id,
            started_at=started_at,
            completed_at=time.time(),
        )
        result.compute_duration()
        vcprint(
            f"[ToolExecutor] mandate candidate STOPPED at step {containment.seq}: "
            f"{tool_def.name} ({containment.side_effect_class}) — {containment.stopped_reason}",
            color="yellow",
        )
        return _candidate_stopped_content(result, stop), result

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    async def _dispatch(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        stream: ToolStreamManager,
        client_tools: frozenset[str] | None = None,
        row_id: str = "",
        authorization_metadata: dict[str, Any] | None = None,
    ) -> ToolResult:
        """Route one tool call, with the AI that made it named on every write.

        🚨 AN AGENT-TIER WRITE NAMES ITSELF. A tool call IS an AI acting: the
        model chose the tool and the arguments. Nothing on this lane sets
        ``app.user_id`` (a durable/background run has no request identity at all),
        so an undeclared write resolves to tier ``system`` with a NULL
        ``app.actor_system`` and ``wf_051``'s CHECK refuses it outright — live
        2026-09-12 23:24, the Masterwork Conductor's ``workflow_plan build_agent``
        could not change how a desk's Writer thinks, and the whole
        teach-by-conversation loop was blocked behind it.

        So the declaration lives HERE, at the one dispatch edge every tool of
        every type passes through — the same shape as the MCP context edge
        (``aidream/api/mcp/agent_service/context_edge.py``) — and every present
        and future tool inherits it. ``declared_actor``, never ``actor_session``:
        a dispatcher above handlers that open their own transactions
        (``acting_as_user`` / ``rls_session`` refuse to nest) can only declare.
        A tool that knows a better system name nests its own declaration and
        wins (the ContextVar is innermost-first). Canonical account:
        ``common-docs/systems/architecture/provenance/FEATURE.md``.
        """
        # A lean row's `guide` is the row's own text: answered here, before any
        # executor or delegated client (neither has a `guide` of its own).
        from matrx_ai.tools.lean_envelope import row_guide, serves_row_guide

        if serves_row_guide(tool_def, args):
            return ToolResult(
                success=True,
                output=row_guide(tool_def, (args or {}).get("topic")),
                started_at=time.time(),
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        from matrx_orm import declared_actor

        from matrx_ai.tools.host_park import settle_parked, tool_call_scope

        # A host check below the tool (the Action apply gate) may park THIS call on a person
        # (``host_park``): its answer then becomes ``delegated_pending``, like ask_person's.
        async with declared_actor("agent", f"tool:{tool_def.name}"):
            with tool_call_scope(ctx) as scope:
                result = await self._dispatch_declared(
                    tool_def,
                    args,
                    ctx,
                    stream,
                    client_tools,
                    row_id,
                    authorization_metadata=authorization_metadata,
                )
            return settle_parked(scope, result)

    async def _dispatch_declared(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        stream: ToolStreamManager,
        client_tools: frozenset[str] | None = None,
        row_id: str = "",
        authorization_metadata: dict[str, Any] | None = None,
    ) -> ToolResult:
        # Client-delegated tools take priority over all other dispatch paths.
        # The tool is NOT executed server-side; instead a tool_delegated event is
        # emitted over the SSE stream and the executor suspends until the client
        # POSTs the result back.
        if client_tools and tool_def.name in client_tools:
            # Pre-suspend contract check. A delegated call hard-suspends the
            # loop and hands the args to the client; if the CLIENT then
            # rejects them against its own schema, the agent pays a full
            # suspend → reject → resume cycle for a mistake the server could
            # have caught in-line. Validate against the same schema the model
            # was shown; a failure is an ordinary failed tool result the model
            # corrects on its very next step (2026-09-13 incident: a 16-char
            # ``header`` on the ``user`` tool).
            schema_error = _validate_against_declared_schema(tool_def, args)
            if schema_error is not None:
                logger.warning(
                    "[ToolExecutor] delegated call %r rejected before suspend: %s",
                    tool_def.name,
                    schema_error,
                )
                return ToolResult(
                    success=False,
                    error=ToolError(
                        refusal=True,
                        error_type="validation",
                        message=(
                            f"Arguments for {tool_def.name} do not match its schema "
                            f"(checked before delegating to the client): {schema_error}"
                        ),
                        suggested_action=(
                            "Fix the named field(s) to satisfy the tool's input schema "
                            "and call the tool again."
                        ),
                    ),
                    started_at=time.time(),
                    completed_at=time.time(),
                    tool_name=tool_def.name,
                    call_id=ctx.call_id,
                )
            return await self._execute_delegated(
                tool_def,
                args,
                ctx,
                row_id,
                authorization_metadata=authorization_metadata,
            )

        # An old Matrx Local name with no Matrx Local attached, on a Matrx 2 computer: the ONE
        # router hands it to its Matrx 2 successor (matrx_ai/tools/implementations/legacy_local.py).
        from matrx_ai.tools.implementations.legacy_local import routes_to_matrx2, run_on_matrx2

        if routes_to_matrx2(tool_def.name):
            return await run_on_matrx2(tool_def.name, args, ctx)

        match tool_def.tool_type:
            case ToolType.LOCAL:
                # Host-executor precedence, dispatch-time layer: a LOCAL def
                # with no execution path of its own (no callable, no
                # function_path — e.g. a server/DB row for a tool the HOST
                # executes) routes to the host's registered external handler
                # when one exists, instead of dying in _execute_local. The
                # registry's load-time flip is the first layer; this one
                # catches defs that arrived after handlers were registered
                # (cache-bust reloads, late loads).
                if (
                    tool_def._callable is None
                    and not (tool_def.function_path or "").strip()
                    and self._has_external_handler(tool_def)
                ):
                    return await self._execute_external_handler(tool_def, args, ctx)
                return await self._execute_local(tool_def, args, ctx, stream)
            case ToolType.EXTERNAL_MCP:
                return await self._execute_external_mcp(tool_def, args, ctx)
            case ToolType.AGENT:
                return await self._execute_agent(tool_def, args, ctx)
            case ToolType.EXTERNAL_HANDLER:
                return await self._execute_external_handler(tool_def, args, ctx)
            case ToolType.CATALOG:
                return await self._execute_catalog(tool_def, args, ctx)
            case _:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        refusal=True,
                        error_type="configuration",
                        message=f"Unknown tool type: {tool_def.tool_type}",
                    ),
                    started_at=time.time(),
                    completed_at=time.time(),
                    tool_name=tool_def.name,
                    call_id=ctx.call_id,
                )

    async def _execute_delegated(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        row_id: str = "",
        authorization_metadata: dict[str, Any] | None = None,
    ) -> ToolResult:
        """Delegate a tool call to the connected client — a SUSPENSION POINT.

        Delegation does NOT block the loop. We (1) flip the cx_tool_call row to
        ``status='delegated'`` (the durable ledger entry) and (2) emit a
        ``tool_delegated`` event over the stream, then return a *pending* result
        immediately. The orchestrator detects ``delegated_pending`` and ends the
        turn. The client executes the tool and POSTs the result to
        ``POST /conversations/{id}/tool_results``; once no delegated rows remain,
        ``POST /conversations/{id}/resume`` reconstructs the conversation (now
        with the tool result) and continues the loop.

        This replaced an in-memory ``ClientToolWaiter.wait_for_result`` blocking
        await that (a) wasn't reliably blocking and (b) fed an empty result into
        the loop when it returned, causing the runaway tool-call loop. Full
        history: docs/tool_delegation/DELEGATION_LOOP_BUGS.md.
        """
        # The tool row alone is not a resumable stored turn. Checkpoint at the
        # actual handoff decision, after aliases and authorization have routed
        # the call. Ephemeral runs deliberately have no cx_message row.
        from matrx_ai.context.app_context import get_app_context
        from matrx_ai.context.events import ToolEventPayload

        if not row_id:
            # An UNSAVED run (store=False) has no chat.tool_call row to park on, so the handoff is in
            # memory, in this process (matrx_ai/tools/in_memory_handoff.py). With NO page attached at all
            # there is nobody to hand it to: answer the model plainly.
            return await self._delegate_in_memory(tool_def, args, ctx, authorization_metadata)
        if getattr(get_app_context(), "store", True):
            if ctx.assistant_checkpoint is not None:
                ctx.message_id = await ctx.assistant_checkpoint()
            if not ctx.message_id:
                raise RuntimeError("client delegation refused: no durable assistant tool_use message")
            from matrx_ai.db import cxm

            assistant_rows = await cxm.message.filter_items(id=ctx.message_id)
            assistant = assistant_rows[0] if assistant_rows else None
            assistant_call_ids = {
                str(block.get("call_id") or block.get("id"))
                for block in (getattr(assistant, "content", None) or [])
                if isinstance(block, dict)
                and block.get("type") == "tool_call"
                and (block.get("call_id") or block.get("id"))
            }
            if (
                assistant is None
                or assistant.role != "assistant"
                or assistant.status != "active"
                or ctx.call_id not in assistant_call_ids
            ):
                raise RuntimeError("client delegation refused: assistant tool_use is not durable")

        started_at = time.time()

        wait_seconds = int(tool_def.max_client_wait_seconds or delegated_call_abandon_seconds())
        expires_at = datetime.now(UTC) + timedelta(seconds=wait_seconds)

        # ── Durability checkpoint — TWO-STEP, NON-NEGOTIABLE ──────────────
        # (1) Queue the UPDATE that flips cx_tool_call to 'delegated' and stamps
        #     expires_at. Combined with the queued INSERT from log_started(),
        #     this is the FULL durable ledger entry the client will look up.
        # (2) `coordinator.finalize(...)` — synchronously flush + drain all
        #     in-flight commits so the row is ON DISK before we emit the
        #     `tool_delegated` event below.
        #
        # WITHOUT (2) the client's POST /tool_results racing this same row's
        # commit will return 404 and the conversation is stuck (the client has
        # no retry). The persistence contract names this as one of the three
        # deliberate blocking points: "the pre-suspend commit before a client-
        # delegated tool" (see CLAUDE.md, packages/matrx-ai/.../persistence
        # skill, and docs/tool_delegation/DELEGATION_LOOP_BUGS.md).
        #
        # We finalize OUTSIDE the emit so a PersistenceBarrierError aborts the
        # delegation entirely — better to fail loudly than to tell the client
        # "go ahead" without a durable ledger to recover against.
        # Desktop targeting is scoped to tools actually bound to the
        # matrx-local executor — a selected desktop target must never capture
        # browser-executed delegated tools (war_room_*, widget_*, ui-first):
        # their results would fail the /tool_results submission-binding check
        # (the browser sends no instance_id) → 404 → wedged turn, while the
        # desktop claims calls it cannot execute.
        is_desktop_bound = any(
            b == "matrx-local" or b.startswith("matrx-local.")
            for b in self.registry.bindings_for_tool(tool_def.name)
        )
        # (1)+(2)+(3) are ONE call now: `delegate_durably` queues the flip onto
        # the coordinator that owns the row, finalizes, and READS THE ROW BACK.
        # A park that cannot be proven on disk raises `DelegationNotDurable`
        # here instead of emitting `tool_delegated` over a ledger that does not
        # say 'delegated' — the 2026-09-22 `ask_person` failure, fixed for every
        # delegated tool at once.
        await self.execution_logger.delegate_durably(
            row_id,
            expires_at=expires_at,
            allow_desktop_target=is_desktop_bound,
            reason="tool_delegation",
        )

        emitter = ctx.emitter
        # THE HELD STREAM: a client that keeps reading gets its result waited for in this stream. The
        # lease is taken on the durable row BEFORE the event, so no result can land ahead of it.
        from matrx_ai.tools import delegated_hold

        hold = self._hold_settings(tool_def, emitter)
        if hold is not None and not await delegated_hold.claim(
            row_id, conversation_id=ctx.conversation_id or "", hold=hold
        ):
            hold = None
        if emitter is not None:
            target_instance_id = (
                self.execution_logger._desktop_target_instance_id() if is_desktop_bound else None
            )
            event_data: dict[str, Any] = {"arguments": args}
            if hold is not None:
                event_data["hold"] = {
                    "until": (datetime.now(UTC) + timedelta(seconds=hold.seconds)).isoformat(),
                    "reason": "client_tool",
                }
            # THE CALL'S OWN DEADLINE, when its tool declares one (``max_client_wait_seconds``): the client's
            # turn header keeps "Working" until it (a long recording, a slow upload) instead of its 10-minute
            # fallback. The default expiry is the 30-day abandon window — no UI deadline — so it is not sent.
            if tool_def.max_client_wait_seconds:
                event_data["step_deadline_at"] = expires_at.isoformat()
            if authorization_metadata:
                event_data["execution_authorization"] = authorization_metadata
            if target_instance_id:
                event_data["target_instance_id"] = target_instance_id
            await emitter.send_tool_event(
                ToolEventPayload(
                    event="tool_delegated",
                    call_id=ctx.call_id,
                    tool_name=tool_def.name,
                    message=f"Delegating {tool_def.name} to client",
                    show_spinner=True,
                    data=event_data,
                )
            )

        if hold is not None:
            held = await self._wait_for_client_result(tool_def, ctx, row_id, hold, started_at)
            if held is not None:
                return held

        # Pending marker — NOT a result. success=False keeps it out of any
        # success path; delegated_pending is the real signal. The caller
        # (execute) returns this without logging so the 'delegated' row stands.
        return ToolResult(
            success=False,
            delegated_pending=True,
            tool_name=tool_def.name,
            call_id=ctx.call_id,
            started_at=started_at,
            completed_at=time.time(),
        )

    @staticmethod
    def _hold_settings(tool_def: ToolDefinition, emitter: Any) -> Any:
        """This delegated call's wait in the open stream; ``None`` means park at once (as before)."""
        from matrx_ai.context.app_context import get_app_context
        from matrx_ai.processing.blocks.saved_blocks import client_reads
        from matrx_ai.tools import delegated_hold

        if emitter is None or not client_reads(get_app_context(), delegated_hold.HOLD_READ):
            return None
        return delegated_hold.settings(cap_seconds=tool_def.max_client_wait_seconds or None)

    async def _wait_for_client_result(
        self,
        tool_def: ToolDefinition,
        ctx: ToolContext,
        row_id: str,
        hold: Any,
        started_at: float,
    ) -> ToolResult | None:
        """Wait in the open stream for the client's result. A result, or ``None`` when the hold was given up."""
        from matrx_ai.tools import delegated_hold

        outcome = await delegated_hold.wait_for_result(
            row_id,
            conversation_id=ctx.conversation_id or "",
            call_id=ctx.call_id,
            hold=hold,
            stop_reason=self._hold_stop_reason(ctx),
        )
        return await self._held_outcome(tool_def, ctx, outcome, started_at, answered_by="the client")

    @staticmethod
    def _hold_stop_reason(ctx: ToolContext) -> Any:
        """The run's own stop look (Stop, interrupt, a spine control), asked on every tick of a held wait."""
        from matrx_ai.tools import delegated_hold

        request_id = str(getattr(ctx, "request_id", "") or "") or None

        async def stop_reason() -> tuple[delegated_hold.ReleaseReason, str] | None:
            from matrx_ai.orchestrator import executor as loop

            if loop._is_request_cancelled(request_id) or loop._is_request_interrupted(request_id):
                return "stopped", "the person stopped the turn"
            spine = await loop._spine_stop_reason()
            if spine:
                return ("stopped" if "cancel" in spine.lower() else "control"), spine
            return None

        return stop_reason

    @staticmethod
    async def _held_outcome(
        tool_def: ToolDefinition,
        ctx: ToolContext,
        outcome: Any,
        started_at: float,
        *,
        answered_by: str,
    ) -> ToolResult | None:
        """THE ONE END OF A HELD WAIT, client tool and person alike (RESUME-AND-RECOVERY 1a, 1b).

        Taken: ``tool_completed`` / ``tool_error`` with ``data.held``, and the stored row's own model-facing
        content (what a rebuild of the row gives). Given up: ``delegated_hold_released`` and ``None`` (the
        caller keeps its ``delegated_pending`` result and the turn parks).
        """
        from matrx_ai.context.events import InfoPayload, ToolEventPayload
        from matrx_ai.db._conversation_rebuild_impl import _rebuild_tool_result_content

        emitter = ctx.emitter
        if not outcome.taken:
            # The fallback announces itself: the turn parks and the client continues it by /resume.
            if emitter is not None:
                await emitter.send_info(
                    InfoPayload(
                        code="delegated_hold_released",
                        system_message=(
                            f"Stopped waiting in the stream for {tool_def.name} "
                            f"({outcome.reason}, {outcome.waited_ms} ms); the turn parks."
                        ),
                        user_message="",
                        metadata={
                            "call_id": ctx.call_id,
                            "tool_name": tool_def.name,
                            "reason": outcome.reason,
                            "waited_ms": outcome.waited_ms,
                        },
                    )
                )
            return None
        content = _rebuild_tool_result_content([outcome.row])[0]
        is_error = bool(getattr(outcome.row, "is_error", False))
        if emitter is not None:
            await emitter.send_tool_event(
                ToolEventPayload(
                    event="tool_error" if is_error else "tool_completed",
                    call_id=ctx.call_id,
                    tool_name=tool_def.name,
                    message=f"{tool_def.name} answered by {answered_by}",
                    show_spinner=False,
                    data=(
                        {
                            "error_type": str(getattr(outcome.row, "error_type", None) or "client_tool_error"),
                            "detail": getattr(outcome.row, "error_message", None),
                            "held": True,
                            "waited_ms": outcome.waited_ms,
                        }
                        if is_error
                        else {
                            "result_omitted": True,
                            "output_chars": getattr(outcome.row, "output_chars", None),
                            "tool_call_id": str(outcome.row.id),
                            "held": True,
                            "waited_ms": outcome.waited_ms,
                        }
                    ),
                )
            )
        return ToolResult(
            success=not is_error,
            client_resolved_content=content,
            output_chars=getattr(outcome.row, "output_chars", None) or 0,
            output_preview=getattr(outcome.row, "output_preview", None),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
            started_at=started_at,
            completed_at=time.time(),
        )

    @staticmethod
    def _person_hold_allowed() -> bool:
        """RESUME-AND-RECOVERY 1b rules P2-P3 — the one check lives in ``delegated_hold.person_reads_live``."""
        from matrx_ai.tools import delegated_hold

        return delegated_hold.person_reads_live()

    async def _hold_for_person(
        self, tool_def: ToolDefinition, ctx: ToolContext, row_id: str, started_at: float
    ) -> ToolResult | None:
        """A call parked on a PERSON, waited for in the open stream (RESUME-AND-RECOVERY 1b rule P4).

        Runs in ``execute`` AFTER the dispatch returned ``delegated_pending`` (outside its timeout and cancel
        branch). The stored answer when it was taken under the hold; ``None`` means park as before.
        """
        from matrx_ai.context.events import InfoPayload
        from matrx_ai.tools import delegated_hold
        from matrx_ai.tools.logger import PARKED_ON_KEY

        emitter = ctx.emitter
        if emitter is None or not row_id or not self._person_hold_allowed():
            return None
        # (1) The row by id: still parked on an action request, unresolved.
        from matrx_ai.db import cxm

        rows = await cxm.tool_call.filter_items(id=row_id)
        row = rows[0] if rows else None
        parked_on = (getattr(row, "metadata", None) or {}).get(PARKED_ON_KEY) if row is not None else None
        if (
            row is None
            or str(getattr(row, "status", "")) != "delegated"
            or not getattr(row, "is_client_delegated", False)
            or getattr(row, "resolved_at", None) is not None
            or not isinstance(parked_on, dict)
            or parked_on.get("kind") != "action_request"
        ):
            return None
        # (2) The assistant tool_use is durable before anything waits.
        if ctx.assistant_checkpoint is None:
            return None
        try:
            message_id = await ctx.assistant_checkpoint()
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - no durable tool_use means no hold: the call parks, announced
            vcprint(f"[delegated hold] {tool_def.name}: the assistant checkpoint failed ({exc!r}); the call "
                    "parks without a hold", color="red")
            try:
                from matrx_connect.streaming.error_capture import capture_error

                await capture_error(exc, kind="person_hold_checkpoint_failed", route="tools/executor",
                                    context={"tool_call_id": row_id, "call_id": ctx.call_id})
            except Exception:  # noqa: BLE001 - the banner above already said it
                pass
            return None
        if not message_id:
            return None
        ctx.message_id = message_id
        # (3) The window: the person knob, and never past the row's own expiry minus one lease (the expiry
        # sweep must never hand a holder its placeholder).
        hold = delegated_hold.settings(reason="person")
        if hold is None:
            return None
        expires_at = getattr(row, "expires_at", None)
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)
        if expires_at is not None:
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=UTC)
            left = (expires_at - datetime.now(UTC)).total_seconds() - hold.lease_seconds
            hold = replace(hold, seconds=min(hold.seconds, left))
        if hold.seconds < hold.lease_seconds:
            return None
        # (4) The lease; a failed claim means the row changed (answered, closed): park as today.
        conversation_id = ctx.conversation_id or ""
        if not await delegated_hold.claim(row_id, conversation_id=conversation_id, hold=hold):
            return None
        # (5) An interrupt must never pair this open call with an "interrupted" result.
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        state = try_get_execution_state()
        if state is not None:
            state.tool_dispatch_response = None
        # (6) The client is told the stream stays open for the person's answer.
        from matrx_connect.context.tool_event_data import DelegatedHoldWaitingInfo

        waiting = DelegatedHoldWaitingInfo(
            call_id=ctx.call_id,
            tool_name=tool_def.name,
            until=(datetime.now(UTC) + timedelta(seconds=hold.seconds)).isoformat(),
            action_request_id=str(parked_on.get("action_request_id") or ""),
        )
        await emitter.send_info(
            InfoPayload(
                code="delegated_hold_waiting",
                system_message=f"Waiting in the stream for the person's answer to {tool_def.name}.",
                user_message="",
                metadata=waiting.model_dump(),
            )
        )
        # (7) The wait.
        outcome = await delegated_hold.wait_for_result(
            row_id,
            conversation_id=conversation_id,
            call_id=ctx.call_id,
            hold=hold,
            stop_reason=self._hold_stop_reason(ctx),
        )
        return await self._held_outcome(tool_def, ctx, outcome, started_at, answered_by="the person")

    async def _delegate_in_memory(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        authorization_metadata: dict[str, Any] | None,
    ) -> ToolResult:
        """The unsaved run's client handoff: emit ``tool_delegated`` (same shape), wait on a future, continue in place."""
        from matrx_ai.context.app_context import get_app_context
        from matrx_ai.context.events import ToolEventPayload
        from matrx_ai.tools import in_memory_handoff

        started_at = time.time()

        def refusal(error_type: str, message: str, exc: BaseException | None = None) -> ToolResult:
            return ToolResult(
                success=False,
                error=ToolError.declared(error_type, message, exc=exc),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        emitter = ctx.emitter
        app_ctx = get_app_context()
        is_desktop_bound = any(
            b == "matrx-local" or b.startswith("matrx-local.")
            for b in self.registry.bindings_for_tool(tool_def.name)
        )
        if emitter is None or not getattr(app_ctx, "client_tools", None) or is_desktop_bound:
            return refusal(
                "client_unavailable",
                f"{tool_def.name} needs the page open: it runs in the person's browser, and no page is "
                "attached to this run to hand it to. Tell the person this action needs the page open, "
                "and answer without it.",
            )

        # Bounded by the same per-call / knob window as a saved call, and never past the dispatch backstop.
        wait_seconds = min(
            float(tool_def.max_client_wait_seconds or delegated_call_abandon_seconds()),
            _DELEGATED_DISPATCH_TIMEOUT_SECONDS - 30.0,
        )
        future = in_memory_handoff.register(
            ctx.call_id, user_id=str(ctx.user_id or ""), conversation_id=str(ctx.conversation_id or "")
        )
        try:
            event_data: dict[str, Any] = {"arguments": args}
            if tool_def.max_client_wait_seconds:
                event_data["step_deadline_at"] = (
                    datetime.now(UTC) + timedelta(seconds=wait_seconds)
                ).isoformat()
            if authorization_metadata:
                event_data["execution_authorization"] = authorization_metadata
            await emitter.send_tool_event(
                ToolEventPayload(
                    event="tool_delegated",
                    call_id=ctx.call_id,
                    tool_name=tool_def.name,
                    message=f"Delegating {tool_def.name} to client",
                    show_spinner=True,
                    data=event_data,
                )
            )
            try:
                answer = await asyncio.wait_for(future, timeout=wait_seconds)
            except TimeoutError as timed_out:
                return refusal(
                    "client_unavailable",
                    f"The page did not answer {tool_def.name}. Tell the person it did not respond, and "
                    "answer without it.",
                    timed_out,
                )
        finally:
            in_memory_handoff.forget(ctx.call_id)

        if answer.get("is_error"):
            return ToolResult(
                success=False,
                error=ToolError(
                    reported_failure="the client that ran the tool",
                    error_type="client_tool_error",
                    message=str(answer.get("error_message") or "Client tool error"),
                    is_retryable=False,
                    suggested_action="The client reported an error executing this tool.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )
        return ToolResult(
            success=True,
            output=answer.get("output"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    async def _execute_local(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        stream: ToolStreamManager,
    ) -> ToolResult:
        func = tool_def._callable
        if func is None:
            return ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type="configuration",
                    message=f"No callable resolved for local tool '{tool_def.name}'",
                ),
                started_at=time.time(),
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        started_at = time.time()
        from matrx_ai.tools.streaming import CURRENT_TOOL_STREAM

        _stream_token = CURRENT_TOOL_STREAM.set(stream)
        try:
            raw_result = await func(args, ctx)
        finally:
            CURRENT_TOOL_STREAM.reset(_stream_token)

        if isinstance(raw_result, ToolResult):
            raw_result.started_at = raw_result.started_at or started_at
            raw_result.completed_at = raw_result.completed_at or time.time()
            raw_result.tool_name = raw_result.tool_name or tool_def.name
            raw_result.call_id = raw_result.call_id or ctx.call_id
            return raw_result

        # Legacy compatibility: dict with "status" / "result"
        if isinstance(raw_result, dict):
            is_error = raw_result.get("status") == "error"
            return ToolResult(
                success=not is_error,
                output=(
                    raw_result.get("result")
                    if not is_error
                    else raw_result.get("error", raw_result.get("result"))
                ),
                error=ToolError(
                    reported_failure=f"local tool {tool_def.name!r} (returned status='error')",
                    error_type="execution",
                    message=str(raw_result.get("error", raw_result.get("result", ""))),
                )
                if is_error
                else None,
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        return ToolResult(
            success=True,
            output=raw_result,
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    async def _execute_external_mcp(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        from .external_mcp import ExternalMCPClient

        # Host-injected per-user MCP auth (the ``mcp_auth_resolver`` seam —
        # ``async (server_slug, user_id) -> dict | None``). The host resolves
        # the user's stored connection credentials (vault-backed in aidream)
        # just in time; matrx-ai never persists or decrypts them. Canonical
        # tool names are ``mcp.<slug>.<local>``.
        if tool_def.mcp_server_auth is None and tool_def.name.startswith("mcp."):
            from matrx_ai._ext import get_ext, has_ext

            if has_ext("mcp_auth_resolver"):
                parts = tool_def.name.split(".", 2)
                if len(parts) == 3 and parts[1]:
                    try:
                        auth = await get_ext("mcp_auth_resolver")(parts[1], ctx.user_id)
                    except Exception:
                        logger.exception(
                            "mcp_auth_resolver failed for %s — calling unauthenticated",
                            tool_def.name,
                        )
                        auth = None
                    if auth is not None:
                        # The host may resolve a per-user scoped endpoint along
                        # with Vault-backed auth. Remove the reserved metadata
                        # before auth headers are built and use it only as the
                        # remote URL for this invocation.
                        resolved_auth = dict(auth)
                        endpoint = resolved_auth.pop("__matrx_mcp_endpoint_url", None)
                        updates: dict[str, Any] = {"mcp_server_auth": resolved_auth}
                        if isinstance(endpoint, str) and endpoint:
                            updates["mcp_server_url"] = endpoint
                        tool_def = tool_def.model_copy(update=updates)

        ceiling = (
            float(tool_def.timeout_seconds)
            if tool_def.timeout_seconds is not None
            else dispatch_timeout_ceiling(tool_def.name)
        )
        # Every attempt and every wait between them fits inside the dispatch ceiling, so the connection's own words
        # ("the provider did not answer … nothing failed on ours") reach the agent — never the ceiling's generic
        # timeout first (adversarial review 2026-10-18: both were 120s, so a hung provider never got its retry).
        client = ExternalMCPClient(timeout=ceiling, budget_seconds=ceiling)
        return await client.call_tool(tool_def, args, ctx)

    async def _execute_agent(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        from .agent_tool import execute_agent_tool

        child_ctx = ctx.model_copy(
            update={
                "recursion_depth": ctx.recursion_depth + 1,
            }
        )
        return await execute_agent_tool(tool_def, args, child_ctx)

    async def _execute_external_handler(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        """Dispatch a tool call to an async handler registered by a host application.

        The handler is resolved from ``ExternalHandlerRegistry`` using a two-tier
        lookup: exact tool-name match first, then app-level (source_kind) fallback.
        If no handler is registered, a structured error is returned to the model.
        """
        from .external_handlers import invoke_external_handler

        child_ctx = ctx.model_copy(update={"tool_name": tool_def.name})
        return await invoke_external_handler(
            tool_name=tool_def.name,
            source_kind=tool_def.source_kind,
            args=args,
            ctx=child_ctx,
        )

    async def _execute_catalog(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        """Run a catalog Tool through the ONE host-injected catalog executor.

        Catalog Tools have no code argument model, so their declared JSON
        Schema is the contract checked here before anything is spent.
        """
        from .catalog_seam import get_catalog_executor

        started = time.time()
        schema_error = _validate_against_declared_schema(tool_def, args)
        if schema_error is not None:
            return ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type="validation",
                    message=f"Arguments for {tool_def.name} do not match its inputs: {schema_error}",
                    suggested_action="Fix the named input(s) and call the tool again.",
                ),
                started_at=started,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )
        executor = get_catalog_executor()
        if executor is None:
            return ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type="configuration",
                    message=f"{tool_def.name} cannot run here: no catalog executor is installed.",
                    suggested_action="Do not retry this tool now.",
                ),
                started_at=started,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )
        child_ctx = ctx.model_copy(update={"tool_name": tool_def.name})
        return await executor(tool_def, args, child_ctx)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _has_external_handler(tool_def: ToolDefinition) -> bool:
        """Whether the host registered an external handler that can run this
        tool (exact name match, or an app-level handler for its source_kind)."""
        from .external_handlers import ExternalHandlerRegistry

        return ExternalHandlerRegistry.get_instance().has_handler(
            tool_def.name, tool_def.source_kind
        )

    def _unknown_tool_hint(
        self,
        tool_name: str,
        allowed_tools: frozenset[str] | None,
    ) -> tuple[str, str]:
        """(message, suggested_action) for an unknown tool name — did-you-mean
        over the full name vocabulary plus a bounded, closest-first list of the
        tools that are actually active for this request. Best-effort: any
        failure degrades to the plain not-registered message."""
        try:
            from matrx_ai.tools.agent_projection import list_projected_tool_names
            from matrx_ai.tools.tool_aliases import get_alias_map

            vocabulary: set[str] = set(self.registry.list_tool_names())
            vocabulary.update(get_alias_map().keys())
            vocabulary.update(list_projected_tool_names())
            active = allowed_tools if allowed_tools is not None else vocabulary
            return build_unknown_tool_hint(tool_name, vocabulary=vocabulary, active_tools=active)
        except Exception as exc:  # noqa: BLE001 — a hint must never mask the error
            vcprint(
                f"[ToolExecutor] unknown-tool hint construction failed: {exc}",
                color="yellow",
            )
            return (
                f"Tool '{tool_name}' is not registered.",
                "Check the tool name and try again. Use a valid tool from the available set.",
            )

    @staticmethod
    def _unknown_tool_result(
        tool_name: str,
        call_id: str,
        started_at: float,
        *,
        message: str | None = None,
        suggested_action: str | None = None,
    ) -> ToolResult:
        return ToolResult(
            success=False,
            error=ToolError(
                refusal=True,
                error_type="not_found",
                message=message or f"Tool '{tool_name}' is not registered.",
                suggested_action=suggested_action
                or "Check the tool name and try again. Use a valid tool from the available set.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=call_id,
        )

    # _persist_output is no longer needed — persist_key and output are stored
    # directly in the cx_tool_call row via the unified logger.log() call.
