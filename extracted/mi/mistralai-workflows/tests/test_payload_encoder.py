import json
import re
from unittest.mock import AsyncMock, Mock, patch

import pytest
import structlog
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from mistralai.extra.exceptions import WorkflowPayloadEncryptionException
from mistralai.extra.workflows import WorkflowEncodingConfig
from mistralai.extra.workflows.encoding.config import (
    PayloadCompressionConfig,
    PayloadEncryptionConfig,
    PayloadEncryptionMode,
    PayloadOffloadingConfig,
)
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder
from pydantic import BaseModel
from pydantic_core import to_json
from temporalio.api.common.v1 import Payload

from mistralai.workflows.core.encoding import CUSTOM_ENCODING_FORMAT
from mistralai.workflows.core.temporal.payload_codec import MistralWorkflowsPayloadCodec
from mistralai.workflows.models import (
    EncodedPayloadOptions,
    EncryptedStrField,
    NetworkEncodedResult,
    PayloadMetadataKeys,
    PayloadWithContext,
    WorkflowContext,
)
from tests.test_helpers import InMemoryBlobStorage

logger = structlog.get_logger(__name__)

LARGE_PAYLOAD_SIZE = 1024 * 1024 + 1  # 1MB + 1B
TEST_MAIN_KEY = AESGCM.generate_key(bit_length=128).hex()
TEST_SECONDARY_KEY = AESGCM.generate_key(bit_length=128).hex()
TEST_NAMESPACE = "test-namespace"
TEST_EXECUTION_ID = "test-execution-id"


class PayloadWithPartialEncryption(BaseModel):
    secret: EncryptedStrField
    not_secret: str


