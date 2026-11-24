"""The run-approval gate — an agent, mandate or automation that cost more than $1 in one run
waits for a person's approval before it runs again (Arman, 2026-10-08;
common-docs/policies/ai-model-and-spend-rules.md §3–4).

Same seam and the same shape as the usage gate (``providers/usage_gate.py``):

* it runs at ``UnifiedAIClient._dispatch_with_billing_net`` — the one place every paid
  provider call passes — right after the usage gate, BEFORE any money is spent;
* the decision is made from the host's MEMORY (a synchronous resolver; never a database read),
  ONCE PER LAUNCH — one request (``request_id``): one agent run with its whole tool loop. A launch
  admitted at its first paid call finishes its loop: a hold that opens while it is going (its own
  subject crossing its threshold, a volume pause, an administrator's decline) never cuts it in
  half — what it already spent would be wasted. Every NEW launch asks again: a sub-agent or a
  mandate child (its own ``request_id``), a workflow step's request, and — before each paid step
  it launches — the workflow engine itself (the host's spend gate, :func:`refusal_for`). ONE rule
  for the code path and the workflow path. The memo is the launch and NOTHING wider: before
  2026-10-27 it was the request tree, so the code-built News monitor's first paid call (a search
  API, no held subject) admitted every later mandate of the run, Arman's rejections included; on
  2026-11-10 it was a whole workflow run tree for the life of the process, so a hold or decline
  placed mid-run stopped no later launch and a fan-out's siblings kept spending after one child
  opened a hold. Never widen it past one request;
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


#: A held SIGN-IN SESSION (subject ``coding_session``: on an account only agents use, the login's session is the
#: subject) is never "this agent": a run of one agent over the limit holds every later run from that login, and the
#: person reading the refusal of an unrelated, cheap agent must be told what is actually held (L12b, 2026-11-03).
SESSION_REFUSAL_SENTENCES: dict[str, str] = {
    "volume": "This sign-in session made many paid calls in the last hour, so its runs are paused until that hour's "
    "volume drops. An administrator can also approve it.",
    "over_threshold": "A run in this sign-in session cost more than its approval limit, so its runs wait for an "
    "administrator to approve them.",
    "expired": "This sign-in session's temporary approval ran out, so it was not run. An administrator can approve it again.",
    "declined": "An administrator declined this sign-in session's spending, so it was not run.",
    "waiting": "This sign-in session is waiting for an administrator to approve its spending, so it was not run.",
}

#: What every other held subject is called in the sentence (an agent, a mandate, a factory door: "this agent").
_SUBJECT_NOUN: dict[str, str] = {
    "workflow": "automation",
    "workflow_trigger": "automation",
    "sch_task": "scheduled task",
    "agent_schedule": "scheduled task",
}


#: Who decides a hold (``RunApprovalRequiredError(decided_by=...)``): the platform's approvers (a system-owned subject)
#: or the admins of the organization that owns it (every other subject: ``billing.run_approval_decide`` lets that
#: organization's admins approve it on its own Spend approvals page).
DECIDED_BY_PLATFORM = "platform"
DECIDED_BY_ORGANIZATION = "organization"

#: The door an organization-owned hold names (P8-RUNS, 2026-11-14: a business owner's chat read "wait for an
#: administrator" while that owner WAS the administrator who could approve it; the page existed, the sentence hid it).
ORGANIZATION_DOOR_SENTENCE = "This organization's admins can approve it on its Spend approvals page."

#: Reasons a decider can still lift with an approval (a decline is final: it names no door).
_DOOR_REASONS: frozenset[str] = frozenset({"volume", "over_threshold", "expired", "waiting"})


def refusal_sentence(subject_kind: str, reason: str, decided_by: str = DECIDED_BY_PLATFORM) -> str:
    """The one sentence a person reads for this held subject and reason (``reason`` from :func:`hold_reason`),
    plus the organization's own door when its admins decide."""
    if subject_kind == "coding_session":
        sentence = SESSION_REFUSAL_SENTENCES[reason]
    else:
        sentence = REFUSAL_SENTENCES[reason]
        noun = _SUBJECT_NOUN.get(subject_kind)
        if noun:
            sentence = sentence.replace("This agent", f"This {noun}").replace("this agent", f"this {noun}")
    if decided_by == DECIDED_BY_ORGANIZATION and reason in _DOOR_REASONS:
        sentence = f"{sentence} {ORGANIZATION_DOOR_SENTENCE}"
    return sentence


