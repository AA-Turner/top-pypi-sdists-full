"""The train-time-RTC runtime (openpi JAX) on shared pools: a checkpoint trained with RTC
(its catalog rtc_max_prefix_rows) runs RTC off or on with the late-bound prefix, one trained
without it plain sampling only, each on the JAX backend at its SDK contract's geometry."""

from __future__ import annotations

from dreamscale_transport import catalog

from dreamscale.policy.runtime.contract import (
    _optional_attr,
    fixed_check,
    runtime_contract_for_model,
)
from dreamscale.policy.runtime.rtc import LATE_BOUND_PREFIX_RTC_CONTRACT_ID


def check(model, resolved_config, *, execution_horizon, chunk_size_override, **overrides):
    entry, own = catalog.entry(model), runtime_contract_for_model(model)
    name = entry.client.refusal_name
    hz, chunk, dim = int(own.action_hz), own.chunk_size, own.action_dim
    expected = {
        "action_hz": hz, "chunk_size": chunk, "action_dim": dim,
        "action_space": own.action_space, "hold_behavior": own.hold_behavior,
        "backend": "jax",
    }
    rtc_contract = _optional_attr(resolved_config, "rtc_contract")
    if entry.rtc_max_prefix_rows:
        # Trained with RTC: off, or on with the late-bound prefix.
        rtc = _optional_attr(resolved_config, "rtc")
        refused = rtc not in ("on", "off") or rtc_contract != (
            LATE_BOUND_PREFIX_RTC_CONTRACT_ID if rtc == "on" else None)
    else:
        # Trained without RTC: plain sampling only.
        expected["rtc"] = "off"
        refused = rtc_contract is not None
    return fixed_check(name, resolved_config, expected, action_hz=hz, chunk_size=chunk,
                       action_dim=dim, refused=refused, chunk_size_override=chunk_size_override,
                       **overrides)

