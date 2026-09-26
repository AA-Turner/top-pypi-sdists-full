"""Test Holders for code calls held by ``matrx_ai.mandates.hold_code_call``.

A converted code site RESOLVES its mandate on every call, so a unit test of that
site needs a resolver — and the honest one is the real ``hold_code_call`` walking
a real resolution to a real (inline) agent, not a monkeypatched ``hold_code_call``
that could return anything. ``install_inline_holders`` installs exactly that:
each key resolves to an ``InlineAgentSource`` built from the config dict you
give it (``model`` + ``messages`` — the same shape an agent row carries).
An optional ``variables`` entry declares the Holder's variables, in the stored
row shape (``[{"name", "defaultValue"}]``), for a Holder whose authored turns
template the site's offered values.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import mandates as _mandates
from matrx_ai.agents.named import InlineAgentSource
from matrx_ai.agents.variables import AgentVariable


def install_inline_holders(
    monkeypatch: pytest.MonkeyPatch, holders: dict[str, dict[str, Any]]
) -> list[str]:
    """Resolve each mandate key in ``holders`` to an inline agent; any other key
    raises like a real resolver would. Returns the list of keys resolved, in order."""
    resolved: list[str] = []

    async def _resolver(mandate_key: str) -> _mandates.MandateResolution:
        if mandate_key not in holders:
            raise LookupError(f"no test Holder for {mandate_key!r}")
        resolved.append(mandate_key)
        config = dict(holders[mandate_key])
        declared = config.pop("variables", None)
        return _mandates.MandateResolution(
            source=InlineAgentSource(
                config_dict=config,
                variable_defaults=AgentVariable.from_list(declared) if declared else None,
                name=f"holder:{mandate_key}",
            )
        )

    monkeypatch.setattr(_mandates, "_MANDATE_RESOLVER", _resolver)
    return resolved


__all__ = ["install_inline_holders"]
