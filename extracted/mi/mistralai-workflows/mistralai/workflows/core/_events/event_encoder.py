"""Event payload encoder for encrypting sensitive data in workflow events."""

from __future__ import annotations

import base64
import json
from typing import TYPE_CHECKING, Any

import structlog
from mistralai.extra.workflows.encoding.config import PayloadEncryptionMode
from mistralai.extra.workflows.encoding.models import EncodedPayloadOptions
from pydantic import TypeAdapter, ValidationError

from mistralai.workflows.protocol.v1.events import (
    JSON_PATCH_PAYLOAD_TYPE,
    JSONPatchPayload,
    JSONPayload,
    Payload,
    WorkflowEvent,
)

if TYPE_CHECKING:
    from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

logger = structlog.get_logger(__name__)

# Type discriminator value for EncryptedPatchValue (for SDK-side detection)
ENCRYPTED_PATCH_TYPE = "__encrypted__"

_payload_adapter: TypeAdapter[Payload] = TypeAdapter(Payload)


def _is_payload_type(value: Any) -> bool:
    """Check if a value is a JSONPayload or JSONPatchPayload."""
    try:
        _payload_adapter.validate_python(value)
        return True
    except ValidationError:
        return False


class EventPayloadEncoder:
    """Encoder for encrypting payload fields in workflow events.

    This class handles encryption of JSONPayload and JSONPatchPayload fields
    in workflow event attributes, using the same PayloadEncoder as Temporal payloads.

    Fields are identified by their type structure, not by field name—any field
    with {"type": "json" | "json_patch", "value": ...} is encrypted.

    When encrypted, the payload's value field contains base64-encoded encrypted data
    and the encoding_options field indicates the type of encryption applied.
    """

    def __init__(self, payload_encoder: PayloadEncoder | None) -> None:
        self._payload_encoder = payload_encoder
        logger.info(
            "EventPayloadEncoder initialized",
            has_payload_encoder=payload_encoder is not None,
            has_encryption_config=payload_encoder.encryption_config is not None if payload_encoder else False,
        )

    @property
    def is_partial_encryption_mode(self) -> bool:
        assert self._payload_encoder is not None and self._payload_encoder.encryption_config is not None
        return self._payload_encoder.encryption_config.mode == PayloadEncryptionMode.PARTIAL

    async def encode_event(self, event: WorkflowEvent) -> WorkflowEvent:
        """Encrypt payload fields in an event's attributes.

        Only JSONPayload and JSONPatchPayload fields are encrypted.
        The value field is replaced with base64-encoded encrypted data,
        and encoding_options is set to indicate the encryption type.
        """
        assert self._payload_encoder is not None

        attributes = event.attributes
        if attributes is None:
            logger.debug("Event has no attributes, returning unchanged")
            return event

        attributes_dict = {}
        modified = False

        # Iterate over all fields and encrypt any JSONPayload or JSONPatchPayload
        for field_name in type(attributes).model_fields:
            original_payload = getattr(attributes, field_name, None)

            # Check if this is a payload type we should encrypt
            if not isinstance(original_payload, (JSONPayload, JSONPatchPayload)):
                continue

            # Skip if already encrypted
            existing_encoding = original_payload.encoding_options or []
            if (
                EncodedPayloadOptions.ENCRYPTED in existing_encoding
                or EncodedPayloadOptions.PARTIALLY_ENCRYPTED in existing_encoding
            ):
                logger.debug("Skipping field - already encrypted", field=field_name)
                continue

            # Encrypt the payload
            payload_type = original_payload.type
            logger.debug("Encrypting payload field", field=field_name, payload_type=payload_type)
            encrypted_payload = await self._encrypt_payload(original_payload)
            attributes_dict[field_name] = encrypted_payload
            modified = True

        if not modified:
            return event

        # Create a new event with the encrypted attributes
        event_dict = event.model_dump(mode="json")
        event_dict["attributes"].update(attributes_dict)
        return type(event).model_validate(event_dict)

    async def _encrypt_payload(self, payload: JSONPayload | JSONPatchPayload) -> dict[str, Any]:
        """Encrypt a payload's value and add encoding_options.

        For JSONPatchPayload in partial encryption mode, selectively encrypts only
        patches marked with should_encrypt=True.
        """
        assert self._payload_encoder is not None

        # Handle JSONPatchPayload with selective encryption in partial mode
        if isinstance(payload, JSONPatchPayload) and self.is_partial_encryption_mode:
            patches = payload.value
            encrypted_paths = payload._encrypted_paths
            if isinstance(patches, list) and encrypted_paths:
                encrypted_patches = await self._encrypt_json_patch_selective(patches, encrypted_paths)
                return {
                    "type": JSON_PATCH_PAYLOAD_TYPE,
                    "value": encrypted_patches,
                    "encoding_options": [EncodedPayloadOptions.PARTIALLY_ENCRYPTED.value],
                }
            # No encrypted paths - return unchanged
            if isinstance(patches, list):
                return payload.model_dump(mode="json")

        # Standard encryption for JSONPayload or json_patch in full mode
        payload_dict = payload.model_dump(mode="json")
        value_bytes = json.dumps(payload_dict["value"]).encode("utf-8")

        encrypted_bytes, encoding_options = await self._payload_encoder.encode_event_payload_content(value_bytes)

        # If no encryption was applied (e.g., PARTIAL mode with no EncryptedStrField), return unchanged
        if not encoding_options:
            return payload_dict

        encrypted_value = base64.b64encode(encrypted_bytes).decode("utf-8")

        return {
            "type": payload.type,
            "value": encrypted_value,
            "encoding_options": [opt.value for opt in encoding_options],
        }

    async def _encrypt_json_patch_selective(
        self, patches: list[Any], encrypted_paths: set[str]
    ) -> list[dict[str, Any]]:
        """Encrypt patches whose path is in encrypted_paths.

        Uses EncryptedPatchValue wrapper for type-safe encrypted values.
        """
        assert self._payload_encoder is not None

        result = []
        for patch in patches:
            patch_dict = patch.model_dump(mode="json")
            patch_path = patch_dict.get("path", "")

            if patch_path in encrypted_paths and "value" in patch_dict:
                value_bytes = json.dumps(patch_dict["value"]).encode("utf-8")
                encrypted = self._payload_encoder._encrypt(value_bytes)
                encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")
                patch_dict["value"] = {"type": ENCRYPTED_PATCH_TYPE, "value": encrypted_b64}

            result.append(patch_dict)

        return result

    async def decode_event(self, event: WorkflowEvent) -> WorkflowEvent:
        """Decrypt payload fields in an event's attributes.

        If the payload is not encrypted, returns the event unchanged.
        """
        assert self._payload_encoder is not None

        attributes = event.attributes
        if attributes is None:
            return event

        attributes_dict = attributes.model_dump(mode="json")
        modified = False

        # Iterate over all fields and decrypt any encrypted JSONPayload or JSONPatchPayload
        for field_name, field_value in attributes_dict.items():
            if not _is_payload_type(field_value):
                continue

            # Check if it has encoding_options (meaning it's encrypted)
            encoding_options = field_value.get("encoding_options", [])
            if not encoding_options:
                continue

            # Decrypt the payload
            decrypted_payload = await self._decrypt_payload(field_value)
            attributes_dict[field_name] = decrypted_payload
            modified = True

        if not modified:
            return event

        # Create a new event with the decrypted attributes
        event_dict = event.model_dump(mode="json")
        event_dict["attributes"] = attributes_dict
        return type(event).model_validate(event_dict)

    async def _decrypt_payload(self, payload_data: dict[str, Any]) -> dict[str, Any]:
        """Decrypt a payload's value and return with cleared encoding_options."""
        assert self._payload_encoder is not None

        payload_type = payload_data.get("type")
        value = payload_data.get("value")

        # Handle json_patch with selective encryption (value is list, not base64 string)
        if payload_type == JSON_PATCH_PAYLOAD_TYPE and isinstance(value, list):
            decrypted_patches = self._decrypt_json_patch_selective(value)
            return {
                "type": payload_type,
                "value": decrypted_patches,
                "encoding_options": [],
            }

        # Standard full encryption (base64 string value)
        if not isinstance(value, str):
            raise ValueError("Expected base64 string value for encrypted payload")
        encrypted_bytes = base64.b64decode(value)
        encoding_options = [EncodedPayloadOptions(opt) for opt in payload_data.get("encoding_options", [])]
        decrypted_bytes = await self._payload_encoder.decode_payload_content(encrypted_bytes, encoding_options)
        decrypted_value = json.loads(decrypted_bytes)

        return {
            "type": payload_type,
            "value": decrypted_value,
            "encoding_options": [],
        }

    def _decrypt_json_patch_selective(self, patches: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Decrypt patches with EncryptedPatchValue wrapper."""
        assert self._payload_encoder is not None

        decrypted = []
        for patch in patches:
            patch_value = patch.get("value")

            if (
                isinstance(patch_value, dict)
                and patch_value.get("type") == ENCRYPTED_PATCH_TYPE
                and "value" in patch_value
            ):
                encrypted_b64 = patch_value["value"]
                encrypted_data = base64.b64decode(encrypted_b64)
                decrypted_bytes = self._payload_encoder._decrypt(encrypted_data)
                decrypted.append(
                    {
                        **patch,
                        "value": json.loads(decrypted_bytes),
                    }
                )
            else:
                decrypted.append(patch)

        return decrypted


async def maybe_encode_event(
    event: WorkflowEvent,
    encoder: EventPayloadEncoder | None,
) -> WorkflowEvent:
    """Encrypt event if an encoder is provided.

    Returns the event unchanged if no encoder is configured.

    Use this before batching to ensure size calculations account for
    the base64 overhead of encrypted payloads.
    """
    if encoder is None:
        return event
    return await encoder.encode_event(event)
