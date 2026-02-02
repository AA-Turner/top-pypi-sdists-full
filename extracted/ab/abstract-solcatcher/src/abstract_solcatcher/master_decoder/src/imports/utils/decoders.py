from .imports import *
# ============================================================================
# DECODERS
# ============================================================================

def read_pubkey(raw: bytes, offset: int) -> tuple[str, int]:
    """Read 32-byte pubkey, return (base58_str, new_offset)"""
    pk = base58.b58encode(raw[offset:offset+32]).decode()
    return pk, offset + 32


def read_u64(raw: bytes, offset: int) -> tuple[int, int]:
    val, = struct.unpack_from("<Q", raw, offset)
    return val, offset + 8


def read_i64(raw: bytes, offset: int) -> tuple[int, int]:
    val, = struct.unpack_from("<q", raw, offset)
    return val, offset + 8


def read_bool(raw: bytes, offset: int) -> tuple[bool, int]:
    val, = struct.unpack_from("<?", raw, offset)
    return val, offset + 1


def read_string(raw: bytes, offset: int) -> tuple[str, int]:
    ln, = struct.unpack_from("<I", raw, offset)
    offset += 4
    val = raw[offset:offset+ln].decode("utf-8")
    return val, offset + ln


def is_null_pubkey(raw: bytes, offset: int) -> bool:
    return raw[offset:offset+32] == bytes(32)
# idl_types.py
import struct, base58

def read_string(buf, o):
    ln = struct.unpack_from("<I", buf, o)[0]
    o += 4
    return buf[o:o+ln].decode(), o + ln

def read_pubkey(buf, o):
    return base58.b58encode(buf[o:o+32]).decode(), o + 32

def read_u64(buf, o):
    return struct.unpack_from("<Q", buf, o)[0], o + 8

def read_i64(buf, o):
    return struct.unpack_from("<q", buf, o)[0], o + 8

def read_bool(buf, o):
    return buf[o] == 1, o + 1

TYPE_READERS = {
    "string": read_string,
    "publicKey": read_pubkey,
    "u64": read_u64,
    "i64": read_i64,
    "bool": read_bool,
}

