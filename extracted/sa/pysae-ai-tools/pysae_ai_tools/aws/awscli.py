"""Thin wrapper around the ``aws`` CLI returning parsed JSON.

Centralises the subprocess concerns shared by the spot commands: UTF-8 capture
with ``errors="replace"`` (Windows-safe), a clear message when the binary is
missing, uniform timeout/failure handling, and a process-wide **call log** that
counts every AWS API request (played / ok / failed / quota-blocked / served
from a local cache) so a command can report its AWS footprint.
"""

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT = 600

# Operation labels (``aws <service> <op>``) that are backed by a local TTL cache,
# mapped to their cache lifetime. Every other AWS operation always hits the API:
# spot prices and the CloudTrail eviction history must stay fresh, and the EKS
# discovery calls are cheap. TTLs reflect how fast each datum changes — a spot
# placement config is replayed free by AWS for 24h, on-demand list prices move
# only on occasional price drops, and hardware specs are immutable.
_DAY_SECONDS = 24 * 3600
OP_PLACEMENT = "ec2 get-spot-placement-scores"
OP_ONDEMAND = "pricing get-products"
OP_SPECS = "ec2 describe-instance-types"
CACHE_TTL_SECONDS: dict[str, float] = {
    OP_PLACEMENT: 1 * _DAY_SECONDS,
    OP_ONDEMAND: 7 * _DAY_SECONDS,
    OP_SPECS: 30 * _DAY_SECONDS,
}
CACHEABLE_OPERATIONS = frozenset(CACHE_TTL_SECONDS)