class TestPayloadEncoder:
    @pytest.fixture
    def mock_blob_storage(self):
        return InMemoryBlobStorage()

    @pytest.fixture
    def context(self):
        return WorkflowContext(namespace=TEST_NAMESPACE, execution_id=TEST_EXECUTION_ID)

    def test_temporal_codec_configures_payload_compression(self):
        codec = MistralWorkflowsPayloadCodec(
            payload_offloading_config=None,
            payload_encryption_config=None,
            payload_compression_config=PayloadCompressionConfig(min_size_bytes=100),
        )

        assert codec.payload_encoder.compression_config == PayloadCompressionConfig(min_size_bytes=100)
        assert codec.payload_encoder.compressor is not None

    @pytest.mark.asyncio
    async def test_encoding_network_payload(self, mock_blob_storage, context):
        # Ensure that network payload encoding/decoding use the main encode/decode methods
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(),
            )

            test_payload = {"hello": "test"}
            with patch.object(PayloadEncoder, "encode_payload_content", new_callable=AsyncMock) as mock_encode:
                mock_encode.return_value = (b"random_data", [])
                encoded = await encoder.encode_network_input(test_payload, context)
                mock_encode.assert_awaited_once_with(to_json(test_payload), context)

            with patch.object(PayloadEncoder, "decode_payload_content", new_callable=AsyncMock) as mock_decode:
                mock_decode.return_value = to_json(test_payload)
                decoded = await encoder.decode_network_result(
                    NetworkEncodedResult.from_encoded_payload(
                        encoded.to_encoded_payload(context.namespace, context.execution_id)
                    )
                )

            assert decoded == test_payload

    @pytest.mark.asyncio
    async def test_encoding_with_offloading(self, mock_blob_storage, context):
        """Test payload offloading."""
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_offloading=PayloadOffloadingConfig(min_size_bytes=100, storage_config={}),
                ),
            )

            large_payload_content = to_json({"data": "x" * LARGE_PAYLOAD_SIZE})
            encoded_data, encoding_options = await encoder.encode_payload_content(large_payload_content, context)
            assert encoding_options == [EncodedPayloadOptions.OFFLOADED]
            assert len(mock_blob_storage.blobs) == 1

            # Verify blob key format
            stored_key = list(mock_blob_storage.blobs.keys())[0]
            assert stored_key.startswith(f"temporal-payload/{TEST_NAMESPACE}/{TEST_EXECUTION_ID}")
            pattern = rb'^\{"key":".*"\}$'
            assert re.match(pattern, encoded_data)

            decoded_content = await encoder.decode_payload_content(encoded_data, encoding_options)
            assert decoded_content == large_payload_content

    @pytest.mark.asyncio
    async def test_encoding_with_compression(self, mock_blob_storage, context):
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_compression=PayloadCompressionConfig(min_size_bytes=100),
                ),
            )

            large_payload_content = to_json({"data": "x" * LARGE_PAYLOAD_SIZE})
            encoded_data, encoding_options = await encoder.encode_payload_content(large_payload_content, context)

            assert encoding_options == [EncodedPayloadOptions.COMPRESSED]
            assert len(encoded_data) < len(large_payload_content)

            decoded_content = await encoder.decode_payload_content(encoded_data, encoding_options)
            assert decoded_content == large_payload_content

    @pytest.mark.asyncio
    async def test_encoding_with_compression_prevents_offloading(self, mock_blob_storage, context):
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_compression=PayloadCompressionConfig(min_size_bytes=100),
                    payload_offloading=PayloadOffloadingConfig(min_size_bytes=1000, storage_config={}),
                ),
            )

            large_payload_content = to_json({"data": "x" * LARGE_PAYLOAD_SIZE})
            encoded_data, encoding_options = await encoder.encode_payload_content(large_payload_content, context)

            assert encoding_options == [EncodedPayloadOptions.COMPRESSED]
            assert len(mock_blob_storage.blobs) == 0

            decoded_content = await encoder.decode_payload_content(encoded_data, encoding_options)
            assert decoded_content == large_payload_content

    @pytest.mark.asyncio
    async def test_encoding_with_encryption(self, mock_blob_storage, context):
        """Test payload encryption."""
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_encryption=PayloadEncryptionConfig(mode=PayloadEncryptionMode.FULL, main_key=TEST_MAIN_KEY),
                ),
            )

            test_payload_content = to_json({"secret": "confidential"})

            encoded_data, encoding_options = await encoder.encode_payload_content(test_payload_content, context)
            assert EncodedPayloadOptions.ENCRYPTED in encoding_options

            # Ensure that the payload include a nonce
            encoded_data_2, _ = await encoder.encode_payload_content(test_payload_content, context)
            assert encoded_data != encoded_data_2

            # Verify payload is encrypted (binary data)
            assert b"confidential" not in encoded_data

            decoded_content = await encoder.decode_payload_content(encoded_data, encoding_options)
            assert decoded_content == test_payload_content

    @pytest.mark.asyncio
    async def test_encode_decode_with_offloading_and_encryption(self, mock_blob_storage, context):
        """Test payload with both offloading and encryption."""
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_offloading=PayloadOffloadingConfig(min_size_bytes=100, storage_config={}),
                    payload_encryption=PayloadEncryptionConfig(mode=PayloadEncryptionMode.FULL, main_key=TEST_MAIN_KEY),
                ),
            )

            large_payload_content = to_json({"data": "x" * LARGE_PAYLOAD_SIZE, "secret": "confidential"})
            encoded_data, encoding_options = await encoder.encode_payload_content(large_payload_content, context)

            assert encoding_options == [EncodedPayloadOptions.OFFLOADED, EncodedPayloadOptions.ENCRYPTED]
            assert len(mock_blob_storage.blobs) == 1

            # Verify payload is uploaded to blob storage
            stored_key = list(mock_blob_storage.blobs.keys())[0]
            stored_data = mock_blob_storage.blobs[stored_key]
            assert stored_data == large_payload_content

            pattern = rb'^\{"key":".*"\}$'
            assert not re.match(pattern, encoded_data)

            decoded_content = await encoder.decode_payload_content(encoded_data, encoding_options)
            assert decoded_content == large_payload_content

    @pytest.mark.asyncio
    async def test_encoding_with_partial_encryption(self, mock_blob_storage, context):
        """Test payload encryption."""
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_encryption=PayloadEncryptionConfig(
                        mode=PayloadEncryptionMode.PARTIAL, main_key=TEST_MAIN_KEY
                    ),
                ),
            )

            partially_encrypted_payload = PayloadWithPartialEncryption(
                secret=EncryptedStrField(data="Shhhh!"),
                not_secret="Hello world",
            )

            encoded_data, encoding_options = await encoder.encode_payload_content(
                partially_encrypted_payload.model_dump_json(), context
            )
            assert EncodedPayloadOptions.PARTIALLY_ENCRYPTED in encoding_options

            # Ensure that the payload include a nonce
            encoded_data_2, _ = await encoder.encode_payload_content(
                partially_encrypted_payload.model_dump_json(), context
            )
            assert encoded_data != encoded_data_2

            # Verify payload is encrypted (binary data)
            partially_encrypted_payload_decoded = PayloadWithPartialEncryption.model_validate_json(encoded_data)
            assert partially_encrypted_payload_decoded.secret.data != partially_encrypted_payload.secret.data
            assert partially_encrypted_payload_decoded.not_secret == partially_encrypted_payload.not_secret

            # Verify that decoding it restore the initial data
            decoded_content = await encoder.decode_payload_content(encoded_data, encoding_options)
            partially_encrypted_payload_decoded = PayloadWithPartialEncryption.model_validate_json(decoded_content)
            assert partially_encrypted_payload_decoded == partially_encrypted_payload

            complex_object = {
                "integrations": [
                    "google",
                    {
                        "name": "github",
                        "token": EncryptedStrField(data="MY_GITHUB_TOKEN").model_dump(),
                    },
                    EncryptedStrField(data="AN_ORPHAN_TOKEN").model_dump(),
                    [
                        EncryptedStrField(data="NESTED_LIST_TOKEN").model_dump(),
                        "Nested list",
                    ],
                ],
                "my_password": EncryptedStrField(data="qwerty1234").model_dump(),
                "username": "myemail",
                "other_infos": {
                    "age": 42,
                    "backup_key_info": {"encrypted_data": EncryptedStrField(data="backup_key").model_dump()},
                },
            }
            encoded_data, encoding_options = await encoder.encode_payload_content(json.dumps(complex_object), context)
            assert EncodedPayloadOptions.PARTIALLY_ENCRYPTED in encoding_options

            encoded_complex_object = json.loads(encoded_data)
            assert encoded_complex_object["integrations"][0] == "google"
            assert encoded_complex_object["integrations"][1]["name"] == "github"
            assert encoded_complex_object["integrations"][1]["token"]["data"] != "MY_GITHUB_TOKEN"
            assert encoded_complex_object["integrations"][2]["data"] != "AN_ORPHAN_TOKEN"
            assert encoded_complex_object["integrations"][3][0]["data"] != "NESTED_LIST_TOKEN"
            assert encoded_complex_object["integrations"][3][1] == "Nested list"
            assert encoded_complex_object["other_infos"]["age"] == 42
            assert encoded_complex_object["other_infos"]["backup_key_info"]["encrypted_data"]["data"] != "backup_key"

            decoded_data = await encoder.decode_payload_content(encoded_data, encoding_options)
            decoded_complex_object = json.loads(decoded_data)
            assert decoded_complex_object["integrations"][0] == "google"
            assert decoded_complex_object["integrations"][1]["name"] == "github"
            assert decoded_complex_object["integrations"][1]["token"]["data"] == "MY_GITHUB_TOKEN"
            assert decoded_complex_object["integrations"][2]["data"] == "AN_ORPHAN_TOKEN"
            assert decoded_complex_object["integrations"][3][0]["data"] == "NESTED_LIST_TOKEN"
            assert decoded_complex_object["integrations"][3][1] == "Nested list"
            assert decoded_complex_object["other_infos"]["age"] == 42
            assert decoded_complex_object["other_infos"]["backup_key_info"]["encrypted_data"]["data"] == "backup_key"

    @pytest.mark.asyncio
    async def test_decode_offloaded_then_partially_encrypted(self, mock_blob_storage, context):
        """Test that decoding handles OFFLOADED and PARTIALLY_ENCRYPTED as independent options.

        Regression test: a bug caused the PARTIALLY_ENCRYPTED branch to match any option
        when PARTIALLY_ENCRYPTED was present in the encoding_options list, making the
        OFFLOADED branch unreachable during decoding.
        """
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_offloading=PayloadOffloadingConfig(min_size_bytes=100, storage_config={}),
                    payload_encryption=PayloadEncryptionConfig(
                        mode=PayloadEncryptionMode.PARTIAL, main_key=TEST_MAIN_KEY
                    ),
                ),
            )

            # Build a payload with an encrypted field that is large enough to be offloaded
            payload = {
                "secret": EncryptedStrField(data="Shhhh!").model_dump(),
                "bulk": "x" * LARGE_PAYLOAD_SIZE,
            }
            payload_bytes = json.dumps(payload).encode()

            encoded_data, encoding_options = await encoder.encode_payload_content(payload_bytes, context)

            assert encoding_options == [EncodedPayloadOptions.PARTIALLY_ENCRYPTED, EncodedPayloadOptions.OFFLOADED]
            decoded = await encoder.decode_payload_content(encoded_data, encoding_options)
            decoded_obj = json.loads(decoded)
            assert decoded_obj["secret"]["data"] == "Shhhh!"
            assert decoded_obj["bulk"] == "x" * LARGE_PAYLOAD_SIZE

            # Also verify a manually offloaded partially encrypted payload decodes in reverse order.
            partially_enc_encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_encryption=PayloadEncryptionConfig(
                        mode=PayloadEncryptionMode.PARTIAL, main_key=TEST_MAIN_KEY
                    ),
                ),
            )
            small_payload = {
                "secret": EncryptedStrField(data="Shhhh!").model_dump(),
                "not_secret": "Hello",
            }
            small_payload_bytes = json.dumps(small_payload).encode()

            enc_data, enc_options = await partially_enc_encoder.encode_payload_content(small_payload_bytes, context)
            assert enc_options == [EncodedPayloadOptions.PARTIALLY_ENCRYPTED]

            # Manually store in blob and build a combined encoding_options list
            blob_key = "temporal-payload/test-namespace/test-execution-id/manual-test"
            mock_blob_storage.blobs[blob_key] = enc_data
            offloaded_ref = json.dumps({"key": blob_key}).encode()

            # Encoding order would be: partially encrypt, then offload.
            # Decoding reverses: de-offload first, then partial decrypt.
            combined_options = [EncodedPayloadOptions.PARTIALLY_ENCRYPTED, EncodedPayloadOptions.OFFLOADED]

            offload_and_partial_encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_offloading=PayloadOffloadingConfig(min_size_bytes=100, storage_config={}),
                    payload_encryption=PayloadEncryptionConfig(
                        mode=PayloadEncryptionMode.PARTIAL, main_key=TEST_MAIN_KEY
                    ),
                ),
            )
            decoded = await offload_and_partial_encoder.decode_payload_content(offloaded_ref, combined_options)
            decoded_obj = json.loads(decoded)
            assert decoded_obj["secret"]["data"] == "Shhhh!"
            assert decoded_obj["not_secret"] == "Hello"

    @pytest.mark.asyncio
    async def test_key_rotation(self, mock_blob_storage, context):
        """Test encryption key rotation with secondary key."""
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            # Encode with main key
            encoder1 = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_encryption=PayloadEncryptionConfig(
                        mode=PayloadEncryptionMode.FULL,
                        main_key=TEST_MAIN_KEY,
                    ),
                ),
            )

            test_payload_content = to_json({"data": "test"})
            encoded_data, encoding_options = await encoder1.encode_payload_content(test_payload_content, context)

            # Try to decode with encoder that has main key as secondary
            encoder2 = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_encryption=PayloadEncryptionConfig(
                        mode=PayloadEncryptionMode.FULL, main_key=TEST_SECONDARY_KEY, secondary_key=TEST_MAIN_KEY
                    ),
                ),
            )

            decoded_content = await encoder2.decode_payload_content(encoded_data, encoding_options)
            assert decoded_content == test_payload_content

    @pytest.mark.asyncio
    async def test_decryption_failure(self, mock_blob_storage, context):
        """Test decryption failure with wrong key."""
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            # Encode with correct key
            encoder1 = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_encryption=PayloadEncryptionConfig(mode=PayloadEncryptionMode.FULL, main_key=TEST_MAIN_KEY),
                ),
            )

            test_payload_content = to_json({"data": "test"})
            encoded_data, encoding_options = await encoder1.encode_payload_content(test_payload_content, context)

            # Try to decode with wrong key
            encoder2 = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_encryption=PayloadEncryptionConfig(
                        mode=PayloadEncryptionMode.FULL, main_key=AESGCM.generate_key(bit_length=128).hex()
                    ),
                ),
            )

            with pytest.raises(WorkflowPayloadEncryptionException):
                await encoder2.decode_payload_content(encoded_data, encoding_options)

    @pytest.mark.asyncio
    async def test_small_payload_not_offloaded(self, mock_blob_storage, context):
        """Test that small payloads aren't offloaded even when offloading is enabled."""
        with patch(
            "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            encoder = PayloadEncoder(
                encoding_config=WorkflowEncodingConfig(
                    payload_offloading=PayloadOffloadingConfig(min_size_bytes=LARGE_PAYLOAD_SIZE, storage_config={}),
                ),
            )

            small_payload_content = to_json({"data": "small"})
            encoded_data, encoding_options = await encoder.encode_payload_content(small_payload_content, context)

            assert encoding_options == []
            assert len(mock_blob_storage.blobs) == 0

            decoded_content = await encoder.decode_payload_content(encoded_data, encoding_options)
            assert decoded_content == small_payload_content


