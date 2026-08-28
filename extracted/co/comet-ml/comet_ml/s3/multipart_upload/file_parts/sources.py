# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2025 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import contextlib
import functools
import io
from typing import IO, Callable, Iterator, List, Optional, Union

from .. import file_parts_strategy
from . import part_types, readers


class FileRangePartsSource(object):
    """Parts of an asset on disk, each read straight from its own byte range.

    Nothing is held in memory: a part's body is a reader over the file, so peak
    memory is independent of the part size. That is what makes the configured part
    size safe to raise towards S3's 5 GiB limit, where a materialised part would
    mean a 5 GiB allocation for every part in flight.

    Producing a part opens a file handle, which the sender closes once the part has
    been sent. Each part has its own, so they can be read concurrently without
    seeking a shared one.
    """

    def __init__(
        self,
        path: str,
        parts_urls: List[str],
        max_part_size: int,
        file_size: int,
        on_part_progress: Optional[Callable[[int, int], None]] = None,
    ):
        self._path = path
        self._parts_urls = parts_urls
        self._max_part_size = max_part_size
        self._file_size = file_size
        # Reported per part as its bytes reach the HTTP layer, so a large part in
        # flight moves the progress display instead of showing nothing until it
        # lands. Only this path can offer it: a materialised part is already fully
        # read before it is sent, so per-part completion is all there is to report.
        self._on_part_progress = on_part_progress

    @property
    def max_part_size(self) -> int:
        return self._max_part_size

    @property
    def holds_parts_in_memory(self) -> bool:
        return False

    def parts(self) -> Iterator[part_types.FilePart]:
        offset = 0
        for index, url in enumerate(self._parts_urls):
            # The final part is whatever is left, which is normally shorter.
            length = min(self._max_part_size, self._file_size - offset)
            if length <= 0:
                return

            part_number = index + 1
            on_progress = None
            if self._on_part_progress is not None:
                on_progress = functools.partial(self._on_part_progress, part_number)

            yield part_types.FilePart(
                part_number=part_number,
                url=url,
                body=readers.FileRangeReader(
                    self._path, offset, length, on_progress=on_progress
                ),
                size=length,
            )
            offset += length


class StreamPartsSource(object):
    """Parts of an asset that is already in memory, or behind a stream we cannot seek.

    Here the bytes have to be materialised: several threads cannot seek one shared
    stream, so each part is read in turn. The payload is resident anyway for an
    in-memory asset, but it does mean the memory budget still governs this path and
    that a very large part size is still costly on it.
    """

    def __init__(
        self,
        # TextIOBase as well as IO, because a text stream is accepted and converted
        # below; the two are unrelated as far as the type stubs are concerned.
        stream: Union[IO, io.TextIOBase],
        parts_urls: List[str],
        max_part_size: int,
    ):
        self._parts_urls = parts_urls
        self._max_part_size = max_part_size
        # A text stream measures its reads in characters, and a part size is a limit
        # in bytes, so reading max_part_size characters produced parts of up to four
        # times that many bytes - over S3's own 5 GiB limit at the top of the
        # configurable range. Budgeting the reads in characters instead cannot fill a
        # part exactly, which leaves a tail behind.
        #
        # So text is encoded once, here, and everything downstream deals in bytes.
        # This path already holds each part in memory, and a str costs more than its
        # UTF-8 encoding, so nothing is made materially worse by it.
        if isinstance(stream, io.TextIOBase):
            stream = io.BytesIO(stream.read().encode("utf-8"))

        self._stream = stream

    @property
    def max_part_size(self) -> int:
        return self._max_part_size

    @property
    def holds_parts_in_memory(self) -> bool:
        return True

    def parts(self) -> Iterator[part_types.FilePart]:
        for index, url in enumerate(self._parts_urls):
            data = self._stream.read(self._max_part_size)
            if not data and index > 0:
                # The stream ran out early. Yielding an empty part would have S3
                # reject the upload, and skipping it silently would complete with a
                # gap, so stop and let the caller complete with what it has.
                return

            yield part_types.FilePart(
                part_number=index + 1, url=url, body=data, size=len(data)
            )

        leftover = self._stream.read(1)
        if leftover:
            # The part count was decided upstream from the asset's declared size. If
            # bytes remain after the last URL, that size was wrong - which happens
            # for text, where a character count is smaller than the UTF-8 byte count.
            # Failing here is the point: iterating the URL list would otherwise drop
            # the tail and report the upload as a success.
            raise ValueError(
                "The asset has more bytes than its declared size allowed for: %d "
                "parts of %d bytes did not cover it. For text this is the difference "
                "between a character count and a byte count."
                % (len(self._parts_urls), self._max_part_size)
            )


# Either shape a source can take: parts of a file read by range, or of a stream
# read into memory. They share a duck-typed contract of parts(), max_part_size and
# holds_parts_in_memory.
PartsSourceType = Union[FileRangePartsSource, StreamPartsSource]


@contextlib.contextmanager
def open_parts_source(
    strategy: file_parts_strategy.BaseFilePartsStrategy,
    parts_urls: List[str],
    on_part_progress: Optional[Callable[[int, int], None]] = None,
) -> Iterator[PartsSourceType]:
    """Yields a source over the asset's parts, streaming it wherever that is possible.

    The single place that knows how each strategy exposes its bytes, so neither the
    uploader nor any scheduler branches on the concrete strategy type.
    """
    max_part_size = strategy.max_file_part_size

    if isinstance(strategy, file_parts_strategy.FilePartsStrategy):
        # On disk, so it can be read by range and never held in memory.
        yield FileRangePartsSource(
            path=strategy.file,
            parts_urls=parts_urls,
            max_part_size=max_part_size,
            file_size=strategy.file_size,
            on_part_progress=on_part_progress,
        )
    elif isinstance(strategy, file_parts_strategy.FileLikePartsStrategy):
        # rewind
        strategy.file_like.seek(0)
        yield StreamPartsSource(
            stream=strategy.file_like,
            parts_urls=parts_urls,
            max_part_size=max_part_size,
        )
    else:
        raise TypeError("Unsupported file parts strategy: %r" % type(strategy).__name__)
