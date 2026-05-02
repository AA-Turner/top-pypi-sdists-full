"""Snapshot JSON IO helpers for the CLI runtime."""

from __future__ import annotations

from collections.abc import Mapping
import json
import os
from pathlib import Path
from uuid import uuid4
from typing import Any


def load_snapshot_payload(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    payload = _decode_snapshot_json(text)
    if not isinstance(payload, Mapping):
        raise ValueError("snapshot payload must be a JSON object")
    return dict(payload)


def write_snapshot_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    try:
        tmp_path.write_text(json.dumps(dict(payload), indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp_path, path)
    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass


def _decode_snapshot_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        decoder = json.JSONDecoder()
        try:
            payload, end = decoder.raw_decode(text)
        except json.JSONDecodeError:
            raise error from None
        if text[end:].strip():
            return payload
        raise error
