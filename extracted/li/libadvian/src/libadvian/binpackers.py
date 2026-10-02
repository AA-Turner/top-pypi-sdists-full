"""Un/packing helpers."""

from typing import List, Sequence, Union
import base64
import uuid


def uuid_to_b64(msgid: uuid.UUID) -> str:
    """Encode UUID to url-safe base64"""
    return base64.urlsafe_b64encode(msgid.bytes).decode("ascii")


def b64_to_uuid(instr: Union[bytes, str]) -> uuid.UUID:
    """Decode base64 to UUID object"""
    if not isinstance(instr, str):
        instr = instr.decode("ascii")
    inbytes = base64.urlsafe_b64decode(instr)
    return uuid.UUID(bytes=inbytes)


def ensure_utf8(instr: Union[bytes, str]) -> bytes:
    """Make sure input is bytes, encode UTF-8 if not."""
    if isinstance(instr, str):
        return instr.encode("utf-8")
    return instr


def ensure_utf8_list(inlst: Union[Sequence[bytes], Sequence[str]]) -> List[bytes]:
    """Make sure all elements are bytes, see `ensure_utf8`."""
    return [ensure_utf8(item) for item in inlst]


def ensure_str(instr: Union[bytes, str]) -> str:
    """Make sure input is str, decode UTF-8 if not."""
    if isinstance(instr, bytes):
        return instr.decode("utf-8")
    return instr


def ensure_str_list(inlst: Union[Sequence[bytes], Sequence[str]]) -> List[str]:
    """Make sure all elements are str, see `ensure_str`."""
    return [ensure_str(item) for item in inlst]
