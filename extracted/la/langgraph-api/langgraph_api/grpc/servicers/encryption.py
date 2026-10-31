"""Encryption gRPC servicer implementation.

This permanent bridge exposes Python custom handlers to the Go server. JSON
reads also support legacy AES ciphertext for AES-to-custom migration; writes
and blob operations use custom handlers only.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import grpc
import orjson
import structlog
from langgraph_grpc_common.proto.encryption_pb2 import (
    DecryptResponse,
    EncryptResponse,
)
from langgraph_grpc_common.proto.encryption_pb2_grpc import EncryptionServicer
from langgraph_sdk import EncryptionContext

from langgraph_api.encryption.custom import (
    JsonEncryptionWrapper,
    get_custom_encryption_instance,
    normalize_decrypt_result,
)
from langgraph_api.encryption.shared import (
    BLOB_ENCRYPTION_CONTEXT_KEY,
    ENCRYPTION_CONTEXT_KEY,
    get_encryption,
)

if TYPE_CHECKING:
    from grpc import aio as grpc_aio

logger = structlog.stdlib.get_logger(__name__)


def _parse_metadata(metadata: dict[str, bytes]) -> dict[str, Any]:
    """Parse metadata from proto map<string, bytes> to dict.

    Args:
        metadata: Map of string keys to JSON-encoded bytes values

    Returns:
        Dict with parsed JSON values

    Raises:
        ValueError: If any value is not valid JSON
    """
    result = {}
    for k, v in metadata.items():
        if v:
            try:
                result[k] = orjson.loads(v)
            except Exception as e:
                raise ValueError(
                    f"Failed to parse metadata value for key '{k}' as JSON: {e}"
                ) from e
        else:
            result[k] = None
    return result


def _build_encryption_context(
    model: str | None,
    field: str | None,
    metadata: dict[str, bytes],
) -> EncryptionContext:
    """Build an EncryptionContext from proto fields.

    Args:
        model: Model type (e.g., "thread", "run")
        field: Field name (e.g., "metadata", "kwargs")
        metadata: Proto metadata map

    Returns:
        EncryptionContext for SDK encryption handlers
    """
    return EncryptionContext(
        model=model or None,
        field=field or None,
        metadata=_parse_metadata(metadata),
    )


class EncryptionServicerImpl(EncryptionServicer):
    """Implementation of the Encryption gRPC service.

    This servicer delegates to the Python custom encryption implementation,
    allowing the Go server to use Python-based encryption when custom
    encryption is configured.

    For JSON operations, uses the JsonEncryptionWrapper which handles:
    - Key preservation validation
    - Encryption context marker storage
    - Migration routing between AES and custom encryption
    """

    async def EncryptJSON(
        self,
        request,
        context: grpc_aio.ServicerContext,
    ) -> EncryptResponse:
        """Encrypt JSON data using the configured encryption.

        Go owns field structure; this method executes one customer-handler call.
        """
        try:
            encryption_instance = get_encryption()
            if encryption_instance is None:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("No encryption configured")
                raise RuntimeError("No encryption configured")

            data: dict[str, Any] = orjson.loads(request.data)

            model_type = request.context.model or None
            field = request.context.field or None

            encryptor = encryption_instance.get_json_encryptor(model_type)
            if encryptor is None:
                metadata = _parse_metadata(dict(request.context.metadata))
                if metadata:
                    data[BLOB_ENCRYPTION_CONTEXT_KEY] = metadata
                    return EncryptResponse(data=orjson.dumps(data))
                return EncryptResponse(data=request.data)

            encrypted = await encryptor(
                _build_encryption_context(
                    model_type, field, dict(request.context.metadata)
                ),
                data,
            )
            encrypted_bytes = orjson.dumps(encrypted)

            return EncryptResponse(data=encrypted_bytes)

        except Exception as e:
            await logger.aerror("EncryptJSON failed", error=str(e), exc_info=True)
            if context.code() is None:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Encryption failed: {e}")
            raise

    async def DecryptJSON(
        self,
        request,
        context: grpc_aio.ServicerContext,
    ) -> DecryptResponse:
        """Decrypt JSON data using the configured encryption."""
        try:
            encryption_instance = get_encryption()
            if encryption_instance is None:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("No encryption configured")
                raise RuntimeError("No encryption configured")

            data: dict[str, Any] = orjson.loads(request.data)

            # Preserve __blob_encryption_context__ — this is user-facing
            # metadata (e.g., tenant/key info for cron execution) that must
            # survive decryption.  The decryptor's strip_encryption_metadata
            # removes it, so we save and restore it after decryption.
            blob_enc_ctx = data.get(BLOB_ENCRYPTION_CONTEXT_KEY)

            model_type = request.model or None
            field = request.field or None

            decryptor = (
                encryption_instance.get_json_decryptor(
                    model_type, with_replacement=True
                )
                if isinstance(encryption_instance, JsonEncryptionWrapper)
                else encryption_instance.get_json_decryptor(model_type)
            )
            if decryptor is None:
                model_err = f"No decryptor configured for model type: {model_type}"
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(model_err)
                raise RuntimeError(model_err)

            stored_ctx = data.get(ENCRYPTION_CONTEXT_KEY)
            metadata = stored_ctx if isinstance(stored_ctx, dict) else {}
            result = normalize_decrypt_result(
                await decryptor(
                    EncryptionContext(model=model_type, field=field, metadata=metadata),
                    data,
                )
            )
            decrypted = result.plaintext
            replacement = result.replacement

            # Restore __blob_encryption_context__ so that internal consumers
            # (e.g., the cron scheduler) can recover the original encryption
            # context when creating downstream runs.
            if blob_enc_ctx is not None and isinstance(decrypted, dict):
                decrypted[BLOB_ENCRYPTION_CONTEXT_KEY] = blob_enc_ctx
            if blob_enc_ctx is not None and isinstance(replacement, dict):
                replacement[BLOB_ENCRYPTION_CONTEXT_KEY] = blob_enc_ctx

            decrypted_bytes = orjson.dumps(decrypted)
            replacement_bytes = None
            if replacement is not None:
                try:
                    replacement_bytes = orjson.dumps(replacement)
                except (TypeError, ValueError):
                    await logger.aerror(
                        "Ignoring unserializable re-encryption replacement",
                        model=model_type,
                        field=field,
                    )

            return DecryptResponse(data=decrypted_bytes, replacement=replacement_bytes)

        except Exception as e:
            await logger.aerror("DecryptJSON failed", error=str(e), exc_info=True)
            if context.code() is None:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Decryption failed: {e}")
            raise

    async def EncryptBlob(
        self,
        request,
        context: grpc_aio.ServicerContext,
    ) -> EncryptResponse:
        """Encrypt opaque bytes with the configured blob handler."""
        try:
            encryption_instance = get_custom_encryption_instance()
            if (
                encryption_instance is None
                or encryption_instance._blob_encryptor is None
            ):
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("No blob encryption configured")
                raise RuntimeError("No blob encryption configured")

            enc_ctx = _build_encryption_context(
                request.context.model or None,
                request.context.field or None,
                dict(request.context.metadata),
            )
            encrypted = await encryption_instance._blob_encryptor(enc_ctx, request.data)
            return EncryptResponse(data=encrypted)
        except Exception as e:
            await logger.aerror("EncryptBlob failed", error=str(e), exc_info=True)
            if context.code() is None:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Blob encryption failed: {e}")
            raise

    async def DecryptBlob(
        self,
        request,
        context: grpc_aio.ServicerContext,
    ) -> DecryptResponse:
        """Decrypt opaque bytes with the configured blob handler."""
        try:
            encryption_instance = get_custom_encryption_instance()
            if (
                encryption_instance is None
                or encryption_instance._blob_decryptor is None
            ):
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("No blob decryption configured")
                raise RuntimeError("No blob decryption configured")

            enc_ctx = _build_encryption_context(
                request.context.model or None,
                request.context.field or None,
                dict(request.context.metadata),
            )
            result = normalize_decrypt_result(
                await encryption_instance._blob_decryptor(enc_ctx, request.data)
            )
            return DecryptResponse(
                data=result.plaintext, replacement=result.replacement
            )
        except Exception as e:
            await logger.aerror("DecryptBlob failed", error=str(e), exc_info=True)
            if context.code() is None:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Blob decryption failed: {e}")
            raise
