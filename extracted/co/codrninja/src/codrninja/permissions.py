"""Advanced permission system for codrninja."""

from __future__ import annotations

import fnmatch
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Tuple


VALID_ACTIONS = {"allow", "deny", "ask"}
VALID_SCOPES = {"read", "write", "execute", "all"}
VALID_AGENT_TYPES = {"all", "build", "plan", "subagent"}


@dataclass(frozen=True)
class PermissionRule:
    """A permission rule for path or command matching."""

    pattern: str
    action: str
    scope: str = "all"
    agent_type: str = "all"
    priority: int = 0

    def __post_init__(self):
        if self.action not in VALID_ACTIONS:
            raise ValueError(f"Invalid action: {self.action}")
        if self.scope not in VALID_SCOPES:
            raise ValueError(f"Invalid scope: {self.scope}")
        if self.agent_type not in VALID_AGENT_TYPES:
            raise ValueError(f"Invalid agent_type: {self.agent_type}")

    def matches(self, action: str, target: str, agent_type: str) -> bool:
        if self.scope not in {"all", action}:
            return False
        if self.agent_type not in {"all", agent_type}:
            return False
        return _glob_match(target, self.pattern)


BUILTIN_RULES: Tuple[PermissionRule, ...] = (
    PermissionRule("**/.env*", "deny", "write", "all", -1000),
    PermissionRule("**/*.pem", "deny", "write", "all", -1000),
    PermissionRule("**/*.key", "deny", "write", "all", -1000),
    PermissionRule("/etc/*", "deny", "write", "all", -1000),
    PermissionRule("**/node_modules/**", "deny", "write", "all", -1000),
    PermissionRule("**/.git/**", "deny", "write", "all", -1000),
    PermissionRule("**/.codrninja/**", "deny", "write", "all", -1000),
    PermissionRule("rm -rf /", "deny", "execute", "all", -1000),
    PermissionRule("dd if=", "deny", "execute", "all", -1000),
    PermissionRule("mkfs.", "deny", "execute", "all", -1000),
    PermissionRule("docker rm -f", "ask", "execute", "all", -1000),
    PermissionRule("docker system prune", "ask", "execute", "all", -1000),
)

DANGEROUS_COMMAND_PATTERNS: Tuple[str, ...] = (
    "rm -rf /",
    "dd if=",
    "mkfs.",
    "docker rm -f",
    "docker system prune",
)


@dataclass(frozen=True)
class PermissionDecision:
    action: str
    rule: Optional[PermissionRule]
    target: str
    scope: str
    agent_type: str
    source: str


