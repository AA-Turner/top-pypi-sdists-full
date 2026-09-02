"""Designated-member enforcement for Orchestras (contract C-26, ruling D-38).

An Orchestra can declare a member (e.g. a validator) as REQUIRED: it must be
successfully called before the orchestrator finishes. The declaration lives on
the member association edge (``metadata.required``), is threaded to the runtime
by the host (``apply_orchestra_aware_tools`` stamps
``ctx.metadata[REQUIRED_ORCHESTRA_MEMBERS_KEY]``), and is enforced HERE — by
the executor, from the durable tool-call record — never by trusting the
prompt (vision principle 11: the guard is independent of the orchestrator).

This module is pure: it reads the stamped declaration, the projection map
(``PROJECTED_AGENT_TOOLS_KEY``, agent_id ↔ ``custom_tool_N`` via
``prompt_id``), and the request's ``tool_call_history`` details
(``{name, success}`` per call), and answers two questions the executor asks at
its finishing exits:

1. ``evaluate_required_members`` — which required members have NOT been
   successfully called this run?
2. ``decide_required_member_action`` — proceed / force one corrective turn /
   pause (chat) / fail (workflow step)?

Scoping rule — why ``active_tool_names`` exists: a child agent forked mid-run
inherits a COPY of the parent's metadata (``fork_for_child_agent``), so the
parent's stamped declaration is visible inside every member's own loop. A
required member is only *enforceable* in the loop whose active toolset
actually offers its projected name — a plain child agent never carries the
parent's ``custom_tool_N`` names, and a nested orchestra allocates distinct
indices and stamps its own declaration. Declared-but-unenforceable members are
reported (``unenforceable``) and never trigger an intervention.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY

if TYPE_CHECKING:
    from matrx_ai.orchestrator.tracking import ToolCallUsage

# ctx.metadata key carrying the host-stamped declaration:
# list[{"agent_id": str, "role_title": str | None}]. Stamped (and re-stamped on
# conversation continue/fork/resume) by the host's apply_orchestra_aware_tools
# chokepoint — matrx-ai never reads the DB for it.
REQUIRED_ORCHESTRA_MEMBERS_KEY = "required_orchestra_members"

# The distinct, resumable terminal status a chat run records when the model
# still refused the required member after the forced turn. NEVER a clean
# 'completed' (D-38). Mirrors the "paused_loop_guard" pattern.
REQUIRED_MEMBER_SKIPPED_STATUS = "paused_required_member_skipped"

# error_type / event vocabulary (see orchestras FEATURE.md § Designated members):
#   warning code "required_member_correction"  — intervention + forced turn
#   warning code "required_member_skipped"     — chat pause (terminal, resumable)
#   error   type "required_member_skipped"     — workflow-step hard failure
REQUIRED_MEMBER_ERROR_TYPE = "required_member_skipped"


@dataclass(frozen=True)
class RequiredMember:
    agent_id: str
    role_title: str | None
    projected_name: str | None  # custom_tool_N, or None when not projected here

    @property
    def display(self) -> str:
        return self.role_title or self.agent_id


@dataclass(frozen=True)
class RequiredMemberReport:
    required: list[RequiredMember]
    missing: list[RequiredMember]  # enforceable here and not successfully called
    unenforceable: list[RequiredMember]  # declared, but not offered in THIS loop

    @property
    def satisfied(self) -> bool:
        return not self.missing

    @property
    def forceable_names(self) -> list[str]:
        return [m.projected_name for m in self.missing if m.projected_name]


RequiredMemberAction = Literal["proceed", "force", "pause", "fail"]


def evaluate_required_members(
    metadata: dict[str, Any] | None,
    tool_call_history: list["ToolCallUsage"] | None,
    *,
    active_tool_names: list[str] | None,
) -> RequiredMemberReport:
    """Compute the required-member predicate from durable runtime facts only.

    ``missing`` = declared required ∧ projected here ∧ offered in the active
    toolset ∧ no SUCCESSFUL call recorded in ``tool_call_history``.
    """
    declared = (metadata or {}).get(REQUIRED_ORCHESTRA_MEMBERS_KEY) or []
    if not isinstance(declared, list) or not declared:
        return RequiredMemberReport(required=[], missing=[], unenforceable=[])

    projections: dict[str, Any] = (metadata or {}).get(PROJECTED_AGENT_TOOLS_KEY) or {}
    name_by_agent_id: dict[str, str] = {}
    for projected_name, dumped in projections.items():
        if isinstance(dumped, dict):
            prompt_id = dumped.get("prompt_id")
            if prompt_id:
                name_by_agent_id[str(prompt_id)] = str(projected_name)

    succeeded: set[str] = {
        str(detail.get("name") or "")
        for usage in tool_call_history or []
        for detail in usage.tool_calls_details
        if detail.get("success") is True
    }
    active = {n for n in (active_tool_names or []) if isinstance(n, str)}

    required: list[RequiredMember] = []
    missing: list[RequiredMember] = []
    unenforceable: list[RequiredMember] = []
    for entry in declared:
        if not isinstance(entry, dict):
            continue
        agent_id = str(entry.get("agent_id") or "")
        if not agent_id:
            continue
        role_title = entry.get("role_title")
        projected_name = name_by_agent_id.get(agent_id)
        member = RequiredMember(
            agent_id=agent_id,
            role_title=role_title if isinstance(role_title, str) else None,
            projected_name=projected_name,
        )
        required.append(member)
        if projected_name is None or projected_name not in active:
            # Not offered in THIS loop — an inherited declaration inside a
            # child agent's run, never a Conductor skipping its member.
            unenforceable.append(member)
            continue
        if projected_name not in succeeded:
            missing.append(member)

    return RequiredMemberReport(
        required=required, missing=missing, unenforceable=unenforceable
    )


def decide_required_member_action(
    report: RequiredMemberReport,
    *,
    already_intervened: bool,
    loop_guard_intervened: bool,
    is_workflow_step: bool,
) -> RequiredMemberAction:
    """One decision table for every finishing exit.

    - satisfied → proceed.
    - loop guard already intervened → proceed: its tools are disabled and the
      run already finalizes as 'paused_loop_guard' (never clean 'completed'),
      so forcing MORE tool calls would fight the other guard.
    - first miss, with a forceable projected tool → force ONE corrective turn
      (one-shot; the flag on ExecutionState makes this unrepeatable).
    - still missing after the forced turn (or nothing forceable) →
      workflow step: fail LOUDLY (no user is present to read a nudge —
      the assert_member_budget posture); chat: pause with the distinct
      resumable status. Never a clean 'completed'.
    """
    if report.satisfied:
        return "proceed"
    if loop_guard_intervened:
        return "proceed"
    if not already_intervened and report.forceable_names:
        return "force"
    return "fail" if is_workflow_step else "pause"


__all__ = [
    "REQUIRED_MEMBER_ERROR_TYPE",
    "REQUIRED_MEMBER_SKIPPED_STATUS",
    "REQUIRED_ORCHESTRA_MEMBERS_KEY",
    "RequiredMember",
    "RequiredMemberAction",
    "RequiredMemberReport",
    "decide_required_member_action",
    "evaluate_required_members",
]
