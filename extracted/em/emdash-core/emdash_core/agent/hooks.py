"""Hook system for running commands on agent events.

Hooks allow users to run shell commands when specific events occur
during agent execution. Hooks are configured per-project in
.emdash/hooks.json and run asynchronously (non-blocking).

Example .emdash/hooks.json:
{
  "hooks": [
    {
      "id": "notify-done",
      "event": "session_end",
      "command": "notify-send 'Agent finished'",
      "enabled": true
    }
  ]
}
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any
import json
import os
import subprocess
import threading

from .events import AgentEvent, EventHandler, EventType
from ..utils.logger import log


class HookEventType(str, Enum):
    """Event types that can trigger hooks.

    This is a subset of EventType exposed for hook configuration.
    """
    TOOL_START = "tool_start"
    TOOL_RESULT = "tool_result"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    RESPONSE = "response"
    ERROR = "error"

    @classmethod
    def from_event_type(cls, event_type: EventType) -> "HookEventType | None":
        """Convert an EventType to HookEventType if mappable."""
        mapping = {
            EventType.TOOL_START: cls.TOOL_START,
            EventType.TOOL_RESULT: cls.TOOL_RESULT,
            EventType.SESSION_START: cls.SESSION_START,
            EventType.SESSION_END: cls.SESSION_END,
            EventType.RESPONSE: cls.RESPONSE,
            EventType.ERROR: cls.ERROR,
        }
        return mapping.get(event_type)


@dataclass
class HookEventData:
    """Data passed to hook commands via stdin as JSON.

    Attributes:
        event: The event type that triggered the hook
        timestamp: ISO format timestamp of when the event occurred
        session_id: The session ID (if available)

        # Tool-specific fields (for tool_start, tool_result)
        tool_name: Name of the tool being executed
        tool_args: Arguments passed to the tool (tool_start only)
        tool_result: Result summary from the tool (tool_result only)
        tool_success: Whether the tool succeeded (tool_result only)
        tool_error: Error message if tool failed (tool_result only)

        # Response fields (for response event)
        response_text: The response content

        # Session fields
        goal: The goal/query for the session (session_start only)
        success: Whether the session completed successfully (session_end only)

        # Error fields
        error_message: Error message (error event only)
        error_details: Additional error details (error event only)
    """
    event: str
    timestamp: str
    session_id: str | None = None

    # Tool fields
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = None
    tool_result: str | None = None
    tool_success: bool | None = None
    tool_error: str | None = None

    # Response fields
    response_text: str | None = None

    # Session fields
    goal: str | None = None
    success: bool | None = None

    # Error fields
    error_message: str | None = None
    error_details: str | None = None

    def to_json(self) -> str:
        """Convert to JSON string, excluding None values."""
        data = {k: v for k, v in asdict(self).items() if v is not None}
        return json.dumps(data)

    def to_env_vars(self) -> dict[str, str]:
        """Convert to environment variables for quick access.

        Returns a dict of EMDASH_* prefixed env vars.
        """
        env = {
            "EMDASH_EVENT": self.event,
            "EMDASH_TIMESTAMP": self.timestamp,
        }
        if self.session_id:
            env["EMDASH_SESSION_ID"] = self.session_id
        if self.tool_name:
            env["EMDASH_TOOL_NAME"] = self.tool_name
        if self.tool_success is not None:
            env["EMDASH_TOOL_SUCCESS"] = str(self.tool_success).lower()
        if self.goal:
            env["EMDASH_GOAL"] = self.goal
        if self.success is not None:
            env["EMDASH_SUCCESS"] = str(self.success).lower()
        if self.error_message:
            env["EMDASH_ERROR"] = self.error_message
        return env


@dataclass
class HookConfig:
    """Configuration for a single hook.

    Attributes:
        id: Unique identifier for the hook
        event: Event type that triggers this hook
        command: Shell command to execute
        enabled: Whether the hook is active
    """
    id: str
    event: HookEventType
    command: str
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "event": self.event.value,
            "command": self.command,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HookConfig":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            event=HookEventType(data["event"]),
            command=data["command"],
            enabled=data.get("enabled", True),
        )


@dataclass
class HooksFile:
    """The .emdash/hooks.json file structure.

    Attributes:
        hooks: List of hook configurations
    """
    hooks: list[HookConfig] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "hooks": [h.to_dict() for h in self.hooks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HooksFile":
        """Create from dictionary."""
        hooks = [HookConfig.from_dict(h) for h in data.get("hooks", [])]
        return cls(hooks=hooks)


class HookManager:
    """Manages hook loading, execution, and configuration.

    Hooks are loaded from .emdash/hooks.json and executed asynchronously
    when matching events occur.
    """

    def __init__(self, repo_root: Path | None = None):
        """Initialize the hook manager.

        Args:
            repo_root: Root directory of the repository.
                      Defaults to current working directory.
        """
        self._repo_root = repo_root or Path.cwd()
        self._hooks_file = self._repo_root / ".emdash" / "hooks.json"
        self._hooks: list[HookConfig] = []
        self._session_id: str | None = None
        self._load_hooks()

    @property
    def hooks_file_path(self) -> Path:
        """Get the path to the hooks file."""
        return self._hooks_file

    def set_session_id(self, session_id: str | None) -> None:
        """Set the current session ID for event data."""
        self._session_id = session_id

    def _load_hooks(self) -> None:
        """Load hooks from .emdash/hooks.json."""
        if not self._hooks_file.exists():
            self._hooks = []
            return

        try:
            data = json.loads(self._hooks_file.read_text())
            hooks_file = HooksFile.from_dict(data)
            self._hooks = hooks_file.hooks
            log.debug(f"Loaded {len(self._hooks)} hooks from {self._hooks_file}")
        except Exception as e:
            log.warning(f"Failed to load hooks: {e}")
            self._hooks = []

    def reload(self) -> None:
        """Reload hooks from disk."""
        self._load_hooks()

    def get_hooks(self) -> list[HookConfig]:
        """Get all configured hooks."""
        return self._hooks.copy()

    def get_enabled_hooks(self, event: HookEventType) -> list[HookConfig]:
        """Get enabled hooks for a specific event type."""
        return [h for h in self._hooks if h.enabled and h.event == event]

    def add_hook(self, hook: HookConfig) -> None:
        """Add a new hook and save to disk."""
        # Check for duplicate ID
        if any(h.id == hook.id for h in self._hooks):
            raise ValueError(f"Hook with id '{hook.id}' already exists")

        self._hooks.append(hook)
        self._save_hooks()

    def remove_hook(self, hook_id: str) -> bool:
        """Remove a hook by ID. Returns True if removed."""
        for i, h in enumerate(self._hooks):
            if h.id == hook_id:
                self._hooks.pop(i)
                self._save_hooks()
                return True
        return False

    def toggle_hook(self, hook_id: str) -> bool | None:
        """Toggle a hook's enabled state. Returns new state or None if not found."""
        for h in self._hooks:
            if h.id == hook_id:
                h.enabled = not h.enabled
                self._save_hooks()
                return h.enabled
        return None

    def _save_hooks(self) -> None:
        """Save hooks to .emdash/hooks.json."""
        self._hooks_file.parent.mkdir(parents=True, exist_ok=True)
        hooks_file = HooksFile(hooks=self._hooks)
        self._hooks_file.write_text(
            json.dumps(hooks_file.to_dict(), indent=2) + "\n"
        )
        log.debug(f"Saved {len(self._hooks)} hooks to {self._hooks_file}")

    def _build_event_data(self, event: AgentEvent, hook_event: HookEventType) -> HookEventData:
        """Build HookEventData from an AgentEvent."""
        data = HookEventData(
            event=hook_event.value,
            timestamp=event.timestamp.isoformat(),
            session_id=self._session_id,
        )

        # Populate event-specific fields
        if hook_event == HookEventType.TOOL_START:
            data.tool_name = event.data.get("name")
            data.tool_args = event.data.get("args")

        elif hook_event == HookEventType.TOOL_RESULT:
            data.tool_name = event.data.get("name")
            data.tool_success = event.data.get("success")
            data.tool_result = event.data.get("summary")
            if not data.tool_success:
                data.tool_error = event.data.get("data", {}).get("error")

        elif hook_event == HookEventType.SESSION_START:
            data.goal = event.data.get("goal")

        elif hook_event == HookEventType.SESSION_END:
            data.success = event.data.get("success")

        elif hook_event == HookEventType.RESPONSE:
            data.response_text = event.data.get("content")

        elif hook_event == HookEventType.ERROR:
            data.error_message = event.data.get("message")
            data.error_details = event.data.get("details")

        return data

    def _execute_hook_async(self, hook: HookConfig, event_data: HookEventData) -> None:
        """Execute a hook command asynchronously (fire and forget)."""
        def run():
            try:
                env = os.environ.copy()
                env.update(event_data.to_env_vars())

                process = subprocess.Popen(
                    hook.command,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    cwd=str(self._repo_root),
                )

                # Send JSON data to stdin
                json_data = event_data.to_json()
                assert process.stdin is not None
                process.stdin.write(json_data.encode())
                process.stdin.close()

                # Don't wait for completion - fire and forget
                # But log if there's an error
                def log_completion():
                    _, stderr = process.communicate(timeout=30)
                    if process.returncode != 0:
                        log.warning(
                            f"Hook '{hook.id}' exited with code {process.returncode}: "
                            f"{stderr.decode()[:200]}"
                        )

                # Run completion logging in another thread to not block
                completion_thread = threading.Thread(target=log_completion, daemon=True)
                completion_thread.start()

            except Exception as e:
                log.warning(f"Failed to execute hook '{hook.id}': {e}")

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    def trigger(self, event: AgentEvent) -> None:
        """Trigger hooks for an event.

        Called by the event system when events occur.
        """
        hook_event = HookEventType.from_event_type(event.type)
        if hook_event is None:
            return

        hooks = self.get_enabled_hooks(hook_event)
        if not hooks:
            return

        event_data = self._build_event_data(event, hook_event)

        for hook in hooks:
            log.debug(f"Triggering hook '{hook.id}' for event '{hook_event.value}'")
            self._execute_hook_async(hook, event_data)


class HookHandler(EventHandler):
    """Event handler that triggers hooks.

    Add this handler to an AgentEventEmitter to enable hooks.
    """

    def __init__(self, manager: HookManager):
        """Initialize with a hook manager.

        Args:
            manager: The HookManager to use for triggering hooks
        """
        self._manager = manager

    def handle(self, event: AgentEvent) -> None:
        """Handle an event by triggering matching hooks."""
        self._manager.trigger(event)


# Convenience functions

_default_manager: HookManager | None = None


def get_hook_manager(repo_root: Path | None = None) -> HookManager:
    """Get or create the default hook manager."""
    global _default_manager
    if _default_manager is None:
        _default_manager = HookManager(repo_root)
    return _default_manager


def reset_hook_manager() -> None:
    """Reset the default hook manager (for testing)."""
    global _default_manager
    _default_manager = None
