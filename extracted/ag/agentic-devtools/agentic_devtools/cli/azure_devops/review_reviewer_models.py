"""Tolerant rubber-duck model resolver for the v2 PR review restructure.

Given a configured rubber-duck model *layer* (``"mainAgent"`` or ``"subagent"``),
the author's model, and the cached ``availableModels`` inventory, this module
resolves the validated set of rubber-duck models to use.

Behaviour (plan §7 + §15.11):

* Keep only models that are non-empty strings **and** present in
  ``availableModels``; every dropped value is logged with ``logger.warning``.
* When the layer is unconfigured, empty, or fully invalid, return the
  :data:`AGENT_PICKS` sentinel meaning "let the agent choose" — this function
  **never raises**.
* Otherwise apply a **best-effort** different-family preference: prefer two
  families different from the author's, then distinct families from each other.
  An unknown family is treated as the (lowercased) model name itself, so two
  unknown-but-differently-named models count as different families.

This is additive (Phase P0): nothing consumes the resolver yet.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from agentic_devtools.cli.azure_devops.review_attribution import get_model_family

if TYPE_CHECKING:  # pragma: no cover - typing only
    from agentic_devtools.cli.config.pull_request_review_config import PullRequestReviewConfig

logger = logging.getLogger(__name__)

# Number of rubber-duck models to select (plan: "2 ducks, different families").
_DUCK_COUNT = 2


class AgentPicks:
    """Sentinel type: no validated models configured; the agent should pick its own."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "AGENT_PICKS"


# Singleton sentinel returned when no validated rubber-duck models are available.
AGENT_PICKS = AgentPicks()


def model_family(model_name: str | None) -> str | None:
    """Return a best-effort family for *model_name*.

    Known families come from
    :func:`agentic_devtools.cli.azure_devops.review_attribution.get_model_family`.
    An unknown but non-empty model name is its **own** family (lowercased), so
    differently-named unknown models are treated as different families. Empty or
    ``None`` input returns ``None``.
    """
    if model_name is None:
        return None
    normalized = model_name.strip()
    if not normalized:
        return None
    family = get_model_family(normalized)
    if family is not None:
        return family
    return normalized.lower()


def _prefer_different_families(models: list[str], author_model: str | None) -> list[str]:
    """Select up to :data:`_DUCK_COUNT` models, best-effort.

    Preference order: models whose family differs from the author's come first,
    then the selection greedily picks distinct families; if fewer than
    :data:`_DUCK_COUNT` distinct families exist, remaining slots are filled in
    stable order. Deterministic and order-preserving.
    """
    author_family = model_family(author_model)
    different = [m for m in models if model_family(m) != author_family]
    same = [m for m in models if model_family(m) == author_family]
    ordered = different + same

    # Greedily pick one model per distinct family, preferring different-from-author
    # families first (their position in ``ordered``).
    picked: list[str] = []
    seen_families: set[str | None] = set()
    for candidate in ordered:
        family = model_family(candidate)
        if family not in seen_families:
            seen_families.add(family)
            picked.append(candidate)

    # If fewer than _DUCK_COUNT distinct families exist, fill remaining slots in
    # stable order (best-effort: same family is acceptable when nothing else fits).
    if len(picked) < _DUCK_COUNT:
        for candidate in ordered:
            if candidate not in picked:
                picked.append(candidate)

    return picked[:_DUCK_COUNT]


def resolve_rubber_duck_models(
    layer: str,
    author_model: str | None,
    available_models: list[str] | None,
    config: PullRequestReviewConfig | None,
) -> list[str] | AgentPicks:
    """Resolve the validated rubber-duck models for *layer*; never raises.

    Args:
        layer: Which rubber-duck list to resolve — ``"mainAgent"`` or ``"subagent"``.
        author_model: The author's model name (drives the different-family
            preference); may be ``None`` when unknown.
        available_models: The cached ``availableModels`` inventory; ``None`` is
            treated as empty.
        config: The :class:`PullRequestReviewConfig` (or ``None``); the layer list
            is read from ``config.rubberDuck``.

    Returns:
        A list of at most two validated model names, or :data:`AGENT_PICKS` when
        no valid models are configured for the layer.
    """
    rubber_duck = getattr(config, "rubberDuck", None)
    if rubber_duck is not None and not getattr(rubber_duck, "enabled", True):
        logger.debug(
            "Rubber-duck critiques are disabled (rubberDuck.enabled=False); the agent will pick its own models.",
        )
        return AGENT_PICKS

    configured = getattr(rubber_duck, layer, None) if rubber_duck is not None else None
    if not isinstance(configured, list):
        logger.warning(
            "Rubber-duck layer %r is not configured as a list; the agent will pick models.",
            layer,
        )
        return AGENT_PICKS

    available_set = {m.strip() for m in (available_models or []) if isinstance(m, str) and m.strip()}

    valid: list[str] = []
    for model in configured:
        if not isinstance(model, str):
            logger.warning("Ignoring invalid rubber-duck model entry: %r", model)
            continue

        normalized = model.strip()
        if not normalized:
            logger.warning("Ignoring invalid rubber-duck model entry: %r", model)
            continue

        if normalized not in available_set:
            logger.warning(
                "Ignoring rubber-duck model %r (not in availableModels).",
                normalized,
            )
            continue

        if normalized not in valid:
            valid.append(normalized)
    if not valid:
        logger.warning(
            "No valid rubber-duck models configured for layer %r; the agent will pick models.",
            layer,
        )
        return AGENT_PICKS

    return _prefer_different_families(valid, author_model)
