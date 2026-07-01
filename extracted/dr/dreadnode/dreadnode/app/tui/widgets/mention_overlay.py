"""@ mention overlay — shows capability agents for selection."""

from __future__ import annotations

import typing as t

from rich.text import Text
from textual.message import Message
from textual.widgets.option_list import Option

from dreadnode.app.tui.theme import BRAND, FG, FG_FAINTEST, FG_MUTED
from dreadnode.app.tui.widgets.overlay_mixin import OverlayMixin


class MentionOverlay(OverlayMixin):
    """Popup overlay triggered by @ — lists agents from loaded capabilities."""

    class AgentSelected(Message):
        """Posted when an agent is selected."""

        def __init__(self, agent_name: str) -> None:
            self.agent_name = agent_name
            super().__init__()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._agents: list[dict[str, str]] = []

    def set_agents(self, agents: list[dict[str, str]]) -> None:
        """Update the agent list from runtime info."""
        self._agents = agents

    def filter(self, query: str) -> None:
        """Filter agents by query and show the overlay."""
        query_lower = query.lower()
        self.clear_options()

        matches = [a for a in self._agents if query_lower in a["name"].lower()]

        if not matches:
            self.add_option(
                Option(Text("No matching agents", style=f"italic {FG_MUTED}"), disabled=True)
            )
            self.add_class("-visible")
            return

        for agent in matches:
            label = Text()
            label.append(" @", style=BRAND)
            label.append(agent["name"], style=f"bold {FG}")
            cap = agent.get("capability", "")
            if cap and cap != "built-in":
                label.append(f"  \u00b7  {cap}", style=FG_FAINTEST)
            if agent.get("model") and agent["model"] != "inherit":
                model = agent["model"]
                if "/" in model:
                    model = model.rsplit("/", 1)[-1]
                label.append(f"  {model}", style=FG_FAINTEST)
            self.add_option(Option(label, id=agent["name"]))

        self.highlighted = 0
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
