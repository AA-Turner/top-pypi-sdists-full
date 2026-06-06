"""Tests for event payload encryption/decryption."""

import base64
import json

import pytest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from mistralai.extra.workflows import WorkflowEncodingConfig
from mistralai.extra.workflows.encoding.config import PayloadEncryptionConfig, PayloadEncryptionMode
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

from mistralai.workflows.core._events.event_encoder import ENCRYPTED_PATCH_TYPE, EventPayloadEncoder
from mistralai.workflows.models import EncryptedStrField
from mistralai.workflows.protocol.v1.events import (
    ActivityTaskCompleted,
    ActivityTaskCompletedAttributes,
    ActivityTaskStarted,
    ActivityTaskStartedAttributes,
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    CustomTaskInProgress,
    CustomTaskInProgressAttributes,
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    JSONPatchPayload,
    JSONPayload,
    WorkflowExecutionCompleted,
    WorkflowExecutionCompletedAttributes,
    WorkflowExecutionStarted,
    WorkflowExecutionStartedAttributes,
)

TEST_MAIN_KEY = AESGCM.generate_key(bit_length=128).hex()


def _create_payload_encoder(mode: PayloadEncryptionMode = PayloadEncryptionMode.FULL) -> PayloadEncoder:
    return PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(
            payload_encryption=PayloadEncryptionConfig(mode=mode, main_key=TEST_MAIN_KEY),
        ),
    )


def _create_base_event_fields() -> dict:
    return {
        "event_id": "evt-1",
        "root_workflow_exec_id": "exec-1",
        "workflow_exec_id": "exec-1",
        "workflow_run_id": "run-1",
        "workflow_name": "test-workflow",
    }


def _decrypt_value(encrypted_b64: str) -> dict:
    ciphertext = base64.b64decode(encrypted_b64)
    aesgcm = AESGCM(bytes.fromhex(TEST_MAIN_KEY))
    plaintext = aesgcm.decrypt(ciphertext[:12], ciphertext[12:], None)
    return json.loads(plaintext)


SECRET_DATA = {"api_key": "sk-secret-12345", "nested": {"value": 42}}


def _workflow_execution_started():
    return WorkflowExecutionStarted(
        **_create_base_event_fields(),
        attributes=WorkflowExecutionStartedAttributes(
            task_id="task-1", workflow_name="test-workflow", input=JSONPayload(value=SECRET_DATA)
        ),
    )


def _workflow_execution_completed():
    return WorkflowExecutionCompleted(
        **_create_base_event_fields(),
        attributes=WorkflowExecutionCompletedAttributes(task_id="task-1", result=JSONPayload(value=SECRET_DATA)),
    )


def _custom_task_started():
    return CustomTaskStarted(
        **_create_base_event_fields(),
        attributes=CustomTaskStartedAttributes(
            custom_task_id="task-1", custom_task_type="test-task", payload=JSONPayload(value=SECRET_DATA)
        ),
    )


def _custom_task_completed():
    return CustomTaskCompleted(
        **_create_base_event_fields(),
        attributes=CustomTaskCompletedAttributes(
            custom_task_id="task-1", custom_task_type="test-task", payload=JSONPayload(value=SECRET_DATA)
        ),
    )


def _activity_task_started():
    return ActivityTaskStarted(
        **_create_base_event_fields(),
        attributes=ActivityTaskStartedAttributes(
            task_id="act-1", activity_name="test-activity", input=JSONPayload(value=SECRET_DATA)
        ),
    )


def _activity_task_completed():
    return ActivityTaskCompleted(
        **_create_base_event_fields(),
        attributes=ActivityTaskCompletedAttributes(
            task_id="act-1", activity_name="test-activity", result=JSONPayload(value=SECRET_DATA)
        ),
    )


