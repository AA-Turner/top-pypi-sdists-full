"""Unified GitLab CI YAML loader for both ``ci run`` and ``ci run-local``.

PyYAML's default loader rejects GitLab's custom tags (``!reference``), so we
subclass :class:`yaml.SafeLoader` and register constructors for them. The two
call sites need different treatment of ``!reference``:

- ``ci run`` only extracts ``needs:``, so it *flattens* a ``!reference`` into
  the plain list it points at (the reference target is irrelevant there).
- ``ci run-local`` must *expand* a reference into the real value later, so it
  keeps each ``!reference [.job, key]`` as a :class:`Reference` sentinel.

``reference_mode`` on :func:`parse` selects between the two. YAML anchors /
aliases (``&x`` / ``*x``) are resolved natively by PyYAML within each document,
matching GitLab's file-scoped anchor behaviour.
"""

from dataclasses import dataclass
from typing import Any

import yaml

# Top-level keys that are not jobs.
RESERVED_TOP_LEVEL = {
    "stages",
    "variables",
    "default",
    "include",
    "workflow",
    "image",
    "services",
    "cache",
    "before_script",
    "after_script",
    "spec",
}


@dataclass
class Reference:
    """A GitLab ``!reference [a, b, c]`` tag, kept until it can be expanded."""

    path: list[str]


def _construct_passthrough(loader: yaml.Loader, node: yaml.Node) -> Any:
    """Construct any tagged node as plain Python data, ignoring the tag."""
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node, deep=True)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node, deep=True)
    return None


def _construct_reference(loader: yaml.Loader, node: yaml.Node) -> Reference:
    if not isinstance(node, yaml.SequenceNode):
        return Reference([])
    seq = loader.construct_sequence(node, deep=True)
    return Reference([str(item) for item in seq])


class _GitLabLoader(yaml.SafeLoader):
    """Base SafeLoader tolerating GitLab CI's custom tags via a catch-all."""


# Catch-all for any GitLab-specific tag (e.g. ``!flatten``) so we never crash.
# PyYAML accepts ``None`` as the sentinel for "unknown tag"; the stubs lag behind.
_GitLabLoader.add_constructor(None, _construct_passthrough)  # type: ignore[arg-type]


class _FlattenLoader(_GitLabLoader):
    """Flattens ``!reference`` into the plain list it points at."""


_FlattenLoader.add_constructor("!reference", _construct_passthrough)


class _KeepLoader(_GitLabLoader):
    """Keeps ``!reference`` as a :class:`Reference` sentinel for later expansion."""


_KeepLoader.add_constructor("!reference", _construct_reference)


def parse(content: str, *, reference_mode: str = "flatten") -> dict[str, Any]:
    """Parse a GitLab YAML document. Returns ``{}`` on failure.

    Multi-document streams (``---`` separators) are merged in order — later docs
    override earlier ones, matching GitLab's ``include:`` override semantics.
    ``reference_mode="flatten"`` collapses ``!reference`` into plain data;
    ``"keep"`` preserves it as a :class:`Reference`.
    """
    if not content:
        return {}
    loader = _KeepLoader if reference_mode == "keep" else _FlattenLoader
    try:
        docs = list(yaml.load_all(content, Loader=loader))
    except yaml.YAMLError:
        return {}
    merged: dict[str, Any] = {}
    for doc in docs:
        if isinstance(doc, dict):
            merged.update(doc)
    return merged


def normalize_needs(needs: Any) -> list[str]:
    """Convert a ``needs:`` directive (any GitLab form) into a list of job names.

    Cross-project / cross-pipeline ``needs:`` (which carry ``project:`` or
    ``pipeline:`` keys) are dropped because the referenced job lives in a
    different pipeline and cannot be triggered locally.
    """
    if isinstance(needs, str):
        return [needs]
    if not isinstance(needs, list):
        return []
    out: list[str] = []
    for item in needs:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            if "project" in item or "pipeline" in item:
                continue
            job = item.get("job")
            if isinstance(job, str):
                out.append(job)
    return out
