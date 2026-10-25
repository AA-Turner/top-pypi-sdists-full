"""THE NO-FALLBACK CLOSURE for device-served runs (L5 design REVISION 1, §R1 / P0-1).

A run the person sent to their own computer has exactly ONE route. Moving it anywhere else
would send their data to a cloud they did not pick, so every site that can change a run's model,
offering or route asks here first and refuses or no-ops on a device run:

* ``orchestrator/overload_reroute.py`` — ``is_reroutable_provider_error`` (False),
  ``load_overload_policy`` (no retries, no fallback), ``load_offering_ladder`` (None),
  ``decide_overload_action`` (give up);
* ``orchestrator/executor.py`` — the same-model retry decision (:func:`may_retry_provider_error`);
* ``providers/free_tier_models.py`` — ``swap_for_free_tier`` (no swap);
* ``providers/child_safety_gate.py`` — a host swap of a device run's model is REFUSED with
  :class:`DeviceRouteMoveRefusedError` and the model is put back (never moved to cloud).

The one fact every site reads is the run's ``served_via`` (on the config) or the profile's
``route_kind == "device"`` — decided once, at resolution.
"""

from __future__ import annotations

from typing import Any


def is_device_served(value: Any) -> bool:
    """True for a config carrying ``served_via``, a profile resolved to a device route, or a
    ``ServedVia`` itself."""
    if value is None:
        return False
    from matrx_ai.config.served_via import ServedVia

    if isinstance(value, ServedVia):
        return True
    if getattr(value, "route_kind", None) == "device":
        return True
    return getattr(value, "served_via", None) is not None


def may_retry_provider_error(config: Any, error_info: Any) -> bool:
    """Whether the executor may run the SAME call again after ``error_info``.

    A device run never retries: the device answered (or the relay did) and a second attempt
    after content may already have streamed would be a different answer, not a recovery.
    """
    if is_device_served(config):
        return False
    return bool(getattr(error_info, "is_retryable", False))


def refuse_device_move(config: Any, *, before_model: Any, site: str) -> None:
    """After a host step that may rewrite ``config.model`` (the child-safety swap): when the
    run is device-served and the model changed, put the model back and refuse the run."""
    if not is_device_served(config):
        return
    after = getattr(config, "model", None)
    if after == before_model:
        return
    config.model = before_model
    from matrx_ai.providers.device.errors import DeviceRouteMoveRefusedError

    raise DeviceRouteMoveRefusedError(
        f"{site} would move a device-served run from {before_model!r} to {after!r}; a device "
        "run has one route and is never moved to another model or to the cloud.",
        user_message=(
            "This model can't run for this account on your computer, and it won't be moved "
            "to the cloud. Pick another model."
        ),
        details={"site": site, "from_model": str(before_model), "to_model": str(after)},
    )


def is_private_device_turn(ctx: Any, config: Any) -> bool:
    """A store:false run on the person's own computer (owner ruling 2026-10-24): NO side agent
    (labeler, memory, condensing, first-runs judge, group cadence, diagram repair) may send
    this conversation to a cloud model. Every such site skips when this is True."""
    return ctx is not None and not getattr(ctx, "store", True) and is_device_served(config)


__all__ = ["is_device_served", "is_private_device_turn", "may_retry_provider_error", "refuse_device_move"]
