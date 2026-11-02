"""Bounded-memory JSONL and exact-layout Parquet decoding with authoritative validation."""

from collections.abc import Iterator
from pathlib import Path
from typing import cast

import pyarrow.parquet as pq

from labqoat.data_layout.data_validation_error import DataValidationError
from labqoat.data_layout.dataset_layout import DatasetLayout
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.identity import Identity


class DatasetRows:
    """Read and validate each row without trusting a file's claimed schema digest."""

    def __init__(self, layout: DatasetLayout, batch_size: int = 1024, max_row_bytes: int = 8_388_608) -> None:
        """Bound batches and individual JSON records independently of total file size."""
        if batch_size < 1 or max_row_bytes < 1:
            raise ValueError("batch_size and max_row_bytes must be positive")
        self.layout = layout
        self.wrapped = layout.root.wraps()
        self.batch_size = batch_size
        self.max_row_bytes = max_row_bytes

    def read(self, path: Path, format_name: str) -> Iterator[dict[str, JsonValue]]:
        """Require an explicit captured format; do not infer it from untrusted metadata."""
        if format_name == "jsonl":
            return self.jsonl(path)
        if format_name == "parquet":
            return self.parquet(path)
        raise ValueError(f"Unsupported dataset input format: {format_name}")

    def jsonl(self, path: Path) -> Iterator[dict[str, JsonValue]]:
        """Validate one logical record at a time, preserving original line locations."""
        with path.open("rb") as stream:
            row = 0
            while line := stream.readline(self.max_row_bytes + 1):
                row += 1
                yield self._decode_jsonl(line, path, row)

    def _decode_jsonl(self, line: bytes, path: Path, row: int) -> dict[str, JsonValue]:
        """Validate one bounded JSON record and preserve its source location."""
        try:
            if len(line) > self.max_row_bytes:
                raise ValueError("/: JSON row exceeds max_row_bytes")
            value = Identity.decode(line.decode("utf-8"))
            self.layout.encode(value)
            return JsonDocument.expect_dict(value)
        except (ValueError, TypeError) as error:
            raise DataValidationError(str(path), row, str(error)) from error

    def parquet(self, path: Path) -> Iterator[dict[str, JsonValue]]:
        """Check the exact physical types, ignoring advisory metadata, and unwrap each stored row."""
        with pq.ParquetFile(path) as source:
            if not source.schema_arrow.equals(self.layout.arrow_schema, check_metadata=False):
                raise DataValidationError(str(path), 0, "/: Parquet physical schema does not match the captured layout")
            row = 0
            for batch in source.iter_batches(batch_size=self.batch_size):
                for value in batch.to_pylist():
                    row += 1
                    yield self._decode_parquet(value, path, row)

    def _decode_parquet(self, value: object, path: Path, row: int) -> dict[str, JsonValue]:
        """Rows without presence wrappers are already logical; others are unwrapped with their location kept."""
        if not self.wrapped:
            return cast(dict[str, JsonValue], value)
        try:
            return self.layout.logical(JsonDocument.expect_value(value))
        except (ValueError, TypeError) as error:
            raise DataValidationError(str(path), row, str(error)) from error
