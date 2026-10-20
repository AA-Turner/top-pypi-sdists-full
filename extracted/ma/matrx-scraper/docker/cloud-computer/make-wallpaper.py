"""Write the Cloud Computer wallpaper: a quiet diagonal gradient PNG.

Pure standard library (zlib + struct) so the image build needs no imaging
package. Usage: python make-wallpaper.py <out.png> [width height]
"""

from __future__ import annotations

import struct
import sys
import zlib

TOP_LEFT = (15, 23, 42)  # slate-900
BOTTOM_RIGHT = (30, 64, 175)  # blue-800
ACCENT = (56, 189, 248)  # sky-400, a soft glow toward the lower right


def _chunk(kind: bytes, data: bytes) -> bytes:
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def render(width: int, height: int) -> bytes:
    rows = bytearray()
    for y in range(height):
        rows.append(0)  # filter: none
        for x in range(width):
            t = (x / width * 0.6) + (y / height * 0.4)
            gx, gy = x / width - 0.78, y / height - 0.72
            glow = max(0.0, 1.0 - (gx * gx + gy * gy) * 6.0) * 0.35
            for c in range(3):
                base = TOP_LEFT[c] + (BOTTOM_RIGHT[c] - TOP_LEFT[c]) * t
                rows.append(int(min(255, base + (ACCENT[c] - base) * glow)))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", header)
        + _chunk(b"IDAT", zlib.compress(bytes(rows), 9))
        + _chunk(b"IEND", b"")
    )


if __name__ == "__main__":
    out = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 900
    with open(out, "wb") as handle:
        handle.write(render(width, height))
