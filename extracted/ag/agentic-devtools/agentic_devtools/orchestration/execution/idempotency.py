"""Idempotency registry for safe tool re-execution on checkpoint resume.

Provides ``IdempotencyEntry``, ``IdempotencyRegistry``, and
``IdempotentToolWrapper`` to prevent duplicate external writes when
LangGraph resumes from a checkpoint.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .run_id import validate_run_id

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class IdempotencyEntry:
    """A single idempotency registry entry.

    Attributes:
        key: Composite key ``<tool_id>:<sha256_hex[:16]>:<node_name>:<run_id>``.
        timestamp: Unix epoch when the entry was recorded.
        result_summary: Truncated summary of the tool result.
        status: Outcome status (``"success"`` or ``"error"``).
    """

    key: str
    timestamp: float
    result_summary: str
    status: str
    result_encoding: str = "raw"


def _compute_composite_key(tool_id: str, args: dict[str, Any], node_name: str, run_id: str) -> str:
    """Compute the composite idempotency key.

    Format: ``<tool_id>:<sha256_hex[:16]>:<node_name>:<run_id>``
    """
    args_json = json.dumps(args, sort_keys=True, separators=(",", ":"), default=str)
    args_hash = hashlib.sha256(args_json.encode()).hexdigest()[:16]
    return f"{tool_id}:{args_hash}:{node_name}:{run_id}"


class IdempotencyRegistry:
    """File-backed idempotency registry with locked critical sections.

    Persists entries to ``<state_dir>/orchestration/<run_id>/idempotency-registry.json``.
    Uses ``locked_file()`` for thread-safe read/check/update/write.

    Graceful degradation: missing or corrupt files produce a warning and
    the registry starts fresh rather than raising.
    """

    def __init__(self, state_dir: Path, run_id: str) -> None:
        self._run_id = validate_run_id(run_id)
        self._registry_dir = state_dir / "orchestration" / self._run_id
        self._registry_dir.mkdir(parents=True, exist_ok=True)
        self._registry_path = self._registry_dir / "idempotency-registry.json"

    @property
    def registry_path(self) -> Path:
        """Path to the registry file."""
        return self._registry_path

    def check(self, tool_id: str, args: dict[str, Any], node_name: str) -> IdempotencyEntry | None:
        """Check if a tool invocation has already been recorded.

        Returns the existing entry if found, else None.
        Malformed or corrupt entries are treated as cache-misses (with a warning)
        rather than raising, to preserve the graceful-degradation contract.
        """
        key = _compute_composite_key(tool_id, args, node_name, self._run_id)
        entries = self._load_entries()
        entry_data = entries.get(key)
        if entry_data is None:
            return None
        if not isinstance(entry_data, dict):
            print(
                f"[IdempotencyRegistry] malformed entry for key={key!r} "
                f"(expected dict, got {type(entry_data).__name__}), treating as cache-miss",
                file=sys.stderr,
            )
            return None
        try:
            return IdempotencyEntry(**entry_data)
        except (TypeError, ValueError) as exc:
            print(
                f"[IdempotencyRegistry] malformed entry for key={key!r}: {exc}, treating as cache-miss",
                file=sys.stderr,
            )
            return None

    def record(
        self,
        tool_id: str,
        args: dict[str, Any],
        node_name: str,
        result_summary: str,
        status: str = "success",
        result_encoding: str = "raw",
    ) -> None:
        """Record a tool invocation in the registry.

        Uses file locking for thread-safe writes.
        """
        key = _compute_composite_key(tool_id, args, node_name, self._run_id)
        entry = IdempotencyEntry(
            key=key,
            timestamp=time.time(),
            result_summary=result_summary[:500],
            status=status,
            result_encoding=result_encoding,
        )

        from agentic_devtools.file_locking import locked_file

        try:
            with locked_file(self._registry_path, "r+") as f:
                content = f.read()
                try:
                    raw = json.loads(content) if content.strip() else {}
                except (json.JSONDecodeError, ValueError):
                    print(
                        f"[IdempotencyRegistry] corrupt registry file, starting fresh: {self._registry_path}",
                        file=sys.stderr,
                    )
                    raw = {}
                if not isinstance(raw, dict):
                    print(
                        "[IdempotencyRegistry] corrupt registry file (non-dict JSON), "
                        f"starting fresh: {self._registry_path}",
                        file=sys.stderr,
                    )
                    entries: dict[str, Any] = {}
                else:
                    entries = raw

                entries[key] = asdict(entry)
                f.seek(0)
                f.write(json.dumps(entries, indent=2))
                f.truncate()
        except OSError as exc:
            print(
                "[IdempotencyRegistry] failed to persist entry "
                f"for key={key!r}, continuing without persisting cache entry: {exc}",
                file=sys.stderr,
            )

    def _load_entries(self) -> dict[str, Any]:
        """Load all entries from the registry file (best-effort)."""
        if not self._registry_path.exists():
            return {}
        try:
            from agentic_devtools.file_locking import locked_file

            with locked_file(self._registry_path, mode="r", exclusive=False) as f:
                content = f.read()
            if not content.strip():
                return {}
            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                print(
                    f"[IdempotencyRegistry] registry file contains {type(parsed).__name__}, "
                    "expected dict — starting fresh",
                    file=sys.stderr,
                )
                return {}
            return parsed
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            print(
                f"[IdempotencyRegistry] failed to load registry, starting fresh: {exc}",
                file=sys.stderr,
            )
            return {}


class IdempotentToolWrapper:
    """Wraps a ``ToolRegistry``-compatible object with idempotency checks.

    Before each invocation, checks the registry for a cached result.
    After successful invocation, records the result.

    Remains ``ToolRegistry``-protocol-compatible for injection into
    ``ExecutionContext``.
    """

    def __init__(
        self,
        inner: Any,
        registry: IdempotencyRegistry,
        node_name: str,
    ) -> None:
        self._inner = inner
        self._registry = registry
        self._node_name = node_name

    def invoke(self, tool_name: str, **kwargs: Any) -> Any:
        """Invoke a tool with idempotency protection."""
        # Check for cached result — only short-circuit on previously successful executions
        existing = self._registry.check(tool_name, kwargs, self._node_name)
        if existing is not None and existing.status == "success":
            logger.info(
                "Idempotency hit for %s (node=%s): returning cached result",
                tool_name,
                self._node_name,
            )
            if existing.result_encoding == "json":
                try:
                    return json.loads(existing.result_summary)
                except json.JSONDecodeError:
                    logger.warning(
                        "Cached idempotency result for %s is not valid JSON; returning raw summary",
                        tool_name,
                    )
            elif existing.result_encoding not in {"raw", "json"}:
                logger.warning(
                    "Unknown result_encoding=%r for cached idempotency result on %s; returning raw summary",
                    existing.result_encoding,
                    tool_name,
                )
            return existing.result_summary

        # Execute the tool
        result = self._inner.invoke(tool_name, **kwargs)

        # Determine the outcome status from the tool result
        if isinstance(result, dict) and result.get("success") is False:
            record_status = "error"
        else:
            record_status = "success"

        # Record the result
        result_encoding = "raw"
        try:
            if isinstance(result, str):
                result_summary = result[:500]
                if len(result) > 500:
                    # Oversized: keep the original result unchanged so callers
                    # always receive the correct value. Mark as non-cacheable
                    # (status="error") so the next call re-executes the tool
                    # rather than returning the truncated summary.
                    record_status = "error"
            else:
                serialized = json.dumps(result)
                if len(serialized) <= 500:
                    result_summary = serialized
                    result_encoding = "json"
                else:
                    result_summary = serialized[:500]
                    # Oversized: keep the original result unchanged so callers
                    # always receive the correct type.  Mark as non-cacheable
                    # (status="error") so the next call re-executes the tool
                    # rather than returning the truncated summary.
                    record_status = "error"
        except (TypeError, ValueError):
            # If we cannot serialize the result deterministically, treat it as
            # non-cacheable to avoid returning a different type/value on cache hits.
            result_summary = str(result)[:500]
            record_status = "error"
        self._registry.record(
            tool_id=tool_name,
            args=kwargs,
            node_name=self._node_name,
            result_summary=result_summary,
            status=record_status,
            result_encoding=result_encoding,
        )

        return result

    def list_all(self) -> dict:
        """Delegate to inner registry."""
        return self._inner.list_all()

    def get_categories(self) -> list[str]:
        """Delegate to inner registry."""
        return self._inner.get_categories()
