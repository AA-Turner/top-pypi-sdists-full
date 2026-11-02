"""Schema-bound transport for typed immutable dataset handles."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from labqoat.argument_codec import decode_result, encode_result
from labqoat.compute.dataset_reference_schema import DatasetReferenceSchema
from labqoat.dataset import Dataset
from labqoat.json_document import JsonValue
from labqoat.references.resolved_dataset_ref import ResolvedDatasetRef
from labqoat.schemas.schema_document import SchemaDocument

T = TypeVar("T")


@dataclass(frozen=True)
class DatasetCodec(Generic[T]):
    """Preserve full revision pins and reconstruct an explicit Python row binding."""

    row_type: type[T]

    def schema(self) -> dict[str, JsonValue]:
        """Own the expected row schema at each declared Dataset position."""
        from labqoat.compute.value_codec import ValueCodec

        digest = SchemaDocument.capture(ValueCodec(self.row_type).schema()).digest
        return DatasetReferenceSchema.document(digest)

    def encode(self, value: object) -> JsonValue:
        """Require the declared binding before serializing complete immutable metadata."""
        if not isinstance(value, Dataset) or value.row_type is not self.row_type:
            raise TypeError("Expected a Dataset bound to the declared row type")
        result = encode_result(value.reference)
        SchemaDocument.capture(self.schema()).validate(result)
        return result

    def decode(self, value: JsonValue) -> Dataset[T]:
        """Reject incomplete or changed identities before reconstructing the handle."""
        SchemaDocument.capture(self.schema()).validate(value)
        reference: ResolvedDatasetRef[object] = decode_result(value, ResolvedDatasetRef)
        return Dataset(reference, self.row_type)
