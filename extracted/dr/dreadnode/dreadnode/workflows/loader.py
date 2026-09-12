"""Load the authored ``Workflow`` behind a stored definition.

Executing a workflow needs more than its topology: the topology says *what* the
graph is, but running it needs the step bodies, which live in the capability's
source. So the runtime host resolves the capability locally and imports the
module the topology was compiled from.

That is not a limitation of local execution — it is what the runtime host *is*.
Capability code runs in the capability runtime; the platform stores a compiled
description of it and never imports it.
"""

import hashlib
import importlib.util
import sys
import types
import typing as t
from pathlib import Path

from dreadnode_workflow_core import Topology

from dreadnode.workflows.workflow import Workflow

__all__ = ["WorkflowSourceNotFound", "load_workflow_file", "load_workflow_for_definition"]


class WorkflowSourceNotFound(ValueError):  # noqa: N818 - reads as the condition, not an error type
    """The capability source for a definition could not be located locally."""


def load_workflow_file(path: Path, capability_root: Path | None = None) -> Workflow:
    """Import a workflow module and return its single ``Workflow`` object."""
    if not path.is_file():
        raise WorkflowSourceNotFound(f"workflow source not found: {path}")

    root = (capability_root or path.parent).resolve()
    relative = path.resolve().relative_to(root).with_suffix("")
    package_root = "_dn_capability_" + hashlib.sha256(str(root).encode()).hexdigest()[:12]
    package_parts = (package_root, *relative.parts)
    for index in range(1, len(package_parts)):
        package_name = ".".join(package_parts[:index])
        package_path = root.joinpath(*relative.parts[: max(index - 1, 0)])
        if package_name not in sys.modules:
            package = types.ModuleType(package_name)
            package.__package__ = package_name
            package.__dict__["__path__"] = [str(package_path)]
            sys.modules[package_name] = package

    module_name = ".".join(package_parts)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise WorkflowSourceNotFound(f"cannot import workflow module: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    workflows = [v for v in vars(module).values() if isinstance(v, Workflow)]
    if not workflows:
        raise WorkflowSourceNotFound(f"{path} declares no Workflow object")
    if len(workflows) > 1:
        raise WorkflowSourceNotFound(
            f"{path} declares {len(workflows)} Workflow objects; exactly one per file is supported"
        )
    # Parent packages stay registered so a step can perform a relative import
    # when its body runs. This module is replaced on the next load.
    return workflows[0]


def load_workflow_for_definition(
    definition: dict[str, t.Any],
    *,
    search_paths: list[Path] | None = None,
) -> tuple[Workflow, Topology]:
    """Resolve a stored definition to its authored workflow and topology.

    Args:
        definition: A ``WorkflowDefinitionResponse`` payload.
        search_paths: Where to look for the capability. Defaults to the
            configured capability directories.

    Raises:
        WorkflowSourceNotFound: When the capability is not installed locally, or
            its source no longer matches the compiled definition.
    """
    topology_json = definition.get("topology_json") or {}
    topology = Topology.model_validate(topology_json)

    source = topology_json.get("source") or {}
    relative = source.get("path")
    if not relative:
        raise WorkflowSourceNotFound(
            f"definition {definition.get('name')!r} records no source path; "
            f"it may have been compiled by an older SDK"
        )

    capability_name = definition.get("capability_name") or ""
    capability_version = definition.get("capability_version") or ""
    root = _find_capability_root(capability_name, capability_version, search_paths)
    if root is None:
        raise WorkflowSourceNotFound(
            f"capability {capability_name!r}@{capability_version} is not installed "
            "locally, so this pinned workflow cannot execute here"
        )

    workflow_path = root / relative
    expected_source_sha256 = topology.source_sha256
    if not expected_source_sha256:
        raise WorkflowSourceNotFound(
            "definition records no workflow source digest; compile and push it again"
        )
    try:
        actual_source_sha256 = hashlib.sha256(workflow_path.read_bytes()).hexdigest()
    except OSError as exc:
        raise WorkflowSourceNotFound(f"workflow source not found: {workflow_path}") from exc
    if actual_source_sha256 != expected_source_sha256:
        raise WorkflowSourceNotFound(
            f"local workflow source does not match definition {definition.get('id')}; "
            "install the pinned capability version"
        )

    workflow = load_workflow_file(workflow_path, root)
    if workflow.name != definition.get("name"):
        raise WorkflowSourceNotFound(
            f"local source declares workflow {workflow.name!r} but the definition "
            f"is {definition.get('name')!r} — the capability may be out of date"
        )
    return workflow, topology


def _find_capability_root(name: str, version: str, search_paths: list[Path] | None) -> Path | None:
    """Locate an installed capability directory by manifest name and version."""
    from dreadnode.capabilities.loader import resolve_search_paths

    bare = name.rsplit("/", 1)[-1]
    roots = search_paths or resolve_search_paths()

    for root in roots:
        if not root.is_dir():
            continue
        for candidate in (root, *sorted(root.iterdir())):
            manifest = candidate / "capability.yaml"
            if not manifest.is_file():
                continue
            identity = _manifest_identity(manifest)
            if identity is not None and identity[0] in (name, bare) and identity[1] == version:
                return candidate
    return None


def _manifest_identity(manifest: Path) -> tuple[str, str] | None:
    import yaml

    try:
        data = yaml.safe_load(manifest.read_text())
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    name = data.get("name")
    version = data.get("version")
    if not isinstance(name, str) or not isinstance(version, str):
        return None
    return name, version
