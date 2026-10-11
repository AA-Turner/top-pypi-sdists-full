"""The run-approval gate — an agent, mandate or automation that cost more than $1 in one run
waits for a person's approval before it runs again (Arman, 2026-10-08;
common-docs/policies/ai-model-and-spend-rules.md §3–4).

Same seam and the same shape as the usage gate (``providers/usage_gate.py``):

* it runs at ``UnifiedAIClient._dispatch_with_billing_net`` — the one place every paid
  provider call passes — right after the usage gate, BEFORE any money is spent;
* the decision is made ONCE, at a request's first paid call, from the host's MEMORY
  (a synchronous resolver; never a database read). Every later paid call of the same
  ``AppContext.request_id`` — sub-agents, workflow steps, tool loops — is admitted
  without asking again, so a running run is never cut in half. A RUN is a request;
* a refusal is a CALLER refusal (``is_caller_refusal``): never retried, rerouted or
  filed as a provider failure, and its message names the approval and links to it.

WHO IS NEVER GATED (Arman, 2026-10-08). A real person typing in their own chat
(``origin_class`` ``human``) or speaking through a verified channel (``delegated_member``) —
their run is their own responsibility and budget. NOT a person: a run through the AI Dream
MCP or a coding-session bridge (``route`` ``mcp:*``, on any account, Arman's included), and
any run on an account only agents use (the host's :func:`set_agent_driven_predicate` — the
shared test accounts and persona-factory accounts). Those, and everything else — scheduled,
workflow, child agents, API callers, system work — are gated when the host says so. The same
rule as ``platform.run_driver`` in the database: :func:`is_person_driven`.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream: the host registers a
``ctx -> RunApprovalRequiredError | None`` resolver with
:func:`set_run_approval_resolver`. With none registered nothing is gated (announced once).
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

RUN_APPROVAL_REQUIRED = "run_approval_required"
FIX_ACTION_APPROVE_RUN = "approve_run"

#: Origins a person drives directly — their own turns are never held.
EXEMPT_ORIGIN_CLASSES: frozenset[str] = frozenset({"human", "delegated_member"})

_ADMITTED_MEMO_MAX = 50_000


class RunApprovalRequiredError(Exception):
    """This agent / mandate / automation is waiting for (or was refused) spend approval."""

    is_caller_refusal = True
    http_status = 403

    def __init__(
        self,
        *,
        approval_id: str,
        subject_kind: str,
        subject_id: str,
        status: str,
        approval_url: str,
    ) -> None:
        self.approval_id = approval_id
        self.subject_kind = subject_kind
        self.subject_id = subject_id
        self.status = status
        self.approval_url = approval_url
        what = subject_kind.replace("_", " ")
        verdict = "was rejected" if status == "rejected" else "is waiting for approval"
        # What the person reads: plain words, no ids, no admin links (members never see the
        # approvals console). Ids and the approval link stay in technical_message (logs) and in
        # the structured envelope, where an admin surface can offer "Approve".
        self.message = (
            "This agent spent more than its approval limit last time, so it was not run. "
            "An administrator can approve it."
            if status != "rejected"
            else "This agent spent more than its approval limit and an administrator declined it, so it was not run."
        )
        self.technical_message = (
            f"Not run: this {what} ({subject_id}) cost more than the approval threshold in one run "
            f"and {verdict}. Approve it here: {approval_url}"
        )
        self.code = RUN_APPROVAL_REQUIRED
        self.error_info = RetryableError(
            error_type=self.code,
            message=self.technical_message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=self.message,
            details=self.envelope(),
        )
        super().__init__(self.message)

    def envelope(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "message": self.message,
            "technical_message": self.technical_message,
            "fix_action": FIX_ACTION_APPROVE_RUN,
            "approval_id": self.approval_id,
            "approval_url": self.approval_url,
            "subject_kind": self.subject_kind,
            "subject_id": self.subject_id,
            "status": self.status,
        }


Resolver = Callable[[Any], "RunApprovalRequiredError | None"]
AgentDrivenPredicate = Callable[[Any], bool]

#: Route prefix of every AI Dream MCP tool call (``mcp:agent_run``, ``mcp:coding_session_bridge``…).
AGENT_ROUTE_PREFIX = "mcp:"

_resolver: Resolver | None = None
_agent_driven: AgentDrivenPredicate | None = None
_unwired_announced = False
_admitted: OrderedDict[str, None] = OrderedDict()


def set_run_approval_resolver(resolver: Resolver | None) -> None:
    """Host wiring: a SYNCHRONOUS ``ctx -> RunApprovalRequiredError | None`` memory read."""
    global _resolver
    _resolver = resolver


def set_agent_driven_predicate(predicate: AgentDrivenPredicate | None) -> None:
    """Host wiring: a SYNCHRONOUS ``ctx -> bool`` memory read — True when the run's account is
    one only agents use (a shared test account), so its "human" turns are agent-driven."""
    global _agent_driven
    _agent_driven = predicate


def is_person_driven(ctx: Any) -> bool:
    """True only for a real person's own turn: never held, never listed (Arman, 2026-10-08)."""
    if ctx is None:
        return False
    if str(getattr(ctx, "origin_class", "") or "") not in EXEMPT_ORIGIN_CLASSES:
        return False
    if str(getattr(ctx, "route", "") or "").startswith(AGENT_ROUTE_PREFIX):
        return False
    if _agent_driven is not None:
        try:
            if _agent_driven(ctx):
                return False
        except Exception as exc:  # noqa: BLE001 — a broken read leaves the claimed origin in force
            vcprint(
                f"[RunApprovalGate] agent-driven predicate raised ({type(exc).__name__}: {exc}) — "
                "treating the run by its origin.",
                color="red",
                log_level="ERROR",
            )
    return True


