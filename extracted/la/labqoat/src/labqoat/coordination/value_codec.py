"""How dict and queue values travel and are stored."""

import base64
import json
from collections.abc import Mapping

from labqoat._generated.encoded_value import EncodedValue
from labqoat.json_document import JsonDocument, JsonValue


class ValueCodec:
    """JSON-compatible data travels as JSON text and bytes as base64, so any language reads what another wrote.

    Nothing is pickled: store other objects by pickling them yourself and putting the bytes. JSON turns tuples
    into lists and the keys of a mapping into text, as ``json.dumps`` does.
    """

    MAXIMUM = 1_048_576

    @staticmethod
    def encode(value: object) -> dict[str, JsonValue]:
        """Encode one value of at most a mebibyte."""
        if isinstance(value, (bytes, bytearray, memoryview)):
            data = bytes(value)
            ValueCodec.check(len(data))
            return {"encoding": "base64", "data": base64.b64encode(data).decode("ascii")}
        try:
            text = json.dumps(value, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        except (TypeError, ValueError) as error:
            raise TypeError(
                "Dict and queue values are JSON data (dict, list, str, int, float, bool, None) or bytes; "
                "pickle anything else yourself and store the bytes"
            ) from error
        ValueCodec.check(len(text.encode()))
        return {"encoding": "json", "data": text}

    @staticmethod
    def decode(value: EncodedValue) -> object:
        """Decode one stored value: bytes for base64, the parsed data for JSON."""
        if value.encoding == "base64":
            return base64.b64decode(value.data)
        return json.loads(value.data)

    @staticmethod
    def size(encoded: Mapping[str, JsonValue]) -> int:
        """Roughly what an encoded value adds to a request body."""
        return len(JsonDocument.expect_scalar(encoded["data"], str)) + 64

    @staticmethod
    def check(size: int) -> None:
        """Refuse a value the service would refuse, before sending it."""
        if size > ValueCodec.MAXIMUM:
            raise ValueError(f"A dict or queue value is at most {ValueCodec.MAXIMUM} bytes; this one is {size}")
