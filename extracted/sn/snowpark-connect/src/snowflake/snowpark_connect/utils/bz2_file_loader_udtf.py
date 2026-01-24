#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import io

from snowflake.snowpark.files import SnowflakeFile
from snowflake.snowpark_connect.utils.bz2_stream_utils import (
    ByteRange,
    ResyncingBZ2SplitRawStream,
    ResyncingLineRecordRawStream,
    SnowflakeFileByteRangeStream,
    calculate_byte_ranges,
)


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
                yield (self._line_number, line_content)
        finally:
            buffered_stream.close()

    def end_partition(self):
        """Called at the end of each partition. Reset line counter."""
        self._line_number = 0
