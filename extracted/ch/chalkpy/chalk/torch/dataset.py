from __future__ import annotations

import datetime

import numpy as np

try:
    import torch
except ModuleNotFoundError:

    class ChalkTorchMapDatasetFromRevision:
        ...

    class ChalkTorchIterDatasetFromRevision:
        ...

else:

    from datetime import timedelta
    from typing import Collection, List, Mapping, Optional, Tuple

    try:
        from typing import override  # pyright: ignore[reportAttributeAccessIssue]
    except (ImportError, AttributeError):
        from typing_extensions import override

    import torch.utils.data

    from chalk.client.dataset import DatasetRevision
    from chalk.client.parquet_file_collection import (
        ParquetFileCollection,
        ParquetRowGroupMetadata,
        parquet_file_from_uri,
    )

    class ChalkTorchIterDatasetFromRevision(torch.utils.data.IterableDataset):  # pyright: ignore[reportRedeclaration]
        def __init__(
            self,
            revision: DatasetRevision,
            columns: Mapping[str, str] | Collection[str] | None = None,
            *,
            download_attempts_per_uri: int = 2,
            materialized_table_cache_size: int = 1,
            shuffle_chunks: bool = False,
            shuffle_rows: bool = False,
            generator: Optional[torch.Generator] = None,
        ):
            super().__init__()
            self.revision = revision
            self._parquet_file_collection: Optional[ParquetFileCollection] = None
            if download_attempts_per_uri <= 0:
                raise ValueError("Must set download attempts to positive integer")
            self.download_attempts_per_uri = download_attempts_per_uri
            self.materialized_table_cache_size = materialized_table_cache_size
            if columns is None:
                self.column_mapping = None
            elif isinstance(columns, Mapping) and all(
                isinstance(k, str) and isinstance(v, str)  # pyright: ignore[reportUnnecessaryIsInstance]
                for k, v in columns.items()
            ):
                self.column_mapping = columns
            elif isinstance(columns, Collection) and all(  # pyright: ignore[reportUnnecessaryIsInstance]
                isinstance(c, str) for c in columns  # pyright: ignore[reportUnnecessaryIsInstance]
            ):
                self.column_mapping = {col: col for col in columns}
            else:
                raise ValueError(
                    f'Failed to create torch dataset from Chalk dataset due to invalid columns mapping. "columns" argument for torch dataset should be None, collection of strings, or mapping from strings to strings, but "columns" was {columns}'
                )

            schema = self.revision.arrow_schema()
            for col in self.column_mapping or {}:
                if schema.get_field_index(col) == -1:
                    raise ValueError(
                        f'Failed to create torch dataset from Chalk dataset due to invalid columns mapping. Column "{col}" was desired as a returned column, but does not exist in the dataset. Dataset\'s columns: {[schema.field(i).name for i in range(len(schema))]}'
                    )

            self.shuffle_chunks = shuffle_chunks
            self.shuffle_rows = shuffle_rows
            self.generator = generator

        @property
        def parquet_file_collection(self) -> ParquetFileCollection:
            if self._parquet_file_collection is None:
                self._hydrate_parquet_files_collection(download_attempts=self.download_attempts_per_uri)
            assert self._parquet_file_collection is not None
            return self._parquet_file_collection

        def get_row_group_size(self, row_group: int):
            if row_group < 0 or row_group >= len(self.parquet_file_collection.row_groups):
                raise IndexError(f"Cannot get size of chunk with out of bounds index {row_group}")
            return self.parquet_file_collection.row_groups[row_group].num_rows

        def _hydrate_parquet_files_collection(
            self,
            *,
            download_attempts: int,
            timeout: float | timedelta | None | ellipsis = ...,
        ):
            for attempt in range(download_attempts):
                try:
                    signed_uris = self.revision.download_uris(
                        show_progress=False,
                        timeout=timeout,
                    )
                    total_rows = 0
                    uris: List[str] = []
                    row_groups: List[ParquetRowGroupMetadata] = []
                    for uri_idx in range(len(signed_uris)):
                        uri = signed_uris[uri_idx]
                        parq_file = parquet_file_from_uri(uri)
                        if parq_file.metadata.num_rows == 0:
                            # For simplicity, we ignore tables with 0 rows, if any exist
                            continue
                        uris.append(uri)
                        for row_group_idx in range(parq_file.num_row_groups):
                            row_group_num_rows = parq_file.metadata.row_group(row_group_idx).num_rows
                            row_groups.append(
                                ParquetRowGroupMetadata(
                                    file_idx=uri_idx,
                                    row_group_idx=row_group_idx,
                                    num_rows=row_group_num_rows,
                                    dataset_row_start_idx=total_rows,
                                )
                            )
                            total_rows += row_group_num_rows
                    self._parquet_file_collection = ParquetFileCollection(
                        parquet_files=uris,
                        row_groups=row_groups,
                        materialized_table_cache_size=self.materialized_table_cache_size,
                    )
                except:
                    if attempt >= download_attempts - 1:
                        raise
                else:
                    return

        def get_row_group_and_row_index_from_row(self, row: int) -> Tuple[int, int]:
            return self.parquet_file_collection.get_row_group_and_row_index_from_row(row)

        def get_dataset_index_from_row_group_and_row(self, row_group: int, row_idx: int) -> int:
            return self.parquet_file_collection.get_dataset_index_from_row_group_and_row(row_group, row_idx)

        def __len__(self):
            return len(self.parquet_file_collection)

        @override
        def __iter__(self):
            if self.generator is None:
                seed = int(torch.empty((), dtype=torch.int64).random_().item())
                generator = torch.Generator()
                generator.manual_seed(seed)
            else:
                generator = self.generator

            if self.shuffle_chunks:
                chunk_index_iterator = torch.randperm(
                    self.parquet_file_collection.num_row_groups(), generator=generator
                )
            else:
                chunk_index_iterator = torch.arange(self.parquet_file_collection.num_row_groups())

            for chunk_tensor_idx in chunk_index_iterator:
                chunk_idx = int(chunk_tensor_idx)
                chunk_size = self.parquet_file_collection.get_row_group_size(chunk_idx)
                if self.shuffle_rows:
                    row_index_iterator = torch.randperm(chunk_size, generator=generator)
                else:
                    row_index_iterator = torch.arange(chunk_size)
                for row_tensor_idx in row_index_iterator:
                    row_idx = int(row_tensor_idx)
                    dataset_row_idx = self.parquet_file_collection.get_dataset_index_from_row_group_and_row(
                        chunk_idx, row_idx
                    )
                    row = self.parquet_file_collection[dataset_row_idx]
                    parsed_row = {}
                    for name, value in row.items():
                        if self.column_mapping is not None and name not in self.column_mapping:
                            continue
                        if self.column_mapping is not None:
                            name = self.column_mapping[name]
                        if isinstance(value, (datetime.datetime, datetime.time, datetime.date)):
                            value = value.isoformat()
                        if isinstance(value, list):
                            value = np.array(value)
                        parsed_row[name] = value
                    yield parsed_row

    class ChalkTorchMapDatasetFromRevision(torch.utils.data.Dataset):  # pyright: ignore[reportRedeclaration]
        """
        PyTorch Dataset wrapper for Chalk dataset revisions.
        Not intended to be used directly. Instead, use Dataset.create_pytorch_dataset(...)
        """

        def __init__(
            self,
            revision: DatasetRevision,
            columns: Mapping[str, str] | Collection[str] | None = None,
        ):
            super().__init__()
            self.revision = revision
            if columns is None:
                self.column_mapping = None
            elif isinstance(columns, Mapping) and all(
                isinstance(k, str) and isinstance(v, str)  # pyright: ignore[reportUnnecessaryIsInstance]
                for k, v in columns.items()
            ):
                self.column_mapping = columns
            elif isinstance(columns, Collection) and all(  # pyright: ignore[reportUnnecessaryIsInstance]
                isinstance(c, str) for c in columns  # pyright: ignore[reportUnnecessaryIsInstance]
            ):
                self.column_mapping = {col: col for col in columns}
            else:
                raise ValueError(
                    f'Failed to create torch dataset from Chalk dataset due to invalid columns mapping. "columns" argument for torch dataset should be None, collection of strings, or mapping from strings to strings, but "columns" was {columns}'
                )

            table = self.revision.to_arrow(show_progress=False)

            schema = table.schema
            for col in self.column_mapping or {}:
                if schema.get_field_index(col) == -1:
                    raise ValueError(
                        f'Failed to create torch dataset from Chalk dataset due to invalid columns mapping. Column "{col}" was desired as a returned column, but does not exist in the dataset. Dataset\'s columns: {[schema.field(i).name for i in range(len(schema))]}'
                    )

            if self.column_mapping is not None:
                table = table.select(self.column_mapping.keys())
                table = table.rename_columns(self.column_mapping)

            self.list_of_rows = table.to_pylist()

        def __len__(self):
            return len(self.list_of_rows)

        @override
        def __getitem__(self, idx: int):
            row = self.list_of_rows[idx]
            parsed_row = {}
            for name, value in row.items():
                if isinstance(value, (datetime.datetime, datetime.time, datetime.date)):
                    value = value.isoformat()
                if isinstance(value, list):
                    value = np.array(value)
                parsed_row[name] = value
            return parsed_row
