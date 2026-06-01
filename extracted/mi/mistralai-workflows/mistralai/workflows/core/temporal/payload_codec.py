import asyncio
from typing import Iterable

import structlog
from mistralai.extra.workflows import WorkflowEncodingConfig
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder
from temporalio.api.common.v1 import Payload
from temporalio.converter import PayloadCodec

from mistralai.workflows.core.config.config import PayloadEncryptionConfig, PayloadOffloadingConfig
from mistralai.workflows.core.encoding import (
    CUSTOM_ENCODING_FORMAT,
    build_info_from_payload_metadata,
    build_temporal_payload_metadata,
    is_custom_encoding_format,
)
from mistralai.workflows.models import (
    EncodedPayloadOptions,
    PayloadMetadataKeys,
    PayloadWithContext,
    WorkflowContext,
)

logger = structlog.get_logger(__name__)


class MistralWorkflowsPayloadCodec(PayloadCodec):
    """Temporal codec for workers.
    It will encode/decode every payload sent and received to the temporal server.
    (workers [MistralWorkflowsPayloadCodec] <-> temporal server)
    """

    BINARY_ENCRYPTED_ENCODING = b"binary/encrypted"

    def __init__(
        self,
        payload_offloading_config: PayloadOffloadingConfig | None,
        payload_encryption_config: PayloadEncryptionConfig | None,
    ) -> None:
        self.payload_encoder = PayloadEncoder(
            encoding_config=WorkflowEncodingConfig(
                payload_offloading=payload_offloading_config,
                payload_encryption=payload_encryption_config,
            ),
        )

    async def _encode(self, payload: Payload) -> Payload:
        encoding_bytes = payload.metadata.get(PayloadMetadataKeys.ENCODING, b"")
        is_custom_encoded = is_custom_encoding_format(encoding_bytes)

        metadata: dict[str, bytes] = payload.metadata  # type: ignore
        data: bytes
        context: WorkflowContext | None = None

        # Everything coming from activities/signals/queries/updates should be encoded with the custom format.
        # We still handle other payload for backward compatibility and to ensure that every data going through the codec
        # will be encrypted properly if needed whatever the format.

        if is_custom_encoded:
            payload_with_context = PayloadWithContext.model_validate_json(payload.data)
            data = payload_with_context.payload
            context = payload_with_context.context
        else:
            data = payload.data

        encoded_data, encoding_options = await self.payload_encoder.encode_payload_content(data, context)
        if is_custom_encoded:
            assert context, "[TemporalCodec] context is required for custom encoding format"  # Just to please mypy
            metadata = build_temporal_payload_metadata(context, encoding_options, payload_with_context.empty)
        elif EncodedPayloadOptions.ENCRYPTED in encoding_options:
            payload.metadata[PayloadMetadataKeys.ENCODING_ORIGINAL] = payload.metadata.get(
                PayloadMetadataKeys.ENCODING, b""
            )
            payload.metadata[PayloadMetadataKeys.ENCODING] = b"binary/encrypted"

        return Payload(
            metadata=metadata,
            data=encoded_data,
        )

    async def encode(self, payloads: Iterable[Payload]) -> list[Payload]:
        new_payloads_coroutines = [asyncio.create_task(self._encode(payload)) for payload in payloads]
        encoded_payloads: list[Payload] = await asyncio.gather(*new_payloads_coroutines)
        return encoded_payloads

    async def _decode(self, payload: Payload) -> Payload:
        encoding_bytes = payload.metadata.get(PayloadMetadataKeys.ENCODING, b"")
        if is_custom_encoding_format(encoding_bytes):
            workflow_context, encoding_options, empty = build_info_from_payload_metadata(payload.metadata)
            if not workflow_context.execution_id:  # or not workflow_context.retention_ttl:
                logger.error("[TemporalCodec] Incomplete context for custom encoded payload", context=workflow_context)
                raise ValueError("Incomplete context for custom encoded payload")

            decoded_data = await self.payload_encoder.decode_payload_content(payload.data, encoding_options)

            payload = Payload(
                metadata={PayloadMetadataKeys.ENCODING: CUSTOM_ENCODING_FORMAT.encode()},
                data=PayloadWithContext(
                    context=workflow_context,
                    payload=decoded_data,
                    empty=empty,
                )
                .model_dump_json()
                .encode(),
            )
        elif payload.metadata.get(PayloadMetadataKeys.ENCODING) == self.BINARY_ENCRYPTED_ENCODING:
            payload.data = await self.payload_encoder.decode_payload_content(
                payload.data, [EncodedPayloadOptions.ENCRYPTED]
            )
            payload.metadata[PayloadMetadataKeys.ENCODING] = payload.metadata.get(
                PayloadMetadataKeys.ENCODING_ORIGINAL, b""
            )
            del payload.metadata[PayloadMetadataKeys.ENCODING_ORIGINAL]
        elif bool(payload.metadata.get(PayloadMetadataKeys.IS_UNENCODED_MEMO, False)):
            # Allow non-encoded-memos
            pass

        return payload

    async def decode(self, payloads: Iterable[Payload]) -> list[Payload]:
        new_payloads_coroutines = [asyncio.create_task(self._decode(payload)) for payload in payloads]
        decoded_payloads = await asyncio.gather(*new_payloads_coroutines)
        return decoded_payloads
