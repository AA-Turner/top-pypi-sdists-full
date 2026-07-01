"""Agent picker dialog — shows available agents for selection."""

from __future__ import annotations

import typing as t

from rich.text import Text
from textual.message import Message
from textual.widgets.option_list import Option

from dreadnode.app.tui.theme import BRAND, FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin


class AgentDialog(OverlayMixin):
    """Popup dialog triggered by ^A — lists agents from loaded capabilities."""

    class AgentSelected(Message):
        """Posted when an agent is selected from the dialog."""

        def __init__(self, agent_name: str) -> None:
            self.agent_name = agent_name
            super().__init__()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._agents: list[dict[str, str]] = []

    def show_agents(self, agents: list[dict[str, str]], current: str = "default") -> None:
        """Populate the dialog with agents and show it.

        Each dict has keys: name, description, model, capability.
        """
        self._agents = agents
        self.clear_options()

        if not agents:
            self.add_option(
                Option(
                    Text("No agents loaded", style=f"italic {FG_MUTED}"),
                    disabled=True,
                )
            )
            self.border_title = "Agents"
            self.add_class("-visible")
            return

        for agent in agents:
            name = agent.get("name", "?")
            is_current = name == current

            label = Text()
            # Selection dot + name
            if is_current:
                label.append(" \u25cf ", style=BRAND)
                label.append(name, style=f"bold {FG}")
            else:
                label.append(" \u25cb ", style=FG_FAINTEST)
                label.append(name, style=FG_SUBTLE)

            # Capability source — separated
            cap = agent.get("capability", "")
            if cap and cap != "built-in":
                label.append(f"  \u00b7  {cap}", style=FG_FAINTEST)

            # Description — same line, truncated
            desc = agent.get("description", "")
            if desc:
                if len(desc) > 60:
                    desc = desc[:57] + "\u2026"
                label.append(f"\n     {desc}", style=FG_MUTED)

            # Model — only if overridden (non-default)
            model = agent.get("model", "inherit")
            if model and model != "inherit":
                # Shorten long model paths
                if "/" in model:
                    model = model.rsplit("/", 1)[-1]
                label.append(f"  {model}", style=FG_FAINTEST)

            self.add_option(Option(label, id=name))

        self.highlighted = 0
        self.border_title = f"Agents ({len(agents)})"
        self.add_class("-visible")

    def select_highlighted(self) -> bool:
        if not self.is_visible or self.option_count == 0:
            return False
        idx = self.highlighted
        if idx is not None and 0 <= idx < self.option_count:
            option = self.get_option_at_index(idx)
            if option.id:
                self.post_message(self.AgentSelected(option.id))
                self.hide()
                return True
        return False

    def on_option_list_option_selected(self, event: OverlayMixin.OptionSelected) -> None:
        option_id = event.option.id
        if option_id:
            self.post_message(self.AgentSelected(option_id))
            self.hide()
