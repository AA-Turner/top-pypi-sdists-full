"""Emitter SpanHook that stamps sdk_version (+ agent_name) onto the root span."""

from __future__ import annotations


class SdkSourceEnricher:
    """Stamps ``metadata.sdk_version`` (+ ``agent_name``) onto the root span
    (``id == trace_id``) only, never overriding caller-set values."""

    def __init__(self, sdk_version: str, agent_name: str | None = None) -> None:
        self._sdk_version = sdk_version
        self._agent_name = agent_name

    def __call__(self, span: dict) -> None:
        trace_id = span.get("trace_id")
        if trace_id is None or span.get("id") != trace_id:
            return
        metadata = span.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}
            span["metadata"] = metadata
        metadata.setdefault("sdk_version", self._sdk_version)
        if self._agent_name:
            metadata.setdefault("agent_name", self._agent_name)