#: Host reasons that read as one of the sentences above. ``test_accounts_only_other_caller``: a caller outside the
#: agents-only seats held under a test-accounts-only approval (spend rule 16) waits for a person.
_REASON_SENTENCE: dict[str, str] = {"test_accounts_only_other_caller": "waiting"}


def hold_reason(status: str, reason: str | None) -> str:
    """The hold's reason as the refusal reports it: the host's when it names a known one, else from the status
    alone (a rejection with no reason is reported as declined; anything else as waiting)."""
    if reason in _REASON_SENTENCE:
        return _REASON_SENTENCE[reason]
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
        decided_by: str = DECIDED_BY_PLATFORM,
        agent_note_hint: str | None = None,
    ) -> None:
        self.approval_id = approval_id
        #: The host's instruction to a held coding agent (how it tells the approver what it is doing). The
        #: package only carries it: in the technical message and the envelope, never in what a person reads.
        self.agent_note_hint = agent_note_hint
        self.decided_by = decided_by
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
        self.message = refusal_sentence(subject_kind, self.reason, decided_by)
        self.technical_message = (
            f"Not run: this {what} ({subject_id}) is held (reason: {self.reason}) "
            f"and {verdict}. Approve it here: {approval_url}"
        )
        if agent_note_hint:
            self.technical_message = f"{self.technical_message} {agent_note_hint}"
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
            "decided_by": getattr(self, "decided_by", DECIDED_BY_PLATFORM),
            "agent_note_hint": getattr(self, "agent_note_hint", None),
        }


Resolver = Callable[[Any], "RunApprovalRequiredError | None"]
AgentDrivenPredicate = Callable[[Any], bool]

#: Route prefix of every AI Dream MCP tool call (``mcp:agent_run``, ``mcp:coding_session_bridge``…).
AGENT_ROUTE_PREFIX = "mcp:"

_resolver: Resolver | None = None
_agent_driven: AgentDrivenPredicate | None = None
_unwired_announced = False
#: Launches (request ids) admitted at their first paid call. Bounded; a request is short-lived.
_ADMITTED_MEMO_MAX = 50_000
_admitted: OrderedDict[str, None] = OrderedDict()


def set_run_approval_resolver(resolver: Resolver | None) -> None:
    """Host wiring: a SYNCHRONOUS ``ctx -> RunApprovalRequiredError | None`` memory read, asked at the first
    paid call of every launch (request) and before every paid workflow step."""
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
    """Tests: forget which launches were admitted (and the one-time "no resolver wired" announcement)."""
    global _unwired_announced
    _unwired_announced = False
    _admitted.clear()


def refusal_for(ctx: Any) -> RunApprovalRequiredError | None:
    """THE ONE ADMISSION RULE: the refusal the paid call (or paid workflow step) about to be made under ``ctx``
    gets right now, or None. No memo, no side effect: every new launch on both paths asks it; a real person's
    own turn is never asked."""
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


def _refuse(refusal: RunApprovalRequiredError, request_id: str) -> None:
    vcprint(
        f"[RunApprovalGate] refused request={request_id[:8]}… {refusal.subject_kind}="
        f"{refusal.subject_id} ({refusal.status}) — {refusal.approval_url}",
        color="yellow",
        log_level="WARNING",
    )
    raise refusal


def admit_run_approval() -> None:
    """Admit or refuse the paid call about to be made: asked at a launch's first paid call, and that launch
    (its ``request_id``, never its tree) then finishes its loop (see the module docstring)."""
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    request_id = str(getattr(ctx, "request_id", "") or "")
    if request_id and request_id in _admitted:
        return  # a running launch is never cut in half
    refusal = refusal_for(ctx)
    if refusal is not None:
        _refuse(refusal, request_id)
    if request_id:
        _admitted[request_id] = None
        while len(_admitted) > _ADMITTED_MEMO_MAX:
            _admitted.popitem(last=False)


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
    "DECIDED_BY_ORGANIZATION",
    "DECIDED_BY_PLATFORM",
    "EXEMPT_ORIGIN_CLASSES",
    "FIX_ACTION_APPROVE_RUN",
    "ORGANIZATION_DOOR_SENTENCE",
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
