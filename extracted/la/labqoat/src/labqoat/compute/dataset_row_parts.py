"""Bounded staging of typed rows for publication: inline when small, exact-layout Parquet part files otherwise."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO

import pyarrow as pa
import pyarrow.parquet as pq

from labqoat.data_layout.dataset_layout import DatasetLayout
from labqoat.json_document import JsonValue
from labqoat.schemas.identity import Identity


@dataclass
class DatasetRowParts:
    """Keep small publications in memory and stream larger ones to ordered Parquet part files of bounded size."""

    directory: Path
    layout: DatasetLayout
    inline_rows: int = 10_000
    inline_bytes: int = 4_194_304
    part_bytes: int = 64 * 1024 * 1024
    batch_rows: int = 1024
    maximum_parts: int = 100
    rows: list[JsonValue] = field(default_factory=list)
    paths: list[Path] = field(default_factory=list)
    _inline_size: int = 0
    _staged: bool = False
    _batch: list[dict[str, JsonValue]] = field(default_factory=list)
    _stream: BinaryIO | None = None
    _writer: pq.ParquetWriter | None = None

    def add(self, value: JsonValue) -> None:
        """Stage one row, moving everything to part files once the inline budget is exceeded."""
        if not self._staged and self._fits(value):
            self.rows.append(value)
            return
        self._staged = True
        for inline in self.rows:
            self._append(inline)
        self.rows = []
        self._append(value)

    def close(self) -> None:
        """Write the buffered rows and finish the open part so its bytes can be hashed and uploaded."""
        if self._batch:
            self._flush()
        self._finish()

    def discard(self) -> None:
        """Remove staged part files once they are retained elsewhere or the publication failed."""
        self._batch = []
        self._finish()
        for path in self.paths:
            path.unlink(missing_ok=True)

    def _fits(self, value: JsonValue) -> bool:
        """Charge a row against the inline budgets, which bound the publication request itself."""
        self._inline_size += len(Identity.bytes(value)) + 1
        return len(self.rows) < self.inline_rows and self._inline_size <= self.inline_bytes

    def _append(self, value: JsonValue) -> None:
        """Buffer one physical row and write a row group once the batch is full."""
        self._batch.append(self.layout.physical(value))
        if len(self._batch) >= self.batch_rows:
            self._flush()

    def _flush(self) -> None:
        """Write the buffered rows as one row group, starting the next part when the open one is full."""
        if self._stream is not None and self._stream.tell() >= self.part_bytes:
            self._finish()
        if self._writer is None:
            self._open()
        assert self._writer is not None
        self._writer.write_batch(pa.RecordBatch.from_pylist(self._batch, schema=self.layout.arrow_schema))
        self._batch = []

    def _open(self) -> None:
        """Start the next ordered part file."""
        if len(self.paths) == self.maximum_parts:
            raise ValueError(f"Typed publication accepts at most {self.maximum_parts} parts of {self.part_bytes} bytes")
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self.directory / f"part-{len(self.paths):05d}.parquet"
        self.paths.append(path)
        self._stream = path.open("wb")
        self._writer = pq.ParquetWriter(self._stream, self.layout.arrow_schema, compression="zstd")

    def _finish(self) -> None:
        """Close the open part, if any."""
        if self._writer is not None:
            self._writer.close()
            self._writer = None
        if self._stream is not None:
            self._stream.close()
            self._stream = None
