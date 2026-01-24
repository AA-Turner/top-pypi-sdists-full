# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from zlib import crc32


class Digest:
    def __init__(self):
        self.crc32 = 0

    def finish(self):
        return str(self.crc32)

    def update(self, value: str):
        self.crc32 = crc32(str(value).encode(), self.crc32)
