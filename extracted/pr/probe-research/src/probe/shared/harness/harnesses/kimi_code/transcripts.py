"""Kimi Code's TranscriptLocator: which files under its root are sessions."""

from __future__ import annotations


def _kimi():
    from probe.foundation.harness_registry import get_registry

    return get_registry().get(KIMI)
from probe.cli.imports.transcripts.roots import KIMI  # noqa: E402 -- pieces need each other; the front door loads this one first
