"""Streaming msgpack trace writer that splices pre-packed frame bytes in
place, without round-tripping them through Python dicts.

The profiler/monitoring backends store each captured frame as already-
serialized ``bytes`` (so ``sum(len(frame) for frame …)`` can drive subtree
flush byte accounting cheaply). When it's time to save — whether the root
trace or a flushed subtree — we need those frame bytes to land inside the
outer trace's ``threads.<tid>.frames`` array. Re-encoding every frame just
to pack the outer map would double the work for no reason and is
prohibitively expensive for 500MB+ flushed subtrees.

Instead, this module writes the outer map header and metadata fields
normally, then for each thread's ``frames`` key writes a msgpack array
header followed by a raw concat of the pre-packed frame bytes. msgpack is
a self-describing concatenative format, so ``<array header><obj1><obj2>…``
is a valid array — no re-encoding required.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

import msgpack


def _pack_key_value(parts: list[bytes], packer: msgpack.Packer, key: str, value: Any):
    parts.append(packer.pack(key))
    parts.append(packer.pack(value))


def build_serialized_trace(
    *,
    command_line_args,
    current_commit_sha,
    current_thread_id: str,
    meta: dict[str, Any],
    timestamp: float,
    trace_id: str,
    trace_name: str | None,
    threads: Mapping[str, Any],
    frames_by_thread: Mapping[str, Sequence[bytes]],
    root_trace_id: str | None = None,
) -> bytes:
    packer = msgpack.Packer(autoreset=True)
    parts: list[bytes] = []

    map_len = 10 + (1 if root_trace_id is not None else 0)
    parts.append(packer.pack_map_header(map_len))
    _pack_key_value(parts, packer, "command_line_args", command_line_args)
    _pack_key_value(parts, packer, "current_commit_sha", current_commit_sha)
    _pack_key_value(parts, packer, "current_thread_id", current_thread_id)
    _pack_key_value(parts, packer, "meta", meta)
    _pack_key_value(parts, packer, "timestamp", timestamp)
    _pack_key_value(parts, packer, "trace_id", trace_id)
    _pack_key_value(parts, packer, "trace_name", trace_name)
    if root_trace_id is not None:
        _pack_key_value(parts, packer, "root_trace_id", root_trace_id)
    _pack_key_value(parts, packer, "frames_of_interest", [])
    _pack_key_value(parts, packer, "frames", {})

    parts.append(packer.pack("threads"))
    parts.append(packer.pack_map_header(len(threads)))
    for thread_id, thread in threads.items():
        parts.append(packer.pack(thread_id))

        has_frames = thread_id in frames_by_thread
        parts.append(packer.pack_map_header(5 + (1 if has_frames else 0)))
        _pack_key_value(parts, packer, "name", thread.name)
        _pack_key_value(parts, packer, "ident", getattr(thread, "ident", None))
        _pack_key_value(parts, packer, "native_id", getattr(thread, "native_id", None))
        _pack_key_value(parts, packer, "daemon", thread.daemon)
        _pack_key_value(parts, packer, "is_alive", thread.is_alive())

        if has_frames:
            frames = frames_by_thread[thread_id]
            parts.append(packer.pack("frames"))
            parts.append(packer.pack_array_header(len(frames)))
            parts.extend(frames)

    return b"".join(parts)
