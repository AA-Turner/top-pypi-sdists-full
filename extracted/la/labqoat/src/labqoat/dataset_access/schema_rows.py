"""Generic typed row iteration owned by the reference's generated schema model."""

from collections.abc import Generator, Iterator
from typing import TypeVar

from labqoat.json_document import JsonDocument
from labqoat.schemas import SchemaRecord

RecordT = TypeVar("RecordT", bound=SchemaRecord)


class SchemaRows:
    """Decode captured records and close the underlying scoped reader on failure or early exit."""

    @staticmethod
    def read(rows: Iterator[dict[str, object]], record_type: type[RecordT]) -> Generator[RecordT, None, None]:
        """Use generated decoding rather than inspecting authored Python annotations."""
        try:
            for row in rows:
                yield record_type.from_dict(JsonDocument.expect_dict(row))
        finally:
            close = getattr(rows, "close", None)
            if callable(close):
                close()
