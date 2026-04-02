"""
Configuration export and import utilities.

Serializes and deserializes device configurations for backup,
transfer, or comparison purposes.

Public API of this module is defined by __all__.
"""

from datetime import UTC, datetime
import inspect
import json
from typing import Any, Final

from pydantic import BaseModel


class ExportedConfiguration(BaseModel):
    """Serializable device configuration snapshot."""

    version: str = "1.0"
    exported_at: str
    device_address: str
    model: str
    channel_address: str
    channel_type: str
    paramset_key: str
    values: dict[str, Any]


_EXPORT_VERSION: Final = "1.0"


def export_configuration(
    *,
    device_address: str,
    model: str,
    channel_address: str,
    channel_type: str,
    paramset_key: str,
    values: dict[str, Any],
) -> str:
    """
    Export a configuration as a JSON string.

    Returns a JSON string containing the device configuration
    with metadata for identification and versioning.
    """
    config = ExportedConfiguration(
        version=_EXPORT_VERSION,
        exported_at=datetime.now(tz=UTC).isoformat(),
        device_address=device_address,
        model=model,
        channel_address=channel_address,
        channel_type=channel_type,
        paramset_key=paramset_key,
        values=values,
    )
    return config.model_dump_json(indent=2)


def import_configuration(*, json_data: str) -> ExportedConfiguration:
    """
    Import a configuration from a JSON string.

    Returns an ExportedConfiguration instance.
    Raises ValueError if the JSON is invalid or the version is unsupported.
    """
    data = json.loads(json_data)
    if not isinstance(data, dict):
        msg = "Invalid configuration: expected a JSON object."
        raise TypeError(msg)

    if (version := data.get("version", "")) != _EXPORT_VERSION:
        msg = f"Unsupported configuration version: {version!r} (expected {_EXPORT_VERSION!r})."
        raise ValueError(msg)

    return ExportedConfiguration.model_validate(data)


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
