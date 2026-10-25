"""``ServedVia`` — WHERE a chat model runs when it is not a cloud offering.

A model on a person's own Matrx 2 computer is just another way to serve a catalog model: the
request names the model exactly as for the cloud (``model`` = ``ai.model_definition.id``) and adds
``served_via`` to say "run it on this device". There is no device ``ai.provider`` row, no per-device
catalog row, no offering and no price (L5 design, REVISION 1 §R2).

LIFECYCLE (``UnifiedConfig``): ``served_via`` is part of the MODEL CHOICE. It is stored with the
conversation, restored on continuation, reverted with the model after a "this message only" pick,
and cleared by an override that names a model without it (a new cloud pick). Only the CALLER's run
request sets it: a mandate's overrides and a workflow step's settings refuse it
(:func:`refuse_served_via_outside_the_run_request`), and a child agent runs its own model.

A device-served run has exactly ONE route. Nothing ever moves it to the cloud: every reroute,
fallback, free-tier swap and child-safety swap site refuses or no-ops on it
(``providers/device/route_guard.py``).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_ai.config.validators import UuidString


class ServedVia(BaseModel):
    """The one device a chat model runs on for this call.

    * ``provider`` — ``"device"``: a person's Matrx 2 computer (the only kind today).
    * ``app_instance_id`` — the device (``public.app_instances.id``).
    * ``local_model_id`` — the device's own key for the model it loads; for a person's own
      uncatalogued model file it is the ``ai.device_model_file.id``.
    * ``variant_id`` — the catalog variant (``ai.model_variant.id``) installed, when known.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    provider: Literal["device"]
    app_instance_id: UuidString
    local_model_id: str = Field(min_length=1, max_length=512)
    variant_id: UuidString | None = None


class ServedViaRefusedError(ValueError):
    """``served_via`` arrived from somewhere other than the caller's own run request."""

    error_type = "served_via_not_allowed_here"

    def __init__(self, where: str) -> None:
        self.where = where
        super().__init__(
            f"served_via cannot be set by {where}: only the person's own run request picks a "
            "device to run on. The agent runs its own model here."
        )


def coerce_served_via(value: Any) -> ServedVia | None:
    """``value`` as a :class:`ServedVia` (a stored dict or an instance), or ``None``."""
    if value is None:
        return None
    if isinstance(value, ServedVia):
        return value
    return ServedVia.model_validate(value)


def served_via_kwargs(source: Any) -> dict[str, Any]:
    """``{"served_via": ...}`` when ``source`` (a config, or a ``ServedVia``/dict) carries a
    device pick, else ``{}`` — so a cloud call's resolver signature is exactly what it was."""
    value = source if isinstance(source, (ServedVia, Mapping)) else getattr(source, "served_via", None)
    return {"served_via": value} if value is not None else {}


def refuse_served_via_outside_the_run_request(
    overrides: Mapping[str, Any] | Any | None, *, where: str
) -> None:
    """Raise :class:`ServedViaRefusedError` when an override layer that is NOT the caller's run
    request (a mandate binding, a workflow step) carries ``served_via``."""
    if overrides is None:
        return
    if isinstance(overrides, Mapping):
        present = overrides.get("served_via") is not None
    else:
        present = getattr(overrides, "served_via", None) is not None
    if present:
        raise ServedViaRefusedError(where)


__all__ = [
    "ServedVia",
    "ServedViaRefusedError",
    "coerce_served_via",
    "served_via_kwargs",
    "refuse_served_via_outside_the_run_request",
]
