"""Public typed argument and result conversion."""

from typing import TypeVar, cast

from labqoat.argument_codec.value_decoder import ValueDecoder
from labqoat.argument_codec.value_encoder import ValueEncoder
from labqoat.json_document import JsonValue

ValueT = TypeVar("ValueT")


class ArgumentCodec:
    """Convert authored dataclass results and explicit argument documents."""

    @staticmethod
    def decode_result(value: object, target: type[ValueT]) -> ValueT:
        """Decode one result using the requested public data type."""
        return cast("ValueT", ValueDecoder.decode(value, target))

    @staticmethod
    def encode_result(value: object, target: object = None) -> JsonValue:
        """Encode one result into deterministic JSON-compatible values."""
        encoded = ValueEncoder.encode(value)
        if target is not None:
            ValueDecoder.decode(encoded, target)
        return encoded

    @staticmethod
    def decode_arguments(value: object, target: type[ValueT]) -> ValueT:
        """Validate and reconstruct one authored argument object."""
        return ArgumentCodec.decode_result(value, target)