def humanize_duration(seconds: float) -> str:
    """Render a cache TTL compactly: ``86400`` → ``24h``, ``604800`` → ``7d``."""
    if seconds % _DAY_SECONDS == 0:
        days = int(seconds // _DAY_SECONDS)
        return f"{days}d" if days != 1 else "24h"
    hours = seconds / 3600
    return f"{hours:.0f}h"


# Substrings (case-insensitive) that mark an AWS *limit* failure — either the
# daily Spot-placement configuration budget (``MaxConfigLimitExceeded``, the one
# that silently turns most placement scores into ``n/a``) or a rate/throttle
# limit. Both are surfaced as quota-blocked so a run can report them honestly.
_QUOTA_MARKERS = (
    "maxconfiglimitexceeded",
    "requestlimitexceeded",
    "throttling",
    "rate exceeded",
    "toomanyrequests",
    "limitexceeded",
)


def is_quota_error(message: str) -> bool:
    """True when an ``aws`` stderr/error message denotes a quota or throttle limit."""
    low = message.lower()
    return any(marker in low for marker in _QUOTA_MARKERS)


class AwsCliError(RuntimeError):
    """An ``aws`` CLI call failed (non-zero exit, timeout, or missing binary)."""


class AwsQuotaError(AwsCliError):
    """An ``aws`` CLI call failed against a quota/throttle limit (see ``is_quota_error``)."""


@dataclass
class OpStats:
    """AWS call accounting for one API operation (e.g. ``ec2 get-spot-placement-scores``)."""

    ok: int = 0
    failed: int = 0
    quota_failed: int = 0  # subset of ``failed`` rejected by a quota/throttle limit
    cache_reads: int = 0  # served from a local cache, never reached the API
    cache_writes: int = 0  # fresh results stored to the local cache this run

    @property
    def played(self) -> int:
        """Requests that actually hit the API this run (cache reads excluded)."""
        return self.ok + self.failed


@dataclass
class AwsCallLog:
    """Process-wide tally of AWS API requests, keyed by operation label."""

    ops: dict[str, OpStats] = field(default_factory=dict)

    def _op(self, operation: str) -> OpStats:
        return self.ops.setdefault(operation, OpStats())

    def record(self, operation: str, *, ok: bool, quota: bool = False) -> None:
        stats = self._op(operation)
        if ok:
            stats.ok += 1
        else:
            stats.failed += 1
            if quota:
                stats.quota_failed += 1

    def record_cache_read(self, operation: str) -> None:
        self._op(operation).cache_reads += 1

    def record_cache_write(self, operation: str) -> None:
        self._op(operation).cache_writes += 1

    def reset(self) -> None:
        self.ops.clear()

    @property
    def played(self) -> int:
        return sum(s.played for s in self.ops.values())

    @property
    def ok(self) -> int:
        return sum(s.ok for s in self.ops.values())

    @property
    def failed(self) -> int:
        return sum(s.failed for s in self.ops.values())

    @property
    def quota_failed(self) -> int:
        return sum(s.quota_failed for s in self.ops.values())

    @property
    def cache_reads(self) -> int:
        return sum(s.cache_reads for s in self.ops.values())

    @property
    def cache_writes(self) -> int:
        return sum(s.cache_writes for s in self.ops.values())


_CALL_LOG = AwsCallLog()


def call_log() -> AwsCallLog:
    """Return the process-wide AWS call log (reset it at the start of a command)."""
    return _CALL_LOG


# Every DiskCache registers here on creation so clear_all_caches() can wipe the lot.
_CACHES: list["DiskCache"] = []


def clear_all_caches() -> list[Path]:
    """Delete every registered cache file. Returns the distinct paths that existed."""
    removed = list({c.path for c in _CACHES if c.path.exists()})
    for cache in _CACHES:
        cache.clear()
    return removed


@dataclass
class DiskCache:
    """Best-effort JSON disk cache with a TTL, keyed by string and lazily loaded.

    Shared by the cacheable AWS fetchers (placement scores, on-demand prices,
    instance specs) so a re-run reuses recent results instead of re-spending API
    calls (and, for placement scores, the daily configuration budget). A missing,
    unreadable, or unwritable file is treated as an empty cache — never an error.
    """

    path: Path
    ttl_seconds: float
    _data: dict[str, dict[str, Any]] | None = None
    _dirty: bool = False

    def __post_init__(self) -> None:
        _CACHES.append(self)  # register so clear_all_caches() can wipe every store

    def clear(self) -> None:
        """Drop the in-memory data and delete the on-disk file (best-effort)."""
        self._data = None
        self._dirty = False
        try:
            self.path.unlink()
        except OSError:
            pass  # already absent or unwritable — nothing to do

    def _ensure(self) -> dict[str, dict[str, Any]]:
        if self._data is None:
            try:
                self._data = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                self._data = {}
        return self._data

    def get(self, key: str, now: float) -> tuple[bool, Any]:
        """Return ``(hit, value)``; ``hit`` is False when the key is missing or stale.

        ``value`` may legitimately be ``None`` on a hit (a cached "no result"),
        which is why the freshness is reported separately rather than via a
        sentinel return.
        """
        entry = self._ensure().get(key)
        if entry is None or (now - float(entry.get("ts", 0))) >= self.ttl_seconds:
            return (False, None)
        return (True, entry.get("value"))

    def set(self, key: str, value: Any, now: float) -> None:
        self._ensure()[key] = {"value": value, "ts": now}
        self._dirty = True

    def save(self) -> None:
        if not self._dirty or self._data is None:
            return
        try:
            self.path.write_text(json.dumps(self._data), encoding="utf-8")
        except OSError:
            pass  # cache is best-effort
        self._dirty = False


def aws_env() -> dict[str, str]:
    """Environment for ``aws`` subprocesses with resilient retry defaults.

    CloudTrail ``lookup-events`` paginates in small 50-event pages and throttles
    easily; the CLI's default 2 retries fail hard ("Rate exceeded"). Adaptive
    retry with more attempts rides out the throttle. Caller-set values win.
    """
    return {"AWS_RETRY_MODE": "adaptive", "AWS_MAX_ATTEMPTS": "10", **os.environ}


def run_aws_json(args: list[str], *, profile: str = "", timeout: int = DEFAULT_TIMEOUT) -> Any:
    """Run ``aws <args> --output json`` and return the parsed payload.

    Every call is recorded (one per invocation) in the process-wide
    :func:`call_log`. Raises :class:`AwsQuotaError` when the failure is a
    quota/throttle limit (still a ``RuntimeError`` subclass, so existing
    ``except RuntimeError`` handlers keep working but quota-aware callers can stop
    early), :class:`AwsCliError` otherwise (missing binary, timeout, or any other
    non-zero exit).
    """
    cmd = ["aws", *args, "--output", "json"]
    if profile:
        cmd += ["--profile", profile]
    label = " ".join(args[:2])
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=aws_env(),
        )
    except FileNotFoundError as exc:
        _CALL_LOG.record(label, ok=False)
        raise AwsCliError("the 'aws' CLI is not installed or not on PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        _CALL_LOG.record(label, ok=False)
        raise AwsCliError(f"aws {label} timed out after {timeout}s.") from exc
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        if is_quota_error(stderr):
            _CALL_LOG.record(label, ok=False, quota=True)
            raise AwsQuotaError(f"aws {label} hit a quota/throttle limit: {stderr}")
        _CALL_LOG.record(label, ok=False)
        raise AwsCliError(f"aws {label} failed: {stderr}")
    _CALL_LOG.record(label, ok=True)
    if not (result.stdout or "").strip():
        return {}
    return json.loads(result.stdout)
