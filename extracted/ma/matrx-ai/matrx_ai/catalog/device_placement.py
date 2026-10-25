"""Host seam: is this model installed on that device? (L5 design §1, guard G12.)

A device-served call (``served_via``) may only resolve when the device actually holds the model:
every required ``ai.device_model_file`` of the model's variant usable on
``served_via.app_instance_id`` — or, for a person's own uncatalogued file, the
``ai.device_model_file`` row whose id IS ``served_via.local_model_id``.

matrx-ai never reads those tables itself (they are the host's ORM models), so the host binds
the answer once at startup::

    from matrx_ai.catalog.device_placement import configure_device_placement
    configure_device_placement(check)   # async (served_via, *, model_id) -> bool

Unbound (a bare package, a client host) means NO device run can be admitted: the call is
refused with ``model_not_on_device`` and says the check is not wired — never admitted blind.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from matrx_ai.config.served_via import ServedVia

#: The host rule's refusal codes (twin of @ai-matrx/agents ``DeviceModelUnavailableError.code``).
DEVICE_PLACEMENT_REFUSAL_CODES: frozenset[str] = frozenset(
    {"not_on_device", "unknown_model", "unknown_variant", "file_not_usable", "not_own_file",
     "not_a_chat_model"}
)


@dataclass(frozen=True)
class DevicePlacementRefusal:
    """Why the device cannot run the model: one of :data:`DEVICE_PLACEMENT_REFUSAL_CODES`."""

    code: str
    message: str


@dataclass(frozen=True)
class DeviceOwnFile:
    """Admitted: ``local_model_id`` is the person's own uncatalogued file on that device
    (``ai.device_model_file`` with ``artifact_id`` null, usable per the twin rule). Carries only
    what the file knows — its file name and its metadata (``metadata.gguf`` when read)."""

    file_id: str
    name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    #: The ModelKey the person's computer runs this file under (any protocol ModelKey it
    #: published on the file row, e.g. ``own-<name>-<hash8>``); ``None`` = not reported yet.
    model_key: str | None = None


#: ``async (served_via, *, model_id) -> None | True | False | DeviceOwnFile | DevicePlacementRefusal``
#: — ``None``/``True`` admits a catalog model; a :class:`DeviceOwnFile` admits the person's own
#: file; ``False`` is ``not_on_device``; a refusal names its code.
DevicePlacementCheck = Callable[
    ..., Awaitable["bool | DeviceOwnFile | DevicePlacementRefusal | None"]
]

_check: DevicePlacementCheck | None = None


def configure_device_placement(check: DevicePlacementCheck | None) -> None:
    """Bind the host's placement check; ``None`` unbinds it (every device run is refused)."""
    global _check
    _check = check


def device_placement_check() -> DevicePlacementCheck | None:
    """The bound check (the host's wiring guard reads it)."""
    return _check


async def assert_model_on_device(
    served_via: ServedVia, *, model_id: str, model_name: str
) -> DeviceOwnFile | None:
    """Raise ``ModelNotOnDeviceError`` unless the device can run ``model_id``; returns the
    :class:`DeviceOwnFile` when the admitted model is the person's own file."""
    from matrx_ai.providers.device.errors import ModelNotOnDeviceError

    if _check is None:
        raise ModelNotOnDeviceError(
            f"device placement check is not wired in this process; refusing to send "
            f"{model_name!r} to device {served_via.app_instance_id}",
            user_message="This model can't be checked on your computer right now.",
            details={"app_instance_id": served_via.app_instance_id, "model_id": model_id},
        )
    verdict = await _check(served_via, model_id=model_id)
    if verdict is None or verdict is True:
        return None
    if isinstance(verdict, DeviceOwnFile):
        return verdict
    if isinstance(verdict, DevicePlacementRefusal):
        code, reason = verdict.code, verdict.message
    else:
        code, reason = "not_on_device", "the device does not hold every required file"
    raise ModelNotOnDeviceError(
        f"model {model_name!r} ({model_id}, local id {served_via.local_model_id!r}, variant "
        f"{served_via.variant_id!r}) cannot run on device {served_via.app_instance_id}: "
        f"{code}: {reason}",
        user_message=f"{model_name} isn't on that computer.",
        details={
            "code": code,
            "app_instance_id": served_via.app_instance_id,
            "model_id": model_id,
            "local_model_id": served_via.local_model_id,
            "variant_id": served_via.variant_id,
        },
    )


__all__ = [
    "DEVICE_PLACEMENT_REFUSAL_CODES",
    "DeviceOwnFile",
    "DevicePlacementCheck",
    "DevicePlacementRefusal",
    "assert_model_on_device",
    "configure_device_placement",
    "device_placement_check",
]
