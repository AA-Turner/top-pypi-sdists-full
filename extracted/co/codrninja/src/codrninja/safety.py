"""Safety module for codrninja — dry-run, approval gates, step limits, restricted modes."""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class SafetyConfig:
    """Configuration for safety features."""
    dry_run: bool = False           # Preview actions without executing
    no_shell: bool = False          # Disable shell command execution
    allow_shell: bool = False       # Explicitly allow shell (overrides no_shell from config)
    allow_write: bool = False       # Explicitly allow file writes
    require_approval: bool = False  # Require approval before each action
    max_steps: int = 50             # Maximum tool invocations per agent run
    git_checkpoint: bool = True     # Auto-checkpoint before file changes
    rollback_on_error: bool = True  # Auto-rollback on error

    # Restricted paths — never allow writes here
    restricted_paths: List[str] = field(default_factory=lambda: [
        "/etc", "/usr", "/bin", "/sbin", "/boot", "/sys", "/proc",
        os.path.expanduser("~/.ssh"),
        os.path.expanduser("~/.gnupg"),
    ])

    # Shell command blacklist
    shell_blacklist: List[str] = field(default_factory=lambda: [
        "rm -rf /", "mkfs", "dd if=", ":(){:|:&};:", "fork bomb",
    ])

    @classmethod
    def from_cli_flags(cls, **kwargs) -> "SafetyConfig":
        """Create from CLI flags."""
        return cls(**{k: v for k, v in kwargs.items() if v is not None})


class SafetyManager:
    """Enforces safety policies during agent execution."""

    def __init__(self, config: SafetyConfig):
        self.config = config
        self.denied_actions: List[Dict[str, Any]] = []
        self.approved_actions: List[Dict[str, Any]] = []
        self.step_count = 0

    def check_tool(self, tool_name: str, params: Dict[str, Any]) -> Optional[str]:
        """Check if a tool call is allowed. Returns None if allowed, error message if denied."""
        # Step limit
        if self.step_count >= self.config.max_steps:
            return f"Maximum steps exceeded ({self.config.max_steps})"

        # Dry run — just log, don't actually deny
        if self.config.dry_run:
            self.denied_actions.append({
                "tool": tool_name, "params": params, "reason": "dry_run",
            })
            # In dry run mode, we still deny execution but record it
            return f"[DRY RUN] Would execute: {tool_name}({self._summarize_params(params)})"

        # Shell restrictions
        if tool_name == "execute_command":
            if self.config.no_shell and not self.config.allow_shell:
                self.denied_actions.append({
                    "tool": tool_name, "params": params, "reason": "no_shell",
                })
                return f"Shell execution is disabled (--no-shell flag active)"

            cmd = params.get("command", "")
            for blacklisted in self.config.shell_blacklist:
                if blacklisted in cmd.lower():
                    self.denied_actions.append({
                        "tool": tool_name, "params": params, "reason": "blacklisted_command",
                    })
                    return f"Command contains blacklisted pattern: {blacklisted}"

        # Write restrictions
        if tool_name in ("write_file", "edit_file"):
            path = params.get("path", "")
            if not self.config.allow_write:
                # Check if path is in restricted area
                for restricted in self.config.restricted_paths:
                    if path.startswith(restricted):
                        self.denied_actions.append({
                            "tool": tool_name, "params": params, "reason": "restricted_path",
                        })
                        return f"Write to restricted path denied: {path}"

        self.step_count += 1
        self.approved_actions.append({
            "tool": tool_name, "params": params, "step": self.step_count,
        })
        return None

    def check_approval(self, tool_name: str, params: Dict[str, Any]) -> bool:
        """Check if explicit approval is required and given."""
        if not self.config.require_approval:
            return True
        # In non-interactive mode, approval cannot be given
        # Interactive mode would prompt here — for CLI agent mode, deny
        return False

    def get_report(self) -> Dict[str, Any]:
        """Get a safety report of what was allowed/denied."""
        return {
            "dry_run": self.config.dry_run,
            "steps_taken": self.step_count,
            "steps_limit": self.config.max_steps,
            "denied_actions": len(self.denied_actions),
            "approved_actions": len(self.approved_actions),
            "denied_details": self.denied_actions[-10:],
        }

    def _summarize_params(self, params: Dict[str, Any]) -> str:
        """Create a short summary of params for dry-run messages."""
        parts = []
        for k, v in params.items():
            val = str(v)
            if len(val) > 50:
                val = val[:47] + "..."
            parts.append(f"{k}={val}")
        return ", ".join(parts)