from __future__ import annotations

import json
import base64
import hashlib
from os import PathLike
from typing import Any, cast
from pathlib import Path
from collections.abc import Mapping, Iterable


def fingerprint_payload(payload: Any) -> str:
    canonical = _canonicalize(payload)
    encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _canonicalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        typed_mapping = cast(Mapping[object, Any], value)
        dict_value = {str(key): _canonicalize(item) for key, item in typed_mapping.items()}
        source_type = dict_value.get("type")
        data = dict_value.get("data")
        if source_type == "base64" and isinstance(data, str):
            return {
                **{key: val for key, val in dict_value.items() if key != "data"},
                "data_sha256": _hash_base64_payload(data),
            }
        return dict(sorted(dict_value.items()))

    if isinstance(value, PathLike):
        return str(Path(cast(PathLike[str], value)))

    if isinstance(value, (str, bytes, bytearray, int, float, bool)) or value is None:
        if isinstance(value, (bytes, bytearray)):
            return {"bytes_sha256": hashlib.sha256(bytes(value)).hexdigest()}
        return value

    if isinstance(value, Iterable):
        return [_canonicalize(item) for item in cast(Iterable[Any], value)]

    return repr(value)


def _hash_base64_payload(data: str) -> str:
    try:
        raw = base64.b64decode(data, validate=True)
    except Exception:
        raw = data.encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
