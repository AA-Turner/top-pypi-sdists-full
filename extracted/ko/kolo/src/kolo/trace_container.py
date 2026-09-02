from __future__ import annotations

import struct
import zlib
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import chain
from typing import Iterator

import msgpack

from .serialize import load_msgpack, load_msgpack_value, resolve_value_references


HEADER_MAGIC = b"KOLOTRC3"
RECORD_MAGIC = b"KR3\0"
FOOTER_MAGIC = b"KOLOEND3"
HEADER_LEN = 24
RECORD_HEADER_LEN = 40
FOOTER_LEN = 32
TRACE_CONTENT_TYPE = "application/vnd.kolo.trace"

CHUNK = 1
THREAD_META = 2
METADATA = 3
INDEX = 4
VALUE_TABLE = 5
CHUNK_TARGET = 512 * 1024


class TraceContainerError(ValueError):
    pass


@dataclass(frozen=True)
class Record:
    kind: int
    thread_token: int
    sequence: int
    item_count: int
    payload: memoryview
    offset: int


@dataclass(frozen=True)
class ParsedContainer:
    header: dict
    records: tuple[Record, ...]
    complete: bool

    def frame_views_by_chunk(
        self,
    ) -> dict[tuple[int, int], tuple[memoryview, ...]]:
        chunks = {}
        for record in self.records:
            if record.kind == CHUNK:
                chunks[(record.thread_token, record.sequence)] = tuple(
                    _chunk_frame_views(record)
                )
        return chunks


def is_v3_trace(data: bytes | bytearray | memoryview) -> bool:
    return bytes(memoryview(data)[: len(HEADER_MAGIC)]) == HEADER_MAGIC