class TestEventPayloadEncoder:
    @pytest.fixture
    def event_encoder(self):
        return EventPayloadEncoder(_create_payload_encoder())

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("event_factory", "field_name"),
        [
            (_workflow_execution_started, "input"),
            (_workflow_execution_completed, "result"),
            (_custom_task_started, "payload"),
            (_custom_task_completed, "payload"),
            (_activity_task_started, "input"),
            (_activity_task_completed, "result"),
        ],
        ids=[
            "WorkflowExecutionStarted",
            "WorkflowExecutionCompleted",
            "CustomTaskStarted",
            "CustomTaskCompleted",
            "ActivityTaskStarted",
            "ActivityTaskCompleted",
        ],
    )
    async def test_encrypt_decrypt_roundtrip(self, event_encoder, event_factory, field_name):
        """Test encryption/decryption roundtrip for each event type."""
        event = event_factory()

        encoded = await event_encoder.encode_event(event)
        encoded_payload = getattr(encoded.attributes, field_name)

        assert "encrypted" in encoded_payload.encoding_options
        assert isinstance(encoded_payload.value, str)
        assert _decrypt_value(encoded_payload.value) == SECRET_DATA

        decoded = await event_encoder.decode_event(encoded)
        decoded_payload = getattr(decoded.attributes, field_name)

        assert decoded_payload.encoding_options == []
        assert decoded_payload.value == SECRET_DATA

    @pytest.mark.asyncio
    async def test_decode_unencrypted_event_returns_unchanged(self, event_encoder):
        plain_data = {"public_info": "hello"}
        event = WorkflowExecutionStarted(
            **_create_base_event_fields(),
            attributes=WorkflowExecutionStartedAttributes(
                task_id="task-1",
                workflow_name="test-workflow",
                input=JSONPayload(value=plain_data),
            ),
        )

        decoded = await event_encoder.decode_event(event)
        assert decoded.attributes.input.value == plain_data
        assert not decoded.attributes.input.encoding_options


