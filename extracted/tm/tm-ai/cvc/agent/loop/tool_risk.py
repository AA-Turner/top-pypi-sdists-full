"""Tool risk tiers — reversibility-weighted permission gating.

Claude Code's "Reversibility-weighted risk assessment" design principle
(arxiv 2604.14228, principle #10) says: lighter oversight for
reversible / read-only actions, heavier oversight for destructive
ones. Claude Code implements this via a 7-mode permission system
backed by an ML classifier. CVC's analog is a 4-tier static table
that the loop body consults before each tool dispatch.

Tiers
-----
* ``read_only`` — no side effects. Always auto-execute. Examples:
  ``read_file``, ``search_files``, ``session_search``.
* ``reversible_write`` — writes inside the project, can be undone
  by git checkout or by re-running the tool. Auto-execute, but log
  to the trajectory for audit. Examples: ``write_file`` to a tracked
  file, ``patch``.
* ``network_write`` — writes that leave the project boundary
  (push to remote, HTTP POST, webhook). Require explicit user
  confirmation per turn unless ``--accept-network`` is set.
  Examples: ``git push``, ``web_post``, ``send_message``.
* ``destructive`` — cannot be trivially undone. Require explicit
  user confirmation AND log to a high-priority audit stream.
  Examples: ``rm -rf``, ``git reset --hard``, ``git clean -fd``,
  anything matched by :func:`is_destructive` from guardrails.py.

Why this lives next to (not inside) ``guardrails.py``
---------------------------------------------------
The existing ``is_destructive()`` is a *regex* check on command
strings — useful for catching ``rm -rf /`` patterns but it has no
notion of which *tool* is running. ``tool_risk.py`` answers the
opposite question: given the tool's identity, what tier does it
default to? The two layers compose: if a tool is ``reversible_write``
*and* its arguments match a destructive pattern, the loop should
escalate to ``destructive``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Mapping, Optional

__all__ = [
    "ToolRiskTier",
    "ToolRiskDecision",
    "ToolRiskRegistry",
    "DEFAULT_RISK_TIERS",
    "classify_tool_risk",
    "requires_confirmation",
]


class ToolRiskTier(str, Enum):
    READ_ONLY = "read_only"
    REVERSIBLE_WRITE = "reversible_write"
    NETWORK_WRITE = "network_write"
    DESTRUCTIVE = "destructive"

    @property
    def ordinal(self) -> int:
        """Higher = more dangerous. Used for tier comparison."""
        return {
            ToolRiskTier.READ_ONLY: 0,
            ToolRiskTier.REVERSIBLE_WRITE: 1,
            ToolRiskTier.NETWORK_WRITE: 2,
            ToolRiskTier.DESTRUCTIVE: 3,
        }[self]


@dataclass(frozen=True)
class ToolRiskDecision:
    """Result of :func:`classify_tool_risk` — drives loop behaviour."""

    tier: ToolRiskTier
    requires_confirmation: bool
    audit_log: bool  # True if the call should go to the high-pri audit stream
    reason: str = ""


# Default tier table for CVC's built-in tools. Mirrors the real
# CVC skill catalogue (cvc/skills/) plus cvc_* tool namespaces.
DEFAULT_RISK_TIERS: Mapping[str, ToolRiskTier] = {
    # ── Read-only (auto-execute) ───────────────────────────────────
    "read_file": ToolRiskTier.READ_ONLY,
    "search_files": ToolRiskTier.READ_ONLY,
    "session_search": ToolRiskTier.READ_ONLY,
    "skill_view": ToolRiskTier.READ_ONLY,
    "skills_list": ToolRiskTier.READ_ONLY,
    "vision_analyze": ToolRiskTier.READ_ONLY,
    "web_search": ToolRiskTier.READ_ONLY,
    "web_extract": ToolRiskTier.READ_ONLY,
    "todo": ToolRiskTier.READ_ONLY,
    "todo_write": ToolRiskTier.READ_ONLY,
    "browser_snapshot": ToolRiskTier.READ_ONLY,
    "browser_navigate": ToolRiskTier.READ_ONLY,  # reading a page, not posting
    "fact_store": ToolRiskTier.READ_ONLY,
    "memory": ToolRiskTier.READ_ONLY,
    "cvc_status": ToolRiskTier.READ_ONLY,
    "cvc_log": ToolRiskTier.READ_ONLY,
    "cvc_insights": ToolRiskTier.READ_ONLY,
    "cvc_skills_list": ToolRiskTier.READ_ONLY,
    "cvc_skills_show": ToolRiskTier.READ_ONLY,
    # ── Reversible write (auto-execute, audit) ──────────────────────
    "write_file": ToolRiskTier.REVERSIBLE_WRITE,
    "patch": ToolRiskTier.REVERSIBLE_WRITE,
    "write_skill": ToolRiskTier.REVERSIBLE_WRITE,
    "patch_skill": ToolRiskTier.REVERSIBLE_WRITE,
    "cvc_commit": ToolRiskTier.REVERSIBLE_WRITE,
    "cvc_branch": ToolRiskTier.REVERSIBLE_WRITE,
    "cvc_archive": ToolRiskTier.REVERSIBLE_WRITE,
    "cvc_restore": ToolRiskTier.REVERSIBLE_WRITE,
    "execute_code": ToolRiskTier.REVERSIBLE_WRITE,
    "cvc_merge": ToolRiskTier.REVERSIBLE_WRITE,
    # ── Network write (confirm unless --accept-network) ─────────────
    "send_message": ToolRiskTier.NETWORK_WRITE,
    "git_push": ToolRiskTier.NETWORK_WRITE,
    "git_publish": ToolRiskTier.NETWORK_WRITE,
    "browser_click": ToolRiskTier.NETWORK_WRITE,
    "browser_type": ToolRiskTier.NETWORK_WRITE,
    "browser_press": ToolRiskTier.NETWORK_WRITE,
    "web_post": ToolRiskTier.NETWORK_WRITE,
    "create_github_issue": ToolRiskTier.NETWORK_WRITE,
    "create_github_pr": ToolRiskTier.NETWORK_WRITE,
    # ── Destructive (always confirm + audit) ───────────────────────
    "delete_file": ToolRiskTier.DESTRUCTIVE,
    "rm_rf": ToolRiskTier.DESTRUCTIVE,
    "git_reset_hard": ToolRiskTier.DESTRUCTIVE,
    "git_clean": ToolRiskTier.DESTRUCTIVE,
    "cvc_drop_workspace": ToolRiskTier.DESTRUCTIVE,
    "cvc_forget": ToolRiskTier.DESTRUCTIVE,
    "drop_skill": ToolRiskTier.DESTRUCTIVE,
}


class ToolRiskRegistry:
    """Mutable registry — CLI flags can bump tiers at runtime.

    Why mutable: ``--accept-network`` (Claude Code's analog) should
    downgrade ``network_write`` -> ``reversible_write`` for the
    duration of one session. Same for ``--yes-destroy`` (rare, but
    power-user feature). Re-instantiate per session.
    """

    def __init__(
        self,
        base: Optional[Mapping[str, ToolRiskTier]] = None,
        *,
        accept_network: bool = False,
        yes_destroy: bool = False,
    ) -> None:
        self._tiers: dict = dict(base or DEFAULT_RISK_TIERS)
        if accept_network:
            for name in list(self._tiers.keys()):
                if self._tiers[name] == ToolRiskTier.NETWORK_WRITE:
                    self._tiers[name] = ToolRiskTier.REVERSIBLE_WRITE
        if yes_destroy:
            for name in list(self._tiers.keys()):
                if self._tiers[name] == ToolRiskTier.DESTRUCTIVE:
                    self._tiers[name] = ToolRiskTier.NETWORK_WRITE

    def tier_of(self, tool_name: str) -> ToolRiskTier:
        """Return the current tier for *tool_name*.

        Unknown tools default to ``NETWORK_WRITE`` (Claude Code's
        deny-first principle: unrecognised actions are escalated to
        the human, not auto-allowed).
        """
        return self._tiers.get(tool_name, ToolRiskTier.NETWORK_WRITE)

    def override(self, tool_name: str, tier: ToolRiskTier) -> None:
        """Force a specific tier (used by tests + CLI overrides)."""
        self._tiers[tool_name] = tier

    def all_in_tier(self, tier: ToolRiskTier) -> FrozenSet[str]:
        return frozenset(n for n, t in self._tiers.items() if t == tier)

    def __contains__(self, tool_name: str) -> bool:
        return tool_name in self._tiers


def classify_tool_risk(
    tool_name: str,
    args: Optional[dict] = None,
    *,
    registry: Optional[ToolRiskRegistry] = None,
    destructive_check=None,
) -> ToolRiskDecision:
    """Classify a tool call and return the loop's gating decision.

    Parameters
    ----------
    tool_name:
        The skill/tool identifier (e.g. ``"write_file"`` or ``"cvc_archive"``).
    args:
        Optional tool arguments. Passed to *destructive_check* (typically
        :func:`cvc.agent.loop.guardrails.is_destructive`) for string-args
        tools like terminal. Ignored for structured-args tools.
    registry:
        The :class:`ToolRiskRegistry` to consult. Defaults to a fresh
        instance (no overrides).
    destructive_check:
        Callable ``(args) -> DestructiveCheck`` for escalating tools
        whose arguments might match destructive patterns even if the
        tool itself is nominally a lower tier.
    """
    reg = registry or ToolRiskRegistry()
    tier = reg.tier_of(tool_name)

    # If the tool itself is reversible_write but its args contain a
    # destructive pattern, escalate. This catches the
    # ``write_file(path="~/.ssh/authorized_keys")`` case without
    # needing the user to remember which patterns are bad.
    if tier == ToolRiskTier.REVERSIBLE_WRITE and destructive_check is not None and args:
        try:
            check = destructive_check(args)
            if getattr(check, "is_destructive", False):
                tier = ToolRiskTier.DESTRUCTIVE
        except Exception:
            pass  # escalation check is best-effort

    if tier == ToolRiskTier.READ_ONLY:
        return ToolRiskDecision(
            tier=tier, requires_confirmation=False, audit_log=False,
        )
    if tier == ToolRiskTier.REVERSIBLE_WRITE:
        return ToolRiskDecision(
            tier=tier, requires_confirmation=False, audit_log=True,
            reason="reversible inside the project — auto-execute, audit",
        )
    if tier == ToolRiskTier.NETWORK_WRITE:
        return ToolRiskDecision(
            tier=tier, requires_confirmation=True, audit_log=True,
            reason="leaves the project boundary — confirm per turn",
        )
    return ToolRiskDecision(
        tier=tier, requires_confirmation=True, audit_log=True,
        reason="destructive — confirm and audit",
    )


def requires_confirmation(
    tool_name: str,
    args: Optional[dict] = None,
    *,
    registry: Optional[ToolRiskRegistry] = None,
) -> bool:
    """One-shot convenience: does this tool call need user approval?"""
    return classify_tool_risk(tool_name, args, registry=registry).requires_confirmation
