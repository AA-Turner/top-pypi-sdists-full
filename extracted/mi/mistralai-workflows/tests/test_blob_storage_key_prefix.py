from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

from mistralai.workflows.core.encoding.fields_offloader import FieldsOffloader
from mistralai.workflows.models import WorkflowContext


class TestFieldsOffloaderBlobStorageKeyPrefix:
    def test_simple_values(self):
        result = FieldsOffloader.blob_storage_key_prefix("my-namespace", "my-run-id")
        assert result == "temporal-activity-payload/my-namespace/my-run-id"

    def test_slashes_are_quoted(self):
        result = FieldsOffloader.blob_storage_key_prefix("ns/with/slashes", "run/id")
        assert result == "temporal-activity-payload/ns%2Fwith%2Fslashes/run%2Fid"

    def test_special_characters_are_quoted(self):
        result = FieldsOffloader.blob_storage_key_prefix("ns with spaces", "run:id?foo=bar")
        assert "ns%20with%20spaces" in result
        assert "run%3Aid%3Ffoo%3Dbar" in result

    def test_percent_is_quoted(self):
        result = FieldsOffloader.blob_storage_key_prefix("ns%20encoded", "run-id")
        assert result == "temporal-activity-payload/ns%2520encoded/run-id"

    def test_prefix_is_not_quoted(self):
        result = FieldsOffloader.blob_storage_key_prefix("ns", "rid")
        assert result.startswith("temporal-activity-payload/")

    def test_exactly_three_segments(self):
        result = FieldsOffloader.blob_storage_key_prefix("ns/a", "rid/b")
        assert result.count("/") == 2


class TestPayloadEncoderBlobStorageKeyPrefix:
    def test_simple_values(self):
        ctx = WorkflowContext(namespace="my-namespace", execution_id="my-execution-id")
        result = PayloadEncoder.blob_storage_key_prefix(ctx)
        assert result == "temporal-payload/my-namespace/my-execution-id"

    def test_slashes_are_quoted(self):
        ctx = WorkflowContext(namespace="ns/with/slashes", execution_id="exec/id")
        result = PayloadEncoder.blob_storage_key_prefix(ctx)
        assert result == "temporal-payload/ns%2Fwith%2Fslashes/exec%2Fid"

    def test_special_characters_are_quoted(self):
        ctx = WorkflowContext(namespace="ns with spaces", execution_id="exec:id?foo=bar")
        result = PayloadEncoder.blob_storage_key_prefix(ctx)
        assert "ns%20with%20spaces" in result
        assert "exec%3Aid%3Ffoo%3Dbar" in result

    def test_exactly_three_segments(self):
        ctx = WorkflowContext(namespace="ns/a", execution_id="eid/b")
        result = PayloadEncoder.blob_storage_key_prefix(ctx)
        assert result.count("/") == 2
