"""Operation ID computation for idempotency (FR-004).

Computes a deterministic, stable operation ID from tool name and inputs
using SHA-256 (truncated to 16 hex chars). Sensitive keys are redacted
and nondeterministic fields are excluded before hashing.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

# Default nondeterministic field names excluded recursively (case-insensitive substring)
_DEFAULT_NONDETERMINISTIC_SUBSTRINGS: frozenset[str] = frozenset({"timestamp", "created_at", "updated_at"})

# Default nondeterministic field names excluded by exact match (case-insensitive)
_DEFAULT_NONDETERMINISTIC_EXACT: frozenset[str] = frozenset({"request_id"})


def compute_operation_id(
    node_name: str,
    tool_name: str,
    inputs: dict[str, Any],
    nondeterministic_fields: tuple[str, ...] = (),
) -> str:
    """Compute a deterministic operation ID for idempotency checks.

    Steps:
    1. Redact sensitive keys (reuses existing blocklist)
    2. Remove default nondeterministic fields (recursive)
    3. Remove per-tool nondeterministic fields (dot-path resolution)
    4. Canonical JSON serialization (sorted keys, compact separators)
    5. SHA-256 hash with node_name prefix, truncated to 16 hex characters
    6. Format: ``<tool_name>:<hash_hex[:16]>``

    Args:
        node_name: The graph node invoking the tool (required for cross-node
            collision prevention per FR-006).
        tool_name: The tool being invoked.
        inputs: The tool invocation inputs.
        nondeterministic_fields: Per-tool dot-paths to exclude.

    Returns:
        A stable operation ID string.

    Raises:
        ValueError: node_name is empty or whitespace.
    """
    if not node_name or not node_name.strip():
        raise ValueError(
            "node_name must be non-empty for compute_operation_id() — "
            "an empty value defeats the cross-node collision-prevention scheme (FR-006)."
        )

    from agentic_devtools.orchestration.execution.tracing import redact_sensitive_keys

    # Step 1: Redact sensitive keys
    cleaned = redact_sensitive_keys(inputs) if isinstance(inputs, dict) else inputs

    # Step 2: Remove default nondeterministic fields (recursive)
    cleaned = _remove_default_nondeterministic(cleaned)

    # Step 3: Remove per-tool nondeterministic fields (dot-path)
    for dot_path in nondeterministic_fields:
        cleaned = _remove_dot_path(cleaned, dot_path)

    # Step 4: Canonical JSON
    canonical = json.dumps(cleaned, sort_keys=True, separators=(",", ":"), default=str)

    # Step 5: SHA-256 with node_name prefix for cross-node collision prevention.
    # Use a JSON-array encoding so the boundary between node_name and canonical
    # is unambiguous regardless of colons or other separator characters in either
    # value (avoids the delimiter-collision problem with bare f-string joining).
    hash_input = json.dumps([node_name, canonical], separators=(",", ":"))
    hash_hex = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:16]

    # Step 6: Format
    return f"{tool_name}:{hash_hex}"


def _remove_default_nondeterministic(value: Any) -> Any:
    """Recursively remove default nondeterministic fields from a value."""
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            k_lower = k.lower()
            # Check exact match
            if k_lower in _DEFAULT_NONDETERMINISTIC_EXACT:
                continue
            # Check substring match
            if any(sub in k_lower for sub in _DEFAULT_NONDETERMINISTIC_SUBSTRINGS):
                continue
            result[k] = _remove_default_nondeterministic(v)
        return result
    if isinstance(value, list):
        return [_remove_default_nondeterministic(item) for item in value]
    return value


def _remove_dot_path(data: Any, dot_path: str) -> Any:
    """Remove a dot-path field from nested dicts (case-sensitive, dicts only).

    Skips silently if path doesn't exist or traverses non-dict segments.
    Does not support list indexing.
    """
    if not isinstance(data, dict):
        return data

    parts = dot_path.split(".")
    if len(parts) == 1:
        # Terminal: remove the key if present
        result = dict(data)
        result.pop(parts[0], None)
        return result

    # Non-terminal: recurse into the next level
    key = parts[0]
    if key not in data or not isinstance(data[key], dict):
        return data

    result = dict(data)
    result[key] = _remove_dot_path(data[key], ".".join(parts[1:]))
    return result
