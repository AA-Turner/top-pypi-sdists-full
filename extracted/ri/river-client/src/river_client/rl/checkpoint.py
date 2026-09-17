"""Atomic local trainer state paired with River training checkpoints."""

from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path

from river_client.images import ImageStore, map_images

from .config import _integer
from .trajectory import decode_state, encode_state


def identity_state(value):
    # Session handles change on recovery; content and renderer dimensions do not.
    return encode_state(
        map_images(
            value,
            lambda image: {
                "__river_image_content__": {
                    "sha256": image.sha256,
                    "byte_count": image.byte_count,
                    "width": image.width,
                    "height": image.height,
                }
            },
        )
    )


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(
            identity_state(value),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def row_order_fingerprint(rows):
    digest = hashlib.sha256()
    for row in rows:
        digest.update(
            json.dumps(
                identity_state(row),
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            ).encode()
        )
        digest.update(b"\n")
    return digest.hexdigest()


def training_plan_fingerprint(rows, groups_per_step, steps, *, repeat_dataset=True):
    digest = hashlib.sha256()
    for step in range(steps):
        digest.update(f"step:{step}\n".encode())
        for i in range(groups_per_step):
            index = step * groups_per_step + i
            if not repeat_dataset and index >= len(rows):
                break
            row = rows[index % len(rows)]
            digest.update(
                json.dumps(
                    identity_state(row),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode()
            )
            digest.update(b"\n")
    return digest.hexdigest()


@dataclass(frozen=True)
class Checkpointing:
    run_dir: str | Path
    weights_every: int = 20
    rollout_every: float = 60.0
    on_signal: tuple[str, ...] = ()

    def __post_init__(self):
        _integer(self.weights_every, "weights_every", 1)
        if "://" in str(self.run_dir):
            raise ValueError(
                "run_dir must be a durable local/shared filesystem directory; River currently stores weights, not arbitrary trainer metadata"
            )
        if (
            self.weights_every < 1
            or self.rollout_every <= 0
            or not math.isfinite(self.rollout_every)
        ):
            raise ValueError("checkpoint cadences must be finite and positive")
        if any(s not in {"SIGINT", "SIGTERM"} for s in self.on_signal):
            raise ValueError("supported checkpoint signals are SIGINT and SIGTERM")


class StateStore:
    def __init__(self, config: Checkpointing):
        self.directory = Path(config.run_dir)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "trainer.json"
        self.images = ImageStore(self.directory / "images")
        self._lock = None

    def __enter__(self):
        import fcntl

        self._lock = (self.directory / ".lock").open("a+")
        try:
            fcntl.flock(self._lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self._lock.close()
            raise RuntimeError(
                "another trainer owns this checkpoint directory"
            ) from None
        return self

    def __exit__(self, exc_type, exc, tb):
        self._lock.close()

    def load(self):
        return (
            decode_state(json.loads(self.path.read_text()))
            if self.path.exists()
            else None
        )

    def save(self, state, *, images=None):
        # Engine/trajectory state may already contain encoded handle markers.
        # Normalize before collecting references, including environment snapshots.
        state = decode_state(state)
        retained = self.images.copy_images(state, images)
        temporary = self.path.with_suffix(".tmp")
        with temporary.open("w") as stream:
            json.dump(
                encode_state(state),
                stream,
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            )
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, self.path)
        descriptor = os.open(self.directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        self.images.prune(retained)
