# Copyright (c) 2025, NVIDIA CORPORATION.
# SPDX-License-Identifier: BSD-3-Clause

import sqlite3
import struct
from pathlib import Path
from typing import BinaryIO, List, Optional, Tuple, Union

from numpy import int8

from megatron.energon.epathlib import EPath


class SqliteIndexWriter:
    sqlite_path: EPath
    db: Optional[sqlite3.Connection]
    duplicates: List[Tuple[str, int]]

    def __init__(self, sqlite_path: EPath):
        """
        Initializes an SQLite database and sets up the samples table:
          - samples(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tar_file_id INTEGER,
                    sample_key TEXT,
                    sample_index INTEGER,
                    byte_offset INTEGER,
                    byte_size INTEGER)
        Also creates an index on samples(sample_key).
        """

        # Final path and temporary path
        self.sqlite_path = sqlite_path

        # Initialize SQLite connection
        path = str(self.sqlite_path)
        # Only supporting local file system, because sqlite does not support remote file systems.
        # TODO: Implement remote file systems. Maybe create locally in tmp then upload?
        assert path.startswith("/"), (
            f"SQLite path must be absolute local file system path: {self.sqlite_path}"
        )
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA busy_timeout = 5000;")  # wait up to 5000ms when locked
        self.db.execute("PRAGMA journal_mode = WAL;")

        # Create the table
        self.db.execute("DROP INDEX IF EXISTS idx_samples_sample_key")
        self.db.execute("DROP TABLE IF EXISTS samples")
        self.db.execute(
            """
            CREATE TABLE samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tar_file_id INTEGER,
                sample_key TEXT,
                sample_index INTEGER,
                byte_offset INTEGER,
                byte_size INTEGER
            )
        """
        )
        # Index on sample_key for fast lookups
        self.db.execute("CREATE INDEX IF NOT EXISTS idx_samples_sample_key ON samples(sample_key)")

        self.duplicates = []

    def append_sample(
        self,
        tar_file_id: int8,
        sample_key: str,
        sample_index: int,
        byte_offset: Optional[int],
        byte_size: Optional[int],
    ):
        """Adds a new sample row to the samples table."""

        assert self.db is not None, "Database is closed"

        # Insert a row in the samples table
        self.db.execute(
            """
            INSERT INTO samples (tar_file_id, sample_key, sample_index, byte_offset, byte_size)
            VALUES (?, ?, ?, ?, ?)
            """,
            (tar_file_id, sample_key, sample_index, byte_offset, byte_size),
        )

    def close(self):
        """
        Closes the DB connection. If finalize=True, the temporary database is
        renamed to the final name, overwriting if necessary.
        """
        assert self.db is not None, "Database is closed"

        # Check if sample_key are all unique
        # self.db.execute("CREATE TEMP TABLE temp AS SELECT sample_key, COUNT(*) AS c FROM samples GROUP BY sample_key HAVING c > 1")
        duplicates = self.db.execute(
            "SELECT sample_key, COUNT(*) AS c FROM samples GROUP BY sample_key HAVING c > 1 LIMIT 5"
        ).fetchall()
        if len(duplicates) > 0:
            self.duplicates = duplicates

        if self.db is not None:
            self.db.commit()
            self.db.close()
            self.db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # If an exception occurred, do not finalize (so you can inspect the temp file)
        self.close()


