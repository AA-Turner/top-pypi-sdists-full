"""PipelineContext — the shared in-memory cache passed to every detector.

The cache lives for the duration of a single analyze_file() call. Detectors
read from it and write to it so expensive work (opening a PDF Document,
rendering pages, extracting per-page text) happens exactly once per file.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from .protocol import DetectorResult


@dataclass
class ResolvedSettings:
    """Output of preferences.resolve(). Drives what the dispatcher actually runs."""

    enabled_detectors: set[str] = field(default_factory=set)
    detector_tiers: dict[str, tuple[str, ...]] = field(default_factory=dict)
    detector_params: dict[str, dict[str, Any]] = field(default_factory=dict)
    pattern_catalog: list[dict[str, Any]] = field(default_factory=list)
    default_redaction_mode: str = "reversible"
    substitute_formats: dict[str, str] = field(default_factory=dict)
    inline_payload_limit_bytes: int = 256 * 1024
    ocr_provider_id: str = "tesseract"


@dataclass
class PipelineContext:
    file_id: str
    owner_id: str
    mime_type: str
    bytes_in_memory: bytes
    settings: ResolvedSettings
    emit: Callable[[DetectorResult], Awaitable[None]]
    cache: dict[str, Any] = field(default_factory=dict)
    started_at: float = field(default_factory=time.monotonic)

    def cache_get(self, key: str) -> Any:
        return self.cache.get(key)

    def cache_set(self, key: str, value: Any) -> None:
        self.cache[key] = value

    def elapsed_ms(self) -> int:
        return int((time.monotonic() - self.started_at) * 1000)


__all__ = ["PipelineContext", "ResolvedSettings"]
