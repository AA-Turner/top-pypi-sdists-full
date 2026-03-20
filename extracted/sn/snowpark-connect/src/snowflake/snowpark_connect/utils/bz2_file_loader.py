#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Utilities for Parallel Processing of BZ2 compressed or uncompressed files

This module provides utilities for loading large BZ2-compressed newline-delimited
files from Snowflake stages with parallel processing support.
"""

import bz2
import io
import json
import logging
import re
from dataclasses import dataclass
from typing import Optional

from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark.files import SnowflakeFile
from snowflake.snowpark.functions import col, lit
from snowflake.snowpark.types import (
    BooleanType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    VariantType,
)

# =============================================================================
# Core Streaming Components
# =============================================================================

LINE_CONTENT = "line_content"
VALUE_COLUMN = "value"
FILE_SPLITS_GENERATOR_NAME = "FILE_SPLITS_GENERATOR"
JSON_PARALLEL_LOADER_NAME = "JSON_PARALLEL_LOADER"


@dataclass
class FileSplit:
    """Represents a file split for downloading a file chunk."""

    split_size_bytes: int
    part_number: int
    start: int


FILE_SPLITS_GENERATOR_OUTPUT_SCHEMA = StructType(
    [
        StructField("split_size_bytes", LongType()),
        StructField("part_number", IntegerType()),
        StructField("start_byte", LongType()),
    ]
)


JSON_PARALLEL_LOADER_OUTPUT_SCHEMA = StructType(
    [
        StructField("line_number", IntegerType()),
        StructField(LINE_CONTENT, VariantType()),
    ]
)


def calculate_byte_ranges(
    file_size: int,
    split_size_bytes: int,
) -> list[FileSplit]:
    """
    Calculate byte ranges for splitting a file into chunks.

    Args:
        file_size: The size of the file in bytes.
        split_size_bytes: The size of each split in bytes.

    Returns:
        A list of FileSplit objects.
    """
    ranges = []
    part_number = 0
    start = 0
    while start < file_size:
        ranges.append(
            FileSplit(
                split_size_bytes=split_size_bytes,
                part_number=part_number,
                start=start,
            )
        )
        start = start + split_size_bytes
        part_number += 1
    return ranges


def register_byte_range_generator_udtf(
    session, name: str = FILE_SPLITS_GENERATOR_NAME
) -> None:
    """Register the ByteRangeGeneratorUDTF with a Snowflake session."""

    # Define UDTF class inline to avoid module dependency issues
    @dataclass
    class FileSplit:
        """Represents a byte range for downloading a file chunk."""

        split_size_bytes: int
        part_number: int
        start: int

    def calculate_byte_ranges(
        file_size: int,
        split_size_bytes: int,
    ) -> list[FileSplit]:
        """
        Calculate byte ranges for splitting a file into chunks.

        Args:
            file_size: The size of the file in bytes.
            split_size_bytes: The size of each split in bytes.
        Returns:
            A list of ByteRange objects.
        """
        ranges = []
        part_number = 0
        start = 0
        while start < file_size:
            ranges.append(
                FileSplit(
                    split_size_bytes=split_size_bytes,
                    part_number=part_number,
                    start=start,
                )
            )
            start = start + split_size_bytes
            part_number += 1
        return ranges

    class FileSplitsGeneratorUDTF:
        """
        Snowflake UDTF that generates byte ranges for parallel processing of large files.

        This UDTF takes a file path (scoped URL) on a Snowflake stage, determines its size,
        and generates byte ranges that can be used for parallel processing.

        Usage in SQL:
            SELECT * FROM TABLE(
                byte_range_generator(
                    BUILD_SCOPED_FILE_URL(@my_stage, 'path/to/file.bz2'),
                    2097152,  -- split_size_bytes (2MB)
                )
            );

        Returns:
            A table with columns:
            - split_size_bytes: The logical split size (before padding)
            - part_number: The partition/split number (0-indexed)
            - start_byte: The starting byte offset for this range
        """

        def __init__(self) -> None:
            self._logger = logging.getLogger(self.__class__.__name__)

        def process(
            self,
            file_path: str,
            split_size_bytes: int,
        ):
            """
            Process a file and yield byte ranges.

            Args:
                file_path: Scoped URL or stage path to the file
                split_size_bytes: Size of each logical split in bytes

            Yields:
                Tuples of (split_size_bytes, part_number, start_byte)
            """
            # Open the file to get its size
            with SnowflakeFile.open(file_path, "rb") as f:
                # Seek to end to get file size
                f.seek(0, 2)  # SEEK_END
                file_size = f.tell()

            # Generate byte ranges
            file_splits = calculate_byte_ranges(
                file_size=file_size,
                split_size_bytes=split_size_bytes,
            )

            # Yield each byte range as a row
            for split in file_splits:
                self._logger.debug(
                    f"Generated file split {split.part_number} of size {split.split_size_bytes} starting at {split.start}"
                )
                yield split.split_size_bytes, split.part_number, split.start

        def end_partition(self):
            """Called at the end of each partition. No cleanup needed."""
            pass

    session.udtf.register(
        FileSplitsGeneratorUDTF,
        output_schema=FILE_SPLITS_GENERATOR_OUTPUT_SCHEMA,
        input_types=[StringType(), LongType()],
        name=name,
        is_permanent=False,
        replace=True,
        packages=["snowflake-snowpark-python"],
    )


def register_bz2_file_processor_udtf(
    session, name: str = JSON_PARALLEL_LOADER_NAME
) -> None:
    """Register the BZ2FileProcessorUDTF with a Snowflake session."""

    class BaseUDTFFileStream(io.RawIOBase):
        """Base class for all File streams used in ingestion UDTFs"""

        def __init__(self, split_size_bytes: int, part_number: int) -> None:
            self._eof = False
            self._split_size_bytes = split_size_bytes
            self._part_number = part_number

        @property
        def split_size(self) -> int:
            return self._split_size_bytes

        @property
        def part_number(self) -> int:
            return self._part_number

        def is_first_split(self) -> bool:
            """Return True if this is the first split (part_number == 0)."""
            return self._part_number == 0

        def readable(self) -> bool:
            """Return True - this stream is readable."""
            return True

    # Define UDTF class inline to avoid module dependency issues
    class SnowflakeFileSplitStream(BaseUDTFFileStream):
        """
        A streaming file-like object that reads a byte range from a Snowflake staged file.
        This class wraps a SnowflakeFile and provides a bounded view of the file from
        'start' to 'end' byte offsets. It streams data directly without loading the
        entire range into memory, making it suitable for large byte ranges (>250MB).
        The stream returns EOF when it has read up to the 'end' offset.

        Usage:
            byte_range = ByteRange(start=0, end=1048575, part_number=0, split_size_bytes=1048576)
            with SnowflakeFileByteRangeStream(file_url, byte_range) as stream:
                while chunk := stream.read(8192):
                    process(chunk)
        """

        def __init__(
            self, file_url: str, split_size_bytes: int, part_number: int, start_pos: int
        ) -> None:
            """
            Initialize the streaming byte range reader.

            Args:
                file_url: Scoped URL or stage path to the Snowflake filex
                byte_range: ByteRange object specifying start, end, and metadata
            """
            super().__init__(split_size_bytes, part_number)
            # Open the file and seek to start position - keep it open for streaming
            self._file = SnowflakeFile.open(file_url, "rb")
            self._file.seek(start_pos)

        def readinto(self, b) -> Optional[int]:
            """
            Read bytes into a pre-allocated buffer.
            Reads up to len(b) bytes, but will not read past the 'stop' offset.
            Returns 0 when EOF is reached (i.e., when 'stop' offset is reached).

            Args:
                b: A writable buffer (e.g., bytearray or memoryview)

            Returns:
                Number of bytes read, or 0 if EOF
            """
            if self._eof:
                return 0

            if self.closed:
                raise ValueError("I/O operation on closed stream")

            n = self._file.readinto(b)
            if n == 0:
                self._eof = True
            return n

        def close(self) -> None:
            """Close the stream and release the underlying file handle."""
            if not self.closed:
                if self._file is not None:
                    self._file.close()
                    self._file = None
                super().close()

    class BZ2DecompressingStream(BaseUDTFFileStream):
        """
        BZ2 split re-syncing raw stream. Skips partial compression block at the start of the split, unless it is the first split.

        - First split starts immediately
        - Non-first splits resync to next block boundary to get the complete block
        - Produces valid decompressed data only
        - Forward-only
        """

        def __init__(
            self,
            raw_stream: SnowflakeFileSplitStream,
            read_size: int = io.DEFAULT_BUFFER_SIZE,
        ) -> None:
            super().__init__(raw_stream.split_size, raw_stream.part_number)
            self.raw = raw_stream
            self.read_size = read_size
            self._compressed_bytes_read = 0
            self._decompressor = bz2.BZ2Decompressor()
            self._buffer = bytearray()
            self._eof = False
            self._re_synced = raw_stream.is_first_split()
            # For compressed streams, we should stop only after finishing the first
            # BZ2 block that crosses split boundary, not immediately after crossing it.
            self.is_reading_past_split_boundary = False
            self.num_reads_past_split_boundary = 0

        def seekable(self):
            return False

        def decompress_block(self, data: memoryview) -> bytes | None:
            try:
                out = self._decompressor.decompress(data)
                self._compressed_bytes_read += len(data)
                if out:
                    if self._decompressor.eof:
                        if self._decompressor.unused_data:
                            self._compressed_bytes_read -= len(
                                self._decompressor.unused_data
                            )
                        # Decompression expands data, so split ownership for compressed files must be tracked in terms
                        # of compressed-byte offsets.
                        # To avoid dropping records while crossing split boundaries, we only stop after completely
                        # consuming the first compression block that straddles the split boundary + one last, additional
                        # record (i.e. line) that straddles the split straddling BZ2 compressed block's boundary
                        # This state machine is tracked using two instance variables
                        #   - is_reading_past_split_boundary: Which turns on when split boundary crossing is detected
                        #       using BZ2 compression block's EOF being reached in the new split
                        #   - num_reads_past_split_boundary: Which starts counting reads *after*
                        #       is_reading_past_split_boundary is turned on
                        if self._compressed_bytes_read > self._split_size_bytes:
                            self.is_reading_past_split_boundary = True
                return out
            except OSError:
                # Invalid BZ2 stream start, reset the decompressor
                self._decompressor = bz2.BZ2Decompressor()
                return None

        def _resync(self):
            bz2_header_pattern = re.compile(b"BZh[1-9]")
            # size of chunk to read & try to decompress after the BZ2 header to see if it's a start of valid BZ2 stream
            chunk_size = 64 * 1024
            # Boundary upto which we will search for a valid BZ2 stream start in this file split.
            # Add 3 to cover the case where BZ2 stream header's (BZh[1-9]) first byte appears at the end of the split.
            search_limit = self.split_size + 3
            # Add CHUNK_SIZE past the +3 boundary to read compressed buffer to probe for valid BZ2 block
            read_buffer = bytearray(search_limit + chunk_size)

            n = self.raw.readinto(read_buffer)
            if n == 0:
                self._eof = True
                return False

            for m in bz2_header_pattern.finditer(read_buffer):
                offset = m.start()
                if offset > self.split_size:
                    # No valid BZ2 stream start in this file split
                    self._eof = True
                    return False

                self._compressed_bytes_read = offset
                data = memoryview(read_buffer)[offset:n]
                out = self.decompress_block(data)
                if out is not None:
                    self._buffer.extend(out)
                    self._re_synced = True
                    return True
                else:
                    # Not a real BZ2 stream start, ignore and skip ahead
                    pass

            self._eof = True
            return False

        def readinto(self, b):
            while len(self._buffer) <= 0:
                if self._eof:
                    return 0

                # Once split ownership has crossed the boundary, stop only after draining all the already decompressed
                # buffered data + 1 additional record (line) that is straddling the compression block's boundary
                if self.is_reading_past_split_boundary:
                    self.num_reads_past_split_boundary += 1

                if not self._re_synced:
                    if not self._resync():
                        return 0

                chunk = None

                if self._decompressor.unused_data:
                    # Decompressor has extra data beyond the block that still needs to be decompressed.
                    chunk = self._decompressor.unused_data
                    self._decompressor = bz2.BZ2Decompressor()

                if self._decompressor.eof:
                    self._decompressor = bz2.BZ2Decompressor()

                if not chunk:
                    n = self.raw.readinto(b)
                    if n == 0:
                        self._eof = True
                        return 0
                    chunk = memoryview(b)[:n]

                out = self.decompress_block(chunk)
                if out:
                    self._buffer.extend(out)

            n = min(len(b), len(self._buffer))
            b[:n] = self._buffer[:n]
            del self._buffer[:n]
            return n

        def close(self) -> None:
            """Close the stream and release the underlying file handle."""
            if not self.closed:
                if self.raw is not None:
                    self.raw.close()
                    self.raw = None
                super().close()

    class JsonFileProcessorUDTF:
        """
        Snowflake UDTF that processes a byte range from a BZ2-compressed or uncompressed file and yields each line as a
        variant row.

        This UDTF is designed to be used with FileSplitsGeneratorUDTF. It takes the file split
        information and processes the compressed or uncompressed data, handling:
        - BZ2 compression block boundaries (resyncs to valid block starts), if any
        - Newline-delimited record boundaries (handles records spanning blocks)
        - Parallel processing (each split processes its owned records)

        Internally uses the chain:
            SnowflakeFileSplitStream → BZ2DecompressingStream → LineReader

        Usage in SQL (chained with FileSplitsGeneratorUDTF):
            -- First get byte ranges, then process each range in parallel
            WITH file_splits AS (
                SELECT * FROM TABLE(
                    FILE_SPLITS_GENERATOR(
                        BUILD_SCOPED_FILE_URL(@my_stage, 'data.jsonl.bz2'),
                        2097152,  -- split_size_bytes (2MB)
                    )
                )
            )
            SELECT
                fs.part_number,
                records.line_number,
                records.line_content
            FROM file_splits fs,
            TABLE(
                JSON_PARALLEL_LOADER(
                    BUILD_SCOPED_FILE_URL(@my_stage, 'data.jsonl.bz2'),
                    fs.split_size_bytes,
                    fs.part_number,
                    fs.start_byte,
                    mode,
                    compressed,
                    encoding
                ) OVER (PARTITION BY fs.part_number)
            ) records;

        Returns:
            A table with columns:
            - line_number: The line number within this split (1-indexed)
            - line_content: The content of the line as a VARIANT
        """

        def __init__(self) -> None:
            self._logger = logging.getLogger(self.__class__.__name__)

        def sanitize_for_utf8(self, obj):
            """Recursively ensure all strings are valid UTF-8 encodable."""
            if isinstance(obj, str):
                # Fast path: try encoding (most strings are fine)
                try:
                    obj.encode("utf-8")
                    return obj
                except UnicodeEncodeError:
                    # Only slow path if needed
                    return obj.encode("utf-8", "replace").decode("utf-8")
            elif isinstance(obj, dict):
                return {
                    self.sanitize_for_utf8(k): self.sanitize_for_utf8(v)
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [self.sanitize_for_utf8(x) for x in obj]
            return obj

        def process(
            self,
            file_url: str,
            split_size_bytes: int,
            part_number: int,
            start_byte: int,
            mode: str,
            compressed: bool,
            encoding: str,
        ):
            """H
            Process a byte range and yield each line as a record.

            Args:
                file_url: Scoped URL or stage path to the file
                split_size_bytes: The logical split size
                part_number: The partition/split number (0-indexed)
                start_byte: Starting byte offset for this range
                mode: PERMISSIVE or FAILFAST (for parsing)
                compressed: Is the file BZ2 compressed?
                encoding: Character encoding used to decode bytes

            Yields:
                Tuples of (line_number, line_content)
            """

            # Build the streaming chain:
            # 1: Raw byte range stream from Snowflake file
            raw_stream = SnowflakeFileSplitStream(
                file_url, split_size_bytes, part_number, start_byte
            )

            # 2: BZ2 decompression with block resync
            decompressed_stream = (
                BZ2DecompressingStream(raw_stream) if compressed else raw_stream
            )

            # 3: Wrap in BufferedReader for efficient line reading
            buffered_stream = io.BufferedReader(decompressed_stream)

            bytes_read = 0
            line_number = 0
            # Except for the very first split, always skip the first line as it could be partial record
            start_consuming_records = decompressed_stream.is_first_split()
            try:
                # Read and yield each line
                for line_bytes in buffered_stream:
                    bytes_read += len(line_bytes)
                    if start_consuming_records:
                        line_number += 1
                        try:
                            # Decode bytes to string, strip trailing newline
                            line_content = line_bytes.decode(
                                encoding, errors="replace"
                            ).rstrip("\n\r")
                            value = self.sanitize_for_utf8(json.loads(line_content))
                            yield line_number, value
                        except (json.JSONDecodeError, UnicodeDecodeError) as e:
                            record = line_bytes[:1024]
                            self._logger.warning("Error parsing line: %s", record)
                            if mode.lower() == "failfast":
                                raise ValueError(f"Error parsing line: {record}") from e
                    else:
                        # We have skipped past the first line in the split
                        start_consuming_records = True

                    if not compressed and bytes_read > split_size_bytes:
                        # Uncompressed file case:
                        # We finished reading the record (line) that is straddling the split boundary
                        self._logger.debug(
                            f"Part {part_number} emitted {line_number} records"
                        )
                        return

                    if (
                        compressed
                        and decompressed_stream.num_reads_past_split_boundary > 0
                    ):
                        # Compressed file case:
                        # We finished reading  the record straddling the BZ2 compress block boundary for the BZ2 block
                        # that itself straddled the split boundary
                        self._logger.debug(
                            f"Part {part_number} emitted {line_number} records"
                        )
                        return
            finally:
                buffered_stream.close()

        def end_partition(self):
            """Called at the end of each partition. Reset line counter."""
            pass

    session.udtf.register(
        JsonFileProcessorUDTF,
        output_schema=JSON_PARALLEL_LOADER_OUTPUT_SCHEMA,
        input_types=[
            StringType(),
            LongType(),
            IntegerType(),
            LongType(),
            StringType(),
            BooleanType(),
            StringType(),
        ],
        name=name,
        is_permanent=False,
        replace=True,
        packages=["snowflake-snowpark-python"],
    )


def register_all_bz2_udtfs(session: Session) -> None:
    """Register all BZ2-related UDTFs with a Snowflake session."""
    register_byte_range_generator_udtf(session)
    register_bz2_file_processor_udtf(session)


# =============================================================================
# High-Level API
# =============================================================================


def load_bz2_file(
    session: Session,
    stage: str,
    file_path: str,
    split_size_mb: int = 200,
    auto_register_udtfs: bool = True,
    mode: str = "PERMISSIVE",
    compressed: bool = True,
    encoding: str = "utf-8",
) -> DataFrame:
    """
    Load a large BZ2-compressed or uncompressed newline-delimited file from a Snowflake stage.

    Args:
        session: Active Snowpark Session
        stage: Snowflake stage name (e.g., "@my_stage")
        file_path: Path to the file within the stage
        split_size_mb: Size of each split in MB (default: 200MB)
        auto_register_udtfs: Whether to automatically register UDTFs (default: True)
        mode: set to "FAILFAST" to throw error if any record is malformed (default: PERMISSIVE)
        compressed: Whether the file to load is compressed or not
        encoding: Character encoding used to decode file bytes (default: utf-8)

    Returns:
        DataFrame with columns: split_size_bytes, part_number, start_byte, line_number, line_content
    """
    if auto_register_udtfs:
        register_all_bz2_udtfs(session)

    split_size_bytes = split_size_mb * 1024 * 1024

    if not stage.startswith("@"):
        stage = f"@{stage}"

    scoped_url_df = session.sql(
        f"""
        SELECT
            BUILD_SCOPED_FILE_URL(
                '{stage}',
                '{file_path}'
            ) AS file_url
    """
    )

    byte_ranges_df = scoped_url_df.join_table_function(
        FILE_SPLITS_GENERATOR_NAME,
        col("file_url"),
        lit(split_size_bytes),
    ).cache_result()

    from snowflake.snowpark.functions import table_function

    bz2_processor_udtf = table_function(JSON_PARALLEL_LOADER_NAME)
    udtf_call = bz2_processor_udtf(
        col("file_url"),
        col("split_size_bytes"),
        col("part_number"),
        col("start_byte"),
        lit(mode),
        lit(compressed),
        lit(encoding),
    )  # .over(partition_by="part_number")

    result_df = byte_ranges_df.join_table_function(udtf_call)
    return result_df


# TODO: Do we need this?
def load_bz2_file_to_table(
    session: Session,
    stage: str,
    file_path: str,
    target_table: str,
    split_size_mb: int = 200,
    mode: str = "overwrite",
    auto_register_udtfs: bool = True,
    compressed: bool = True,
) -> None:
    """
    Load a large BZ2-compressed file from a Snowflake stage directly into a table.

    Args:
        session: Active Snowpark Session
        stage: Snowflake stage name
        file_path: Path to the file within the stage
        target_table: Name of the target table
        split_size_mb: Size of each split in MB (default: 200MB)
        additional_padding_mb: Additional padding in MB (default: 2MB)
        mode: Write mode - "overwrite", "append", "errorifexists", "ignore"
        auto_register_udtfs: Whether to automatically register UDTFs (default: True)
    """
    df = load_bz2_file(
        session=session,
        stage=stage,
        file_path=file_path,
        split_size_mb=split_size_mb,
        auto_register_udtfs=auto_register_udtfs,
        compressed=compressed,
    )

    df.write.mode(mode).save_as_table(target_table)