class TestEventPayloadEncoderPartialEncryption:
    @pytest.fixture
    def partial_event_encoder(self):
        return EventPayloadEncoder(_create_payload_encoder(mode=PayloadEncryptionMode.PARTIAL))

    @pytest.mark.asyncio
    async def test_partial_encryption_only_encrypts_marked_fields(self, partial_event_encoder):
        data = {
            "public_key": "not-secret",
            "private_key": EncryptedStrField(data="super-secret").model_dump(),
        }

        event = WorkflowExecutionStarted(
            **_create_base_event_fields(),
            attributes=WorkflowExecutionStartedAttributes(
                task_id="task-1",
                workflow_name="test-workflow",
                input=JSONPayload(value=data),
            ),
        )

        encoded = await partial_event_encoder.encode_event(event)
        assert "encrypted-partial" in encoded.attributes.input.encoding_options

        parsed = json.loads(base64.b64decode(encoded.attributes.input.value))
        assert parsed["public_key"] == "not-secret"
        assert parsed["private_key"]["data"] != "super-secret"

    @pytest.mark.asyncio
    async def test_json_payload_no_encryption_without_encrypted_fields(self, partial_event_encoder):
        """JSONPayload without encrypted field markers remains unchanged in partial mode."""
        data = {"public_key": "visible", "count": 42}

        event = WorkflowExecutionStarted(
            **_create_base_event_fields(),
            attributes=WorkflowExecutionStartedAttributes(
                task_id="task-1",
                workflow_name="test-workflow",
                input=JSONPayload(value=data),
            ),
        )

        encoded = await partial_event_encoder.encode_event(event)
        # No encryption applied - payload should be unchanged
        assert not encoded.attributes.input.encoding_options
        assert encoded.attributes.input.value == data

    @pytest.mark.asyncio
    async def test_json_patch_no_encryption_without_encrypted_fields(self, partial_event_encoder):
        """json_patch payloads without encrypted field markers remain unencrypted."""
        event = CustomTaskInProgress(
            **_create_base_event_fields(),
            attributes=CustomTaskInProgressAttributes(
                custom_task_id="task-1",
                custom_task_type="test-task",
                payload=JSONPatchPayload(value=[{"op": "replace", "path": "/content", "value": "not-sensitive"}]),
            ),
        )

        encoded = await partial_event_encoder.encode_event(event)
        # No encryption applied since there are no encrypted field markers
        assert not encoded.attributes.payload.encoding_options
        assert encoded.attributes.payload.value[0].value == "not-sensitive"

    @pytest.mark.asyncio
    async def test_json_patch_selective_encryption_with_encrypted_fields(self, partial_event_encoder):
        """json_patch selectively encrypts only patches targeting encrypted fields."""
        from mistralai.workflows.core._events.json_patch import make_json_patch

        previous_state = {
            "progress": "0%",
            "secret": EncryptedStrField(data="old-secret").model_dump(),
        }
        new_state = {
            "progress": "50%",
            "secret": EncryptedStrField(data="new-secret").model_dump(),
        }

        patches, encrypted_paths = make_json_patch(previous_state, new_state)
        payload = JSONPatchPayload(value=patches)
        payload._encrypted_paths = encrypted_paths
        event = CustomTaskInProgress(
            **_create_base_event_fields(),
            attributes=CustomTaskInProgressAttributes(
                custom_task_id="task-1",
                custom_task_type="test-task",
                payload=payload,
            ),
        )

        encoded = await partial_event_encoder.encode_event(event)

        # Should have partially encrypted encoding
        assert "encrypted-partial" in encoded.attributes.payload.encoding_options

        # Value should be a list (selective encryption, not base64 string)
        patches_list = encoded.attributes.payload.value
        assert isinstance(patches_list, list)
        assert len(patches_list) == 2

        patches_by_path = {p.path: p for p in patches_list}

        # Progress should remain unencrypted
        assert patches_by_path["/progress"].value == "50%"

        # Secret data should be encrypted with EncryptedPatchValue structure, no cleartext
        # Note: JSONPatchReplace has value: Any, so the dict stays as dict (not coerced to EncryptedPatchValue)
        secret_patch = patches_by_path["/secret/data"]
        assert isinstance(secret_patch.value, dict)
        assert secret_patch.value.get("type") == ENCRYPTED_PATCH_TYPE
        assert "value" in secret_patch.value
        assert "new-secret" not in secret_patch.value["value"]

        # Decrypt and verify
        decoded = await partial_event_encoder.decode_event(encoded)
        decoded_patches = {p.path: p for p in decoded.attributes.payload.value}
        assert decoded_patches["/secret/data"].value == "new-secret"

    @pytest.mark.asyncio
    async def test_json_patch_encrypted_field_with_append_optimization(self, partial_event_encoder):
        """Encrypted fields work with append optimization using EncryptedPatchValue wrapper.

        When EncryptedStrField.data is updated incrementally (new value starts with old),
        the append optimization is triggered. Encryption uses EncryptedPatchValue wrapper.
        """
        from mistralai.workflows.core._events.json_patch import make_json_patch

        # Simulate incremental update to encrypted field (triggers append optimization)
        previous_state = {
            "response": EncryptedStrField(data="Hello").model_dump(),
        }
        new_state = {
            "response": EncryptedStrField(data="Hello, world!").model_dump(),
        }

        patches, encrypted_paths = make_json_patch(previous_state, new_state)

        # Should use "append" optimization even for encrypted path
        assert len(patches) == 1
        assert patches[0].op == "append", "Should use append optimization"
        assert patches[0].value == ", world!", "Append value should be the delta"
        assert patches[0].path in encrypted_paths, "Path should be in encrypted_paths"

        # Create payload with encrypted paths
        payload = JSONPatchPayload(value=patches)
        payload._encrypted_paths = encrypted_paths

        # Create and encode the event
        event = CustomTaskInProgress(
            **_create_base_event_fields(),
            attributes=CustomTaskInProgressAttributes(
                custom_task_id="task-1",
                custom_task_type="test-task",
                payload=payload,
            ),
        )

        encoded = await partial_event_encoder.encode_event(event)

        # Verify encryption used EncryptedPatchValue wrapper by serializing to JSON and parsing back
        # This simulates the actual wire format sent to the API
        encoded_json = encoded.model_dump(mode="json")
        patches_json = encoded_json["attributes"]["payload"]["value"]
        assert patches_json[0]["value"]["type"] == "__encrypted__", "Patch value should have type discriminator"
        assert patches_json[0]["value"]["value"]  # Has encrypted data
        assert ", world!" not in patches_json[0]["value"]["value"]  # Original value should be encrypted

        # Verify encoding options are present
        assert "encrypted-partial" in encoded_json["attributes"]["payload"]["encoding_options"]

        # Verify round-trip decryption
        decoded = await partial_event_encoder.decode_event(encoded)
        assert decoded.attributes.payload.value[0].value == ", world!"


