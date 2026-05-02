"""Sensitive action confirmation — require user approval before dangerous actions.

Two-phase flow:
  1. ConfirmationPlugin intercepts sensitive tool calls in before_tool_callback
  2. Returns a fake result telling the agent to ask the user for confirmation
  3. Orchestrator intercepts the user's YES/NO reply and executes/cancels

This sits BETWEEN SafetyPlugin (hard blocks) and CostTrackingPlugin:
  Safety → Confirmation → Cost → Observability
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

# Timeout for pending confirmations (seconds)
CONFIRMATION_TIMEOUT = 120.0

# ── Sensitive terminal command patterns ──────────────────────────────────────
# These are dangerous-but-not-catastrophic. SafetyPlugin blocks the truly
# catastrophic ones (format c:, rm -rf /, etc.). These require user approval.
_SENSITIVE_TERMINAL_PATTERNS: list[re.Pattern[str]] = [
    # File/directory deletion
    re.compile(r"\b(del|erase)\b", re.IGNORECASE),
    re.compile(r"\bremove-item\b", re.IGNORECASE),
    re.compile(r"\brm\s+", re.IGNORECASE),
    re.compile(r"\b(rmdir|rd)\b", re.IGNORECASE),
    # Package management (install/uninstall)
    re.compile(r"\b(choco|winget|pip|npm|yarn|pnpm)\s+(install|uninstall|remove)\b", re.IGNORECASE),
    # Service manipulation
    re.compile(r"\b(net|sc)\s+(stop|start|config|delete)\b", re.IGNORECASE),
    # Registry modification
    re.compile(r"\breg\s+(add|delete|import)\b", re.IGNORECASE),
    # Git destructive commands
    re.compile(r"\bgit\s+push\s+.*--force\b", re.IGNORECASE),
    re.compile(r"\bgit\s+reset\s+--hard\b", re.IGNORECASE),
    re.compile(r"\bgit\s+clean\s+-[a-z]*f", re.IGNORECASE),
    # PowerShell dangerous
    re.compile(r"\bSet-ExecutionPolicy\b", re.IGNORECASE),
    re.compile(r"\bInvoke-Expression\b", re.IGNORECASE),
    # Process termination (standalone commands, not kill_process tool)
    re.compile(r"\b(taskkill|stop-process)\b", re.IGNORECASE),
]

# Tools that are inherently sensitive
SENSITIVE_TOOL_NAMES: set[str] = {"kill_process"}

# Manage_window is sensitive only when action="close"
_CONDITIONAL_TOOLS: dict[str, list[tuple[str, str]]] = {
    "manage_window": [("action", "close")],
}

# ── Confirmation reply parsing ───────────────────────────────────────────────
_YES_WORDS: set[str] = {
    "yes",
    "y",
    "confirm",
    "ok",
    "go",
    "do it",
    "proceed",
    "sure",
    "yep",
    "yeah",
    "yea",
    "approved",
    "approve",
}
_NO_WORDS: set[str] = {
    "no",
    "n",
    "cancel",
    "stop",
    "dont",
    "don't",
    "nah",
    "nope",
    "never",
    "abort",
    "deny",
    "denied",
    "reject",
}


@dataclass
class PendingConfirmation:
    """A tool call waiting for user approval."""

    user_id: str
    tool_name: str
    tool_args: dict[str, object]
    description: str
    created_at: float = field(default_factory=time.monotonic)

    @property
    def is_expired(self) -> bool:
        return (time.monotonic() - self.created_at) > CONFIRMATION_TIMEOUT


class ConfirmationManager:
    """Tracks pending confirmations per user.

    Thread-safe for single-writer (asyncio event loop) usage.
    """

    def __init__(self) -> None:
        self._pending: dict[str, PendingConfirmation] = {}

    @property
    def pending_count(self) -> int:
        """Return the number of non-expired pending confirmations."""
        self._evict_expired()
        return len(self._pending)

    def _evict_expired(self) -> None:
        """Remove expired entries from the pending map."""
        expired = [uid for uid, p in self._pending.items() if p.is_expired]
        for uid in expired:
            del self._pending[uid]

    def has_pending(self, user_id: str) -> bool:
        """Check if a user has a non-expired pending confirmation."""
        p = self._pending.get(user_id)
        if p is None:
            return False
        if p.is_expired:
            del self._pending[user_id]
            return False
        return True

    def create(
        self,
        user_id: str,
        tool_name: str,
        tool_args: dict[str, object],
        description: str,
    ) -> PendingConfirmation:
        """Store a new pending confirmation (replaces any existing one)."""
        p = PendingConfirmation(
            user_id=user_id,
            tool_name=tool_name,
            tool_args=tool_args,
            description=description,
        )
        self._pending[user_id] = p
        return p

    def get(self, user_id: str) -> PendingConfirmation | None:
        """Get a pending confirmation without removing it."""
        p = self._pending.get(user_id)
        if p and p.is_expired:
            del self._pending[user_id]
            return None
        return p

    def pop(self, user_id: str) -> PendingConfirmation | None:
        """Remove and return a pending confirmation."""
        p = self._pending.pop(user_id, None)
        if p and p.is_expired:
            return None
        return p


def classify_action(tool_name: str, tool_args: dict[str, object]) -> str:
    """Classify a tool call as 'safe' or 'sensitive'.

    Returns:
        'sensitive' if the action needs user confirmation, 'safe' otherwise.
    """
    # Check tool name directly
    if tool_name in SENSITIVE_TOOL_NAMES:
        return "sensitive"

    # Check conditional tools (e.g., manage_window with action="close")
    if tool_name in _CONDITIONAL_TOOLS:
        for arg_name, arg_value in _CONDITIONAL_TOOLS[tool_name]:
            if str(tool_args.get(arg_name, "")).lower() == arg_value:
                return "sensitive"

    # Check terminal command patterns
    if tool_name == "run_terminal":
        command = str(tool_args.get("command", ""))
        for pattern in _SENSITIVE_TERMINAL_PATTERNS:
            if pattern.search(command):
                return "sensitive"

    return "safe"


def parse_confirmation_reply(text: str) -> bool | None:
    """Parse a user's YES/NO reply to a confirmation request.

    Returns:
        True for approval, False for denial, None for ambiguous input.
    """
    normalized = text.lower().strip().rstrip("!.?")
    if normalized in _YES_WORDS:
        return True
    if normalized in _NO_WORDS:
        return False
    return None
