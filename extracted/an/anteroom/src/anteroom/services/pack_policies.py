"""Pack-distributed policy artifact parser (#924).

Policy artifacts let packs set configuration values through the same
overlay pipeline that :class:`ArtifactType.CONFIG_OVERLAY` uses, with
one crucial difference: policy artifacts are restricted to a narrow
allowlist of configuration keys. A misconfigured (or malicious) pack
cannot use a ``policy`` artifact to, for example, flip
``safety.approval_mode`` to ``auto`` or disable audit logging.

Allowlist
---------

Only two top-level key paths are accepted today:

* ``memory.promotion.*``
* ``memory.retention.*``

Everything else is **silently dropped with a WARNING log**. Graceful
degradation is preferred over install-time failure because a pack may
carry a mix of known and unknown policy keys across upgrade cycles.

Parser contract
---------------

* Input: raw YAML text of a single policy artifact.
* Output: a dot-path dict suitable for the existing overlay merge
  pipeline. Only allowlisted paths appear in the output; the rest are
  dropped.
* Failures (invalid YAML, non-mapping root) return an empty dict and
  log at WARNING level.
"""

from __future__ import annotations

import logging
from typing import Any

import yaml

logger = logging.getLogger(__name__)


# Allowlisted top-level key paths. The tuple tail is the remainder of
# the key path that is accepted verbatim (anything under the allowed
# prefix lands in the overlay).
_ALLOWED_PREFIXES: tuple[tuple[str, ...], ...] = (
    ("memory", "promotion"),
    ("memory", "retention"),
)


def _is_allowed(path: tuple[str, ...]) -> bool:
    """Return True when *path* starts with an allowlisted prefix."""
    for prefix in _ALLOWED_PREFIXES:
        if len(path) >= len(prefix) and path[: len(prefix)] == prefix:
            return True
    return False


def _flatten(mapping: Any, prefix: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    """Walk a nested dict, yielding ``(key-path, leaf-value)`` tuples.

    Lists and scalars are treated as leaves. Non-dict roots raise
    :class:`TypeError` so the caller can surface a parse error.
    """
    if not isinstance(mapping, dict):
        raise TypeError(f"Expected mapping at {'.'.join(prefix) or '<root>'}, got {type(mapping).__name__}")

    leaves: list[tuple[tuple[str, ...], Any]] = []
    for key, value in mapping.items():
        if not isinstance(key, str):
            logger.warning("pack_policies: non-string key %r ignored at %s", key, ".".join(prefix) or "<root>")
            continue
        path = (*prefix, key)
        if isinstance(value, dict):
            leaves.extend(_flatten(value, path))
        else:
            leaves.append((path, value))
    return leaves


def parse_policy_artifact(content: str, *, source: str = "<inline>") -> dict[str, Any]:
    """Parse *content* (YAML text) into a nested dict of allowlisted keys.

    Returns a nested dict so the existing overlay merge pipeline can
    consume it alongside ``CONFIG_OVERLAY`` artifacts. Keys that fall
    outside :data:`_ALLOWED_PREFIXES` are dropped with a WARNING log
    that names the *source* so operators can trace which pack artifact
    carried the rejected key.

    Malformed input (invalid YAML, non-mapping root) returns an empty
    dict; the failure is logged.
    """
    try:
        raw = yaml.safe_load(content) if content.strip() else {}
    except yaml.YAMLError as exc:
        logger.warning("pack_policies: invalid YAML in %s: %s", source, exc)
        return {}

    if raw is None:
        return {}
    if not isinstance(raw, dict):
        logger.warning(
            "pack_policies: %s root must be a mapping, got %s",
            source,
            type(raw).__name__,
        )
        return {}

    try:
        leaves = _flatten(raw)
    except TypeError as exc:
        logger.warning("pack_policies: %s structure invalid: %s", source, exc)
        return {}

    # Re-assemble the allowlisted leaves into a nested dict.
    result: dict[str, Any] = {}
    dropped: list[str] = []
    for path, value in leaves:
        if not _is_allowed(path):
            dropped.append(".".join(path))
            continue
        node: dict[str, Any] | None = result
        for segment in path[:-1]:
            assert node is not None  # loop guard; set to None only on conflict below
            node = node.setdefault(segment, {})
            if not isinstance(node, dict):
                # A previous leaf already occupied this position —
                # indicates a malformed policy (same prefix used as both
                # leaf and subtree). Drop the conflicting leaf.
                dropped.append(".".join(path))
                node = None  # sentinel to break out below
                break
        if node is None:
            continue
        node[path[-1]] = value

    if dropped:
        logger.warning(
            "pack_policies: %s dropped %d non-allowlisted key(s): %s",
            source,
            len(dropped),
            ", ".join(sorted(dropped)[:10]) + ("..." if len(dropped) > 10 else ""),
        )

    return result
