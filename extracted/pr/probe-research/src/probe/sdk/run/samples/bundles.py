"""Per-(step, producer) bundles: one gzip file per kind where each sample is its own gzip member, so the
server reads one sample back by byte range (RL plan §3.3b-c). Written on local disk, uploaded at seal."""

from __future__ import annotations

import gzip
import hashlib
import os
import tempfile
import threading
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from ....generated.samples import BundleKind


def get_artifact_kind(kind: str) -> str:
    """The kind word a bundle or blob uploads under: the server files it as `other` and keeps the
    word (`meta.kind_label`), which keeps it out of the search index."""
    return f"sample_{kind}"


#: The kind word a text blob over 64 KiB uploads under.
TEXT_ARTIFACT_KIND = get_artifact_kind("text")


#: A bundle past this starts a new part: the upload door inspects at most 64 MiB.
BUNDLE_MAX_BYTES = 32 * 1024 * 1024


@dataclass
class Bundle:
    """One open bundle file: where it lives, what it holds, and the refs handed out for it. A ref
    is `{sha256, offset, length}` (`BundleRef`): its sha256 is filled in when the bundle closes."""

    kind: BundleKind
    step: int | None
    part: int
    path: Path
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    size: int = 0
    members: int = 0
    refs: list[dict] = field(default_factory=list)

    def append(self, payload: bytes) -> dict:
        """Write ``payload`` as one gzip member; its ref, whose sha256 comes at close."""
        member = gzip.compress(payload, compresslevel=6, mtime=0)
        with open(self.path, "ab") as handle:
            handle.write(member)
        ref = {"offset": self.size, "length": len(member)}
        self.refs.append(ref)
        self.size += len(member)
        self.members += 1
        return ref

    def get_digest(self) -> str:
        """sha256 of the file as written."""
        digest = hashlib.sha256()
        with open(self.path, "rb") as handle:
            for block in iter(lambda: handle.read(1 << 20), b""):
                digest.update(block)
        return digest.hexdigest()


@dataclass(frozen=True)
class SealedBundle:
    """A bundle closed at its seal: what the seal declares and capture checks against storage."""

    id: str
    kind: BundleKind
    sha256: str
    size: int
    members: int

    def to_wire(self) -> dict:
        """As a seal declares it (`SealBundle`)."""
        return {"kind": str(self.kind), "sha256": self.sha256}


class Bundles:
    """A producer's open bundles, one per (kind, step). ``upload(bundle)`` sends a closed one
    (the run's artifact door, which copies the bytes into the outbox) and never raises; the file is
    removed after."""

    def __init__(self, folder: Path, upload: Callable[[Bundle], None]) -> None:
        self._folder = folder
        self._upload = upload
        self._open: dict[tuple[BundleKind, int | None], Bundle] = {}
        self._parts: dict[tuple[BundleKind, int | None], int] = {}
        self._lock = threading.Lock()

    def append(self, kind: BundleKind, step: int | None, payload: bytes) -> dict:
        """Add one sample's payload to its step's bundle of ``kind``; the sample's ref."""
        key = (kind, step)
        sealed: Bundle | None = None
        with self._lock:
            bundle = self._open.get(key)
            if bundle is not None and bundle.size >= BUNDLE_MAX_BYTES:
                sealed = self._open.pop(key)
                bundle = None
            if bundle is None:
                bundle = self._open_bundle(kind, step)
            ref = bundle.append(payload)
        if sealed is not None:
            self._send(sealed)
        return ref

    def close_step(self, step: int | None) -> list[SealedBundle]:
        """Close and upload every bundle of one step; what the step's seal declares. Every ref
        handed out for them has its sha256 from here on."""
        with self._lock:
            keys = [key for key in self._open if key[1] == step]
            closing = [self._open.pop(key) for key in keys]
        return [sealed for sealed in map(self._send, closing) if sealed is not None]

    def get_open_steps(self) -> list[int | None]:
        """Steps with a bundle still open."""
        with self._lock:
            return sorted({key[1] for key in self._open}, key=lambda step: (step is None, step or 0))

    def _open_bundle(self, kind: BundleKind, step: int | None) -> Bundle:
        key = (kind, step)
        part = self._parts.get(key, 0) + 1
        self._parts[key] = part
        self._folder.mkdir(parents=True, exist_ok=True)
        label = "none" if step is None else str(step)
        handle, name = tempfile.mkstemp(prefix=f"{kind}-{label}-p{part}-", suffix=".gz", dir=self._folder)
        os.close(handle)
        bundle = Bundle(kind=kind, step=step, part=part, path=Path(name))
        self._open[key] = bundle
        return bundle

    def _send(self, bundle: Bundle) -> SealedBundle | None:
        """Digest, upload and remove one closed bundle. The digest is declared even when the upload
        fails, so capture answers "no: bundle missing" rather than never knowing of it."""
        try:
            sealed = SealedBundle(
                id=bundle.id,
                kind=bundle.kind,
                sha256=bundle.get_digest(),
                size=bundle.size,
                members=bundle.members,
            )
        except OSError:
            sealed = None
        for ref in bundle.refs:
            ref["sha256"] = sealed.sha256 if sealed is not None else None
        try:
            if sealed is not None:
                self._upload(bundle)
        finally:
            try:
                bundle.path.unlink()
            except OSError:
                pass
        return sealed
