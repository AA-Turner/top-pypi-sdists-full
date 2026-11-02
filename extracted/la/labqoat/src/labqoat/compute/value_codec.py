"""Schema-owned scalar and immutable asset transport for authored compute values."""

from collections.abc import Callable
from dataclasses import dataclass, is_dataclass
from functools import cached_property
from typing import Generic, Literal, TypeVar, cast, get_args, get_origin

from labqoat.argument_codec import decode_result, encode_result
from labqoat.compute.dataset_codec import DatasetCodec
from labqoat.compute.checkpoint_codec import CheckpointCodec
from labqoat.compute.literal_codec import LiteralCodec
from labqoat.compute.mapping_codec import MappingCodec
from labqoat.compute.optional_codec import OptionalCodec
from labqoat.compute.record_codec import RecordCodec
from labqoat.compute.scalar_codec import ScalarCodec
from labqoat.compute.sequence_codec import SequenceCodec
from labqoat.dataset import Dataset
from labqoat.json_document import JsonValue
from labqoat.references.asset_ref import AssetRef
from labqoat.references.checkpoint_ref import CheckpointRef
from labqoat.schemas.asset_schema import AssetSchema
from labqoat.schemas.schema_document import SchemaDocument

T = TypeVar("T")


@dataclass(frozen=True)
class ValueCodec(Generic[T]):
    """Retain explicit reference semantics instead of treating arbitrary ID-shaped objects as assets."""

    value_type: type[T]
    ancestors: tuple[object, ...] = ()

    def schema(self) -> dict[str, JsonValue]:
        """Embed the shared closed immutable asset descriptor or a portable scalar schema."""
        if self.value_type is AssetRef:
            return dict(AssetSchema.document())
        if (get_origin(self.value_type) or self.value_type) is CheckpointRef:
            return CheckpointCodec.schema()
        if get_origin(self.value_type) is Dataset:
            return DatasetCodec(get_args(self.value_type)[0]).schema()
        if get_origin(self.value_type) is Literal:
            return LiteralCodec(self.value_type).schema()
        return self._ordinary().schema()

    def encode(self, value: T) -> JsonValue:
        """Check the Python declaration, then validate the whole encoded value against its schema once."""
        document = self._document
        encoded = self.convert(value)
        document.validate(encoded)
        return encoded

    def convert(self, value: T) -> JsonValue:
        """Encode by declared type; references validate their own exact catalog identity."""
        return self._converter(value)

    def decode(self, value: JsonValue) -> T:
        """Validate the whole value against its schema once, then reconstruct its immutable Python value."""
        self._document.validate(value)
        return self.restore(value)

    def restore(self, value: JsonValue) -> T:
        """Reconstruct by declared type a value the enclosing document already validated."""
        return cast(T, self._restorer(value))

    @cached_property
    def _converter(self) -> Callable[[T], JsonValue]:
        """Choose the encoder for the declared type once, not once per value."""
        if (get_origin(self.value_type) or self.value_type) is CheckpointRef:
            return CheckpointCodec.encode
        if get_origin(self.value_type) is Literal:
            return LiteralCodec(self.value_type).convert
        if get_origin(self.value_type) is Dataset:
            return DatasetCodec(get_args(self.value_type)[0]).encode
        if self.value_type is not AssetRef:
            return self._delegate.convert
        return self._asset

    @cached_property
    def _restorer(self) -> Callable[[JsonValue], object]:
        """Choose the decoder for the declared type once, not once per value."""
        if (get_origin(self.value_type) or self.value_type) is CheckpointRef:
            return CheckpointCodec.decode
        if get_origin(self.value_type) is Dataset:
            return DatasetCodec(get_args(self.value_type)[0]).decode
        if get_origin(self.value_type) is Literal:
            return self._unchanged
        if self.value_type is not AssetRef:
            return self._delegate.restore
        return self._asset_reference

    @staticmethod
    def _asset(value: object) -> JsonValue:
        """Encode an artifact's exact catalog identity."""
        if not isinstance(value, AssetRef):
            raise TypeError("Expected an immutable Artifact")
        return encode_result(value)

    @staticmethod
    def _asset_reference(value: JsonValue) -> AssetRef:
        """Rebuild an artifact reference from its validated descriptor."""
        return decode_result(value, AssetRef)

    @staticmethod
    def _unchanged(value: JsonValue) -> JsonValue:
        """A validated closed string choice is its own Python value."""
        return value

    @cached_property
    def _document(self) -> SchemaDocument:
        """Capture and compile the complete schema once for every value this codec handles."""
        return SchemaDocument.capture(self.schema())

    @cached_property
    def _delegate(self) -> RecordCodec[T] | ScalarCodec[T] | SequenceCodec[T] | MappingCodec[T] | OptionalCodec[T]:
        """Select the ordinary codec once, so nested codecs are resolved a single time."""
        return self._ordinary()

    def _ordinary(self) -> RecordCodec[T] | ScalarCodec[T] | SequenceCodec[T] | MappingCodec[T] | OptionalCodec[T]:
        """Select ordinary data transport after explicit semantic types have been handled."""
        if OptionalCodec.matches(self.value_type):
            return OptionalCodec(self.value_type, self.ancestors)
        if is_dataclass(self.value_type):
            return RecordCodec(self.value_type, self.ancestors)
        if get_origin(self.value_type) in (list, tuple):
            return SequenceCodec(self.value_type, self.ancestors)
        if get_origin(self.value_type) is dict:
            return MappingCodec(self.value_type, self.ancestors)
        return ScalarCodec(self.value_type)
