#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
BZ2 file loading utilities for Snowflake stages.

This module provides utilities for loading large BZ2-compressed newline-delimited
files from Snowflake stages with parallel processing support.
"""

import bz2
import io
import json
from dataclasses import dataclass
from typing import Optional

from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark.files import SnowflakeFile
from snowflake.snowpark.functions import col, lit
from snowflake.snowpark.types import (
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    VariantType,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

# =============================================================================
# Core Streaming Components
# =============================================================================

# BZ2 block magic marker used for resyncing
BZ2_BLOCK_MAGIC_MARKER = b"\x31\x41\x59\x26\x53\x59"
LINE_CONTENT = "line_content"


@dataclass
class ByteRange:
    """Represents a byte range for downloading a file chunk."""

    start: int
    end: int
    part_number: int
    split_size_bytes: int

    @property
    def size(self) -> int:
        return self.end - self.start + 1

    def to_range_header(self) -> str:
        """Convert to HTTP Range header format."""
        return f"bytes={self.start}-{self.end}"


BYTE_RANGE_GENERATOR_OUTPUT_SCHEMA = StructType(
    [
        StructField("part_number", IntegerType()),
        StructField("start_byte", LongType()),
        StructField("end_byte", LongType()),
        StructField("split_size_bytes", LongType()),
        StructField("file_size", LongType()),
    ]
)


BZ2_FILE_PROCESSOR_OUTPUT_SCHEMA = StructType(
    [
        StructField("line_number", IntegerType()),
        StructField(LINE_CONTENT, VariantType()),
    ]
)


def calculate_byte_ranges(
    file_size: int,
    split_size_bytes: int,
    additional_padding_bytes_at_end: int = 2 * 1024 * 1024,  # 2MB for BZ2 compression
) -> list[ByteRange]:
    """
    Calculate byte ranges for splitting a file into chunks.

    Args:
        file_size: The size of the file in bytes.
        split_size_bytes: The size of each split in bytes.
        additional_padding_bytes_at_end: Number of additional bytes to download beyond the split size, to ensure
            that we get complete compression block that was started in this split but did not fit fully in the split.
            We need to download complete compression block that started in this split because BZ2 compression blocks
            cannot be decompressed until the complete block is available, so next split can't decompress partial block at its start.
            The split in which the compression block starts is the owner of that block, and hence needs to get the complete block
            even if it goes beyond the split boundary.
            Same is true for new line delimited records that are inside the compression block. The new line delimited record
            can similarly stradle the compresison block boundary, and we cannot parse partial recode. So we need to not only go
            beyond the split size to get the complete compresion block but after decompressing that block, we need to get the
            complete last record that started in that block but did not finish. So we may now need to get the following compresison
            block too. This next block will be completely contained in the next split, but will contain partial record from the
            previous compresison block at its start.
            So in total we need to download Byte range that covers original split size + (2 * max compression block size) - 1MB for BZ2
            compression - in total.
            This means after first split, there will be overlap in byte ranges at the end of previous split and the start of the next split.

    Returns:
        A list of ByteRange objects.
    """
    ranges = []
    part_number = 0
    start = 0

    while start < file_size:
        end = min(
            start + split_size_bytes + additional_padding_bytes_at_end - 1,
            file_size - 1,
        )
        ranges.append(
            ByteRange(
                start=start,
                end=end,
                part_number=part_number,
                split_size_bytes=split_size_bytes,
            )
        )
        start = start + split_size_bytes
        part_number += 1
    return ranges


def register_byte_range_generator_udtf(
    session, name: str = "byte_range_generator"
) -> None:
    """Register the ByteRangeGeneratorUDTF with a Snowflake session."""

    # Define UDTF class inline to avoid module dependency issues
    @dataclass
    class ByteRange:
        """Represents a byte range for downloading a file chunk."""

        start: int
        end: int
        part_number: int
        split_size_bytes: int

        @property
        def size(self) -> int:
            return self.end - self.start + 1

        def to_range_header(self) -> str:
            """Convert to HTTP Range header format."""
            return f"bytes={self.start}-{self.end}"

    def calculate_byte_ranges(
        file_size: int,
        split_size_bytes: int,
        additional_padding_bytes_at_end: int = 2
        * 1024
        * 1024,  # 2MB for BZ2 compression
    ) -> list[ByteRange]:
        """
        Calculate byte ranges for splitting a file into chunks.

        Args:
            file_size: The size of the file in bytes.
            split_size_bytes: The size of each split in bytes.
            additional_padding_bytes_at_end: Number of additional bytes to download beyond the split size, to ensure
                that we get complete compression block that was started in this split but did not fit fully in the split.
                We need to download complete compression block that started in this split because BZ2 compression blocks
                cannot be decompressed until the complete block is available, so next split can't decompress partial block at its start.
                The split in which the compression block starts is the owner of that block, and hence needs to get the complete block
                even if it goes beyond the split boundary.
                Same is true for new line delimited records that are inside the compression block. The new line delimited record
                can similarly stradle the compresison block boundary, and we cannot parse partial recode. So we need to not only go
                beyond the split size to get the complete compresion block but after decompressing that block, we need to get the
                complete last record that started in that block but did not finish. So we may now need to get the following compresison
                block too. This next block will be completely contained in the next split, but will contain partial record from the
                previous compresison block at its start.
                So in total we need to download Byte range that covers original split size + (2 * max compression block size) - 1MB for BZ2
                compression - in total.
                This means after first split, there will be overlap in byte ranges at the end of previous split and the start of the next split.

        Returns:
            A list of ByteRange objects.
        """
        ranges = []
        part_number = 0
        start = 0

        while start < file_size:
            end = min(
                start + split_size_bytes + additional_padding_bytes_at_end - 1,
                file_size - 1,
            )
            ranges.append(
                ByteRange(
                    start=start,
                    end=end,
                    part_number=part_number,
                    split_size_bytes=split_size_bytes,
                )
            )
            start = start + split_size_bytes
            part_number += 1
        return ranges

    class ByteRangeGeneratorUDTF:
        """
        Snowflake UDTF that generates byte ranges for parallel processing of large files.

        This UDTF takes a file path (scoped URL) on a Snowflake stage, determines its size,
        and generates byte ranges that can be used for parallel processing.

        Usage in SQL:
            SELECT * FROM TABLE(
                byte_range_generator(
                    BUILD_SCOPED_FILE_URL(@my_stage, 'path/to/file.bz2'),
                    2097152,  -- split_size_bytes (2MB)
                    2097152   -- additional_padding_bytes (2MB)
                )
            );

        Returns:
            A table with columns:
            - part_number: The partition/split number (0-indexed)
            - start_byte: The starting byte offset for this range
            - end_byte: The ending byte offset for this range (inclusive)
            - split_size_bytes: The logical split size (before padding)
            - file_size: Total size of the file in bytes
        """

        def __init__(self) -> None:
            pass

        def process(
            self,
            file_path: str,
            split_size_bytes: int,
            additional_padding_bytes_at_end: int = 2 * 1024 * 1024,
        ):
            """
            Process a file and yield byte ranges.

            Args:
                file_path: Scoped URL or stage path to the file
                split_size_bytes: Size of each logical split in bytes
                additional_padding_bytes_at_end: Extra bytes to read beyond split boundary
                    for handling compressed blocks that straddle boundaries

            Yields:
                Tuples of (part_number, start_byte, end_byte, split_size_bytes, file_size)
            """
            # Open the file to get its size
            with SnowflakeFile.open(file_path, "rb") as f:
                # Seek to end to get file size
                f.seek(0, 2)  # SEEK_END
                file_size = f.tell()

            # Generate byte ranges
            byte_ranges = calculate_byte_ranges(
                file_size=file_size,
                split_size_bytes=split_size_bytes,
                additional_padding_bytes_at_end=additional_padding_bytes_at_end,
            )

            # Yield each byte range as a row
            for br in byte_ranges:
                yield (br.part_number, br.start, br.end, br.split_size_bytes, file_size)

        def end_partition(self):
            """Called at the end of each partition. No cleanup needed."""
            pass

    session.udtf.register(
        ByteRangeGeneratorUDTF,
        output_schema=BYTE_RANGE_GENERATOR_OUTPUT_SCHEMA,
        input_types=[StringType(), LongType(), LongType()],
        name=name,
        is_permanent=False,
        replace=True,
        packages=["snowflake-snowpark-python"],
    )


def register_bz2_file_processor_udtf(session, name: str = "bz2_file_processor") -> None:
    """Register the BZ2FileProcessorUDTF with a Snowflake session."""

    # Define UDTF class inline to avoid module dependency issues
    # Same
    @dataclass
    class ByteRange:
        """Represents a byte range for downloading a file chunk."""

        start: int
        end: int
        part_number: int
        split_size_bytes: int

        @property
        def size(self) -> int:
            return self.end - self.start + 1

        def to_range_header(self) -> str:
            """Convert to HTTP Range header format."""
            return f"bytes={self.start}-{self.end}"

    class SnowflakeFileByteRangeStream(io.RawIOBase):
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

        def __init__(self, file_url: str, byte_range: ByteRange) -> None:
            """
            Initialize the streaming byte range reader.

            Args:
                file_url: Scoped URL or stage path to the Snowflake filex
                byte_range: ByteRange object specifying start, end, and metadata
            """
            super().__init__()
            self._file_url = file_url
            self._byte_range = byte_range
            self._bytes_read = 0
            self._eof = False
            self._max_bytes = (
                byte_range.end - byte_range.start + 1
            )  # +1 because end is inclusive

            # Open the file and seek to start position - keep it open for streaming
            self._file = SnowflakeFile.open(file_url, "rb")
            self._file.seek(byte_range.start)

        @property
        def is_first_split(self) -> bool:
            """Return True if this is the first split (part_number == 0)."""
            return self._byte_range.part_number == 0

        @property
        def bytes_read(self) -> int:
            """Return the total number of bytes read from this stream."""
            return self._bytes_read

        @property
        def bytes_remaining(self) -> int:
            """Return the number of bytes remaining in the range."""
            return max(0, self._max_bytes - self._bytes_read)

        @property
        def split_size(self) -> int:
            """Return the logical split size (before padding)."""
            return self._byte_range.split_size_bytes

        def readable(self) -> bool:
            """Return True - this stream is readable."""
            return True

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

            # Calculate how many bytes we can read without exceeding the range
            remaining = self.bytes_remaining
            if remaining <= 0:
                self._eof = True
                return 0

            # Limit the read to not exceed our byte range
            bytes_to_read = min(len(b), remaining)

            # Create a limited view of the buffer if needed
            if bytes_to_read < len(b):
                limited_buffer = memoryview(b)[:bytes_to_read]
                n = self._file.readinto(limited_buffer)
            else:
                n = self._file.readinto(b)

            if n is None:
                n = 0

            self._bytes_read += n

            if n == 0 or self._bytes_read >= self._max_bytes:
                self._eof = True

            return n

        def close(self) -> None:
            """Close the stream and release the underlying file handle."""
            if not self.closed:
                if self._file is not None:
                    self._file.close()
                    self._file = None
                super().close()

    class ResyncingBZ2SplitRawStream(io.RawIOBase):
        """
        BZ2 split re-syncing raw stream. Skips partial compression block at the start of the split, unless it is the first split.

        - First split starts immediately
        - Non-first splits resync to next block boundary to get the complete block
        - Produces valid decompressed data only
        - Forward-only
        """

        def __init__(
            self,
            raw_stream: SnowflakeFileByteRangeStream,
            scan_limit: int = 1024
            * 1024,  # At max scan up to 1MB of data to find BZ2 block magic marker.
            read_size: int = io.DEFAULT_BUFFER_SIZE,
        ) -> None:
            self.raw = raw_stream
            self.scan_limit = scan_limit
            self.read_size = read_size

            self._decompressor = bz2.BZ2Decompressor()
            self._buffer = bytearray()
            self._eof = False
            self._resynced = raw_stream.is_first_split
            self._bytes_read = 0
            self._num_blocks_decompressed_past_split_boundary = 0

        @property
        def is_first_split(self) -> bool:
            return self.raw.is_first_split

        @property
        def bytes_read(self) -> int:
            """Return the total number of bytes read from this stream."""
            return self._bytes_read

        @property
        def num_blocks_decompressed_past_split_boundary(self) -> int:
            return self._num_blocks_decompressed_past_split_boundary

        def readable(self):
            return True

        def seekable(self):
            return False

        def _resync(self):
            # Buffer in which we will accumulate read data to scan for BZ2 block magic marker and decompress.
            scanned = bytearray()
            read_buffer = bytearray(self.read_size)
            # Search from this position onwards for BZ2 block magic marker.
            search_from_pos = 0
            # Decompressed up to this position.
            start_decompressing_from_pos = -1

            while len(scanned) < self.scan_limit:
                n = self.raw.readinto(read_buffer)
                if n == 0:
                    self._eof = True
                    return False

                # Append the read chunk to the scanned buffer.
                scanned += memoryview(read_buffer)[:n]

                while True:
                    if start_decompressing_from_pos == -1:
                        # We have not started to decompress yet, still searching for the first valid BZ2 block marker.
                        bz2_marker_pos = scanned.find(
                            BZ2_BLOCK_MAGIC_MARKER, search_from_pos
                        )
                        if bz2_marker_pos >= 4:
                            # We need to look back 4 bytes to include BZ2 stream header BZh[1-9]
                            search_from_pos = bz2_marker_pos + 1
                            # Start searching for the next BZ2 marker after the current one.
                            start_decompressing_from_pos = bz2_marker_pos - 4
                        else:
                            # Start searching from the end of the scanned buffer.
                            search_from_pos = len(scanned)
                            # No BZ2 marker found in the remaining scanned buffer. We need to read more data.
                            break

                    self._bytes_read = start_decompressing_from_pos  # we skipped start_decompressing_from_pos bytes in the compressed stream.
                    candidate = memoryview(scanned)[start_decompressing_from_pos:]
                    try:
                        uncompressed_data = self._decompressor.decompress(candidate)
                        if not uncompressed_data and self._decompressor.needs_input:
                            # Decompressor read everything scanned so far but needs more input.
                            start_decompressing_from_pos = len(scanned)
                            # we consumed len(scanned) bytes in the compressed stream.
                            self._bytes_read = len(scanned)
                            break  # We need to read more data to decompress.
                        else:
                            # Decompressor produced uncompressed data. Append it to the buffer.
                            self._buffer.extend(uncompressed_data)
                            # we consumed everything except the unused data.
                            self._bytes_read += len(candidate) - len(
                                self._decompressor.unused_data
                            )
                            # We found a valid BZ2 block magic marker. Set the resync flag to true.
                            self._resynced = True
                            # Return true to indicate that we found a valid BZ2 block magic marker.
                            return True
                    except OSError as e:
                        logger.error(f"Error decompressing during resync: {e}")
                        # False positive - we found a BZ2 block magic marker but decompression failed. Keep scanning. Reset the decompressor to start fresh.
                        self._decompressor = bz2.BZ2Decompressor()
                        start_decompressing_from_pos = (
                            -1
                        )  # We did not decompress anything. Reset the decompressed till position.
                    finally:
                        candidate.release()

            # Hadoop behavior: no valid block → empty split
            self._eof = True
            return False

        def readinto(self, b):
            while len(self._buffer) <= 0:
                if self._eof:
                    return 0

                if not self._resynced:
                    if not self._resync():
                        return 0

                chunk = None

                if self._decompressor and self._decompressor.eof:
                    if self._decompressor.unused_data:
                        # We decompressed one block and decompressor has extra data beyond the block that still needs to be decompressed.
                        chunk = self._decompressor.unused_data

                    # Reset the decompressor to start afresh for the next compressed block.
                    self._decompressor = bz2.BZ2Decompressor()
                    if self.bytes_read > self.raw.split_size:
                        self._num_blocks_decompressed_past_split_boundary += 1

                if not chunk:
                    n = self.raw.readinto(b)
                    if n == 0:
                        self._eof = True
                        return 0
                    chunk = memoryview(b)[:n]

                try:
                    uncompressed_data = self._decompressor.decompress(chunk)
                    # we consumed everything except the unused data.
                    self._bytes_read += len(chunk) - len(self._decompressor.unused_data)
                    if not uncompressed_data and self._decompressor.needs_input:
                        # Decompressor may consume a chunk but not produce any output. In that case, we need to read more data and feed it to the decompressor.
                        continue
                    else:
                        self._buffer.extend(uncompressed_data)
                except OSError:
                    self._eof = True
                    return 0

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

    class ResyncingLineRecordRawStream(io.RawIOBase):
        """
        Record-aware (newline-delimited) resync stream.

        - First split: pass through unchanged
        - Non-first split: discard bytes until first newline
        """

        def __init__(
            self, raw_stream: ResyncingBZ2SplitRawStream, read_size=8192
        ) -> None:
            self.raw = raw_stream
            self.read_size = read_size

            self._buffer = bytearray()
            self._eof = False
            self._resynced = raw_stream.is_first_split

        @property
        def is_first_split(self) -> bool:
            return self.raw.is_first_split

        def readable(self):
            return True

        def seekable(self):
            return False

        def _resync(self):
            """
            Discard data until after first newline.
            """
            read_buffer = bytearray(self.read_size)

            while True:
                n = self.raw.readinto(read_buffer)
                if n == 0:
                    self._eof = True
                    return False

                chunk = memoryview(read_buffer)[:n]

                if self.raw.num_blocks_decompressed_past_split_boundary >= 1:
                    # First new line delimited record - that we must skip - can not lie past the split boundary.
                    self._eof = True
                    return False

                nl = read_buffer.find(b"\n", 0, n)
                if nl != -1:
                    # Start AFTER the newline
                    self._buffer.extend(chunk[nl + 1 :])
                    self._resynced = True
                    return True

        def readinto(self, b):
            while len(self._buffer) <= 0:
                if self._eof:
                    return 0

                if not self._resynced:
                    if not self._resync():
                        return 0

                n = self.raw.readinto(b)
                if n == 0:
                    self._eof = True
                    return 0

                chunk = memoryview(b)[:n]

                nl = bytes(chunk).find(b"\n")
                if (
                    nl != -1
                    and self.raw.num_blocks_decompressed_past_split_boundary >= 1
                ):
                    # We read up to the first new line character that is in the compressedblock that starts in the next split.
                    # his is the record that the next split reader will skip because it can not decompress the previous compressed
                    # block which may have beginning of this record. Next reader can not decompress the previous compressed block
                    # because that compression block may havestarted in the previous split.
                    self._buffer.extend(chunk[: nl + 1])
                    # We are done reading here.
                    self._eof = True
                else:
                    self._buffer.extend(chunk)

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

    class BZ2FileProcessorUDTF:
        """
        Snowflake UDTF that processes a byte range from a BZ2-compressed file and yields each line as a record.

        This UDTF is designed to be used with ByteRangeGeneratorUDTF. It takes the byte range
        information and processes the compressed data, handling:
        - BZ2 compression block boundaries (resyncs to valid block starts)
        - Newline-delimited record boundaries (handles records spanning blocks)
        - Parallel processing (each split processes its owned records)

        Internally uses the chain:
            SnowflakeFileByteRangeStream → ResyncingBZ2SplitRawStream → ResyncingLineRecordRawStream

        Usage in SQL (chained with ByteRangeGeneratorUDTF):
            -- First get byte ranges, then process each range in parallel
            WITH byte_ranges AS (
                SELECT * FROM TABLE(
                    byte_range_generator(
                        BUILD_SCOPED_FILE_URL(@my_stage, 'data.jsonl.bz2'),
                        2097152,  -- split_size_bytes (2MB)
                        2097152   -- additional_padding_bytes (2MB)
                    )
                )
            )
            SELECT
                br.part_number,
                records.line_number,
                records.line_content
            FROM byte_ranges br,
            TABLE(
                snowflake_file_uploader(
                    BUILD_SCOPED_FILE_URL(@my_stage, 'data.jsonl.bz2'),
                    br.part_number,
                    br.start_byte,
                    br.end_byte,
                    br.split_size_bytes
                ) OVER (PARTITION BY br.part_number)
            ) records;

        Returns:
            A table with columns:
            - line_number: The line number within this split (1-indexed)
            - line_content: The content of the line (bytes decoded as UTF-8)
        """

        def __init__(self) -> None:
            self._line_number = 0

        def process(
            self,
            file_url: str,
            part_number: int,
            start_byte: int,
            end_byte: int,
            split_size_bytes: int,
        ):
            """
            Process a byte range and yield each line as a record.

            Args:
                file_url: Scoped URL or stage path to the file
                part_number: The partition/split number (0-indexed)
                start_byte: Starting byte offset for this range
                end_byte: Ending byte offset for this range (inclusive)
                split_size_bytes: The logical split size (before padding)

            Yields:
                Tuples of (line_number, line_content)
            """
            # Reconstruct ByteRange from arguments
            byte_range = ByteRange(
                start=start_byte,
                end=end_byte,
                part_number=part_number,
                split_size_bytes=split_size_bytes,
            )

            # Build the streaming chain:
            # SnowflakeFileByteRangeStream → ResyncingBZ2SplitRawStream → ResyncingLineRecordRawStream

            # Layer 1: Raw byte range stream from Snowflake file
            raw_stream = SnowflakeFileByteRangeStream(file_url, byte_range)

            # Layer 2: BZ2 decompression with block resync
            bz2_stream = ResyncingBZ2SplitRawStream(raw_stream)

            # Layer 3: Line record extraction with boundary handling
            record_stream = ResyncingLineRecordRawStream(bz2_stream)

            # Wrap in BufferedReader for efficient line reading
            buffered_stream = io.BufferedReader(record_stream)

            try:
                # Read and yield each line
                for line_bytes in buffered_stream:
                    self._line_number += 1
                    # Decode bytes to string, strip trailing newline
                    line_content = line_bytes.decode("utf-8", errors="replace").rstrip(
                        "\n\r"
                    )
                    yield (self._line_number, json.loads(line_content))
            finally:
                buffered_stream.close()

        def end_partition(self):
            """Called at the end of each partition. Reset line counter."""
            self._line_number = 0

    session.udtf.register(
        BZ2FileProcessorUDTF,
        output_schema=BZ2_FILE_PROCESSOR_OUTPUT_SCHEMA,
        input_types=[StringType(), IntegerType(), LongType(), LongType(), LongType()],
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
    additional_padding_mb: int = 2,
    auto_register_udtfs: bool = True,
) -> DataFrame:
    """
    Load a large BZ2-compressed newline-delimited file from a Snowflake stage.

    Args:
        session: Active Snowpark Session
        stage: Snowflake stage name (e.g., "@my_stage")
        file_path: Path to the file within the stage
        split_size_mb: Size of each split in MB (default: 200MB)
        additional_padding_mb: Additional padding in MB (default: 2MB)
        auto_register_udtfs: Whether to automatically register UDTFs (default: True)

    Returns:
        DataFrame with columns: part_number, start_byte, end_byte, split_size_bytes,
        file_size, line_number, line_content
    """
    if auto_register_udtfs:
        register_all_bz2_udtfs(session)

    split_size_bytes = split_size_mb * 1024 * 1024
    additional_padding_bytes = additional_padding_mb * 1024 * 1024

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
        "byte_range_generator",
        col("file_url"),
        lit(split_size_bytes),
        lit(additional_padding_bytes),
        lit(False),
    ).cache_result()

    from snowflake.snowpark.functions import table_function

    bz2_processor_udtf = table_function("bz2_file_processor")
    udtf_call = bz2_processor_udtf(
        col("file_url"),
        col("part_number"),
        col("start_byte"),
        col("end_byte"),
        col("split_size_bytes"),
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
    additional_padding_mb: int = 2,
    mode: str = "overwrite",
    auto_register_udtfs: bool = True,
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
        additional_padding_mb=additional_padding_mb,
        auto_register_udtfs=auto_register_udtfs,
    )

    df.write.mode(mode).save_as_table(target_table)
