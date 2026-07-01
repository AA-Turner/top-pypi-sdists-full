"""
cvc.agent.permissions — Granular permission system for tool execution.

Implements Claude Code-style tool permissions with pattern matching:
  - Allow/Deny/Ask per tool with glob patterns
  - Pattern specifiers: Bash(npm run *), Edit(/src/**/*.ts), Read(~/.env)
  - Deny rules always win over allow rules
  - First-match semantics within same priority level
  - Session-level approval tracking (approve once vs approve always)

Permission evaluation order:
  1. Deny rules (highest priority) — block immediately
  2. Ask rules (medium) — prompt for approval
  3. Allow rules (lowest) — approve without prompting
  4. Default — ask on first use
"""

from __future__ import annotations

import fnmatch
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.permissions")


class PermissionAction(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


class PermissionDecision(str, Enum):
    """Result of evaluating a permission check."""
    ALLOWED = "allowed"
    DENIED = "denied"
    ASK_USER = "ask_user"


@dataclass
class PermissionRule:
    """
    A single permission rule.

    Examples of rule strings:
        "Bash"                  → all bash commands
        "Bash(npm run *)"       → bash commands matching 'npm run *'
        "Edit(/src/**/*.ts)"    → edit operations on src/ TypeScript files
        "Read(~/.env)"          → reading ~/.env specifically
        "Read"                  → all file reads
        "web_search"            → web search tool
        "cvc_*"                 → all CVC tools
    """
    raw: str
    tool_name: str
    pattern: str | None  # None means "all invocations of this tool"
    action: PermissionAction

    @classmethod
    def parse(cls, rule_str: str, action: PermissionAction) -> "PermissionRule":
        """
        Parse a rule string like 'Bash(npm run *)' into a PermissionRule.
        """
        # Map display names to internal tool names
        _name_map = {
            "bash": "bash",
            "read": "read_file",
            "edit": "edit_file",
            "write": "write_file",
            "patch": "patch_file",
            "webfetch": "web_search",
            "websearch": "web_search",
            "glob": "glob",
            "grep": "grep",
            "agent": "agent",
            "skill": "skill",
            "notebookedit": "notebook_edit",
        }

        match = re.match(r'^(\w[\w*]*)(?:\((.+)\))?$', rule_str.strip())
        if not match:
            return cls(raw=rule_str, tool_name=rule_str.lower(), pattern=None, action=action)

        name_part = match.group(1)
        pattern_part = match.group(2)  # may be None

        # Resolve the tool name (case-insensitive lookup, then fallback to raw)
        tool_name = _name_map.get(name_part.lower(), name_part.lower())

        return cls(
            raw=rule_str,
            tool_name=tool_name,
            pattern=pattern_part,
            action=action,
        )

    def matches_tool(self, tool_name: str) -> bool:
        """Check if this rule applies to the given tool name."""
        # Wildcard tool names like "cvc_*"
        if "*" in self.tool_name:
            return fnmatch.fnmatch(tool_name, self.tool_name)
        return self.tool_name == tool_name

    def matches_args(self, tool_name: str, tool_input: dict[str, Any]) -> bool:
        """
        Check if this rule matches the specific invocation arguments.

        For Bash rules, matches against the command string.
        For file operation rules, matches against the file path.
        For agent/skill rules, matches against the agent/skill name.
        """
        if not self.matches_tool(tool_name):
            return False

        # No pattern → matches all invocations of this tool
        if self.pattern is None:
            return True

        pattern = self.pattern

        # Tool-specific matching
        if tool_name == "bash":
            command = tool_input.get("command", "")
            return fnmatch.fnmatch(command, pattern)

        elif tool_name in ("read_file", "write_file", "edit_file", "patch_file"):
            path = tool_input.get("path", "")
            # Normalize path separators
            path = path.replace("\\", "/")
            pattern_normalized = pattern.replace("\\", "/")
            return fnmatch.fnmatch(path, pattern_normalized)

        elif tool_name == "agent":
            agent_name = tool_input.get("name", "")
            return fnmatch.fnmatch(agent_name, pattern)

        elif tool_name == "skill":
            skill_name = tool_input.get("name", "")
            return fnmatch.fnmatch(skill_name, pattern)

        elif tool_name == "web_search":
            # Domain matching: WebFetch(domain:example.com)
            if pattern.startswith("domain:"):
                domain = pattern[7:]
                query = tool_input.get("query", "")
                return domain.lower() in query.lower()
            return fnmatch.fnmatch(tool_input.get("query", ""), pattern)

        # Fallback: match against first arg value
        if tool_input:
            first_val = str(next(iter(tool_input.values()), ""))
            return fnmatch.fnmatch(first_val, pattern)

        return True  # No pattern, no args → matches


class PermissionEngine:
    """
    Evaluates tool permissions against configured rules.

    Rules are organized in three tiers:
      1. deny  — always checked first, blocks execution
      2. ask   — prompts user for approval
      3. allow — auto-approves without prompting

    Session-level approvals track what the user has already approved
    during this session (approve-once vs approve-always).

    Trust modes:
      - strict: all writes/executes require permission
      - smart:  safe commands auto-allowed, risky ones prompt
      - yolo:   everything auto-allowed (power user / CI)
    """

    # Commands considered safe in "smart" mode — auto-allowed without prompting
    SAFE_COMMANDS: set[str] = {
        "ls", "dir", "cat", "type", "head", "tail", "wc", "echo", "pwd",
        "grep", "find", "which", "where", "whoami", "date", "diff", "sort",
        "uniq", "tr", "cut", "env", "printenv", "hostname",
        "npm test", "npm run test", "npm run build", "npm run lint",
        "npm run typecheck", "npm run check", "npm run dev", "npm start",
        "npx tsc --noEmit", "npx eslint", "npx prettier",
        "yarn test", "yarn build", "yarn lint",
        "pnpm test", "pnpm build", "pnpm lint",
        "python -m pytest", "python -m unittest", "python -m mypy",
        "pytest", "mypy", "ruff check", "ruff format --check", "black --check",
        "cargo test", "cargo build", "cargo check", "cargo clippy",
        "go test", "go build", "go vet",
        "dotnet test", "dotnet build",
        "make", "make test", "make build", "make check",
        "git status", "git log", "git diff", "git branch", "git show",
        "git stash list",
    }

    # Patterns that indicate a risky command (regex fragments)
    _RISKY_PATTERNS: list[str] = [
        r"\brm\b", r"\bdel\b", r"\brmdir\b",
        r"git\s+push", r"git\s+reset", r"git\s+rebase", r"git\s+force",
        r"npm\s+publish", r"pip\s+install", r"pip3\s+install",
        r"\bsudo\b", r"\bdocker\b", r"\bkubectl\b",
        r"curl\s.*\|\s*sh", r"curl\s.*\|\s*bash", r"wget\s.*\|\s*sh",
        r"\beval\b", r"\bexec\b",
        r">\s*/", r"truncate\b", r"mkfs\b", r"dd\s+if=",
        r"chmod\s+777", r"chown\b",
        r"npm\s+uninstall", r"yarn\s+remove",
        r"git\s+checkout\s+--", r"git\s+clean\s+-fd",
        r"Remove-Item", r"Set-ExecutionPolicy",
    ]

    def __init__(self) -> None:
        self._deny_rules: list[PermissionRule] = []
        self._ask_rules: list[PermissionRule] = []
        self._allow_rules: list[PermissionRule] = []

        # Session-level approvals: tool_name → set of approved patterns
        self._session_always_approved: set[str] = set()
        # Approved-once: (tool_name, frozen_args_repr)
        self._session_once_approved: set[str] = set()

        # Trust mode — set by settings loader or /trust command
        self._trust_mode: str = "smart"  # "strict" | "smart" | "yolo"
        # User-configured safe/blocked commands (from settings)
        self._user_trusted_commands: list[str] = []
        self._user_blocked_commands: list[str] = []
        # Session-wide trust-all flag (escalated via 't' option)
        self._session_trust_all: bool = False

        # Read-only tools that never need permission
        self._always_allowed: set[str] = {
            "read_file", "glob", "grep", "list_dir",
            "cvc_status", "cvc_log", "cvc_search",
            "cvc_smart_search", "cvc_diff",
            "cvc_list_documents", "task_list", "task_get",
        }

    def load_rules(
        self,
        allow: list[str] | None = None,
        deny: list[str] | None = None,
        ask: list[str] | None = None,
    ) -> None:
        """
        Load permission rules from parsed settings.

        Parameters match the 'permissions' section of settings.json:
            {
                "permissions": {
                    "allow": ["Bash(npm run *)", "Read"],
                    "deny": ["Bash(rm -rf *)"],
                    "ask": ["Edit", "WebFetch"]
                }
            }
        """
        if deny:
            for rule_str in deny:
                self._deny_rules.append(PermissionRule.parse(rule_str, PermissionAction.DENY))
        if ask:
            for rule_str in ask:
                self._ask_rules.append(PermissionRule.parse(rule_str, PermissionAction.ASK))
        if allow:
            for rule_str in allow:
                self._allow_rules.append(PermissionRule.parse(rule_str, PermissionAction.ALLOW))

    def add_rule(self, rule: PermissionRule) -> None:
        """
        Append a single PermissionRule to the appropriate tier.

        Used by sub-agent permission setup and the `/permissions` CLI command.
        Normalizes the action field — callers may pass either a PermissionAction
        enum or the raw string ("allow"/"deny"/"ask"); the rule is bucketed by
        action regardless, and evaluate() compares on the enum, so we coerce
        here to keep matching consistent.
        """
        action = rule.action
        if isinstance(action, str):
            try:
                action = PermissionAction(action.lower())
                rule.action = action
            except ValueError:
                logger.warning("add_rule: unknown action %r — defaulting to ALLOW", rule.action)
                action = PermissionAction.ALLOW
                rule.action = action

        if action == PermissionAction.DENY:
            self._deny_rules.append(rule)
        elif action == PermissionAction.ASK:
            self._ask_rules.append(rule)
        else:
            self._allow_rules.append(rule)

    def add_cli_rules(
        self,
        allowed_tools: list[str] | None = None,
        disallowed_tools: list[str] | None = None,
    ) -> None:
        """
        Add rules from CLI flags (highest precedence after deny).
        --allowedTools and --disallowedTools CLI arguments.
        """
        if disallowed_tools:
            for rule_str in disallowed_tools:
                # CLI denied tools get inserted at the front (highest priority)
                self._deny_rules.insert(
                    0, PermissionRule.parse(rule_str, PermissionAction.DENY)
                )
        if allowed_tools:
            for rule_str in allowed_tools:
                self._allow_rules.insert(
                    0, PermissionRule.parse(rule_str, PermissionAction.ALLOW)
                )

    def evaluate(
        self, tool_name: str, tool_input: dict[str, Any]
    ) -> PermissionDecision:
        """
        Evaluate whether a tool call should be allowed, denied, or asked about.

        Returns PermissionDecision.ALLOWED, DENIED, or ASK_USER.
        """
        # Always-allowed tools (read-only) bypass all rules
        if tool_name in self._always_allowed:
            return PermissionDecision.ALLOWED

        # Session-wide trust-all escalation (via 't' option)
        if self._session_trust_all:
            return PermissionDecision.ALLOWED

        # Yolo mode: everything auto-allowed
        if self._trust_mode == "yolo":
            return PermissionDecision.ALLOWED

        # Check session-level "always approve" for this tool
        if tool_name in self._session_always_approved:
            return PermissionDecision.ALLOWED

        # Check session-level "once approve" for this specific invocation
        invocation_key = f"{tool_name}:{_args_key(tool_input)}"
        if invocation_key in self._session_once_approved:
            return PermissionDecision.ALLOWED

        # 1. Deny rules — checked first, always win
        for rule in self._deny_rules:
            if rule.matches_args(tool_name, tool_input):
                logger.info("Permission DENIED by rule: %s", rule.raw)
                return PermissionDecision.DENIED

        # Check user-blocked commands for bash
        if tool_name == "bash":
            cmd = tool_input.get("command", "")
            for blocked in self._user_blocked_commands:
                if blocked in cmd:
                    return PermissionDecision.DENIED

        # 2. Allow rules — auto-approve
        for rule in self._allow_rules:
            if rule.matches_args(tool_name, tool_input):
                return PermissionDecision.ALLOWED

        # 3. Ask rules — prompt user
        for rule in self._ask_rules:
            if rule.matches_args(tool_name, tool_input):
                return PermissionDecision.ASK_USER

        # 4. Trust-mode-aware default
        if self._trust_mode == "smart":
            return self._smart_evaluate(tool_name, tool_input)

        # Strict mode: ask for everything not explicitly allowed
        return PermissionDecision.ASK_USER

    def _smart_evaluate(
        self, tool_name: str, tool_input: dict[str, Any]
    ) -> PermissionDecision:
        """Smart trust mode: auto-allow safe operations, ask for risky ones."""
        # File writes within workspace are auto-allowed in smart mode
        if tool_name in ("write_file", "edit_file", "patch_file"):
            return PermissionDecision.ALLOWED

        # Bash commands: ALWAYS ask for permission
        if tool_name == "bash":
            return PermissionDecision.ASK_USER

        # Agent/skill tools: ask before delegation
        if tool_name in ("agent", "skill"):
            return PermissionDecision.ASK_USER

        # Everything else: allow in smart mode
        return PermissionDecision.ALLOWED

    def _is_safe_command(self, command: str) -> bool:
        """Check if a bash command is in the safe list."""
        cmd_lower = command.lower().strip()
        # Check user-trusted commands first
        for trusted in self._user_trusted_commands:
            if cmd_lower.startswith(trusted.lower()):
                return True
        # Check built-in safe commands
        for safe in self.SAFE_COMMANDS:
            if cmd_lower == safe.lower() or cmd_lower.startswith(safe.lower() + " "):
                return True
        return False

    def _is_risky_command(self, command: str) -> bool:
        """Check if a bash command matches risky patterns."""
        for pattern in self._RISKY_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    def set_trust_mode(self, mode: str) -> None:
        """Set the trust mode. Valid: 'strict', 'smart', 'yolo'."""
        if mode in ("strict", "smart", "yolo"):
            self._trust_mode = mode

    def get_trust_mode(self) -> str:
        """Get the current trust mode."""
        return self._trust_mode

    def trust_all_session(self) -> None:
        """Escalate to trust-all for the remainder of this session."""
        self._session_trust_all = True

    def load_trust_settings(
        self,
        trust_mode: str = "smart",
        trusted_commands: list[str] | None = None,
        blocked_commands: list[str] | None = None,
    ) -> None:
        """Load trust settings from CvcSettings."""
        self.set_trust_mode(trust_mode)
        if trusted_commands:
            self._user_trusted_commands = trusted_commands
        if blocked_commands:
            self._user_blocked_commands = blocked_commands

    def approve_always(self, tool_name: str) -> None:
        """Mark a tool as always-approved for this session."""
        self._session_always_approved.add(tool_name)

    def approve_once(self, tool_name: str, tool_input: dict[str, Any]) -> None:
        """Mark a specific tool invocation as approved for this session."""
        key = f"{tool_name}:{_args_key(tool_input)}"
        self._session_once_approved.add(key)

    def get_rules_summary(self) -> dict[str, list[str]]:
        """Get a summary of all loaded rules for display."""
        return {
            "allow": [r.raw for r in self._allow_rules],
            "deny": [r.raw for r in self._deny_rules],
            "ask": [r.raw for r in self._ask_rules],
            "session_approved": sorted(self._session_always_approved),
        }

    def reset_session(self) -> None:
        """Clear session-level approvals."""
        self._session_always_approved.clear()
        self._session_once_approved.clear()


def _args_key(tool_input: dict[str, Any]) -> str:
    """Create a hashable key from tool arguments for once-approval tracking."""
    if not tool_input:
        return ""
    # Use the first argument value as the key (e.g., command for bash, path for edit)
    first_val = next(iter(tool_input.values()), "")
    return str(first_val)[:200]
