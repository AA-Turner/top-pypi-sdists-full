"""Event-to-edge mapping — declarative LangGraph routing.

Provides ``EventEdgeRule``, ``EventEdgeConfig``, ``load_event_edge_mapping()``,
and ``build_routing_function()`` for mapping workflow events to LangGraph
graph transitions with dual-write to agdt workflow state.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class EventEdgeMappingError(Exception):
    """Raised when an event-edge mapping configuration is invalid."""


# Identifier conventions
_UNDERSCORE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_HYPHEN_PATTERN = re.compile(r"^[a-z][a-z0-9\-]*$")


@dataclass(frozen=True)
class EventEdgeRule:
    """A single event-to-edge routing rule.

    Attributes:
        event_name: The event that triggers this routing.
        source_node: Source node name (underscore convention).
        target_node: Target node name (underscore convention).
        agdt_step_name: Corresponding agdt workflow step (hyphen convention).
    """

    event_name: str
    source_node: str
    target_node: str
    agdt_step_name: str

    def __post_init__(self) -> None:
        """Validate identifier conventions."""
        if not _UNDERSCORE_PATTERN.match(self.source_node):
            raise EventEdgeMappingError(f"source_node must use underscores: {self.source_node!r}")
        if not _UNDERSCORE_PATTERN.match(self.target_node):
            raise EventEdgeMappingError(f"target_node must use underscores: {self.target_node!r}")
        if not _HYPHEN_PATTERN.match(self.agdt_step_name):
            raise EventEdgeMappingError(f"agdt_step_name must use hyphens: {self.agdt_step_name!r}")


@dataclass(frozen=True)
class EventEdgeConfig:
    """Collection of event-edge routing rules.

    Attributes:
        rules: Tuple of routing rules (immutable).
    """

    rules: tuple[EventEdgeRule, ...] = field(default_factory=tuple)


def load_event_edge_mapping(path: Path) -> EventEdgeConfig:
    """Load an event-edge mapping from a YAML or JSON file.

    Args:
        path: Path to the mapping file.

    Returns:
        A validated ``EventEdgeConfig``.

    Raises:
        EventEdgeMappingError: If the file is malformed.
        FileNotFoundError: If the file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Event-edge mapping file not found: {path}")

    content = path.read_text()

    if path.suffix in (".yml", ".yaml"):
        try:
            import yaml

            data = yaml.safe_load(content)
        except Exception as exc:
            raise EventEdgeMappingError(f"Failed to parse YAML: {exc}") from exc
    else:
        try:
            data = json.loads(content)
        except Exception as exc:
            raise EventEdgeMappingError(f"Failed to parse JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise EventEdgeMappingError(f"Mapping must be a dict, got {type(data).__name__}")

    raw_rules = data.get("rules", [])
    if not isinstance(raw_rules, list):
        raise EventEdgeMappingError("'rules' must be a list")

    rules: list[EventEdgeRule] = []
    for idx, rule_data in enumerate(raw_rules):
        if not isinstance(rule_data, dict):
            raise EventEdgeMappingError(f"Rule at index {idx} must be a dict")
        try:
            rule = EventEdgeRule(
                event_name=rule_data["event_name"],
                source_node=rule_data["source_node"],
                target_node=rule_data["target_node"],
                agdt_step_name=rule_data["agdt_step_name"],
            )
            rules.append(rule)
        except KeyError as exc:
            raise EventEdgeMappingError(f"Rule at index {idx} missing field: {exc}") from exc

    return EventEdgeConfig(rules=tuple(rules))


def build_routing_function(
    config: EventEdgeConfig,
    source_node: str,
    *,
    default_target: str = "end",
) -> Callable[[dict[str, Any]], str]:
    """Build a conditional edge routing function for a source node.

    Returns a callable that examines the state dict for events and returns
    the appropriate target node name.  Performs dual-write to agdt workflow
    state (non-printing) when a matching rule is found.

    Args:
        config: The event-edge configuration.
        source_node: The source node this routing function serves.
        default_target: Fallback target when no event matches.

    Returns:
        A function ``(state: dict) -> str`` suitable for LangGraph conditional edges.
    """
    # Pre-filter rules for this source node
    relevant_rules = [r for r in config.rules if r.source_node == source_node]

    def route(state: dict[str, Any]) -> str:
        events = state.get("events", [])
        if not events:
            return default_target

        # Check the most recent event
        latest_event = events[-1] if isinstance(events, list) else None
        if latest_event is None:
            return default_target

        if isinstance(latest_event, str):
            event_name = latest_event
        elif isinstance(latest_event, dict):
            event_name = latest_event.get("name", "")
        else:
            return default_target

        for rule in relevant_rules:
            if rule.event_name == event_name:
                # Dual-write: sync agdt workflow state (non-printing)
                _sync_workflow_state(rule.agdt_step_name)
                return rule.target_node

        return default_target

    return route


def _sync_workflow_state(step_name: str) -> None:
    """Sync agdt workflow state without printing prompts.

    This is a non-printing helper that updates the workflow step
    in state without rendering prompt output to stdout.
    """
    try:
        from agentic_devtools.state import update_workflow_step

        update_workflow_step(step_name)
    except Exception:  # noqa: BLE001
        # Never fail the graph routing due to state sync issues
        pass
