"""Who answered and what it cost — read ONE way for every caller.

A programmatic agent run (``matrx_ai.agents.executor.run_agent`` → the research
pipeline's ``rs_analysis`` / ``rs_synthesis`` rows) and a workflow AI step
(``matrx_ai.graph_nodes.shared.normalize_completed_result``) both report the model
that ran and the run's usage record. These two functions are that reading, so a
row written by either path carries the same ``model_id`` and ``token_usage``.
"""

from __future__ import annotations

from typing import Any


def run_model_id(metadata: dict[str, Any] | None, config: Any, usage: dict[str, Any] | None = None) -> str | None:
    """The model that ANSWERED: the one model the run's usage names (``by_model`` / ``models``), else the execution
    metadata's ``model``, else the resolved config's slug. A run moved to another model (a top-tier model swapped to its
    fallback for a person not approved for it) is configured on one model and answered by another; a stored row names
    the answering one (program-lead ruling, 2026-11-19, research side-by-side). Usage naming no single model (none, or
    several) leaves the configured reading."""
    # Two shapes of one record: ``AggregatedUsage.to_dict()`` keys by ``by_model``; the stored ``AiUsage`` by ``models``.
    named = (usage or {}).get("by_model") or (usage or {}).get("models") or {}
    names = list(named.keys())
    model_id = (metadata or {}).get("model")
    if not model_id:
        model_id = getattr(config, "model", None)
    # A row stores the catalog model ID, never a name: usage names the model by NAME, and a config may hold a name too
    # (a per-turn swap sets ``config.model`` to the stand-in's NAME — ``swap_model_this_turn_only``; live workflow run
    # 68c8c791 saved ``claude-sonnet-5-5`` where the code engine saved its id). Every reading goes through the
    # catalog's one name->id seam; a ref the catalog does not know stays as given.
    from matrx_ai.catalog.manager import ai_catalog_manager

    if len(names) == 1 and names[0]:
        return str(ai_catalog_manager.resolve_model_ref(str(names[0])))
    return str(ai_catalog_manager.resolve_model_ref(str(model_id))) if model_id else None


def run_token_usage(total_usage: Any) -> dict[str, Any]:
    """The run's usage record as stored (``AggregatedUsage.to_dict()``); ``{}``
    when the run reported none."""
    if total_usage is None:
        return {}
    try:
        return dict(total_usage.to_dict())
    except Exception:  # noqa: BLE001 — a usage object that cannot serialize is no usage
        return {}
