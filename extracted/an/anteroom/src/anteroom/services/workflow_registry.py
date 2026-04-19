"""Pack-aware workflow template registry (#924).

Resolves workflow definitions from three sources, unified behind a single
entry point:

* **Built-in** workflows shipped in the installed package (``workflows/``)
* **Examples** shipped in the repo source tree (``examples/workflows/``)
* **Packs** — installed via :mod:`anteroom.services.packs`, stored on
  disk under ``{pack.source_path}/workflow_templates/*.yaml``

Resolution precedence (filesystem wins) is documented at each entry
point. ``list_available_workflows`` is the single source of truth used
by the web ``GET /workflows`` listing and the CLI, so the two surfaces
can never drift.

FQN support
-----------

``resolve_workflow`` accepts two identifier forms:

1. Bare ID — ``"issue_delivery"``. Looks up filesystem first, then
   packs. Rejects path-traversal characters.
2. FQN — ``"@{namespace}/workflow/{id}"``. Targets a specific pack.
   Falls back to the bare id if no pack-qualified artifact is found.

Path-traversal and FQN-shape validation happen BEFORE any DB query.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

logger = logging.getLogger(__name__)


# ``@{namespace}/workflow/{id}`` — matches the artifact FQN regex but
# pinned to ``/workflow/`` so callers that pass a full artifact FQN
# land on the pack-resolution path.
_FQN_RE = re.compile(
    r"^@(?P<namespace>[a-z0-9][a-z0-9._-]{0,62})"
    r"/workflow/"
    r"(?P<id>[a-z0-9_][a-z0-9_.-]{0,62})$"
)


# ---------------------------------------------------------------------------
# Public dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkflowRef:
    """A resolved reference to a workflow definition (#924).

    ``path`` is always present — for both filesystem and pack-sourced
    workflows — because packs install their yaml files on disk under
    ``{pack.source_path}/workflow_templates/{id}.yaml``. Callers that
    hold a :class:`WorkflowRef` can therefore always pass ``ref.path``
    straight to :func:`anteroom.services.workflow_engine.load_definition`
    without any content-vs-path branching.
    """

    id: str
    path: Path
    source: Literal["built_in", "example", "pack"]
    pack_id: str | None = None
    namespace: str | None = None


# ---------------------------------------------------------------------------
# Safety helpers
# ---------------------------------------------------------------------------


def _is_safe_workflow_id(workflow_id: str) -> bool:
    """Reject characters that could escape the workflow directory."""
    return ".." not in workflow_id and "/" not in workflow_id and "\\" not in workflow_id


def _parse_fqn(value: str) -> tuple[str, str] | None:
    """Return (namespace, id) when *value* is a workflow FQN; else None."""
    match = _FQN_RE.match(value)
    if match is None:
        return None
    return match.group("namespace"), match.group("id")


# ---------------------------------------------------------------------------
# Filesystem resolution (shared with ``workflow_resolution``)
# ---------------------------------------------------------------------------


def _resolve_from_filesystem(
    workflow_id: str, *, allow_direct_path: bool
) -> tuple[Path, Literal["built_in", "example"]] | None:
    """Resolve a workflow id (or raw path) on the filesystem only.

    Returns ``(path, source)`` when found, else ``None``. Path traversal
    is rejected for id-based lookups; only ``allow_direct_path=True``
    callers (the CLI) may pass a raw filesystem path.
    """
    from .workflow_resolution import _package_root

    if allow_direct_path:
        candidate = Path(workflow_id)
        if candidate.exists() and candidate.suffix in (".yaml", ".yml"):
            # Treat user-supplied explicit paths as the "example" class;
            # the caller already has the path, so precedence is moot.
            return (candidate, "example")

    if not _is_safe_workflow_id(workflow_id):
        return None

    pkg_root = _package_root()

    pkg_example_path = pkg_root / "workflows" / "examples" / f"{workflow_id}.yaml"
    if pkg_example_path.exists():
        return (pkg_example_path, "example")

    src_examples_dir = pkg_root.parent.parent / "examples" / "workflows"
    src_example_path = src_examples_dir / f"{workflow_id}.yaml"
    if src_example_path.exists():
        return (src_example_path, "example")

    builtin_path = pkg_root / "workflows" / f"{workflow_id}.yaml"
    if builtin_path.exists():
        return (builtin_path, "built_in")

    return None


# ---------------------------------------------------------------------------
# Pack resolution
# ---------------------------------------------------------------------------


def _list_pack_workflow_paths(db: ThreadSafeConnection) -> list[tuple[Path, str, str, str]]:
    """Enumerate workflow-template yaml paths from installed packs.

    Returns ``(yaml_path, workflow_id, pack_id, namespace)`` tuples.
    Paths outside the pack directory (traversal) are silently dropped.

    ``workflow_id`` is derived from the yaml filename (``{id}.yaml``)
    — NOT from the ``id`` field inside the YAML. Callers that need the
    parsed ``WorkflowDefinition`` should call ``load_definition`` on
    the path and read ``defn.id`` from there; the filename is a cheap
    discovery handle.
    """
    from . import packs as packs_mod

    results: list[tuple[Path, str, str, str]] = []
    try:
        pack_rows = packs_mod.list_packs(db)
    except Exception:
        logger.debug("Failed to list installed packs for workflow discovery", exc_info=True)
        return results

    for pack in pack_rows:
        source_path = pack.get("source_path")
        if not source_path:
            continue
        pack_dir = Path(source_path)
        templates_dir = pack_dir / "workflow_templates"
        if not templates_dir.is_dir():
            continue
        try:
            pack_resolved = pack_dir.resolve()
        except OSError:
            continue
        for yaml_path in sorted(templates_dir.glob("*.yaml")):
            try:
                if not yaml_path.resolve().is_relative_to(pack_resolved):
                    continue
            except OSError:
                continue
            workflow_id = yaml_path.stem
            if not _is_safe_workflow_id(workflow_id):
                continue
            results.append((yaml_path, workflow_id, pack["id"], pack["namespace"]))
    return results


def _resolve_from_packs(
    db: ThreadSafeConnection,
    workflow_id: str,
    *,
    target_namespace: str | None = None,
) -> WorkflowRef | None:
    """Resolve *workflow_id* against installed packs.

    When *target_namespace* is non-None, only a pack with that namespace
    may satisfy the lookup. Bare-id callers pass ``None`` and take the
    first matching pack (ordered by :func:`packs.list_packs`).
    """
    for yaml_path, pack_workflow_id, pack_id, namespace in _list_pack_workflow_paths(db):
        if pack_workflow_id != workflow_id:
            continue
        if target_namespace is not None and namespace != target_namespace:
            continue
        return WorkflowRef(
            id=workflow_id,
            path=yaml_path,
            source="pack",
            pack_id=pack_id,
            namespace=namespace,
        )
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def resolve_workflow(
    workflow_id: str,
    *,
    db: ThreadSafeConnection | None = None,
    allow_filesystem: bool = True,
) -> WorkflowRef | None:
    """Resolve a workflow definition by id, FQN, or filesystem path.

    Precedence:

    1. **FQN form** (``@ns/workflow/id``) — pack-targeted; no filesystem
       fallback (FQN is explicit intent).
    2. **Filesystem** (package examples, source-tree examples, built-ins).
       Filesystem wins over packs on id collision so a pack cannot
       silently replace a built-in.
    3. **Packs** (via *db* when provided).

    *allow_filesystem* gates raw paths (``./my.yaml``); ID-based lookups
    always reject path traversal. Web API callers should pass
    ``allow_filesystem=False``.

    Returns ``None`` when no matching workflow is found. Safe to call
    with ``db=None`` — behaves as the legacy filesystem-only resolver.
    """
    fqn = _parse_fqn(workflow_id)
    if fqn is not None:
        namespace, bare_id = fqn
        if db is None:
            return None
        return _resolve_from_packs(db, bare_id, target_namespace=namespace)

    fs_hit = _resolve_from_filesystem(workflow_id, allow_direct_path=allow_filesystem)
    if fs_hit is not None:
        path, source = fs_hit
        return WorkflowRef(id=workflow_id, path=path, source=source)

    if db is None:
        return None

    return _resolve_from_packs(db, workflow_id)


def list_available_workflows(
    db: ThreadSafeConnection | None = None,
    *,
    include_filesystem: bool = True,
    include_packs: bool = True,
) -> list[WorkflowRef]:
    """List every workflow reachable from filesystem + installed packs.

    Dedupe precedence: filesystem wins on id collision. The web listing
    and the CLI share this function so the two surfaces can never drift.
    """
    refs: list[WorkflowRef] = []
    seen_ids: set[str] = set()

    if include_filesystem:
        from .workflow_resolution import builtin_workflow_dirs

        for directory in builtin_workflow_dirs():
            if not directory.is_dir():
                continue
            # Classify: "workflows/" → built_in; "examples/" → example.
            source: Literal["built_in", "example"] = "example" if "example" in directory.name else "built_in"
            for yaml_path in sorted(directory.glob("*.yaml")):
                workflow_id = yaml_path.stem
                if not _is_safe_workflow_id(workflow_id):
                    continue
                if workflow_id in seen_ids:
                    continue
                seen_ids.add(workflow_id)
                refs.append(WorkflowRef(id=workflow_id, path=yaml_path, source=source))

    if include_packs and db is not None:
        for yaml_path, pack_workflow_id, pack_id, namespace in _list_pack_workflow_paths(db):
            if pack_workflow_id in seen_ids:
                # Filesystem wins; skip pack entry on collision.
                continue
            seen_ids.add(pack_workflow_id)
            refs.append(
                WorkflowRef(
                    id=pack_workflow_id,
                    path=yaml_path,
                    source="pack",
                    pack_id=pack_id,
                    namespace=namespace,
                )
            )

    return refs
