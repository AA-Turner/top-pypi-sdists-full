"""Invocation-local Agent Tasks evidence shared by scheduler scan consumers."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from agentic_devtools.cli.ci.agent_task_inventory import (
    AgentTaskInventoryAvailability,
    AgentTaskInventoryLoadResult,
)
from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.pipeline.session_detector import SessionState

logger = logging.getLogger(__name__)


@dataclass
class SchedulerInventoryScan:
    """Cache one load, retaining typed uncertainty and only captured metadata."""

    inventory: list[object] | AgentTaskInventoryLoadResult | None = None
    loaded: bool = False
    source: str | None = None
    reason: str | None = None
    _observed_availability: AgentTaskInventoryAvailability | None = None
    session_diagnostics: SessionState | None = None

    @property
    def availability(self) -> AgentTaskInventoryAvailability | None:
        """Legacy lists are complete; an unobserved scan is not complete-empty."""
        if self._observed_availability is not None:
            return self._observed_availability
        if isinstance(self.inventory, AgentTaskInventoryLoadResult):
            return self.inventory.availability
        if isinstance(self.inventory, list):
            return AgentTaskInventoryAvailability.COMPLETE
        return AgentTaskInventoryAvailability.UNAVAILABLE if self.loaded else None

    def load(self, loader: Callable[[], list[object] | AgentTaskInventoryLoadResult]) -> None:
        """Load once without owning retries or reconstructing exception metadata."""
        if self.loaded:
            return
        try:
            self.inventory = loader()
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning("Failed to load Agent Tasks inventory for scheduler scan: %s", exc)
        self.loaded = True
        if isinstance(self.inventory, AgentTaskInventoryLoadResult):
            self.reason = "; ".join(self.inventory.incomplete_reasons) or None

    def observe_session(self, state: SessionState) -> None:
        """Retain an existing session-boundary downgrade without inferring failure facts."""
        from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome

        if (
            self.inventory is None
            or state.outcome is SessionOutcome.EXPIRED
            or state.inventory_availability
            not in {
                AgentTaskInventoryAvailability.PARTIAL,
                AgentTaskInventoryAvailability.UNAVAILABLE,
            }
        ):
            return
        if self.availability is not AgentTaskInventoryAvailability.COMPLETE:
            if (
                isinstance(self.inventory, AgentTaskInventoryLoadResult)
                and self.inventory.availability is state.inventory_availability
                and self.inventory.http_status == state.http_status
                and self.inventory.failure_category == state.failure_category
            ):
                self.source = self.source or state.failure_source
            return
        self.session_diagnostics = state
        self._observed_availability = state.inventory_availability
        self.source = state.failure_source
        self.reason = state.failure_category.value if state.failure_category else None