def reset_run_approval_gate_state() -> None:
    """Tests: forget which requests were already admitted."""
    _admitted.clear()


def _remember(request_id: str) -> None:
    _admitted[request_id] = None
    _admitted.move_to_end(request_id)
    while len(_admitted) > _ADMITTED_MEMO_MAX:
        _admitted.popitem(last=False)


def refusal_for(ctx: Any) -> RunApprovalRequiredError | None:
    """The refusal this context's run would get right now, or None. No memo, no side effect."""
    global _unwired_announced
    if ctx is None:
        return None
    if is_person_driven(ctx):
        return None
    if _resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[RunApprovalGate] no resolver wired by the host — runs over the approval "
                "threshold are NOT held in this process.",
                color="red",
                log_level="WARNING",
            )
        return None
    try:
        return _resolver(ctx)
    except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run
        vcprint(
            f"[RunApprovalGate] resolver raised ({type(exc).__name__}: {exc}) — run admitted.",
            color="red",
            log_level="ERROR",
        )
        return None


def admit_run_approval() -> None:
    """Admit or refuse the paid call about to be made. Raises only at a request's FIRST paid call."""
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    request_id = str(getattr(ctx, "request_id", "") or "")
    if request_id and request_id in _admitted:
        return  # a running run is never stopped
    refusal = refusal_for(ctx)
    if refusal is not None:
        vcprint(
            f"[RunApprovalGate] refused request={request_id[:8]}… {refusal.subject_kind}="
            f"{refusal.subject_id} ({refusal.status}) — {refusal.approval_url}",
            color="yellow",
            log_level="WARNING",
        )
        raise refusal
    if request_id:
        _remember(request_id)


def run_approval_refusal_in(source: Any, *, _max_depth: int = 16) -> RunApprovalRequiredError | None:
    """The run-approval refusal inside ``source`` (exception chain or ``.exception``), or None."""
    seen: set[int] = set()
    stack: list[Any] = [source]
    while stack and len(seen) < _max_depth:
        node = stack.pop()
        if node is None or id(node) in seen:
            continue
        seen.add(id(node))
        if isinstance(node, RunApprovalRequiredError):
            return node
        for attr in ("exception", "terminal_exception"):
            carried = getattr(node, attr, None)
            if isinstance(carried, BaseException):
                stack.append(carried)
        if isinstance(node, BaseException):
            stack.append(node.__cause__)
            stack.append(node.__context__)
            members = getattr(node, "exceptions", None)
            if isinstance(members, (list, tuple)):
                stack.extend(m for m in members if isinstance(m, BaseException))
    return None


__all__ = [
    "AGENT_ROUTE_PREFIX",
    "EXEMPT_ORIGIN_CLASSES",
    "FIX_ACTION_APPROVE_RUN",
    "RUN_APPROVAL_REQUIRED",
    "RunApprovalRequiredError",
    "admit_run_approval",
    "is_person_driven",
    "refusal_for",
    "reset_run_approval_gate_state",
    "run_approval_refusal_in",
    "set_agent_driven_predicate",
    "set_run_approval_resolver",
]
