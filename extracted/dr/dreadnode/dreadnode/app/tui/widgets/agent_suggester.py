"""Ghost-text autocomplete for @agent mentions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.suggester import Suggester

if TYPE_CHECKING:
    from dreadnode.app.client.models import RuntimeInfo


class AgentSuggester(Suggester):
    """Provides ghost-text suggestions for @agent-name completions."""

    def __init__(self) -> None:
        super().__init__(use_cache=False, case_sensitive=False)
        self._agent_names: list[str] = []

    def update_agents(self, runtime_info: RuntimeInfo | None) -> None:
        """Refresh the list of available agent names from runtime info."""
        if runtime_info is None:
            self._agent_names = []
            return
        self._agent_names = [
            agent.name for capability in runtime_info.capabilities for agent in capability.agents
        ]

    async def get_suggestion(self, value: str) -> str | None:
        """Return a suggestion if the input starts with @ and matches an agent."""
        if not value.startswith("@") or " " in value:
            return None

        prefix = value[1:].lower()
        if not prefix:
            return None

        for name in self._agent_names:
            if name.lower().startswith(prefix):
                return f"@{name} "

        return None