class TestPayloadMetadataCodec:
    def _make_codec(self) -> MistralWorkflowsPayloadCodec:
        return MistralWorkflowsPayloadCodec(
            payload_offloading_config=None,
            payload_encryption_config=None,
        )

    def _make_input_payload(self, context: WorkflowContext) -> Payload:
        payload_with_context = PayloadWithContext(context=context, payload=b"{}", empty=False)
        return Payload(
            metadata={PayloadMetadataKeys.ENCODING: CUSTOM_ENCODING_FORMAT.encode()},
            data=payload_with_context.model_dump_json().encode(),
        )

    @pytest.mark.asyncio
    async def test_codec_round_trip_preserves_new_context_fields(self):
        context = WorkflowContext(
            namespace="ns",
            execution_id="exec-1",
            continued_run_id="run-prev",
            first_execution_run_id="run-first",
            schedule_id="my-schedule",
        )
        [encoded] = await self._make_codec().encode([self._make_input_payload(context)])
        [decoded] = await self._make_codec().decode([encoded])

        result = PayloadWithContext.model_validate_json(decoded.data)
        assert result.context.continued_run_id == "run-prev"
        assert result.context.first_execution_run_id == "run-first"
        assert result.context.schedule_id == "my-schedule"

    @pytest.mark.asyncio
    async def test_codec_round_trip_new_fields_absent_when_none(self):
        context = WorkflowContext(namespace="ns", execution_id="exec-1")
        [encoded] = await self._make_codec().encode([self._make_input_payload(context)])
        [decoded] = await self._make_codec().decode([encoded])

        result = PayloadWithContext.model_validate_json(decoded.data)
        assert result.context.continued_run_id is None
        assert result.context.first_execution_run_id is None
        assert result.context.schedule_id is None
