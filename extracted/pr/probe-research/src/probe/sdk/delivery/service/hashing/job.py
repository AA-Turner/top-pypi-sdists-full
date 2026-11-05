"""HashJob: one `files.hash` request (plan D20), checked: the files a training process opened (one fd
each) and how to hash each: `full` (sha256, newlines and the last byte for row counts) or `edges` (the
first and last `edge_bytes`, the lineage fingerprint's digest). The wire shape: DESIGN.md beside this."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

from probe.foundation.service_api.wire import invalid_params

MODES = frozenset({"full", "edges"})
#: `edges`' `edge_bytes`, at most (the lineage fingerprint reads 4 MiB at each end).
MAX_EDGE_BYTES = 64 << 20
#: A job's `timeout`, at most (seconds): past it, what is left is answered `cut`.
MAX_TIMEOUT_S = 3600.0


@dataclass
class HashJob:
    files: list[dict]
    fds: list[int]
    #: Monotonic: a job still queued past it is answered `expired`; a hash running past it, `cut`.
    deadline: float
    queued_at: float = field(default_factory=time.monotonic)

    def close(self) -> None:
        for fd in self.fds:
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds = []


def need_files_hash(parameters: dict, fds: list[int]) -> HashJob:
    """`files.hash`'s parameters, checked; the job owns `fds` from here (closed on a refusal too)."""
    try:
        files = parameters.get("files")
        if not isinstance(files, list) or len(files) != len(fds) or not files:
            raise invalid_params("files must list one {mode, ...} per passed fd")
        checked = [_need_file(item) for item in files]
        timeout = parameters.get("timeout", 600.0)
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not 0 < timeout <= MAX_TIMEOUT_S:
            raise invalid_params(f"timeout must be seconds, at most {MAX_TIMEOUT_S:.0f}")
        return HashJob(files=checked, fds=list(fds), deadline=time.monotonic() + float(timeout))
    except BaseException:
        for fd in fds:
            try:
                os.close(fd)
            except OSError:
                pass
        raise


def _need_file(item: object) -> dict:
    if not isinstance(item, dict) or item.get("mode") not in MODES:
        raise invalid_params(f"each file needs a mode, one of {sorted(MODES)}")
    out = {"mode": item["mode"], "count_lines": bool(item.get("count_lines"))}
    if item["mode"] == "edges":
        size, edge = item.get("size"), item.get("edge_bytes")
        if not all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in (size, edge)) \
                or not 0 < edge <= MAX_EDGE_BYTES:
            raise invalid_params(f"edges needs the observed size and edge_bytes (at most {MAX_EDGE_BYTES})")
        out.update(size=size, edge_bytes=edge)
    return out
