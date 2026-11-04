"""Normalize simulator ``config`` payloads to plain dicts.

The generated ``SimulatorResponse.config`` is a discriminated
``ProxySimulatorConfig | DockerAppSimulatorConfig`` union (older specs used a
plain ``dict``). Callers that read config keys should go through
:func:`sim_config_dict` so both shapes keep working.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def sim_config_dict(config: Any) -> dict[str, Any]:
    """Return a simulator config as a plain dict, whether it's a pydantic model or a dict.

    ``exclude_unset`` keeps only the keys the server actually sent (extras are
    preserved via ``extra="allow"``), matching the shape of the raw JSON payload.
    """
    if isinstance(config, BaseModel):
        return config.model_dump(mode="json", exclude_unset=True)
    if isinstance(config, dict):
        return config
    return {}
