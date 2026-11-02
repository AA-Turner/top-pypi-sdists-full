"""Complete immutable checkpoint transport for authored compute values."""

from labqoat.argument_codec import decode_result, encode_result
from labqoat.compute.background_checkpoint import BackgroundCheckpoint
from labqoat.json_document import JsonValue
from labqoat.manifests.manifest_formats import ManifestFormats
from labqoat.references.checkpoint_ref import CheckpointRef
from labqoat.schemas.schema_document import SchemaDocument


class CheckpointCodec:
    """Reject incomplete descriptors and retain explicit semantic checkpoint authority."""

    @staticmethod
    def schema() -> dict[str, JsonValue]:
        """Use the service-owned closed reference shape without a handwritten parallel contract."""
        return ManifestFormats.schema("checkpoint_reference")

    @classmethod
    def encode(cls, value: object) -> JsonValue:
        """Accept only immutable handles whose full descriptor satisfies the portable schema."""
        if not isinstance(value, CheckpointRef):
            raise TypeError("Expected an immutable Checkpoint")
        encoded = encode_result(value.result() if isinstance(value, BackgroundCheckpoint) else value)
        SchemaDocument.capture(cls.schema()).validate(encoded)
        return encoded

    @classmethod
    def decode(cls, value: JsonValue) -> CheckpointRef[object]:
        """Validate every identity coordinate before reconstructing a checkpoint handle."""
        SchemaDocument.capture(cls.schema()).validate(value)
        return decode_result(value, CheckpointRef[object])
