"""Exact success results for local desktop operations."""

from __future__ import annotations

from typing import Literal

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind
from pydantic import Field

_MAX_SAFE_INTEGER = 9_007_199_254_740_991


class TranscriptSegmentResult(KindSubModel):
    start_s: float = Field(ge=0)
    end_s: float = Field(ge=0)
    text: str = Field(max_length=4_000)


@kind(
    "desktop_transcribe_result",
    disposition="record",
    label="Desktop Transcription Result",
    family="desktop",
    example={
        "text": "Hello.", "language": "en", "duration_s": 1.0, "model": "whisper-small",
        "elapsed_ms": 150, "segments": [{"start_s": 0.0, "end_s": 1.0, "text": "Hello."}],
        "segments_total": 1, "path": "/tmp/audio.wav",
    },
    maturity="placeholder",
)
class DesktopTranscribeResult(KindModel):
    text: str = Field(max_length=400_000)
    language: str = Field(max_length=8)
    duration_s: float = Field(ge=0)
    model: str = Field(
        min_length=1,
        max_length=128,
        pattern=r"^[a-z0-9][a-z0-9._-]*(/[a-z0-9][a-z0-9._-]*)?$",
    )
    elapsed_ms: int = Field(ge=0, le=_MAX_SAFE_INTEGER)
    segments: list[TranscriptSegmentResult] = Field(max_length=200)
    segments_total: int = Field(ge=0, le=20_000)
    path: str = Field(
        min_length=1,
        max_length=4_096,
        pattern=r"^(\/|[A-Za-z]:\/)[^\\\u0000]*$",
    )


class ProcessInfo(KindSubModel):
    pid: int = Field(ge=0, le=_MAX_SAFE_INTEGER)
    ppid: int | None = Field(ge=0, le=_MAX_SAFE_INTEGER)
    name: str = Field(max_length=256)
    command: str = Field(max_length=1_024)
    cpu_percent: float | None = Field(ge=0)
    memory_bytes: int | None = Field(ge=0, le=_MAX_SAFE_INTEGER)
    user: str | None = Field(max_length=128)


class ProcessPort(KindSubModel):
    port: int = Field(ge=1, le=65_535)
    protocol: Literal["tcp", "udp"]
    address: str = Field(max_length=64)
    pid: int | None = Field(ge=0, le=_MAX_SAFE_INTEGER)
    process: str | None = Field(max_length=256)


@kind(
    "desktop_process_list_result",
    disposition="record",
    label="Desktop Process List Result",
    family="desktop",
    example={"action": "list", "processes": [], "total": 0, "truncated": False},
    maturity="placeholder",
)
class DesktopProcessListResult(KindModel):
    action: Literal["list"]
    processes: list[ProcessInfo] = Field(max_length=500)
    total: int = Field(ge=0, le=_MAX_SAFE_INTEGER)
    truncated: bool


@kind(
    "desktop_process_ports_result",
    disposition="record",
    label="Desktop Process Ports Result",
    family="desktop",
    example={"action": "ports", "ports": []},
    maturity="placeholder",
)
class DesktopProcessPortsResult(KindModel):
    action: Literal["ports"]
    ports: list[ProcessPort] = Field(max_length=4000)


@kind(
    "desktop_process_kill_result",
    disposition="record",
    label="Desktop Process Kill Result",
    family="desktop",
    example={"action": "kill", "pid": 123, "signal": "SIGTERM", "exited": True},
    maturity="placeholder",
)
class DesktopProcessKillResult(KindModel):
    action: Literal["kill"]
    pid: int = Field(ge=1, le=_MAX_SAFE_INTEGER)
    signal: Literal["SIGTERM", "SIGKILL"]
    exited: bool


@kind(
    "desktop_clipboard_read_result",
    disposition="record",
    label="Desktop Clipboard Read Result",
    family="desktop",
    example={"action": "read", "text": "Copied text", "truncated": False},
    maturity="placeholder",
)
class DesktopClipboardReadResult(KindModel):
    action: Literal["read"]
    text: str = Field(max_length=1_048_576)
    truncated: bool


@kind(
    "desktop_clipboard_write_result",
    disposition="record",
    label="Desktop Clipboard Write Result",
    family="desktop",
    example={"action": "write", "bytes": 11},
    maturity="placeholder",
)
class DesktopClipboardWriteResult(KindModel):
    action: Literal["write"]
    bytes: int = Field(ge=0, le=_MAX_SAFE_INTEGER)


__all__ = [
    "DesktopClipboardReadResult", "DesktopClipboardWriteResult", "DesktopProcessKillResult",
    "DesktopProcessListResult", "DesktopProcessPortsResult", "DesktopTranscribeResult",
]
