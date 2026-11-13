"""Streaming local CRC64/XZ and SHA-256 for metadata-only upload verification."""
import hashlib

_POLYNOMIAL = 0xC96C5795D7870F42
_MASK = (1 << 64) - 1
_TABLE = []
for _value in range(256):
    for _bit in range(8):
        _value = (_value >> 1) ^ (_POLYNOMIAL if _value & 1 else 0)
    _TABLE.append(_value)


def _crc64_fallback(crc, data):
    for value in data:
        crc = _TABLE[(crc ^ value) & 255] ^ (crc >> 8)
    return crc


def crc64_file(path):
    # oss2's optional crcmod accelerator avoids a Python loop for large archives.
    try:
        from oss2.utils import Crc64
    except ImportError:
        checksum = None
    else:
        checksum = Crc64()
    sha, size, crc = hashlib.sha256(), 0, _MASK
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            sha.update(chunk)
            size += len(chunk)
            if checksum is None:
                crc = _crc64_fallback(crc, chunk)
            else:
                checksum(chunk)
    return size, crc ^ _MASK if checksum is None else checksum.crc, "sha256:" + sha.hexdigest()
