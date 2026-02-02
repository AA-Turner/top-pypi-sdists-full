from .imports import *
def sanitize_string(s: str) -> str:
    """Remove null bytes and trim whitespace."""
    if not s:
        return s
    return s.replace('\x00', '').strip()


def read_string(buffer: bytes, offset: int) -> tuple[str, int]:
    """
    Read length-prefixed string from buffer.
    Returns (value, new_offset).
    """
    if offset + 4 > len(buffer):
        raise ValueError(f"Not enough data to read string length at offset {offset}")
    
    str_len = struct.unpack_from('<I', buffer, offset)[0]
    offset += 4
    
    if offset + str_len > len(buffer):
        raise ValueError(f"Not enough data to read string of length {str_len} at offset {offset}")
    
    value = buffer[offset:offset + str_len].decode('utf-8', errors='replace')
    value = sanitize_string(value)
    
    return value, offset + str_len
