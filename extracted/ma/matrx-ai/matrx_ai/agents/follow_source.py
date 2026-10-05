"""A copy that follows its source — the one place a run resolves it.

A template install copies a platform agent into a person's organization and points its
variables at her tables. The copy carries ``follows_source = true``
(``agent.definition``, campaign migration ``templates7_b``). While it does, a RUN resolves
the SOURCE's current instructions, tools, model and settings, and keeps only the copy's own
variable bindings — so a fix to the platform agent reaches everyone who installed it. An
edit to the copy's instructions, tools or model turns ``follows_source`` off in the database
(trigger ``zz_follows_source_stops_on_edit``); ``agx_reset_agent_to_source`` turns it back on.

``followed_row(copy, source)`` is pure; ``resolve_followed_row(row, load_source)`` is the
one code path ``AgxDefinitionManager.to_config`` calls for every definition row.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

# What a following copy takes from its source (the trigger's list, plus the switch that
# travels with context_policies).
FOLLOWED_FIELDS: tuple[str, ...] = (
    "messages",
    "tools",
    "custom_tools",
    "mcp_servers",
    "model_id",
    "model_tiers",
    "settings",
    "output_schema",
    "context_policies",
    "auto_context_disabled",
    "tool_config",
    "skill_config",
)

# What a variable keeps from the COPY: the person's own binding (her tables).
OWN_VARIABLE_KEYS: tuple[str, ...] = ("binding", "defaultValue")


def follows_its_source(row: Any) -> bool:
    return bool(getattr(row, "follows_source", False)) and bool(getattr(row, "source_agent_id", None))


def merge_variable_definitions(source_defs: Any, own_defs: Any) -> list[Any]:
    """The source's variables, each carrying the copy's own binding/default when the copy has one."""
    own_by_name: dict[str, dict[str, Any]] = {}
    for d in own_defs or []:
        if isinstance(d, dict) and isinstance(d.get("name"), str):
            own_by_name[d["name"]] = d
    merged: list[Any] = []
    for d in source_defs or []:
        if not isinstance(d, dict):
            merged.append(d)
            continue
        out = dict(d)
        own = own_by_name.get(str(d.get("name")))
        if own is not None:
            for key in OWN_VARIABLE_KEYS:
                if key in own:
                    out[key] = own[key]
                else:
                    out.pop(key, None)
        merged.append(out)
    return merged


class FollowedRow:
    """The copy's row with the followed fields read from its source."""

    def __init__(self, copy: Any, source: Any) -> None:
        self._copy = copy
        self._source = source
        self.variable_definitions = merge_variable_definitions(
            getattr(source, "variable_definitions", None),
            getattr(copy, "variable_definitions", None),
        )

    def __getattr__(self, name: str) -> Any:
        if name in FOLLOWED_FIELDS:
            return getattr(self._source, name)
        return getattr(self._copy, name)


def followed_row(copy: Any, source: Any) -> FollowedRow:
    return FollowedRow(copy, source)


async def resolve_followed_row(row: Any, load_source: Callable[[str], Awaitable[Any | None]]) -> Any:
    """``row`` itself, or — when it follows its source — the row a run executes."""
    if not follows_its_source(row):
        return row
    source_id = str(row.source_agent_id)
    source = await load_source(source_id)
    if source is None or getattr(source, "deleted_at", None) is not None:
        vcprint(
            {"agent_id": str(getattr(row, "id", "?")), "source_agent_id": source_id},
            "[follow_source] The source agent is gone — running the copy's own content",
            color="yellow",
        )
        return row
    return followed_row(row, source)