class JoinIndexWriter:
    """Describes how one primary dataset is joined with multiple secondary datasets.

    For fast random access, this is a binary format that is memory-mapped.
    The first 16 bytes are a header with the number of columns (1 primary + N secondary).
    Each row contains (shard_idx, byte_offset, byte_size) for each column.
    """

    def __init__(self, join_index_path: EPath):
        self.join_index_path = join_index_path
        self.join_index_file = join_index_path.open("wb")
        self.num_columns = None

    def append(self, *columns: Tuple[int, int, int]):
        """Appends a new row to the join index file.

        Each row contains (shard_idx, byte_offset, byte_size) for each column.
        """

        if self.num_columns is None:
            # Write the number of columns
            self.join_index_file.write(b"JIDX0001")  # Magic bytes with version
            self.join_index_file.write(struct.pack("q", len(columns)))
            self.num_columns = len(columns)
        else:
            assert len(columns) == self.num_columns, (
                f"Inconsistent number of keys: Had {self.num_columns} before, got {len(columns)}"
            )

        # Write the columns
        for key in columns:
            assert isinstance(key, tuple) and len(key) == 3
            self.join_index_file.write(struct.pack("qqq", *key))

    def close(self):
        self.join_index_file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class JoinIndexReader:
    """Reads a join index file in different ways.

    If a column is specified, only that column is read, otherwise the full rows.
    You can iterate over the rows, or read a specific row by index, or get the full tensor.

    Each row contains (shard_idx, byte_offset, byte_size) for each column.
    """

    join_index_path: EPath
    join_index_file: BinaryIO
    column: Optional[int]
    num_columns: int
    has_iterated: bool
    index_row_position: int

    def __init__(self, join_index_path: EPath, column: Optional[int] = None):
        self.join_index_path = join_index_path
        self.join_index_byte_size = join_index_path.size()

        self.column = column

        self.join_index_file = join_index_path.open("rb")
        self.has_iterated = False
        self.index_row_position = -1

        # Read the header
        bytes_magic = self.join_index_file.read(8)
        assert isinstance(bytes_magic, bytes)
        assert bytes_magic[:4] == b"JIDX", f"Invalid magic bytes: {bytes_magic}"
        assert bytes_magic[4:8] == b"0001", f"Unsupported version: {bytes_magic[4:8]}"

        # Read the number of columns
        bytes_seckeys = self.join_index_file.read(8)
        assert isinstance(bytes_seckeys, bytes)
        self.num_columns = struct.unpack("q", bytes_seckeys)[0]

        self.index_row_position = 0

    def get_as_tensor(self):
        """Returns the join index as a tensor with shape (N, num_columns, 3)."""

        assert not self.has_iterated, "Cannot get_as_tensor after iterating"

        import torch

        # Read the raw bytes for all N * 3 int64s.
        data = self.join_index_file.read()
        self.index_file_position = self.join_index_file.tell()
        assert len(data) % (8 * 3) == 0, (
            f"Index file reading: Expected multiple of 3 * 8 bytes, got {len(data)} bytes"
        )

        return torch.frombuffer(data, dtype=torch.int64).view(-1, self.num_columns, 3)

    def __len__(self):
        return (self.join_index_byte_size - 16) // (self.num_columns * 8 * 3)

    def __iter__(self):
        return self

    def _read_one_row(
        self, column: Optional[int] = None
    ) -> Union[None, List[Tuple[int, int, int]]]:
        row = []
        for col_idx in range(self.num_columns):
            if column is not None and col_idx != column:
                # Skip this column
                self.join_index_file.seek(8 * 3, 1)
                continue

            bytes_key = self.join_index_file.read(8 * 3)
            if not bytes_key:
                return None
            assert isinstance(bytes_key, bytes)
            key_tuple = struct.unpack("qqq", bytes_key)
            row.append(key_tuple)
        self.index_row_position += 1
        return row

    def __next__(self) -> Union[None, List[Tuple[int, int, int]]]:
        self.has_iterated = True
        return self._read_one_row(column=self.column)

    def tell_row(self) -> int:
        return self.index_row_position

    def __getitem__(self, idx: int) -> List[Tuple[int, int, int]]:
        """Reads the idx-th row of the join index file."""

        assert 0 <= idx < len(self), f"Index out of bounds: {idx} not in [0, {len(self)})"

        # Seek to the correct position

        if self.index_row_position != idx:
            self.join_index_file.seek(16 + idx * self.num_columns * 8 * 3)
            self.index_row_position = idx

        # Read the secondary keys
        row = self._read_one_row(column=self.column)
        assert row is not None, f"Failed to read row {idx}"

        return row

    def close(self):
        self.join_index_file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
