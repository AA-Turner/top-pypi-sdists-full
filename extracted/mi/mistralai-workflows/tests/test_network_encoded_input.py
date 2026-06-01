from mistralai.workflows.models import EncodedPayload, EncodedPayloadOptions, NetworkEncodedInput, WorkflowContext


class TestNetworkEncodedInput:
    def test_from_data(self):
        encoded = NetworkEncodedInput.from_data(b"test", [EncodedPayloadOptions.ENCRYPTED])
        assert encoded.get_payload() == b"test"
        assert encoded.encoding_options == [EncodedPayloadOptions.ENCRYPTED]

    def test_from_encoded_payload(self):
        payload = EncodedPayload(
            payload=b"test",
            encoding_options=[EncodedPayloadOptions.OFFLOADED],
            context=WorkflowContext(namespace="ns", execution_id="exec"),
        )
        encoded = NetworkEncodedInput.from_encoded_payload(payload)
        assert encoded.get_payload() == b"test"
        assert encoded.encoding_options == [EncodedPayloadOptions.OFFLOADED]

    def test_to_encoded_payload(self):
        encoded = NetworkEncodedInput.from_data(b"test", [EncodedPayloadOptions.ENCRYPTED])
        payload = encoded.to_encoded_payload(namespace="ns", execution_id="exec")
        assert payload.payload == b"test"
        assert payload.encoding_options == [EncodedPayloadOptions.ENCRYPTED]
        assert payload.context.namespace == "ns"
        assert payload.context.execution_id == "exec"

    def test_get_payload(self):
        encoded = NetworkEncodedInput.from_data(b"test", [])
        assert encoded.get_payload() == b"test"

    def test_roundtrip(self):
        original = EncodedPayload(
            payload=b'{"key": "value"}',
            encoding_options=[EncodedPayloadOptions.ENCRYPTED, EncodedPayloadOptions.OFFLOADED],
            context=WorkflowContext(namespace="ns", execution_id="exec"),
        )
        encoded = NetworkEncodedInput.from_encoded_payload(original)
        restored = encoded.to_encoded_payload(namespace="ns", execution_id="exec")
        assert restored.payload == original.payload
        assert restored.encoding_options == original.encoding_options
