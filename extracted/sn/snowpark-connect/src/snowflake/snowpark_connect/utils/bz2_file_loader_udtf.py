#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import io
import json
import logging

from snowflake.snowpark.files import SnowflakeFile
from snowflake.snowpark_connect.utils.bz2_stream_utils import (
    BZ2DecompressingStream,
    SnowflakeFileSplitStream,
    calculate_byte_ranges,
)


class FileSplitsGeneratorUDTF:
    """
    Snowflake UDTF that generates fil splits for parallel processing of large files.

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
        - split_size_bytes: The logical split size
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
                f"Generating file split {split.part_number} of size {split.split_size_bytes} starting at {split.start}"
            )
            yield split.split_size_bytes, split.part_number, split.start

    def end_partition(self):
        """Called at the end of each partition. No cleanup needed."""
        pass


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
                compressed
            ) OVER (PARTITION BY fs.part_number)
        ) records;

    Returns:
        A table with columns:
        - line_number: The line number within this split (1-indexed)
        - line_content: The content of the line as a VARIANT
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def process(
        self,
        file_url: str,
        split_size_bytes: int,
        part_number: int,
        start_byte: int,
        mode: str,
        compressed: bool,
    ):
        """
        Process a byte range and yield each line as a record.

        Args:
            file_url: Scoped URL or stage path to the file
            split_size_bytes: The logical split size (before padding)
            part_number: The partition/split number (0-indexed)
            start_byte: Starting byte offset for this range
            mode: PERMISSIVE or FAILFAST (for parsing)
            compressed: Is the file BZ2 compressed?

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
                    line_content = line_bytes.decode("utf-8", errors="replace").rstrip(
                        "\n\r"
                    )
                    try:
                        # Decode bytes to string, strip trailing newline
                        yield line_number, json.loads(line_content)
                    except json.JSONDecodeError as e:
                        record = line_content[:1024]
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

                if compressed and decompressed_stream.num_reads_past_split_boundary > 0:
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
