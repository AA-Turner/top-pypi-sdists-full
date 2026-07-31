import temporalio.api.common.v1
from pydantic import BaseModel
from pydantic_core import to_json

from mistralai.workflows.core.encoding import CUSTOM_ENCODING_FORMAT, LEGACY_ENCODING_FORMAT
from mistralai.workflows.core.temporal.payload_converter import (
    LegacyWithContextJSONPayloadConverter,
    MistralWorkflowsPayloadConverter,
    WithContextJSONPayloadConverter,
)
from mistralai.workflows.models import PayloadMetadataKeys, PayloadWithContext, WorkflowContext


class MyModel(BaseModel):
    name: str
    value: int


def _make_payload_with_context(payload_data: dict, encoding: str) -> temporalio.api.common.v1.Payload:
    """Build a Temporal Payload mimicking what the SDK produces.

    The inner payload must be JSON-encoded bytes inside the PayloadWithContext
    wrapper, matching what `from_json()` expects during deserialization.
    """
    context = WorkflowContext(namespace="test-ns", execution_id="test-exec-id")
    pwc = PayloadWithContext(context=context, payload=to_json(payload_data))
    return temporalio.api.common.v1.Payload(
        metadata={PayloadMetadataKeys.ENCODING: encoding.encode()},
        data=pwc.model_dump_json().encode(),
    )


class TestWithContextJSONPayloadConverter:
    def test_encoding_property(self):
        converter = WithContextJSONPayloadConverter()
        assert converter.encoding == CUSTOM_ENCODING_FORMAT

    def test_to_payload_with_payload_with_context(self):
        context = WorkflowContext(namespace="test-ns", execution_id="test-exec-id")
        pwc = PayloadWithContext(context=context, payload={"name": "test", "value": 42})
        converter = WithContextJSONPayloadConverter()

        result = converter.to_payload(pwc)
        assert result is not None
        assert result.metadata[PayloadMetadataKeys.ENCODING] == CUSTOM_ENCODING_FORMAT.encode()

    def test_to_payload_with_non_payload_with_context(self):
        converter = WithContextJSONPayloadConverter()
        result = converter.to_payload({"not": "a PayloadWithContext"})
        assert result is None

    def test_from_payload_without_type_hint(self):
        converter = WithContextJSONPayloadConverter()
        payload = _make_payload_with_context({"name": "test", "value": 42}, CUSTOM_ENCODING_FORMAT)

        result = converter.from_payload(payload)
        assert isinstance(result, PayloadWithContext)
        assert result.payload == {"name": "test", "value": 42}
        assert result.context.namespace == "test-ns"

    def test_from_payload_with_type_hint(self):
        converter = WithContextJSONPayloadConverter()
        payload = _make_payload_with_context({"name": "test", "value": 42}, CUSTOM_ENCODING_FORMAT)

        result = converter.from_payload(payload, type_hint=MyModel)
        assert isinstance(result, PayloadWithContext)
        assert isinstance(result.payload, MyModel)
        assert result.payload.name == "test"
        assert result.payload.value == 42


class TestLegacyWithContextJSONPayloadConverter:
    def test_encoding_property(self):
        converter = LegacyWithContextJSONPayloadConverter()
        assert converter.encoding == LEGACY_ENCODING_FORMAT

    def test_to_payload_always_returns_none(self):
        converter = LegacyWithContextJSONPayloadConverter()
        context = WorkflowContext(namespace="test-ns", execution_id="test-exec-id")
        pwc = PayloadWithContext(context=context, payload={"name": "test"})

        result = converter.to_payload(pwc)
        assert result is None

    def test_from_payload_decodes_legacy_encoding(self):
        converter = LegacyWithContextJSONPayloadConverter()
        payload = _make_payload_with_context({"name": "test", "value": 42}, LEGACY_ENCODING_FORMAT)

        result = converter.from_payload(payload)
        assert isinstance(result, PayloadWithContext)
        assert result.payload == {"name": "test", "value": 42}

    def test_from_payload_with_type_hint(self):
        converter = LegacyWithContextJSONPayloadConverter()
        payload = _make_payload_with_context({"name": "test", "value": 42}, LEGACY_ENCODING_FORMAT)

        result = converter.from_payload(payload, type_hint=MyModel)
        assert isinstance(result, PayloadWithContext)
        assert isinstance(result.payload, MyModel)
        assert result.payload.name == "test"
        assert result.payload.value == 42


class TestMistralWorkflowsPayloadConverter:
    def test_decodes_new_encoding(self):
        converter = MistralWorkflowsPayloadConverter()
        payload = _make_payload_with_context({"name": "test", "value": 1}, CUSTOM_ENCODING_FORMAT)

        result = converter.from_payloads([payload])
        assert len(result) == 1
        assert isinstance(result[0], PayloadWithContext)
        assert result[0].payload == {"name": "test", "value": 1}

    def test_decodes_legacy_encoding(self):
        converter = MistralWorkflowsPayloadConverter()
        payload = _make_payload_with_context({"name": "legacy", "value": 2}, LEGACY_ENCODING_FORMAT)

        result = converter.from_payloads([payload])
        assert len(result) == 1
        assert isinstance(result[0], PayloadWithContext)
        assert result[0].payload == {"name": "legacy", "value": 2}

    def test_encodes_with_new_format_only(self):
        converter = MistralWorkflowsPayloadConverter()
        context = WorkflowContext(namespace="test-ns", execution_id="test-exec-id")
        pwc = PayloadWithContext(context=context, payload={"name": "test"})

        payloads = converter.to_payloads([pwc])
        assert len(payloads) == 1
        assert payloads[0].metadata[PayloadMetadataKeys.ENCODING] == CUSTOM_ENCODING_FORMAT.encode()


class TestPayloadMetadataRoundTrip:
    """build_temporal_payload_metadata <-> build_info_from_payload_metadata."""

    def test_trusted_extensions_round_trips_independently_of_extensions(self):
        from mistralai.workflows.core.encoding.utils import (
            build_info_from_payload_metadata,
            build_temporal_payload_metadata,
        )

        context = WorkflowContext(
            namespace="test-ns",
            execution_id="test-exec-id",
            extensions={"mistralai": {"connectors": {"bindings": [{"credentials_name": "caller"}]}}},
            trusted_extensions={"mistralai": {"resolved_connectors": {"bindings": [{"connector_name": "github"}]}}},
        )

        metadata = build_temporal_payload_metadata(context, encoding_options=[])
        restored, _, _ = build_info_from_payload_metadata(metadata)

        assert restored.extensions == context.extensions
        assert restored.trusted_extensions == context.trusted_extensions
        # Distinct metadata keys — the two channels never bleed into each other.
        assert PayloadMetadataKeys.EXTENSIONS in metadata
        assert PayloadMetadataKeys.TRUSTED_EXTENSIONS in metadata
        assert metadata[PayloadMetadataKeys.EXTENSIONS] != metadata[PayloadMetadataKeys.TRUSTED_EXTENSIONS]

    def test_absent_trusted_extensions_defaults_to_empty(self):
        from mistralai.workflows.core.encoding.utils import (
            build_info_from_payload_metadata,
            build_temporal_payload_metadata,
        )

        context = WorkflowContext(namespace="test-ns", execution_id="test-exec-id")
        metadata = build_temporal_payload_metadata(context, encoding_options=[])

        assert PayloadMetadataKeys.TRUSTED_EXTENSIONS not in metadata
        restored, _, _ = build_info_from_payload_metadata(metadata)
        assert restored.trusted_extensions == {}