class TestJsonPointerEscaping:
    """Test RFC6901 JSON Pointer escaping in encrypted path detection.

    JSON Pointer (RFC6901) requires escaping special characters in keys:
    - '~' must be escaped as '~0'
    - '/' must be escaped as '~1'

    find_encrypted_paths must use the same escaping as jsonpatch library
    so that _should_encrypt_path correctly matches paths to encrypted fields.
    """

    def test_encrypted_field_under_key_with_slash(self):
        """Keys containing '/' must be escaped as '~1' to match jsonpatch paths."""
        from mistralai.workflows.core._events.json_patch import find_encrypted_paths, make_json_patch

        # Key contains '/' which must be escaped as '~1' in JSON Pointer
        previous_state = {
            "parent": {
                "foo/bar": EncryptedStrField(data="secret").model_dump(),
            }
        }
        new_state = {
            "parent": {
                "foo/bar": EncryptedStrField(data="secret-updated").model_dump(),
            }
        }

        # Verify find_encrypted_paths uses proper escaping
        field_paths = find_encrypted_paths(new_state)
        assert "/parent/foo~1bar" in field_paths, f"Path should use RFC6901 escaping (/ -> ~1). Got: {field_paths}"

        # Verify patch path is in encrypted_paths
        patches, encrypted_paths = make_json_patch(previous_state, new_state)
        data_patch = next((p for p in patches if p.path.endswith("/data")), None)
        assert data_patch is not None, f"Expected patch for /data field. Got: {[p.path for p in patches]}"
        assert data_patch.path in encrypted_paths, "Patch path should be in encrypted_paths"

    def test_encrypted_field_under_key_with_tilde(self):
        """Keys containing '~' must be escaped as '~0' to match jsonpatch paths."""
        from mistralai.workflows.core._events.json_patch import find_encrypted_paths, make_json_patch

        previous_state = {
            "key~name": EncryptedStrField(data="secret").model_dump(),
        }
        new_state = {
            "key~name": EncryptedStrField(data="secret-updated").model_dump(),
        }

        field_paths = find_encrypted_paths(new_state)
        assert "/key~0name" in field_paths, f"Path should use RFC6901 escaping (~ -> ~0). Got: {field_paths}"

        patches, encrypted_paths = make_json_patch(previous_state, new_state)
        data_patch = next((p for p in patches if p.path.endswith("/data")), None)
        assert data_patch is not None
        assert data_patch.path in encrypted_paths

    def test_encrypted_field_under_key_with_both_special_chars(self):
        """Keys with both '~' and '/' must escape ~ first, then / (RFC6901 order)."""
        from mistralai.workflows.core._events.json_patch import find_encrypted_paths, make_json_patch

        # Key "a/b~c" should become "a~1b~0c" in JSON Pointer
        previous_state = {
            "a/b~c": EncryptedStrField(data="secret").model_dump(),
        }
        new_state = {
            "a/b~c": EncryptedStrField(data="secret-updated").model_dump(),
        }

        field_paths = find_encrypted_paths(new_state)
        assert "/a~1b~0c" in field_paths, f"Path should escape ~ before / (RFC6901). Got: {field_paths}"

        patches, encrypted_paths = make_json_patch(previous_state, new_state)
        data_patch = next((p for p in patches if p.path.endswith("/data")), None)
        assert data_patch is not None
        assert data_patch.path in encrypted_paths

    def test_parent_path_patch_with_nested_encrypted_field(self):
        """Parent path patches must be encrypted when they contain nested encrypted fields.

        When jsonpatch emits an "add" or "replace" on a parent path (e.g., /credentials),
        and the value contains a nested EncryptedStrField (e.g., at /credentials/api_key),
        the patch must be marked for encryption to prevent secret leakage.
        """
        from mistralai.workflows.core._events.json_patch import make_json_patch

        # Start with empty state, add a parent object containing nested encrypted field
        previous_state = {}
        new_state = {
            "credentials": {
                "api_key": EncryptedStrField(data="super-secret-key").model_dump(),
                "region": "us-east-1",
            }
        }

        patches, encrypted_paths = make_json_patch(previous_state, new_state)

        # Should have a single "add" patch for /credentials
        assert len(patches) == 1
        assert patches[0].op == "add"
        assert patches[0].path == "/credentials"

        # The parent path must be in encrypted_paths because it contains nested secret
        assert "/credentials" in encrypted_paths, (
            "Parent path /credentials should be marked for encryption because it contains "
            f"nested encrypted field. Got encrypted_paths: {encrypted_paths}"
        )
