"""One ART checkpoint on the run (RL plan §6.2): a LoRA adapter folder up to 256 MiB is uploaded, a bigger one
is recorded where it is with the sha256 of its file manifest; either way the weight version names it."""

from __future__ import annotations

import hashlib
import os
import re
from collections.abc import Callable
from typing import Any

from probe.sdk.artifact.hashing import local_file_uri

from .. import _checkpoints

#: A checkpoint at most this big is uploaded whole; past it, only its location and digest are kept.
MAX_UPLOAD_BYTES = 256 * 1024 * 1024
_SAFE_NAME = re.compile(r"[^A-Za-z0-9_.-]+")
#: ServerlessBackend keeps checkpoints as W&B artifacts (`serverless/backend.py:383-384`): a pointer only.
WANDB_ARTIFACT_SCHEME = "wandb-artifact://"


def get_folder_files(path: str) -> list[tuple[str, str]]:
    """Every regular file under ``path`` (a file is its own one), as (relative path, full path), sorted."""
    if os.path.isfile(path):
        return [(os.path.basename(path), path)]
    found = []
    for root, dirs, names in os.walk(path, followlinks=False):
        dirs.sort()
        for name in sorted(names):
            full = os.path.join(root, name)
            if os.path.isfile(full) and not os.path.islink(full):
                found.append((os.path.relpath(full, path).replace(os.sep, "/"), full))
    return found


def get_manifest_sha256(files: list[tuple[str, str]]) -> str:
    """One digest for a folder: sha256 over `<path>\\0<file sha256>\\n` per file, sorted by path."""
    manifest = hashlib.sha256()
    for rel, full in files:
        digest = hashlib.sha256()
        with open(full, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        manifest.update(f"{rel}\0{digest.hexdigest()}\n".encode())
    return manifest.hexdigest()


def record_checkpoint(
    run: Any, path: str, *, name: str, step: int, warn: Callable[[str, str], None], taken: dict[str, str]
) -> dict:
    """Record the checkpoint at ``path`` (saved by step ``step``) and return its ref for the weight
    version: `{uri, sha256, step}`. ``taken`` is this run's set names so far (`_checkpoints.upload_set`)."""
    files = get_folder_files(path)
    size = sum(os.path.getsize(full) for _, full in files)
    sha256 = get_manifest_sha256(files)
    meta = {"framework": "art", "manifest_sha256": sha256, "step": step}
    label = _SAFE_NAME.sub("_", name) or "checkpoint"
    if files and size <= MAX_UPLOAD_BYTES:
        _checkpoints.upload_set(
            run, path, name=label, step=step, meta=meta, size=size, strict=False, warn=warn, taken=taken
        )
    else:
        run.log_artifact(
            _checkpoints.set_name(label, step),
            path=path,
            kind="checkpoint",
            reference=True,
            allow_missing=True,
            size_bytes=size,
            step_index=step,
            meta=meta,
            strict=False,
        )
    return {"uri": local_file_uri(os.path.abspath(path)), "sha256": sha256, "step": step}


def make_artifact_ref(artifact_name: str, step: int) -> dict:
    """A ServerlessBackend checkpoint: where W&B keeps it. Probe never reads it (no W&B anywhere)."""
    return {"uri": WANDB_ARTIFACT_SCHEME + artifact_name, "step": step}
