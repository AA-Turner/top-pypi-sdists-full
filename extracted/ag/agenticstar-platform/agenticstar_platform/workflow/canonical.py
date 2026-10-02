"""RFC 8785 (JCS) 相当の正規化と SHA-256（marketplace-3.0 00 §4）。

front（Node、JSON.stringify ベースの JCS）・executer-marketplace（`src/core/canonical.py`）と同じ規約:
- object のキーは UTF-16 code unit 順、区切りに空白なし、非 ASCII はエスケープしない
- 数値は有限の IEEE 754 倍精度で ES6 の最短表現。安全整数（|n| <= 2^53-1）を超える整数は倍精度として扱う
"""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any

_MAX_SAFE_INT = 2**53 - 1


class CanonicalizationError(ValueError):
    pass


def _utf16_key(s: str) -> list[int]:
    b = s.encode("utf-16-be")
    return [int.from_bytes(b[i:i + 2], "big") for i in range(0, len(b), 2)]


def _fmt_number(v: float) -> str:
    if not math.isfinite(v):
        raise CanonicalizationError("non-finite number is not allowed in canonical JSON")
    if v == 0:
        return "0"
    if v == int(v) and abs(v) <= _MAX_SAFE_INT + 1:
        return str(int(v))
    r = repr(v)
    mantissa, _, exp = r.partition("e")
    if not exp:
        return r[:-2] if r.endswith(".0") else r
    e = int(exp)
    digits = mantissa.replace("-", "").replace(".", "")
    sign = "-" if v < 0 else ""
    if -7 < e < 21:
        if e >= 0:
            int_part = digits[: e + 1].ljust(e + 1, "0")
            frac = digits[e + 1:]
            return sign + int_part + ("." + frac if frac else "")
        return sign + "0." + "0" * (-e - 1) + digits
    m = digits[0] + ("." + digits[1:] if len(digits) > 1 else "")
    return f"{sign}{m}e{'+' if e > 0 else '-'}{abs(e)}"


def canonical_json(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        if abs(value) > _MAX_SAFE_INT:
            return _fmt_number(float(value))  # JS の Number と同じ扱い
        return str(value)
    if isinstance(value, float):
        return _fmt_number(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(canonical_json(v) for v in value) + "]"
    if isinstance(value, dict):
        items = []
        for k in sorted(value.keys(), key=lambda k: _utf16_key(str(k))):
            if not isinstance(k, str):
                raise CanonicalizationError("object keys must be strings")
            items.append(json.dumps(k, ensure_ascii=False) + ":" + canonical_json(value[k]))
        return "{" + ",".join(items) + "}"
    raise CanonicalizationError(f"unsupported type for canonical JSON: {type(value).__name__}")


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path, chunk: int = 1024 * 1024) -> tuple[str, int]:
    """ファイル内容の SHA-256（小文字 hex）と bytes 数。改行の暗黙変換はしない。"""
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
            size += len(b)
    return h.hexdigest(), size
