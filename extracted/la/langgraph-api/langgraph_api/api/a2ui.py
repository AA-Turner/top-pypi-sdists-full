"""A2UI v0.9 extension negotiation and schema validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import jsonschema_rs
import orjson

A2UI_EXTENSION_URI = "https://a2ui.org/a2a-extension/a2ui/v0.9"
A2UI_MIME_TYPE = "application/json+a2ui"
_COMPAT_A2UI_MIME_TYPE = "application/a2ui+json"
_SCHEMA_DIR = Path(__file__).with_name("a2ui_schemas")


class A2UIValidationError(ValueError):
    """Raised when A2UI metadata or a payload does not match v0.9."""


def _load_schema(name: str) -> dict[str, Any]:
    return orjson.loads((_SCHEMA_DIR / name).read_bytes())


def _relax_catalog_refs(value: Any) -> Any:
    """Keep v0.9 message envelopes strict while accepting custom catalogs."""
    if isinstance(value, dict):
        ref = value.get("$ref")
        if isinstance(ref, str) and ref.startswith("catalog.json#"):
            return {"type": "object"}
        return {key: _relax_catalog_refs(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_relax_catalog_refs(item) for item in value]
    return value


_CLIENT_MESSAGE_VALIDATOR = jsonschema_rs.validator_for(
    _load_schema("client_to_server.json"), validate_formats=True
)
_SERVER_MESSAGE_VALIDATOR = jsonschema_rs.validator_for(
    _relax_catalog_refs(_load_schema("server_to_client.json")), validate_formats=True
)
_CLIENT_CAPABILITIES_VALIDATOR = jsonschema_rs.validator_for(
    _load_schema("client_capabilities.json"), validate_formats=True
)
_CLIENT_DATA_MODEL_VALIDATOR = jsonschema_rs.validator_for(
    _load_schema("client_data_model.json"), validate_formats=True
)


def is_a2ui_mime_type(value: Any) -> bool:
    return value in {A2UI_MIME_TYPE, _COMPAT_A2UI_MIME_TYPE}


def normalize_metadata(
    metadata: dict[str, Any], *, mime_type: str = A2UI_MIME_TYPE
) -> dict[str, Any]:
    if is_a2ui_mime_type(metadata.get("mimeType")):
        return {**metadata, "mimeType": mime_type}
    return metadata


def validate_client_metadata(metadata: dict[str, Any]) -> None:
    try:
        capabilities = metadata.get("a2uiClientCapabilities")
        if capabilities is not None:
            _CLIENT_CAPABILITIES_VALIDATOR.validate(capabilities)
        data_model = metadata.get("a2uiClientDataModel")
        if data_model is not None:
            _CLIENT_DATA_MODEL_VALIDATOR.validate(data_model)
    except ValueError as exc:
        raise A2UIValidationError("Invalid A2UI message metadata") from exc


def validate_payload(
    data: Any,
    *,
    direction: Literal["client", "server"],
) -> None:
    if isinstance(data, list):
        messages = data
    elif isinstance(data, dict):
        messages = (data,)
    else:
        raise A2UIValidationError("A2UI DataPart data must be an array or object")

    validator = (
        _CLIENT_MESSAGE_VALIDATOR
        if direction == "client"
        else _SERVER_MESSAGE_VALIDATOR
    )
    try:
        for message in messages:
            validator.validate(message)
    except ValueError as exc:
        raise A2UIValidationError(f"Invalid A2UI {direction} message") from exc
