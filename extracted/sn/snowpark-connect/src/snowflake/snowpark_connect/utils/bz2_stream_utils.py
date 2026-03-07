#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Utilities for Parallel Processing of BZ2 compressed or uncompressed, newline-delimited files

IMPORTANT: This library is designed for BZ2 files created with multiple independent
compression streams (concatenated/chained BZ2 blocks), where each block can be
decompressed independently. This is the format created by:
  - bz2.BZ2Compressor() with periodic flush() calls
  - Hadoop's BZip2Codec
  - Parallel compression tools that create multiple streams

This library does NOT support standard single-stream BZ2 files created by:
  - bz2.compress() - creates one header followed by many dependent blocks
  - Standard bzip2 command-line tool - single compression stream
  - Files where blocks depend on previous blocks' dictionary state

The key difference is that concatenated BZ2 files have multiple "BZh[1-9]" headers
throughout the file (one per independent stream), while single-stream files have
only one header at the beginning. This library relies on finding these internal
headers (BZh[1-9]   ) to resync at split boundaries.
"""

import bz2
import io
import re
from dataclasses import dataclass
from typing import Optional

from snowflake.snowpark.files import SnowflakeFile


@dataclass
class FileSplit:
    """Represents a file split for downloading a file chunk."""

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