class PermissionManager:
    """Evaluate and persist permission rules."""

    VALID_MODES = {"none", "ask", "auto", "strict", "relaxed", "custom"}

    def __init__(
        self,
        config_path: Optional[Path] = None,
        mode: str = "ask",
        project_root: Optional[str] = None,
        parent: Optional["PermissionManager"] = None,
    ):
        self.config_path = Path(config_path or Path.home() / ".codrninja" / "permissions.json")
        self.project_root = os.path.abspath(project_root or os.getcwd())
        self.parent = parent
        
        # Load saved mode from config file if it exists
        saved_mode = mode
        if self.config_path.exists():
            try:
                data = json.loads(self.config_path.read_text())
                saved_mode = data.get("mode", mode)
            except Exception:
                pass
        self.mode = saved_mode if saved_mode in self.VALID_MODES else "ask"
        self.default_action = self._mode_default_action(self.mode)
        self._custom_rules: List[PermissionRule] = []
        self._compiled_rules: List[PermissionRule] = []
        self.load_config(self.config_path)

    def _mode_default_action(self, mode: Optional[str] = None) -> str:
        effective_mode = mode or self.mode
        if effective_mode == "none":
            return "deny"
        if effective_mode in {"auto", "relaxed"}:
            return "allow"
        return "ask"

    def set_mode(self, mode: str):
        if mode not in self.VALID_MODES:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode
        self.default_action = self._mode_default_action(mode)
        self._rebuild_rules()

    def _rebuild_rules(self):
        mode_rules = self._mode_rules()
        combined = [*self._custom_rules, *mode_rules, *BUILTIN_RULES]
        self._compiled_rules = sorted(combined, key=lambda rule: rule.priority, reverse=True)

    def _mode_rules(self) -> List[PermissionRule]:
        if self.mode == "strict":
            return [
                PermissionRule(os.path.join(self.project_root, "**"), "allow", "all", "all", 5),
                PermissionRule("*", "ask", "all", "all", -10),
            ]
        if self.mode in {"relaxed", "auto"}:
            return [PermissionRule("*", "allow", "all", "all", -10)]
        if self.mode == "ask":
            return [PermissionRule("*", "ask", "all", "all", -10)]
        if self.mode == "none":
            return [PermissionRule("*", "deny", "all", "all", -10)]
        return []

    def load_config(self, path: Optional[Path] = None):
        """Load permission configuration from disk."""
        if path is not None:
            self.config_path = Path(path)

        self.default_action = self._mode_default_action()
        self._custom_rules = []

        if self.config_path.exists():
            try:
                data = json.loads(self.config_path.read_text())
                default_action = data.get("default", self.default_action)
                if default_action in VALID_ACTIONS:
                    self.default_action = default_action
                self._custom_rules = [PermissionRule(**rule) for rule in data.get("rules", [])]
            except (json.JSONDecodeError, OSError, TypeError, ValueError):
                self.default_action = self._mode_default_action()
                self._custom_rules = []

        self._rebuild_rules()

    def save_config(self):
        """Persist custom rules and default action."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "mode": self.mode,
            "default": self.default_action,
            "rules": [asdict(rule) for rule in self._custom_rules],
        }
        self.config_path.write_text(json.dumps(payload, indent=2) + "\n")

    def add_rule(self, rule: PermissionRule):
        self._custom_rules = [existing for existing in self._custom_rules if not self._same_rule(existing, rule)]
        self._custom_rules.append(rule)
        self._rebuild_rules()
        self.save_config()

    def remove_rule(self, pattern: str) -> bool:
        before = len(self._custom_rules)
        self._custom_rules = [rule for rule in self._custom_rules if rule.pattern != pattern]
        changed = len(self._custom_rules) != before
        if changed:
            self._rebuild_rules()
            self.save_config()
        return changed

    def list_rules(self) -> List[PermissionRule]:
        return list(self._compiled_rules)

    def set_default(self, action: str):
        if action not in VALID_ACTIONS:
            raise ValueError(f"Invalid action: {action}")
        self.default_action = action
        self.save_config()

    def check(self, action: str, path: str, agent_type: str) -> str:
        return self.decide(action, path, agent_type).action

    def decide(self, action: str, path: str, agent_type: str) -> PermissionDecision:
        action = _normalize_scope(action)
        agent_type = agent_type if agent_type in VALID_AGENT_TYPES else "all"
        target = _normalize_target(path, action)

        for rule in self._compiled_rules:
            if rule.matches(action, target, agent_type):
                decision = PermissionDecision(rule.action, rule, target, action, agent_type, self._rule_source(rule))
                return self._apply_parent_restriction(decision)

        decision = PermissionDecision(self.default_action, None, target, action, agent_type, "default")
        return self._apply_parent_restriction(decision)

    def explain(self, action: str, path: str, agent_type: str) -> str:
        decision = self.decide(action, path, agent_type)
        if decision.rule:
            return (
                f"{decision.action.upper()} via {decision.source} rule "
                f"pattern={decision.rule.pattern!r} scope={decision.rule.scope} "
                f"agent_type={decision.rule.agent_type} priority={decision.rule.priority}"
            )
        return f"{decision.action.upper()} via default action ({self.default_action})"

    def check_dangerous(self, command: str) -> bool:
        normalized = _normalize_command(command)
        return any(pattern in normalized for pattern in DANGEROUS_COMMAND_PATTERNS)

    def _apply_parent_restriction(self, decision: PermissionDecision) -> PermissionDecision:
        if not self.parent:
            return decision
        parent_decision = self.parent.decide(decision.scope, decision.target, "build")
        child_rank = _action_rank(decision.action)
        parent_rank = _action_rank(parent_decision.action)
        if child_rank > parent_rank:
            return PermissionDecision(
                parent_decision.action,
                parent_decision.rule,
                decision.target,
                decision.scope,
                decision.agent_type,
                "parent",
            )
        return decision

    def _rule_source(self, rule: PermissionRule) -> str:
        if rule in BUILTIN_RULES:
            return "builtin"
        if rule in self._custom_rules:
            return "custom"
        return f"mode:{self.mode}"

    @staticmethod
    def _same_rule(left: PermissionRule, right: PermissionRule) -> bool:
        return (
            left.pattern == right.pattern
            and left.scope == right.scope
            and left.agent_type == right.agent_type
        )


def _action_rank(action: str) -> int:
    return {"deny": 0, "ask": 1, "allow": 2}[action]


def _normalize_scope(action: str) -> str:
    if action not in {"read", "write", "execute"}:
        raise ValueError(f"Invalid scope/action: {action}")
    return action


def _normalize_target(target: str, action: str) -> str:
    if action == "execute":
        return _normalize_command(target)
    expanded = os.path.abspath(os.path.expanduser(target))
    return expanded.replace("\\", "/")


def _normalize_command(command: str) -> str:
    return " ".join(command.strip().lower().split())


def _glob_match(target: str, pattern: str) -> bool:
    normalized_target = target.replace("\\", "/")
    normalized_pattern = pattern.replace("\\", "/")
    if fnmatch.fnmatch(normalized_target, normalized_pattern):
        return True
    basename = os.path.basename(normalized_target)
    return fnmatch.fnmatch(basename, normalized_pattern)
