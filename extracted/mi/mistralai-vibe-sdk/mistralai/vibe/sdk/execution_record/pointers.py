"""Small JSON Pointer helpers used by patch production and application."""

from collections.abc import Iterable

type JsonPointer = str


def escape_segment(segment: object) -> str:
    """Escape one JSON Pointer segment per RFC 6901."""
    return str(segment).replace("~", "~0").replace("/", "~1")


def unescape_segment(segment: str) -> str:
    """Unescape one JSON Pointer segment per RFC 6901."""
    return segment.replace("~1", "/").replace("~0", "~")


def split_pointer(pointer: JsonPointer) -> list[str]:
    """Split a JSON Pointer into unescaped segments.

    Empty segments are ignored to preserve the runtime's existing tolerant
    behavior for ``""`` and ``"/"`` root-like paths.
    """
    if not pointer or pointer == "/":
        return []
    return [unescape_segment(part) for part in pointer.split("/") if part]


def join_segments(segments: Iterable[object]) -> JsonPointer:
    """Build a JSON Pointer from raw, unescaped path segments."""
    parts = [escape_segment(segment) for segment in segments]
    if not parts:
        return ""
    return "/" + "/".join(parts)


def append_segment(pointer: JsonPointer, segment: object) -> JsonPointer:
    """Append one raw segment to an existing JSON Pointer."""
    suffix = escape_segment(segment)
    if not pointer:
        return f"/{suffix}"
    return f"{pointer.rstrip('/')}/{suffix}"


def join_pointers(*pointers: JsonPointer) -> JsonPointer:
    """Join JSON Pointer fragments, preserving segment escaping semantics."""
    segments: list[str] = []
    for pointer in pointers:
        segments.extend(split_pointer(pointer))
    return join_segments(segments)


def prepend_pointer(prefix: JsonPointer, pointer: JsonPointer) -> JsonPointer:
    """Prepend a JSON Pointer prefix to another pointer."""
    return join_pointers(prefix, pointer)


__all__ = [
    "append_segment",
    "escape_segment",
    "join_pointers",
    "join_segments",
    "prepend_pointer",
    "split_pointer",
    "unescape_segment",
]
