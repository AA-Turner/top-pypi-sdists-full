"""The run-approval gate — an agent, mandate or automation that cost more than $1 in one run
waits for a person's approval before it runs again (Arman, 2026-10-08;
common-docs/policies/ai-model-and-spend-rules.md §3–4).

Same seam and the same shape as the usage gate (``providers/usage_gate.py``):

* it runs at ``UnifiedAIClient._dispatch_with_billing_net`` — the one place every paid
  provider call passes — right after the usage gate, BEFORE any money is spent;
* the decision is made from the host's MEMORY (a synchronous resolver; never a database read),
  ONCE per request tree (``tree_request_id``) for the subjects the tree's first paid call runs as.
  The host names those subjects with the SAME derivation its resolver judges (the ``subjects``
  reader of :func:`set_run_approval_resolver`: mandate, agent, trigger, schedule, workflow,
  factory door, coding session). Every later paid call of the tree whose subjects were all
  admitted rides that admission — sub-agents, workflow steps, tool loops — so a running run is
  never cut in half: a subject the tree already runs as that crosses its threshold mid-run is
  held for its NEXT run, never stopped in this one. A subject NEW to the tree (a workflow step
  running another mandate, a sub-agent with its own agent id) is refused only when the host
  already holds that subject (``refusal_among``: a person's rejection, a waiting approval, an
  expired one); otherwise it joins the tree's admission. Before 2026-10-27 the memo was the tree
  alone, so the code-built News monitor's first paid call (a search API, no held subject)
  admitted every later mandate of the run, Arman's rejections included;
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
#: The host's hard refusal of an automated run on a protected account (a RunApprovalRequiredError
#: subclass the host raises). Named here so every caller classifies it from ONE registry
#: (``providers/caller_refusal.py``), never from a hand-written copy of the string.
PROTECTED_ACCOUNT_RUN_REFUSED = "protected_account_run_refused"
FIX_ACTION_APPROVE_RUN = "approve_run"

#: Origins a person drives directly — their own turns are never held.
EXEMPT_ORIGIN_CLASSES: frozenset[str] = frozenset({"human", "delegated_member"})

_ADMITTED_MEMO_MAX = 50_000


#: Why a subject is held (``billing.run_approval_holds().hold_reason``) -> the one sentence a person reads.
#: Plain words, no ids, no admin links (members never see the approvals console).
REFUSAL_SENTENCES: dict[str, str] = {
    "volume": "This agent made many paid calls in the last hour, so its runs are paused until that hour's volume drops. "
    "An administrator can also approve it.",
    "over_threshold": "This agent's first run cost more than its approval limit, so it waits for an administrator to approve it.",
    "expired": "This agent's temporary approval ran out, so it was not run. An administrator can approve it again.",
    "declined": "An administrator declined this agent's spending, so it was not run.",
    "waiting": "This agent is waiting for an administrator to approve its spending, so it was not run.",
}


def hold_reason(status: str, reason: str | None) -> str:
    """The hold's reason as the refusal reports it: the host's when it names a known one, else from the status
    alone (a rejection with no reason is reported as declined; anything else as waiting)."""
    if reason in REFUSAL_SENTENCES:
        return str(reason)
    return "declined" if status == "rejected" else "waiting"


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
        reason: str | None = None,
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
        # WHY it is held decides the sentence (review 4, F4): never "spent more than its limit" for a volume
        # pause, never "an administrator declined it" for a temporary approval that simply ran out.
        self.reason = hold_reason(status, reason)
        self.message = REFUSAL_SENTENCES[self.reason]
        self.technical_message = (
            f"Not run: this {what} ({subject_id}) is held (reason: {self.reason}) "
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
            "reason": self.reason,
        }


Resolver = Callable[[Any], "RunApprovalRequiredError | None"]
#: ``ctx -> [(subject_kind, subject_id), ...]``: the subjects the resolver judges this call as.
SubjectsReader = Callable[[Any], "list[tuple[str, str]]"]
#: ``(ctx, subjects) -> refusal | None``: the host's hold among exactly ``subjects`` (a new subject
#: inside an admitted tree; the run-level checks already passed at the tree's first paid call).
RefusalAmong = Callable[[Any, "list[tuple[str, str]]"], "RunApprovalRequiredError | None"]
AgentDrivenPredicate = Callable[[Any], bool]

#: Route prefix of every AI Dream MCP tool call (``mcp:agent_run``, ``mcp:coding_session_bridge``…).
AGENT_ROUTE_PREFIX = "mcp:"

_resolver: Resolver | None = None
_subjects_reader: SubjectsReader | None = None
_refusal_among: RefusalAmong | None = None
_agent_driven: AgentDrivenPredicate | None = None
_unwired_announced = False
#: tree key -> the subjects that tree was admitted for (empty when the host names none).
_admitted: OrderedDict[str, set[tuple[str, str]]] = OrderedDict()


def set_run_approval_resolver(
    resolver: Resolver | None,
    *,
    subjects: SubjectsReader | None = None,
    refusal_among: RefusalAmong | None = None,
) -> None:
    """Host wiring: a SYNCHRONOUS ``ctx -> RunApprovalRequiredError | None`` memory read, plus the
    subjects reader and the per-subject refusal it is built from (one derivation). Without a
    subjects reader a tree is admitted as a whole at its first paid call."""
    global _resolver, _subjects_reader, _refusal_among
    _resolver = resolver
    _subjects_reader = subjects if resolver is not None else None
    _refusal_among = refusal_among if resolver is not None else None


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


def _remember(tree_key: str, subjects: list[tuple[str, str]]) -> None:
    _admitted.setdefault(tree_key, set()).update(subjects)
    _admitted.move_to_end(tree_key)
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


def _read_subjects(ctx: Any) -> list[tuple[str, str]]:
    """The host's subjects for this call (its resolver's own derivation), or [] when none is wired."""
    if _subjects_reader is None:
        return []
    try:
        return [(str(k), str(i)) for k, i in (_subjects_reader(ctx) or [])]
    except Exception as exc:  # noqa: BLE001 — a broken read admits like a broken resolver, loudly
        vcprint(
            f"[RunApprovalGate] subjects reader raised ({type(exc).__name__}: {exc}) — "
            "judging the tree as a whole.",
            color="red",
            log_level="ERROR",
        )
        return []


def _refuse(refusal: RunApprovalRequiredError, request_id: str) -> None:
    vcprint(
        f"[RunApprovalGate] refused request={request_id[:8]}… {refusal.subject_kind}="
        f"{refusal.subject_id} ({refusal.status}) — {refusal.approval_url}",
        color="yellow",
        log_level="WARNING",
    )
    raise refusal


def admit_run_approval() -> None:
    """Admit or refuse the paid call about to be made (see the module docstring for the memo)."""
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    request_id = str(getattr(ctx, "request_id", "") or "")
    from matrx_connect.context.app_context import tree_request_id_of

    tree_key = tree_request_id_of(ctx)
    subjects = _read_subjects(ctx)
    admitted = _admitted.get(tree_key) if tree_key else None
    if admitted is not None:
        new = [s for s in subjects if s not in admitted]
        if not new:
            return  # a running run is never stopped
        if _refusal_among is not None and not is_person_driven(ctx):
            try:
                refusal = _refusal_among(ctx, new)
            except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run
                vcprint(
                    f"[RunApprovalGate] refusal_among raised ({type(exc).__name__}: {exc}) — admitted.",
                    color="red",
                    log_level="ERROR",
                )
                refusal = None
            if refusal is not None:
                _refuse(refusal, request_id)
        _remember(tree_key, new)
        return
    refusal = refusal_for(ctx)
    if refusal is not None:
        _refuse(refusal, request_id)
    if tree_key:
        _remember(tree_key, subjects)


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
