"""Who answered and what it cost — read ONE way for every caller.

A programmatic agent run (``matrx_ai.agents.executor.run_agent`` → the research
pipeline's ``rs_analysis`` / ``rs_synthesis`` rows) and a workflow AI step
(``matrx_ai.graph_nodes.shared.normalize_completed_result``) both report the model
that ran and the run's usage record. These two functions are that reading, so a
row written by either path carries the same ``model_id`` and ``token_usage``.
"""

from __future__ import annotations

from typing import Any


def run_model_id(metadata: dict[str, Any] | None, config: Any) -> str | None:
    """The model that ran: the execution metadata's ``model``, else the
    resolved config's slug (programmatic runs do not reliably stamp metadata)."""
    model_id = (metadata or {}).get("model")
    if not model_id:
        model_id = getattr(config, "model", None)
    return str(model_id) if model_id else None


def run_token_usage(total_usage: Any) -> dict[str, Any]:
    """The run's usage record as stored (``AggregatedUsage.to_dict()``); ``{}``
    when the run reported none."""
    if total_usage is None:
        return {}
    try:
        return dict(total_usage.to_dict())
    except Exception:  # noqa: BLE001 — a usage object that cannot serialize is no usage
        return {}
