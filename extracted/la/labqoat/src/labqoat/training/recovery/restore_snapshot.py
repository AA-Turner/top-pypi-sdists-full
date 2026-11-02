"""Verified opaque payload and exact immutable metadata supplied to a restoration adapter."""

from dataclasses import dataclass
from pathlib import Path

from labqoat.manifests import Manifest
from labqoat.training.recovery.restore_envelope import RestoreEnvelope


@dataclass(frozen=True)
class RestoreSnapshot:
    """Keep scoped scratch bytes and accepted state requirements together through deserialization."""

    path: Path
    manifest: Manifest
    envelope: RestoreEnvelope
