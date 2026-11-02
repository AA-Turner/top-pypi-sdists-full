"""Checkpoints whose served contract is the catalog's on any backend, executing the
checkpoint's horizon (named by their public names), served from us-west-2 (their placement
refusal names them by the catalog's placement name)."""

from __future__ import annotations

from dreamscale_transport import catalog

from dreamscale.model_names import public_model
from dreamscale.policy.runtime.contract import _optional_attr


def check(model, resolved_config, *, execution_horizon, action_hz_override, chunk_size_override,
          control_hz):
    entry = catalog.entry(model)
    contract, name = entry.contract, public_model(model)
    expected = {
        "action_hz": contract.action_hz, "chunk_size": contract.chunk_size,
        "action_dim": contract.action_dim, "action_space": contract.action_space,
        "hold_behavior": contract.hold_behavior, "rtc": entry.defaults.rtc,
    }
    if any(_optional_attr(resolved_config, key) != value for key, value in expected.items()):
        raise ValueError(f"{name} server returned an incomplete or incompatible contract")
    if execution_horizon is not None and execution_horizon != contract.execution_horizon:
        raise ValueError(f"{name} server returned an incompatible execution_horizon")
    if any(value is not None and value != contract.action_hz
           for value in (action_hz_override, control_hz)):
        raise ValueError(f"{name} requires {contract.action_hz} Hz execution")
    if chunk_size_override is not None and chunk_size_override != contract.chunk_size:
        raise ValueError(f"{name} requires {contract.chunk_size}-action chunks")
    return chunk_size_override


def placement(model, provider, region):
    """Served from us-west-2; its provider is checked as any model's."""
    from dreamscale.region_probe import _US_WEST_OK

    if region not in _US_WEST_OK:
        name = catalog.entry(model).client.placement_name
        raise ValueError(f"{name} is served from us-west-2; use region='available' or "
                         "'us-west-2'")
    return False
