"""Characterization recorder: run a delivery scenario and dump everything it did, normalised.

Goldens are recorded on unchanged main code before a function is cut into stages, then must stay
byte-identical (`PROBE_GOLDENS_RECORD=1` re-records). DESIGN.md beside this file says what each holds."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Callable

import httpx

RECORDED = Path(__file__).with_name("recorded")
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
_HEX32 = re.compile(r"\b(?:[0-9a-f]{64}|[0-9a-f]{32})\b")
_ISO = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)?")
_NS_NAME = re.compile(r"(^|-)\d{16,}(?=-)")
_PID_HOST = re.compile(r"sdk:[^:\"]+:\d+:([0-9a-f]{8}\b)?")
_TIME_KEYS = re.compile(r"(_at|_ns|_ts|_time|time|deadline|expires|_since|since|wake_by|lease)$")


class Normaliser:
    """Map run-to-run values (ids, times, tmp paths, pids) to stable placeholders, first seen first."""

    def __init__(self, tmp: Path):
        self.tmp = str(tmp)
        self.ids: dict[str, str] = {}

    def text(self, value: str) -> str:
        value = value.replace(self.tmp, "<tmp>")
        value = _ISO.sub("<iso>", value)
        value = _PID_HOST.sub(lambda m: "sdk:<host>:<pid>:" + ("<producer>" if m.group(1) else ""), value)
        value = re.sub(r"sdk_[^_/]+_\d+_[0-9a-f]{8}", "sdk_<host>_<pid>_<producer>", value)
        value = re.sub(r"\boffline-[0-9a-f]{8}\b", "offline-<hex8>", value)
        value = re.sub(r"would leave \d+ bytes free", "would leave <n> bytes free", value)  # this disk's free space
        value = re.sub(r"-\d{16,}-", "-<ns>-", value)
        value = _UUID.sub(lambda m: self._id(m.group(0)), value)
        return _HEX32.sub(lambda m: self._id(m.group(0)), value)

    def _id(self, raw: str) -> str:
        return self.ids.setdefault(raw, f"<id{len(self.ids) + 1}>")

    def value(self, value: Any, key: str = "") -> Any:
        if dataclasses.is_dataclass(value) and not isinstance(value, type):
            return self.value({f.name: getattr(value, f.name) for f in dataclasses.fields(value)}, key)
        if isinstance(value, dict):
            return {self.text(str(k)): self.value(v, str(k)) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))}
        if isinstance(value, (set, frozenset)):
            return sorted((self.value(v) for v in value), key=repr)
        if isinstance(value, (list, tuple)):
            return [self.value(v) for v in value]
        if isinstance(value, (int, float)) and not isinstance(value, bool) and _TIME_KEYS.search(key):
            return "<time>"
        if isinstance(value, str):
            if _TIME_KEYS.search(key) and value:
                return "<time>"
            return self.text(value)
        if isinstance(value, Path):
            return self.text(str(value))
        if value is None or isinstance(value, (bool, int, float)):
            return value
        if hasattr(value, "__dict__") and not isinstance(value, type):
            return {"<object>": type(value).__name__, **self.value(vars(value))}
        return f"<{type(value).__name__}>"

    def name(self, filename: str) -> str:
        return self.text(_NS_NAME.sub(lambda m: m.group(1) + "<ns>", filename))


def dump_tree(root: Path, norm: Normaliser) -> dict:
    """Every file under `root`: JSON parsed and normalised, other bytes as size + sha256."""
    out: dict = {}
    if not root.exists():
        return out
    for path in sorted(root.rglob("*"), key=lambda p: str(p)):
        if path.is_dir():
            continue
        parts = [norm.name(part) for part in path.relative_to(root).parts]
        if len(parts) > 1 and parts[-2] == ".run-locks":
            parts[-1] = "<slot>.lock"  # a hash of the run id: its slot varies run to run
        rel = "/".join(parts)
        data = path.read_bytes()
        if path.suffix == ".json":
            try:
                out[rel] = norm.value(json.loads(data))
                continue
            except ValueError:
                pass
        if path.suffix in (".lock", ".db", ".sqlite") or path.name.endswith((".lock", "-journal", "-wal", "-shm")):
            out[rel] = "<lock-or-db>"
            continue
        try:
            text = data.decode()
        except UnicodeDecodeError:
            text = None
        if text is not None and len(text) < 4096 and path.parent.name != "blobs":
            out[rel] = {"text": norm.text(re.sub(r"\d{9,}(\.\d+)?", "<num>", text))}
            continue
        out[rel] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()[:16]}
    return dict(sorted(out.items()))


def record_transport_sleeps(monkeypatch, into: list) -> None:
    """Record the pauses the transport takes between attempts (not sleeping); other sleeps run."""
    import sys
    import time

    real = time.sleep

    def sleep(seconds: float) -> None:
        if sys._getframe(1).f_globals.get("__name__", "").startswith("probe.sdk.delivery.transport"):
            into.append(round(seconds, 3))
        else:
            real(seconds)

    monkeypatch.setattr(time, "sleep", sleep)


def describe_error(exc: BaseException, norm: Normaliser) -> dict:
    attrs = {k: getattr(exc, k) for k in ("status", "retry_after", "sent", "unreachable", "permanent", "detail")
             if hasattr(exc, k)}
    return {"type": type(exc).__name__, "message": norm.text(str(exc)), **norm.value(attrs)}


class HttpScript:
    """Wrap a handler: answer from a script where one matches, record every request."""

    def __init__(self, handler: Callable[[httpx.Request], httpx.Response], norm: Normaliser):
        self.handler = handler
        self.norm = norm
        self.rules: list[list] = []  # [method, path regex, remaining count, answer]
        self.log: list[dict] = []

    def answer(self, method: str, path: str, answer, times: int = 1) -> None:
        """`answer`: an int status, (status, json, headers), or an exception instance to raise."""
        self.rules.append([method, re.compile(path), times, answer])

    def __call__(self, request: httpx.Request) -> httpx.Response:
        body: Any
        try:
            body = json.loads(request.content) if request.content else None
        except ValueError:
            body = {"bytes": len(request.content), "sha256": hashlib.sha256(request.content).hexdigest()[:16]}
        entry = {
            "method": request.method,
            "path": self.norm.text(request.url.path),
            "query": self.norm.value(dict(sorted(request.url.params.items()))),
            "headers": sorted(h for h in request.headers.keys() if h not in ("content-length",)),
            "body": self.norm.value(body),
        }
        for rule in self.rules:
            method, pattern, left, answer = rule
            if left and request.method == method and pattern.search(request.url.path):
                rule[2] -= 1
                entry["scripted"] = answer if isinstance(answer, int) else (
                    type(answer).__name__ if isinstance(answer, BaseException) else answer[0])
                self.log.append(entry)
                if isinstance(answer, BaseException):
                    raise answer
                if isinstance(answer, int):
                    return httpx.Response(answer, json={"detail": f"scripted {answer}"})
                headers = answer[2] if len(answer) > 2 else {}
                return httpx.Response(answer[0], json=answer[1], headers=headers)
        response = self.handler(request)
        entry["status"] = response.status_code
        self.log.append(entry)
        return response


def check(name: str, record: dict, root: Path = RECORDED) -> None:
    """Compare `record` with <root>/<name>.json; PROBE_GOLDENS_RECORD=1 writes it instead."""
    path = root / f"{name}.json"
    text = json.dumps(record, indent=1, sort_keys=True, default=str) + "\n"
    if os.environ.get("PROBE_GOLDENS_RECORD") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return
    assert path.exists(), f"no golden {path.name}: record it on unchanged main (PROBE_GOLDENS_RECORD=1)"
    assert text == path.read_text(), f"golden {path.name} changed"
