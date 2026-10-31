"""Encryption/decryption middleware for API layer.

This module provides helpers to encrypt data before storing and decrypt
after retrieving, keeping encryption logic at the API layer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import structlog
from starlette.authentication import BaseUser

from langgraph_api.auth.noop import UnauthenticatedUser
from langgraph_api.auth.studio_user import StudioUser
from langgraph_api.config import LANGGRAPH_ENCRYPTION
from langgraph_api.encryption.aes_json import (
    AesEncryptionInstance,
    DecryptorMissingError,
    is_aes_encryption_context,
)
from langgraph_api.encryption.context import (
    get_encryption_context,
)
from langgraph_api.encryption.custom import (
    JsonEncryptionWrapper,
    ModelType,
)
from langgraph_api.encryption.shared import (
    BLOB_ENCRYPTION_CONTEXT_KEY,
    ENCRYPTION_CONTEXT_KEY,
    get_encryption,
    strip_encryption_metadata,
)
from langgraph_api.serde import Fragment, json_loads

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

# Only import EncryptionContext at module load if encryption is configured
# This avoids requiring langgraph-sdk>=0.2.14 for users who don't use encryption
if LANGGRAPH_ENCRYPTION:
    from langgraph_sdk import EncryptionContext

logger = structlog.stdlib.get_logger(__name__)


def _serialize_user_for_encryption(user: BaseUser) -> dict[str, Any]:
    """Serialize a BaseUser to a JSON-serializable dict for encryption.

    Called by _prepare_data_for_encryption when langgraph_auth_user contains a
    BaseUser that needs to be serialized before JSON encryption.

    Args:
        user: The BaseUser to serialize (ProxyUser, SimpleUser, or custom subclass)

    Returns:
        A JSON-serializable dict with user data
    """
    # If the auth function returns a pydantic object as the User object, we
    # want to preserve the additional fields
    if hasattr(user, "model_dump") and callable(user.model_dump):
        return cast("dict[str, Any]", user.model_dump())

    if isinstance(user, StudioUser):
        return user.dict()

    # Plain BaseUser subclasses - extract the required properties
    return {
        "identity": user.identity,
        "is_authenticated": user.is_authenticated,
        "display_name": user.display_name,
    }


def _prepare_data_for_encryption(data: dict[str, Any]) -> dict[str, Any]:
    """Prepare data dict for encryption by serializing non-JSON-serializable objects.

    Specifically handles langgraph_auth_user which may contain BaseUser objects
    that can't be JSON-serialized. Dicts pass through unchanged (already serializable).

    Args:
        data: The data dict to prepare

    Returns:
        A new dict with serialized values where needed
    """
    if "langgraph_auth_user" not in data:
        return data

    user = data["langgraph_auth_user"]
    if isinstance(user, BaseUser):
        data = dict(data)  # shallow copy
        if isinstance(user, UnauthenticatedUser):
            data["langgraph_auth_user"] = None
        else:
            data["langgraph_auth_user"] = _serialize_user_for_encryption(user)

    return data


class DoubleEncryptionError(Exception):
    """Raised when attempting to encrypt data that is already encrypted.

    This typically indicates a bug where encrypted data is being passed through
    the encryption pipeline again, which would corrupt the data.
    """


async def encrypt_json_if_needed(
    data: dict[str, Any] | None,
    encryption_instance: JsonEncryptionWrapper | AesEncryptionInstance | None,
    model_type: ModelType,
    field: str | None = None,
    path: str | None = None,
    should_skip: Callable[[str, str], bool] | None = None,
) -> dict[str, Any] | None:
    """Encrypt JSON data dict if encryption is configured.

    Uses a unified interface where both custom (via wrapper) and AES encryption
    implement the same encryptor interface (get_json_encryptor). The wrapper
    handles key validation and context storage internally.

    Runtime-owned system fields may be excluded from custom encryption through
    ``should_skip``. AES uses an explicit allowlist and ignores this callback.

    Args:
        data: The plaintext data dict
        encryption_instance: The encryption instance (wrapped custom, AES, or None)
        model_type: The type of model (e.g., "thread", "assistant", "run")
        field: The specific field being encrypted (e.g., "metadata", "context")
        path: The full dot-separated path for path-based skip rules
              (e.g., "run.kwargs.config.configurable")

    Returns:
        Encrypted data dict with stored context, or original if no encryption configured

    Raises:
        EncryptionKeyError: If the encryptor adds or removes keys (violates key preservation)
        DoubleEncryptionError: If data already has encryption context marker (already encrypted)
    """
    if data is None:
        return data

    # Early return if no encryption configured (avoid unnecessary context lookups)
    if encryption_instance is None:
        return data

    # Safety check: detect if data is already encrypted to prevent double encryption.
    # Both AES and custom encryption use __encryption_context__ marker.
    if ENCRYPTION_CONTEXT_KEY in data:
        raise DoubleEncryptionError(
            f"Attempted to encrypt data that is already encrypted (has {ENCRYPTION_CONTEXT_KEY}). "
            f"model_type={model_type}, field={field}. "
            f"This indicates a bug where encrypted data is being re-encrypted. "
            f"Ensure data is decrypted before re-encrypting."
        )

    # Get encryptor from the instance (works for both custom wrapper and AES)
    encryptor = encryption_instance.get_json_encryptor(model_type)
    if encryptor is not None:
        # Prepare data for encryption by serializing non-JSON-serializable objects
        # (e.g., BaseUser in langgraph_auth_user)
        data = _prepare_data_for_encryption(data)

        # For custom encryption, extract fields that should never be encrypted.
        # AES uses an allowlist so it doesn't need this exclusion logic.
        skipped_fields: dict[str, Any] = {}
        is_custom_encryption = isinstance(encryption_instance, JsonEncryptionWrapper)
        if is_custom_encryption and should_skip is not None:
            # Build path for skip field evaluation
            effective_path = path if path else model_type
            skipped_fields = {
                key: value
                for key, value in data.items()
                if should_skip(key, effective_path)
            }
            data = {
                key: value for key, value in data.items() if key not in skipped_fields
            }

        # Build context for SDK interface (AES ignores this, custom uses it)
        context_dict = get_encryption_context()
        if LANGGRAPH_ENCRYPTION:
            ctx = EncryptionContext(
                model=model_type, field=field, metadata=context_dict
            )
        else:
            ctx = None  # AES doesn't need the EncryptionContext

        # The encryptor handles key validation and context storage internally
        encrypted = await encryptor(ctx, data)

        # Merge back skipped fields (for custom encryption)
        if skipped_fields and isinstance(encrypted, dict):
            encrypted = {**encrypted, **skipped_fields}

        await logger.adebug(
            "Encrypted JSON data",
            model_type=model_type,
            field=field,
            encryption_type="aes_only"
            if isinstance(encryption_instance, AesEncryptionInstance)
            else "custom_with_aes_migration",
            skipped_fields=list(skipped_fields.keys()) if skipped_fields else None,
        )
        return encrypted

    # No JSON encryption configured, but store context for blob encryption
    # This allows the worker to extract context even when JSON encryption is disabled
    context_dict = get_encryption_context()
    if context_dict and isinstance(data, dict):
        data = dict(data)  # shallow copy to avoid mutating input
        data[BLOB_ENCRYPTION_CONTEXT_KEY] = context_dict
    return data


async def decrypt_json_if_needed(
    data: dict[str, Any] | None,
    encryption_instance: JsonEncryptionWrapper | AesEncryptionInstance | None,
    model_type: ModelType,
    field: str | None = None,
) -> dict[str, Any] | None:
    """Decrypt JSON data dict based on encryption markers.

    Routes to the appropriate decryptor based on the type in __encryption_context__:
    1. If marker present with AES type → use AES decryptor
    2. If marker present without AES type → use custom decryptor
    3. No marker → plaintext (return unchanged)

    The routing logic is handled internally by the wrapper/instance:
    - JsonEncryptionWrapper handles routing for custom + AES migration
    - AesEncryptionInstance handles AES-only decryption

    Args:
        data: The data dict (encrypted or plaintext)
        encryption_instance: The effective encryption instance (wrapper or AES-only)
        model_type: The type of model (e.g., "thread", "assistant", "run")
        field: The specific field being decrypted (e.g., "metadata", "context")

    Returns:
        Decrypted data dict (without reserved keys), or original if not encrypted

    Raises:
        DecryptorMissingError: If data is encrypted but required decryptor is not configured
        EncryptionRoutingError: If markers are inconsistent (e.g., AES values with custom marker)
    """
    if data is None:
        return data

    # No encryption configured
    if encryption_instance is None:
        # If data has encryption marker but no decryptor, raise error
        if ENCRYPTION_CONTEXT_KEY in data:
            context_dict = data[ENCRYPTION_CONTEXT_KEY]
            if is_aes_encryption_context(context_dict):
                raise DecryptorMissingError(
                    f"Data has AES encryption marker but LANGGRAPH_AES_KEY is not configured "
                    f"for {model_type}.{field}"
                )
            raise DecryptorMissingError(
                f"Data contains custom encryption marker but no encryption instance is configured "
                f"for {model_type}.{field}"
            )
        return strip_encryption_metadata(data)

    # Get decryptor - the wrapper/instance handles routing (AES/custom/plaintext) internally
    decryptor = encryption_instance.get_json_decryptor(model_type)

    # Build context for SDK interface (AES ignores this, custom uses it)
    context_dict = data.get(ENCRYPTION_CONTEXT_KEY, {})
    if LANGGRAPH_ENCRYPTION:
        ctx = EncryptionContext(model=model_type, field=field, metadata=context_dict)
    else:
        ctx = None

    decrypted = await decryptor(ctx, data)

    await logger.adebug(
        "Decrypted JSON data",
        model_type=model_type,
        field=field,
        encryption_type="aes_only"
        if isinstance(encryption_instance, AesEncryptionInstance)
        else "custom_with_aes_migration",
    )
    return decrypted


async def decrypt_response(
    obj: Mapping[str, Any],
    model_type: ModelType,
    *,
    plaintext_from_core: bool,
) -> dict[str, Any]:
    """Decrypt runtime-owned fields, or return Go-decrypted data unchanged."""
    if plaintext_from_core:
        return obj

    encryption_instance = get_encryption()
    if encryption_instance is None:
        # Even without encryption, the error field is stored as bytes (bytea column)
        # and must be parsed to return as a dict in the API response.
        error = obj.get("error")
        if isinstance(error, bytes | memoryview | Fragment):
            result = dict(obj)
            error_bytes = cast(
                "bytes | Fragment",
                bytes(error) if isinstance(error, memoryview) else error,
            )
            result["error"] = json_loads(error_bytes)
            return result
        return obj

    from langgraph_runtime.encryption import (  # noqa: PLC0415
        decrypt_fields,
        encryption_fields,
    )

    field_names = encryption_fields(model_type)
    result = dict(obj)
    for field_name in field_names:
        value = result.get(field_name)
        if isinstance(value, (bytes, bytearray, memoryview, str, Fragment)):
            result[field_name] = json_loads(value)
    await decrypt_fields(result, model_type, field_names, encryption_instance)
    return result


async def encrypt_request(
    data: Mapping[str, Any],
    model_type: ModelType,
    *,
    plaintext_for_core: bool,
) -> dict[str, Any]:
    """Encrypt runtime-owned fields, or leave data plaintext for Go."""
    if plaintext_for_core:
        return data

    encryption_instance = get_encryption()
    if encryption_instance is None:
        return data

    from langgraph_runtime.encryption import (  # noqa: PLC0415
        encrypt_fields,
        encryption_fields,
    )

    field_names = encryption_fields(model_type)
    return await encrypt_fields(data, model_type, field_names, encryption_instance)
