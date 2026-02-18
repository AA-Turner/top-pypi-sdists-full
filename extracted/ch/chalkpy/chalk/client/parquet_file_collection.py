from __future__ import annotations

import bisect
import dataclasses
import functools
from typing import List, Tuple

import pyarrow as pa
import pyarrow.parquet as pq
from fsspec.implementations.http import HTTPFileSystem
from pyarrow.fs import FSSpecHandler, PyFileSystem

_HTTP_FS = PyFileSystem(FSSpecHandler(HTTPFileSystem()))


def parquet_file_from_uri(uri: str) -> pq.ParquetFile:
    if uri.startswith("file://"):
        return pq.ParquetFile(uri)
    elif uri.startswith(("http://", "https://")):
        return pq.ParquetFile(uri, filesystem=_HTTP_FS)
    raise NotImplementedError(f'Cannot read parquet contents for file: "{uri}" unknown prefix')


@dataclasses.dataclass
class ParquetRowGroupMetadata:
    file_idx: int
    """Which parquet file this row group corresponds with"""

    row_group_idx: int
    """Which row group in its parquet this row group is"""

    num_rows: int
    """Number of rows in this row group"""

    dataset_row_start_idx: int
    """Absolute index in dataset where this row group starts."""


@dataclasses.dataclass
class ParquetFileCollection:
    parquet_files: List[str]
    row_groups: List[ParquetRowGroupMetadata]

    def __init__(
        self,
        *,
        parquet_files: List[str],
        row_groups: List[ParquetRowGroupMetadata],
        materialized_table_cache_size: int,
    ):
        super().__init__()
        self.parquet_files = parquet_files
        self.row_groups = row_groups
        self.materialize_row_group = functools.lru_cache(maxsize=materialized_table_cache_size)(
            self._materialize_row_group
        )

    def _materialize_row_group(self, dataset_row_group_idx: int) -> pa.Table:
        """
        Prefer to use materialize_row_group(), which has an LRU cache on top of it
        """
        parquet_file_idx = self.row_groups[dataset_row_group_idx].file_idx
        parquet_file = parquet_file_from_uri(self.parquet_files[parquet_file_idx])
        return parquet_file.read_row_group(self.row_groups[dataset_row_group_idx].row_group_idx)

    def num_files(self):
        return len(self.parquet_files)

    def num_row_groups(self):
        return len(self.row_groups)

    def get_row_group_size(self, row_group_idx: int):
        return self.row_groups[row_group_idx].num_rows

    def __len__(self):
        return self.row_groups[-1].dataset_row_start_idx + self.row_groups[-1].num_rows

    def __getitem__(self, idx: int):
        if idx < 0 or idx >= len(self):
            raise ValueError(f"Cannot get dataset row with out of bounds index {idx}")
        row_group_idx, tbl_idx = self.get_row_group_and_row_index_from_row(idx)
        tbl = self.materialize_row_group(row_group_idx)
        return tbl.to_pylist()[tbl_idx]

    def get_row_group_and_row_index_from_row(self, row: int) -> Tuple[int, int]:
        if row < 0 or row >= len(self):
            raise IndexError(f"Cannot get row group for dataset row with out of bounds index {row}")
        row_group_idx = bisect.bisect_right([rg.dataset_row_start_idx for rg in self.row_groups], row) - 1
        tbl_idx = row - self.row_groups[row_group_idx].dataset_row_start_idx
        return row_group_idx, tbl_idx

    def get_dataset_index_from_row_group_and_row(self, row_group: int, row_idx: int) -> int:
        return self.row_groups[row_group].dataset_row_start_idx + row_idx
