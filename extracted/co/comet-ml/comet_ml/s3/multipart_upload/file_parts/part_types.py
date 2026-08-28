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
from typing import Any


class FilePart(object):
    """One part of an asset: where it goes, and a body to send.

    The body is either raw ``bytes`` or a FileRangeReader. Which one decides
    whether the part is resident in memory, and therefore whether a large part
    size is survivable:

    * an asset on disk yields a reader, so the part costs whatever the HTTP layer
      buffers regardless of its size
    * an asset already in memory yields bytes, because several threads cannot seek
      one shared stream, and its payload is resident anyway

    ``size`` is carried explicitly rather than measured from the body, so it is
    known without reading anything.

    Instances are handed between threads and treated as immutable once created.
    """

    __slots__ = ["part_number", "url", "body", "size"]

    def __init__(self, part_number: int, url: str, body: Any, size: int):
        self.part_number = part_number
        self.url = url
        self.body = body
        self.size = size

    @property
    def is_resident(self) -> bool:
        """True when the body is bytes, and so counts against the memory budget."""
        return isinstance(self.body, (bytes, bytearray))

    def close(self) -> None:
        """Releases a reader's file handle. A bytes body needs nothing."""
        close = getattr(self.body, "close", None)
        if callable(close):
            close()

    def __repr__(self) -> str:
        return "FilePart(part_number=%d, size=%d, resident=%s)" % (
            self.part_number,
            self.size,
            self.is_resident,
        )


class PartMetadata(object):
    """The outcome of a successfully uploaded part, as S3 needs it back at completion."""

    __slots__ = ["e_tag", "part_number", "size"]

    def __init__(self, e_tag: str, part_number: int, size: int):
        self.e_tag = e_tag
        self.part_number = part_number
        self.size = size

    def __repr__(self) -> str:
        return "PartMetadata(part_number=%d, size=%d, e_tag=%r)" % (
            self.part_number,
            self.size,
            self.e_tag,
        )
