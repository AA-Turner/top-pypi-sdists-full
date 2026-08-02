"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Copyright (C) 2023 Michael Hall <https://github.com/mikeshardmind>
"""

# This creates base2048/b2048.zlib
# as the object is used, it shouldnt be possible for this to be malicious
# but it's here for reproducability anyway.
# This file should *never* need regeneration, it's lookup tables for a stable
# encoding

import lzma
import struct
from pathlib import Path

from .dec_table import dec
from .enc_table import enc


def write_data() -> None:
    packed = struct.pack("!4340H2048H", *dec, *map(ord, enc))
    compressed = lzma.compress(
        packed, preset=lzma.PRESET_EXTREME, format=lzma.FORMAT_XZ, check=lzma.CHECK_NONE
    )
    with Path(__file__).with_name("b2048.data").open(mode="wb") as fp:
        fp.write(compressed)
