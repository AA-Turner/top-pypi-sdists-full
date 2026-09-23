"""Atomic local trainer state paired with River training checkpoints."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

import numpy as np

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
        if not self.path.exists():
            return None
        state = json.loads(self.path.read_text())
        storage = state.pop("__river_arrays__", None)
        if not isinstance(storage, dict) or storage.get("version") != 1:
            raise ValueError("checkpoint requires binary array storage version 1")
        name = storage["file"]
        if not re.fullmatch(r"trainer-arrays-[0-9a-f]{32}\.bin", name):
            raise ValueError("invalid checkpoint array filename")
        payload = (self.directory / name).read_bytes()
        if (
            len(payload) != storage["bytes"]
            or hashlib.sha256(payload).hexdigest() != storage["sha256"]
        ):
            raise ValueError("checkpoint array integrity verification failed")
        return _unpack_arrays(decode_state(state), payload)

    def save(self, state, *, images=None):
        if "__river_arrays__" in state:
            raise ValueError("checkpoint state contains reserved storage metadata")
        # Numeric leaves leave the object tree before the generic handle codecs
        # and image traversal, avoiding repeated Python walks over every token.
        binary = self.directory / f"trainer-arrays-{uuid.uuid4().hex}.bin"
        with binary.open("x+b") as stream:
            state = _pack_arrays(state, stream)
            size = stream.tell()
            stream.flush()
            stream.seek(0)
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
            os.fsync(stream.fileno())
        self._sync_directory()
        state = decode_state(state)
        retained = self.images.copy_images(state, images)
        state["__river_arrays__"] = {
            "version": 1,
            "file": binary.name,
            "bytes": size,
            "sha256": digest,
        }
        temporary = self.path.with_suffix(".tmp")
        with temporary.open("w") as stream:
            stream.write(
                json.dumps(
                    encode_state(state),
                    ensure_ascii=False,
                    separators=(",", ":"),
                    allow_nan=False,
                )
            )
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, self.path)
        self._sync_directory()
        # Only a durably committed metadata file may release the previous blob.
        for path in self.directory.glob("trainer-arrays-*.bin"):
            if path != binary:
                path.unlink()
        self.images.prune(retained)

    def _sync_directory(self):
        descriptor = os.open(self.directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _pack_arrays(value, stream):
    if isinstance(value, dict):
        if "__river_array__" in value:
            raise ValueError("checkpoint state contains reserved array metadata")
        return {key: _pack_arrays(item, stream) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        if len(value) >= 64:
            kind = type(value[0])
            dtype = {int: "<i8", float: "<f8", bool: "|b1"}.get(kind)
            if dtype and all(type(item) is kind for item in value):
                try:
                    array = np.asarray(value, dtype=dtype)
                except OverflowError:
                    # Python integers outside int64 remain lossless JSON numbers.
                    return list(value)
                if kind is int:
                    lower, upper = array.min(), array.max()
                    if lower >= 0 and upper <= 255:
                        dtype = "|u1"
                    elif lower >= -(2**31) and upper < 2**31:
                        dtype = "<i4"
                    array = array.astype(dtype, copy=False)
                if kind is float and not np.isfinite(array).all():
                    raise ValueError("checkpoint arrays must contain finite values")
                offset = stream.tell()
                stream.write(array.tobytes())
                return {"__river_array__": [offset, len(value), dtype]}
        return [_pack_arrays(item, stream) for item in value]
    return value


def _unpack_arrays(value, payload):
    if isinstance(value, dict):
        if set(value) == {"__river_array__"}:
            offset, count, dtype = value["__river_array__"]
            if (
                dtype not in {"<i8", "<i4", "|u1", "<f8", "|b1"}
                or type(offset) is not int
                or type(count) is not int
                or offset < 0
                or count < 0
                or offset + count * np.dtype(dtype).itemsize > len(payload)
            ):
                raise ValueError("invalid checkpoint array bounds or dtype")
            return np.frombuffer(
                payload, dtype=dtype, count=count, offset=offset
            ).tolist()
        return {key: _unpack_arrays(item, payload) for key, item in value.items()}
    if isinstance(value, list):
        return [_unpack_arrays(item, payload) for item in value]
    return value
