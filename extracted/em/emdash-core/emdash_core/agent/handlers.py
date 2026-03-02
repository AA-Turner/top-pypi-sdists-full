"""Event handlers for agent output.

Provides various handler implementations for routing agent events
to different destinations.
"""

import json
import sys
from typing import IO, Optional

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from .events import AgentEvent, AgentEventEmitter, EventType


class RichConsoleHandler(AgentEventEmitter):
    """Handler that renders events to the console using Rich.

    Provides a nice interactive display with spinners, panels,
    and formatted output.
    """

    def __init__(
        self,
        agent_name: str = "Agent",
        console: Optional[Console] = None,
        show_thinking: bool = True,
    ):
        """Initialize the console handler.

        Args:
            agent_name: Name to display for the agent
            console: Rich console instance
            show_thinking: Whether to show thinking blocks
        """
        super().__init__(agent_name)
        self.console = console or Console()
        self.show_thinking = show_thinking
        self._current_message = ""
        self._current_thinking = ""
        self._in_message = False
        self._in_thinking = False

    def _handle(self, event: AgentEvent) -> None:
        """Handle an event by rendering to console."""
        if event.type == EventType.AGENT_START:
            goal = event.data.get("goal", "")
            self.console.print(
                Panel(
                    f"[bold cyan]{self.agent_name}[/bold cyan] starting...\n"
                    f"[dim]Goal: {goal}[/dim]",
                    border_style="cyan",
                )
            )

        elif event.type == EventType.AGENT_END:
            success = event.data.get("success", True)
            if success:
                self.console.print("[green]Agent completed successfully[/green]")
            else:
                self.console.print("[red]Agent finished with errors[/red]")

        elif event.type == EventType.AGENT_ERROR:
            error = event.data.get("error", "Unknown error")
            self.console.print(f"[red bold]Error:[/red bold] {error}")

        elif event.type == EventType.MESSAGE_START:
            self._in_message = True
            self._current_message = ""

        elif event.type == EventType.MESSAGE_DELTA:
            content = event.data.get("content", "")
            self._current_message += content
            # Print incrementally
            self.console.print(content, end="")

        elif event.type == EventType.MESSAGE_END:
            self._in_message = False
            if self._current_message:
                self.console.print()  # Newline

        elif event.type == EventType.TOOL_START:
            name = event.data.get("name", "tool")
            args = event.data.get("args", {})
            args_str = ", ".join(f"{k}={v!r}" for k, v in list(args.items())[:3])
            self.console.print(f"[dim]> {name}({args_str})[/dim]")

        elif event.type == EventType.TOOL_RESULT:
            name = event.data.get("name", "tool")
            success = event.data.get("success", True)
            summary = event.data.get("summary", "")
            if success:
                self.console.print(f"[green]  {name}: {summary}[/green]")
            else:
                self.console.print(f"[red]  {name} failed: {summary}[/red]")

        elif event.type == EventType.THINKING_START:
            if self.show_thinking:
                self._in_thinking = True
                self._current_thinking = ""
                self.console.print("[dim italic]Thinking...[/dim italic]")

        elif event.type == EventType.THINKING_DELTA:
            if self.show_thinking:
                content = event.data.get("content", "")
                self._current_thinking += content

        elif event.type == EventType.THINKING_END:
            if self.show_thinking and self._current_thinking:
                # Optionally show thinking summary
                self._in_thinking = False


class JSONStreamHandler(AgentEventEmitter):
    """Handler that outputs events as JSON lines.

    Suitable for piping to other processes or web clients.
    """

    def __init__(
        self,
        agent_name: str = "Agent",
        output: IO = sys.stdout,
    ):
        """Initialize the JSON stream handler.

        Args:
            agent_name: Name for the agent
            output: Output stream (default stdout)
        """
        super().__init__(agent_name)
        self.output = output

    def _handle(self, event: AgentEvent) -> None:
        """Handle an event by writing JSON."""
        try:
            json_line = json.dumps(event.to_dict())
            self.output.write(json_line + "\n")
            self.output.flush()
        except Exception:
            pass  # Don't break on serialization errors


class CollectingHandler(AgentEventEmitter):
    """Handler that collects all events for later processing.

    Useful for testing or batch processing.
    """

    def __init__(self, agent_name: str = "Agent"):
        """Initialize the collecting handler."""
        super().__init__(agent_name)
        self.events: list[AgentEvent] = []

    def _handle(self, event: AgentEvent) -> None:
        """Collect the event."""
        self.events.append(event)

    def clear(self) -> None:
        """Clear collected events."""
        self.events.clear()

    def get_events(self, event_type: Optional[EventType] = None) -> list[AgentEvent]:
        """Get collected events, optionally filtered by type.

        Args:
            event_type: Optional type to filter by

        Returns:
            List of events
        """
        if event_type is None:
            return list(self.events)
        return [e for e in self.events if e.type == event_type]


class CompositeHandler(AgentEventEmitter):
    """Handler that forwards events to multiple handlers.

    Allows combining multiple output destinations.
    """

    def __init__(
        self,
        agent_name: str = "Agent",
        handlers: Optional[list[AgentEventEmitter]] = None,
    ):
        """Initialize the composite handler.

        Args:
            agent_name: Name for the agent
            handlers: List of handlers to forward to
        """
        super().__init__(agent_name)
        self.handlers = handlers or []

    def add_handler(self, handler: AgentEventEmitter) -> None:
        """Add a handler.

        Args:
            handler: Handler to add
        """
        self.handlers.append(handler)

    def remove_handler(self, handler: AgentEventEmitter) -> None:
        """Remove a handler.

        Args:
            handler: Handler to remove
        """
        self.handlers = [h for h in self.handlers if h != handler]

    def _handle(self, event: AgentEvent) -> None:
        """Forward event to all handlers."""
        for handler in self.handlers:
            try:
                handler.emit(event)
            except Exception:
                pass  # Don't let one handler break others