def _crc32(data: bytes | memoryview) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def _read_uleb128(payload: memoryview, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while offset < len(payload):
        byte = payload[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if byte & 0x80 == 0:
            return value, offset
        shift += 7
        if shift >= 64:
            raise TraceContainerError("v3 frame length exceeds u64")
    raise TraceContainerError("truncated v3 frame-length table")


def _chunk_frame_views(record: Record) -> Iterator[memoryview]:
    payload = record.payload
    lengths = []
    offset = 0
    for _ in range(record.item_count):
        length, offset = _read_uleb128(payload, offset)
        lengths.append(length)
    frame_offset = offset
    if sum(lengths) != len(payload) - frame_offset:
        raise TraceContainerError("v3 frame lengths do not match chunk payload")
    for length in lengths:
        end = frame_offset + length
        yield payload[frame_offset:end]
        frame_offset = end


def parse_v3_container(
    data: bytes | bytearray | memoryview, *, recover: bool = False
) -> ParsedContainer:
    view = memoryview(data)
    if len(view) < HEADER_LEN or bytes(view[:8]) != HEADER_MAGIC:
        raise TraceContainerError("not a Kolo v3 trace container")
    version, payload_format, codec, flags, payload_len, payload_crc = (
        struct.unpack_from("<HBBIII", view, 8)
    )
    if version != 3 or payload_format not in (1, 2):
        raise TraceContainerError(
            f"unsupported Kolo trace container version {version}/{payload_format}"
        )
    if codec != 0:
        raise TraceContainerError(f"unsupported Kolo trace codec {codec}")
    if flags != 0:
        raise TraceContainerError(f"unsupported Kolo trace flags {flags:#x}")
    header_end = HEADER_LEN + payload_len
    if header_end > len(view):
        raise TraceContainerError("truncated Kolo v3 header payload")
    header_payload = view[HEADER_LEN:header_end]
    if _crc32(header_payload) != payload_crc:
        raise TraceContainerError("Kolo v3 header checksum mismatch")
    header = load_msgpack(header_payload)
    if not isinstance(header, dict):
        raise TraceContainerError("Kolo v3 header payload is not a map")

    complete = False
    records_end = len(view)
    footer_index_offset = None
    has_footer_magic = (
        len(view) >= FOOTER_LEN
        and bytes(view[-FOOTER_LEN : -FOOTER_LEN + 8]) == FOOTER_MAGIC
    )
    if has_footer_magic:
        footer = view[-FOOTER_LEN:]
        index_offset, file_len = struct.unpack_from("<QQ", footer, 8)
        footer_crc, footer_flags = struct.unpack_from("<II", footer, 24)
        if (
            file_len != len(view)
            or footer_flags != 0
            or _crc32(footer[:24]) != footer_crc
            or index_offset < header_end
            or index_offset >= len(view) - FOOTER_LEN
        ):
            if not recover:
                raise TraceContainerError("invalid Kolo v3 footer")
        else:
            complete = True
            footer_index_offset = index_offset
            records_end -= FOOTER_LEN

    recovering = recover and not complete

    records = []
    offset = header_end
    while offset < records_end:
        if records_end - offset < RECORD_HEADER_LEN:
            if recovering:
                break
            raise TraceContainerError("truncated Kolo v3 record header")
        record_header = view[offset : offset + RECORD_HEADER_LEN]
        if bytes(record_header[:4]) != RECORD_MAGIC:
            if recovering:
                break
            raise TraceContainerError(f"invalid Kolo v3 record magic at {offset}")
        if _crc32(record_header[:36]) != struct.unpack_from("<I", record_header, 36)[0]:
            if recovering:
                break
            raise TraceContainerError(
                f"Kolo v3 record header checksum mismatch at {offset}"
            )
        kind = record_header[4]
        thread_token = struct.unpack_from("<I", record_header, 8)[0]
        sequence = struct.unpack_from("<Q", record_header, 12)[0]
        item_count, raw_len, stored_len, stored_crc = struct.unpack_from(
            "<IIII", record_header, 20
        )
        payload_start = offset + RECORD_HEADER_LEN
        payload_end = payload_start + stored_len
        if payload_end > records_end:
            if recovering:
                break
            raise TraceContainerError(f"truncated Kolo v3 record payload at {offset}")
        if raw_len != stored_len:
            if recovering:
                break
            raise TraceContainerError("compressed Kolo v3 chunks are not implemented")
        payload = view[payload_start:payload_end]
        if stored_crc and _crc32(payload) != stored_crc:
            if recovering:
                break
            raise TraceContainerError(f"Kolo v3 record checksum mismatch at {offset}")
        records.append(
            Record(kind, thread_token, sequence, item_count, payload, offset)
        )
        offset = payload_end

    if complete and not any(
        record.offset == footer_index_offset and record.kind == INDEX
        for record in records
    ):
        raise TraceContainerError("Kolo v3 footer does not reference an index record")

    return ParsedContainer(header, tuple(records), complete)


def _logical_frame_views(parsed: ParsedContainer) -> dict[int, list[memoryview]]:
    chunks = parsed.frame_views_by_chunk()
    physical = defaultdict(list)
    index = None
    for record in parsed.records:
        if record.kind == CHUNK:
            physical[record.thread_token].append(record.sequence)
        elif record.kind == INDEX:
            value = load_msgpack(record.payload)
            if not isinstance(value, dict):
                raise TraceContainerError("v3 index payload is not a map")
            index = value

    result: dict[int, list[memoryview]] = {}
    layouts = index.get("threads", {}) if isinstance(index, dict) else {}
    if not isinstance(layouts, dict):
        raise TraceContainerError("v3 thread index is not a map")
    layout_tokens = set()
    for token in layouts:
        if type(token) is not int or not 0 <= token <= 0xFFFFFFFF:
            raise TraceContainerError("invalid v3 thread token")
        layout_tokens.add(token)
    tokens = set(physical) | layout_tokens
    for token in sorted(tokens):
        layout = layouts.get(token)
        frames: list[memoryview] = []
        if layout is None:
            for sequence in sorted(physical[token]):
                frames.extend(chunks[(token, sequence)])
        else:
            for span in layout:
                if (
                    not isinstance(span, (list, tuple))
                    or len(span) != 3
                    or any(type(value) is not int for value in span)
                ):
                    raise TraceContainerError("invalid v3 frame span")
                sequence, first_frame, frame_count = span
                chunk = chunks.get((token, sequence))
                if chunk is None:
                    raise TraceContainerError(
                        f"v3 index references missing chunk {token}/{sequence}"
                    )
                end = first_frame + frame_count
                if first_frame < 0 or frame_count < 0 or end > len(chunk):
                    raise TraceContainerError("v3 index references invalid frame range")
                frames.extend(chunk[first_frame:end])
        result[token] = frames
    return result


def iter_v3_frame_bytes(data: bytes | bytearray | memoryview) -> Iterator[bytes]:
    parsed = parse_v3_container(data, recover=True)
    frames_by_token = _logical_frame_views(parsed)
    for token in sorted(frames_by_token):
        for frame in frames_by_token[token]:
            yield bytes(frame)


def load_v3_trace(data: bytes | bytearray | memoryview) -> dict:
    parsed = parse_v3_container(data, recover=True)
    metadata = {}
    thread_metadata = {}
    value_table: dict[int, str | bytes] = {}
    for record in parsed.records:
        if record.kind == METADATA:
            value = load_msgpack(record.payload)
            if not isinstance(value, dict):
                raise TraceContainerError("v3 metadata payload is not a map")
            metadata.update(value)
        elif record.kind == THREAD_META:
            value = load_msgpack(record.payload)
            if not isinstance(value, dict):
                raise TraceContainerError("v3 thread metadata payload is not a map")
            thread_metadata[record.thread_token] = value
        elif record.kind == VALUE_TABLE:
            value = load_msgpack(record.payload)
            if (
                record.item_count != 1
                or record.sequence > 0xFFFFFFFF
                or not isinstance(value, (str, bytes))
                or record.sequence in value_table
            ):
                raise TraceContainerError("invalid v3 value table")
            value_table[record.sequence] = value

    trace = dict(metadata)
    # Completeness is a property of the container we actually read, not
    # user-controlled trace metadata.  Keep complete and legacy traces
    # unchanged while making a recovered prefix impossible to mistake for a
    # complete execution.
    trace.pop("recovered", None)
    if not parsed.complete:
        trace["recovered"] = True
    trace.setdefault("trace_id", parsed.header.get("trace_id"))
    trace.setdefault("timestamp", parsed.header.get("timestamp"))
    trace.setdefault("frames_of_interest", [])
    trace.setdefault("frames", {})
    frames_by_token = _logical_frame_views(parsed)
    threads = {}
    for token in sorted(set(frames_by_token) | set(thread_metadata)):
        thread = dict(thread_metadata.get(token, {}))
        thread_id = str(thread.pop("thread_id", token))
        thread["frames"] = [
            resolve_value_references(load_msgpack_value(frame), value_table)
            for frame in frames_by_token.get(token, ())
        ]
        threads[thread_id] = thread
    trace["threads"] = threads
    return trace


def extract_v3_trace_name(data: bytes | bytearray | memoryview) -> str | None:
    parsed = parse_v3_container(data, recover=True)
    trace_name = None
    for record in parsed.records:
        if record.kind != METADATA:
            continue
        value = load_msgpack(record.payload)
        if isinstance(value, dict) and value.get("trace_name"):
            trace_name = value["trace_name"]
    return trace_name


def load_trace(data: bytes | bytearray | memoryview):
    if is_v3_trace(data):
        return load_v3_trace(data)
    trace = load_msgpack(data)
    if isinstance(trace, dict):
        trace.pop("recovered", None)
    return trace


def _append_uleb128(encoded: bytearray, value: int) -> None:
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            byte |= 0x80
        encoded.append(byte)
        if not value:
            return


def _uleb128(value: int) -> bytes:
    encoded = bytearray()
    _append_uleb128(encoded, value)
    return bytes(encoded)


def _record_header(
    kind: int,
    thread_token: int,
    sequence: int,
    item_count: int,
    stored_len: int,
    payload_crc: int,
) -> bytes:
    if not 0 <= stored_len <= 0xFFFFFFFF:
        raise OverflowError("Kolo v3 record exceeds u32")
    header = bytearray(
        struct.pack(
            "<4sB3xIQIIII",
            RECORD_MAGIC,
            kind,
            thread_token,
            sequence,
            item_count,
            stored_len,
            stored_len,
            payload_crc,
        )
    )
    header.extend(struct.pack("<I", _crc32(header)))
    return bytes(header)


def _packed(value) -> bytes:
    return msgpack.packb(value, use_bin_type=True)


def _thread_value(thread: object, name: str):
    if isinstance(thread, Mapping):
        return thread.get(name)
    value = getattr(thread, name, None)
    return value() if name == "is_alive" and callable(value) else value


def iter_v3_trace_chunks(
    *,
    command_line_args,
    current_commit_sha,
    current_thread_id: str,
    meta: dict,
    timestamp: float,
    trace_id: str,
    trace_name: str | None,
    threads: Mapping[str, object],
    frames_by_thread: Mapping[str, Sequence[bytes]],
    value_table: Mapping[int, str | bytes] | Sequence[str | bytes] = (),
    root_trace_id: str | None = None,
) -> Iterator[bytes]:
    """Yield one complete write-once v3 container without joining frame bytes."""
    header_payload = _packed({"trace_id": trace_id, "timestamp": timestamp})
    header = struct.pack(
        "<8sHBBIII",
        HEADER_MAGIC,
        3,
        2,
        0,
        0,
        len(header_payload),
        _crc32(header_payload),
    )
    yield header
    yield header_payload
    offset = HEADER_LEN + len(header_payload)
    index_entries: list[list[int]] = []
    layouts: dict[int, list[list[int]]] = {}

    # A recoverable prefix must never contain a frame reference whose value
    # record appears later in the file. Publish the bounded dictionary first
    # on materialized/Python paths; the native streaming writer publishes
    # each entry lazily immediately before its first referencing chunk.
    value_items = (
        value_table.items()
        if isinstance(value_table, Mapping)
        else enumerate(value_table)
    )
    for value_id, value in value_items:
        if not 0 <= value_id <= 0xFFFFFFFF:
            raise OverflowError("Kolo v3 value ID exceeds u32")
        value_table_payload = _packed(value)
        record_header = _record_header(
            VALUE_TABLE,
            0,
            value_id,
            1,
            len(value_table_payload),
            _crc32(value_table_payload),
        )
        index_entries.append(
            [VALUE_TABLE, offset, len(value_table_payload), 0, value_id, 1]
        )
        yield record_header
        yield value_table_payload
        offset += RECORD_HEADER_LEN + len(value_table_payload)

    thread_ids = list(dict.fromkeys((*frames_by_thread.keys(), *threads.keys())))
    thread_tokens = {thread_id: index + 1 for index, thread_id in enumerate(thread_ids)}

    for thread_id, frames in frames_by_thread.items():
        token = thread_tokens[thread_id]
        sequence = 0
        spans = []
        chunk: list[bytes] = []
        chunk_bytes = 0

        def emit_chunk() -> Iterable[bytes]:
            nonlocal chunk, chunk_bytes, offset, sequence
            if not chunk:
                return ()
            # Build one sidecar buffer instead of allocating a temporary bytes
            # object for every frame length. A Python-backend trace can contain
            # tens of thousands of frames, so the per-frame allocations made
            # post-capture persistence contend materially with the application.
            encoded_lengths = bytearray()
            for frame in chunk:
                _append_uleb128(encoded_lengths, len(frame))
            sidecar = bytes(encoded_lengths)
            stored_len = len(sidecar) + chunk_bytes
            record_header = _record_header(
                CHUNK, token, sequence, len(chunk), stored_len, 0
            )
            index_entries.append(
                [CHUNK, offset, stored_len, token, sequence, len(chunk)]
            )
            spans.append([sequence, 0, len(chunk)])
            offset += RECORD_HEADER_LEN + stored_len
            parts = chain((record_header, sidecar), chunk)
            sequence += 1
            chunk = []
            chunk_bytes = 0
            return parts

        for frame in frames:
            if chunk and chunk_bytes + len(frame) > CHUNK_TARGET:
                yield from emit_chunk()
            chunk.append(frame)
            chunk_bytes += len(frame)
            if chunk_bytes >= CHUNK_TARGET:
                yield from emit_chunk()
        yield from emit_chunk()
        layouts[token] = spans

    for sequence, (thread_id, thread) in enumerate(threads.items()):
        token = thread_tokens[thread_id]
        payload = _packed(
            {
                "thread_id": thread_id,
                "name": _thread_value(thread, "name"),
                "ident": _thread_value(thread, "ident"),
                "native_id": _thread_value(thread, "native_id"),
                "daemon": _thread_value(thread, "daemon"),
                "is_alive": _thread_value(thread, "is_alive"),
            }
        )
        record_header = _record_header(
            THREAD_META, token, sequence, 1, len(payload), _crc32(payload)
        )
        index_entries.append([THREAD_META, offset, len(payload), token, sequence, 1])
        yield record_header
        yield payload
        offset += RECORD_HEADER_LEN + len(payload)

    metadata = {
        "command_line_args": command_line_args,
        "current_commit_sha": current_commit_sha,
        "current_thread_id": current_thread_id,
        "meta": meta,
        "timestamp": timestamp,
        "trace_id": trace_id,
        "trace_name": trace_name,
        "frames_of_interest": [],
        "frames": {},
    }
    if root_trace_id is not None:
        metadata["root_trace_id"] = root_trace_id
    metadata_payload = _packed(metadata)
    record_header = _record_header(
        METADATA, 0, 0, 1, len(metadata_payload), _crc32(metadata_payload)
    )
    index_entries.append([METADATA, offset, len(metadata_payload), 0, 0, 1])
    yield record_header
    yield metadata_payload
    offset += RECORD_HEADER_LEN + len(metadata_payload)

    index_offset = offset
    index_payload = _packed({"records": index_entries, "threads": layouts})
    yield _record_header(
        INDEX,
        0,
        0,
        len(index_entries),
        len(index_payload),
        _crc32(index_payload),
    )
    yield index_payload
    offset += RECORD_HEADER_LEN + len(index_payload)
    footer_prefix = struct.pack(
        "<8sQQ", FOOTER_MAGIC, index_offset, offset + FOOTER_LEN
    )
    yield footer_prefix + struct.pack("<II", _crc32(footer_prefix), 0)


def build_v3_trace(**kwargs) -> bytes:
    """Explicitly materialize a v3 container for upload/build_trace callers."""
    return b"".join(iter_v3_trace_chunks(**kwargs))
