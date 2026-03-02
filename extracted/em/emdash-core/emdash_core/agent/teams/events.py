"""Event bridge — connects team events to EmDash's existing event system.

Agent Teams emits its own events (TeamEventType). This bridge:
1. Converts TeamEventType → EventType for the existing SSE pipeline
2. Extends HookEventType with team-specific hook triggers
3. Forwards teammate events to the lead's emitter (with attribution)

Integration points:
  - AgentEventEmitter: team events flow through as PROGRESS events
    with a "team_event" key for the SSE handler to detect
  - HookManager: team hooks (teammate_idle, team_task_completed) trigger
    shell commands like any other hook
  - SSE stream: clients receive team events tagged with teammate name
"""

from typing import Any

from ..events import AgentEvent, AgentEventEmitter, EventType, EventHandler
from ..hooks import HookEventType, HookEventData, HookManager
from .models import TeamEventType


# ─────────────────────────────────────────────────────────────
# Extended hook events for teams
# ─────────────────────────────────────────────────────────────

# These are additional hook event types that can trigger shell commands.
# They extend the base HookEventType enum conceptually.
# In the hooks.json, users specify them as string event names.

TEAM_HOOK_EVENTS = {
    "teammate_idle": "Triggered when a teammate finishes and goes idle",
    "team_task_completed": "Triggered when a task is marked complete",
    "teammate_spawned": "Triggered when a new teammate is spawned",
    "teammate_stopped": "Triggered when a teammate shuts down",
    "team_message": "Triggered when an inter-agent message is sent",
}


# ─────────────────────────────────────────────────────────────
# Event bridge
# ─────────────────────────────────────────────────────────────


class TeamEventBridge(EventHandler):
    """Bridges team events into the standard event pipeline.

    Attached to the lead's AgentEventEmitter. When team events
    arrive (via PROGRESS events with team_event key), this bridge:
    1. Triggers team-specific hooks
    2. Formats events for SSE clients

    Usage:
        bridge = TeamEventBridge(hook_manager=get_hook_manager())
        emitter.add_handler(bridge)
    """

    def __init__(self, hook_manager: HookManager | None = None):
        self._hook_manager = hook_manager

    def handle(self, event: AgentEvent) -> None:
        """Handle an event — check if it's a team event and process it."""
        if event.event_type != EventType.PROGRESS:
            return

        team_event = event.data.get("team_event")
        if not team_event:
            return

        # Trigger team hooks
        if self._hook_manager:
            self._trigger_team_hooks(team_event, event.data)

    def _trigger_team_hooks(self, team_event: str, data: dict[str, Any]) -> None:
        """Trigger hooks for team events.

        Maps team events to hook event names and executes matching hooks.
        """
        # Map TeamEventType values to hook event names
        hook_event_map = {
            TeamEventType.TEAMMATE_IDLE.value: "teammate_idle",
            TeamEventType.TEAM_TASK_COMPLETED.value: "team_task_completed",
            TeamEventType.TEAMMATE_SPAWNED.value: "teammate_spawned",
            TeamEventType.TEAMMATE_STOPPED.value: "teammate_stopped",
            TeamEventType.TEAM_MESSAGE_SENT.value: "team_message",
        }

        hook_event_name = hook_event_map.get(team_event)
        if not hook_event_name:
            return

        # Build hook data and trigger
        hook_data = HookEventData(
            event=hook_event_name,
            timestamp=data.get("timestamp", ""),
            session_id=data.get("agent_id"),
        )

        # Find hooks matching this event name
        # Since team hooks aren't in the HookEventType enum,
        # we check manually against hook configs
        for hook in self._hook_manager.get_hooks():
            if hook.enabled and hook.event.value == hook_event_name:
                self._hook_manager._execute_hook_async(hook, hook_data)


class TeammateEventForwarder(EventHandler):
    """Forwards events from a teammate's emitter to the lead.

    Wraps each event with teammate attribution so the lead's
    UI can display per-teammate activity.
    """

    def __init__(self, teammate_name: str, lead_emitter: AgentEventEmitter):
        self._teammate_name = teammate_name
        self._lead_emitter = lead_emitter

    def handle(self, event: AgentEvent) -> None:
        """Forward event to lead with attribution."""
        # Skip forwarding session-level events (too noisy)
        if event.event_type in (EventType.SESSION_START, EventType.SESSION_END):
            return

        self._lead_emitter.emit(EventType.PROGRESS, {
            "teammate_event": True,
            "teammate_name": self._teammate_name,
            "original_type": event.event_type.value,
            "data": event.data,
        })
