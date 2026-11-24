"""The small-model tool limit — a MODEL limit, so it lives at the call-time layer (L2).

Owner rulings this reconciles:

* Arman (``common-docs/systems/apps/desktop/projects/matrx-2/VISION.md`` § Cloud Chat as a platform Surface):
  "some of the really small models should never get that many tools" — so each tool bundle
  carries a small-model off switch (``tool.bundle.metadata.small_model = "off"``).
* TOOL-SOURCES.md rule L: the core toolset (L1, aidream ``apply_unified_tools``) never reads
  the model; a model/provider limit lives HERE (``matrx_ai/providers``) and every removal is
  announced.

So the core computes the same toolset for every model and only NAMES the surface-added
listers of bundles marked off (``SMALL_MODEL_OPTIONAL_TOOLS_KEY`` on the request metadata —
the bundle row is the declared source). At call time, a model the catalog rates at or below
the small-model ceiling has those listers removed from THIS call, and the removal is
announced (``SMALL_MODEL_TOOLS_REMOVED``). Only tools the automatic layer added are removed:
a bundle the agent declares or the person picked always rides. The tools stay on the
conversation (stickiness), so a larger model on the next call gets them again.
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_ai.providers.tool_adaptation import (
    SMALL_MODEL_OPTIONAL_TOOLS_KEY,
    SMALL_MODEL_TOOLS_REMOVED,
    ToolAdaptation,
    automatic_tool_names,
)

#: A model is "small" when its catalog ``ai.model_definition.cost_rating`` is at or below this
#: (the rating runs 1..6, 6 the top tier).
#: KNOB MIRROR of platform.feature_knob "tool_bundles" "small_model_max_cost_rating".
logger = logging.getLogger(__name__)

SMALL_MODEL_MAX_COST_RATING = 2


def small_model_ceiling() -> int:
    """The live ceiling: the knob when the host has it, else the mirror above."""
    from matrx_ai.knobs import package_knob

    raw = package_knob("tool_bundles", "small_model_max_cost_rating", SMALL_MODEL_MAX_COST_RATING)
    try:
        return int(raw)
    except (TypeError, ValueError):
        # A bad knob value is an admin mistake to see, never a silent default.
        logger.error("tool_bundles.small_model_max_cost_rating is not a whole number (%r); using %d", raw, SMALL_MODEL_MAX_COST_RATING)
        return SMALL_MODEL_MAX_COST_RATING


def is_small_model(rating: object) -> bool:
    """True for a model the catalog rates at or below the small-model ceiling.

    An unrated model (``None``) is NOT small: a model the catalog says nothing about keeps
    everything its surface offers.
    """
    if rating is None or isinstance(rating, bool):
        return False
    try:
        value = int(rating)  # type: ignore[call-overload]
    except (TypeError, ValueError):
        return False
    return value <= small_model_ceiling()


def _optional_tool_names() -> set[str]:
    from matrx_connect.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    metadata = getattr(ctx, "metadata", None) if ctx is not None else None
    if not isinstance(metadata, dict):
        return set()
    return {str(n) for n in metadata.get(SMALL_MODEL_OPTIONAL_TOOLS_KEY) or () if n}


def _tool_name(tool: Any) -> str:
    return str(tool if isinstance(tool, str) else getattr(tool, "name", tool))


def strip_small_model_optional_tools(
    config: Any, caps: Any, wire_format: str | None = None
) -> ToolAdaptation | None:
    """Remove, for a small model, the surface-added listers of bundles marked small-model off."""
    optional = _optional_tool_names()
    if not optional or not is_small_model(getattr(caps, "model_cost_rating", None)):
        return None
    tools = list(getattr(config, "tools", None) or [])
    automatic = automatic_tool_names(config)
    removed = sorted({_tool_name(t) for t in tools if _tool_name(t) in optional and _tool_name(t) in automatic})
    if not removed:
        return None
    # THIS TURN ONLY (CGU-10 IMG9 #7): the stored chat keeps its tools (the lister included) and a
    # larger model next turn gets them again. ``authored_tools`` is never touched: writing the
    # pre-strip list there made an automatic lister permanent.
    from matrx_ai.config.unified_config import narrow_tools_this_turn_only

    narrow_tools_this_turn_only(
        config,
        [t for t in tools if _tool_name(t) not in removed],
        list(getattr(config, "custom_tools", None) or []),
    )
    return ToolAdaptation(
        code=SMALL_MODEL_TOOLS_REMOVED,
        model=getattr(caps, "model_name", None),
        wire_format=wire_format,
        removed=removed,
        reason=(
            "This is a small model, so the tool bundles marked off for small models were not "
            "offered on this call."
        ),
        detail={
            "model_cost_rating": getattr(caps, "model_cost_rating", None),
            "small_model_max_cost_rating": small_model_ceiling(),
        },
    )


__all__ = [
    "SMALL_MODEL_MAX_COST_RATING",
    "is_small_model",
    "small_model_ceiling",
    "strip_small_model_optional_tools",
]
