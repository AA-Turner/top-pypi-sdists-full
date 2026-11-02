"""Finding kind instances in real data, wherever they are.

``availability`` answers "what COULD appear, per the registered schemas". This
module answers the runtime twin: "what DID appear, in this actual payload" —
and it is deliberately ONE implementation, because both consumers need exactly
the same answer (plan of record §7.3 / §7.7c):

* **Kind-filtered edges** — an edge declaring "carry ``website`` instances"
  draws them out of whatever the source produced.
* **Kind-triggered nodes** — *"all of a particular kind, wherever they're
  generated from, doesn't matter what node, where, and doesn't matter how
  deeply nested they are."*

Two consumers, one scan. If edges used a shallow rule and triggers a deep one,
an author would watch the same value fire a trigger and not fire an edge on the
same run, with nothing to explain the difference.

WHAT COUNTS AS AN INSTANCE
--------------------------
Any value carrying the wire discriminator (``__kind``), model or serialized —
``kind_of`` is the one authority, so this module never re-derives identity.
Runtime wrappers ARE kinds, so the scan sees through them by walking into their
payload like any other structure; a caller that does not want to match wrappers
filters by slug, which is the normal case.

NESTING IS NOT SHADOWED
-----------------------
A ``website`` inside a ``website`` yields TWO occurrences. That is the honest
answer: both are real instances, and a rule that hid the inner one would make
"trigger on every website" silently lossy. Callers that want only the outermost
use ``top_level_only``.

IDENTITY IS THE PATH
--------------------
Every occurrence carries an INDEXED path (``results[2].author``) — its identity
within one payload — alongside the ``[]`` PATTERN that matches what the
availability index publishes. The indexed path is what a subscription dedupes
on, so re-observing the same value never re-fires; the pattern is what a UI
shows next to a picker entry.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.model import kind_of

__all__ = ["KindOccurrence", "find_occurrences", "MAX_SCAN_DEPTH"]

#: Deep-scan guard. Run payloads are JSON-shaped and shallow in practice; this
#: stops a pathological or cyclic structure from walking forever. It is
#: deliberately larger than ``availability.MAX_NESTING_DEPTH``: that one bounds
#: a SCHEMA walk (kinds inside kinds), this one bounds a DATA walk, where each
#: schema level costs several container levels.
MAX_SCAN_DEPTH = 24


class KindOccurrence(BaseModel):
    """One kind instance found in real data."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    kind: str
    #: Indexed path from the scanned root (``results[2].author``). Identity.
    path: str
    #: The same path with indices collapsed to ``[]`` — the shape the
    #: availability index publishes, so an occurrence can be lined up with the
    #: picker entry that predicted it.
    pattern: str
    #: Container nesting depth, not kind depth.
    depth: int
    value: Any

    def identity(self, scope: str = "") -> str:
        """Stable key for dedupe: ``<scope>#<kind>@<path>``.

        ``scope`` is whatever the caller considers one production event — a
        node id, or a node id plus fan-out item index. Two different steps
        producing structurally identical data are two occurrences, correctly:
        the second one is a real second event, not a repeat.
        """
        return f"{scope}#{self.kind}@{self.path}"


def find_occurrences(
    root: Any,
    slug: str | None = None,
    *,
    base_path: str = "",
    max_depth: int = MAX_SCAN_DEPTH,
    top_level_only: bool = False,
) -> list[KindOccurrence]:
    """Every kind instance inside ``root``, in document order.

    ``slug=None`` finds instances of every kind (what an inventory or a
    debugging surface wants); a slug filters to one (what an edge filter and a
    trigger want). ``top_level_only`` stops descending into a value once it
    matched — for "the outermost websites", never for "every website".
    """
    found: list[KindOccurrence] = []
    _scan(
        value=root,
        slug=slug,
        path=base_path,
        pattern=base_path,
        depth=0,
        max_depth=max_depth,
        top_level_only=top_level_only,
        seen=set(),
        out=found,
    )
    return found


def _scan(
    *,
    value: Any,
    slug: str | None,
    path: str,
    pattern: str,
    depth: int,
    max_depth: int,
    top_level_only: bool,
    seen: set[int],
    out: list[KindOccurrence],
) -> None:
    if depth > max_depth or value is None:
        return
    # Cycle guard by object identity. Python payloads can share substructure
    # (the same dict referenced twice is common after a merge) and a genuine
    # cycle would otherwise recurse until the depth cap on every branch.
    if isinstance(value, Mapping | BaseModel) or (
        isinstance(value, Sequence) and not isinstance(value, str | bytes)
    ):
        marker = id(value)
        if marker in seen:
            return
        seen = seen | {marker}

    found_slug = kind_of(value)
    if found_slug and (slug is None or found_slug == slug):
        out.append(
            KindOccurrence(
                kind=found_slug,
                path=path,
                pattern=pattern,
                depth=depth,
                value=value,
            )
        )
        if top_level_only:
            return

    for _key, child, indexed, patterned in _children(value, path, pattern):
        _scan(
            value=child,
            slug=slug,
            path=indexed,
            pattern=patterned,
            depth=depth + 1,
            max_depth=max_depth,
            top_level_only=top_level_only,
            seen=seen,
            out=out,
        )


def _children(value: Any, path: str, pattern: str) -> list[tuple[str, Any, str, str]]:
    """(key, child, indexed_path, pattern_path) for every child of ``value``."""
    out: list[tuple[str, Any, str, str]] = []
    if isinstance(value, BaseModel):
        for name, field in type(value).model_fields.items():
            key = field.serialization_alias or field.alias or name
            child = getattr(value, name, None)
            out.append((key, child, _join(path, key), _join(pattern, key)))
        return out
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                continue
            out.append((key, child, _join(path, key), _join(pattern, key)))
        return out
    if isinstance(value, Sequence) and not isinstance(value, str | bytes):
        for index, child in enumerate(value):
            # A list child's INDEX is its identity; its PATTERN is ``[]`` —
            # which is exactly the shape the availability index publishes, so
            # the two line up without a translation step.
            out.append((str(index), child, f"{path}[{index}]", f"{pattern}[]"))
        return out
    return out


def _join(prefix: str, key: str) -> str:
    return f"{prefix}.{key}" if prefix else key
