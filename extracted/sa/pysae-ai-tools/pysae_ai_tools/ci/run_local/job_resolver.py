"""Resolve a CI job into a concrete, runnable shape.

Handles, in order: ``extends:`` deep-merge (multi-parent, multi-level),
``default:`` inheritance, ``!reference`` expansion, then flattening of the
``before_script`` / ``script`` / ``after_script`` blocks into flat command
lists. Image variable expansion is deferred to the caller (it needs the fully
resolved environment, which is built separately).
"""

import copy
from typing import Any

from ..common.gitlab_yaml import Reference, normalize_needs
from .models import ResolvedJob

# GitLab caps ``extends`` nesting at 11 levels; we guard a bit above that.
_MAX_EXTENDS_DEPTH = 15
_MAX_REFERENCE_DEPTH = 30

# ``default:`` keys we propagate to a job that does not define them itself.
_DEFAULT_INHERITED = ("image", "before_script", "after_script", "services", "tags", "cache")


def _scalar_to_str(value: Any) -> str:
    """Coerce a YAML scalar to the string GitLab would expose as a variable."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def _normalize_extends(extends: Any) -> list[str]:
    if isinstance(extends, str):
        return [extends]
    if isinstance(extends, list):
        return [p for p in extends if isinstance(p, str)]
    return []


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge ``override`` into ``base`` (GitLab ``extends`` semantics).

    Mappings are merged recursively; lists and scalars are replaced wholesale.
    Returns ``base`` (mutated) for convenience.
    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = copy.deepcopy(value)
    return base


def resolve_extends(name: str, full_map: dict[str, Any], seen: set[str], depth: int = 0) -> dict[str, Any]:
    """Return the deep-merged body of ``name`` following its ``extends:`` chain."""
    if depth > _MAX_EXTENDS_DEPTH or name in seen:
        return {}
    job = full_map.get(name)
    if not isinstance(job, dict):
        return {}

    result: dict[str, Any] = {}
    for parent in _normalize_extends(job.get("extends")):
        parent_body = resolve_extends(parent, full_map, seen | {name}, depth + 1)
        _deep_merge(result, parent_body)

    own = {k: v for k, v in job.items() if k != "extends"}
    _deep_merge(result, own)
    return result


def _lookup(full_map: dict[str, Any], path: list[str]) -> Any:
    node: Any = full_map
    for key in path:
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return None
    return node


def resolve_references(value: Any, full_map: dict[str, Any], depth: int = 0) -> Any:
    """Recursively replace :class:`Reference` sentinels with their target value."""
    if depth > _MAX_REFERENCE_DEPTH:
        return None
    if isinstance(value, Reference):
        target = _lookup(full_map, value.path)
        if target is None:
            return None
        return resolve_references(target, full_map, depth + 1)
    if isinstance(value, dict):
        return {k: resolve_references(v, full_map, depth + 1) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve_references(v, full_map, depth + 1) for v in value]
    return value


def flatten_script(value: Any) -> list[str]:
    """Flatten a (possibly nested) script block into a flat list of commands."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(flatten_script(item))
        return out
    return []


def parse_image(image_value: Any) -> tuple[str, list[str] | None]:
    """Return the (raw, unexpanded) image name and optional entrypoint override."""
    if isinstance(image_value, str):
        return image_value, None
    if isinstance(image_value, dict):
        name = image_value.get("name", "")
        entrypoint = image_value.get("entrypoint")
        entry = [str(e) for e in entrypoint] if isinstance(entrypoint, list) else None
        return (str(name) if name else ""), entry
    return "", None


def _normalize_dependencies(deps: Any) -> list[str] | None:
    if deps is None:
        return None
    if isinstance(deps, str):
        return [deps]
    if isinstance(deps, list):
        return [d for d in deps if isinstance(d, str)]
    return None


def _service_names(services: Any) -> list[str]:
    if not isinstance(services, list):
        return []
    names: list[str] = []
    for svc in services:
        if isinstance(svc, str):
            names.append(svc)
        elif isinstance(svc, dict) and isinstance(svc.get("name"), str):
            names.append(svc["name"])
    return names


def build_resolved_job(name: str, full_map: dict[str, Any]) -> ResolvedJob:
    """Resolve ``name`` into a :class:`ResolvedJob` (image kept unexpanded)."""
    if name not in full_map or not isinstance(full_map.get(name), dict):
        raise KeyError(name)

    merged = resolve_extends(name, full_map, set())
    merged = resolve_references(merged, full_map)

    default_block = full_map.get("default")
    if isinstance(default_block, dict):
        for key in _DEFAULT_INHERITED:
            if key not in merged and key in default_block:
                merged[key] = resolve_references(copy.deepcopy(default_block[key]), full_map)

    # Top-level ``image:`` is GitLab's (legacy) global default, equivalent to
    # ``default: image:`` — inherit it when the job still has no image.
    if "image" not in merged and isinstance(full_map.get("image"), (str, dict)):
        merged["image"] = resolve_references(copy.deepcopy(full_map["image"]), full_map)

    raw_image, entrypoint = parse_image(merged.get("image"))

    job_vars: dict[str, str] = {}
    raw_vars = merged.get("variables")
    if isinstance(raw_vars, dict):
        job_vars = {str(k): _scalar_to_str(v) for k, v in raw_vars.items()}

    job = ResolvedJob(
        name=name,
        stage=str(merged.get("stage", "test") or "test"),
        image=raw_image,
        image_entrypoint=entrypoint,
        before_script=flatten_script(merged.get("before_script")),
        script=flatten_script(merged.get("script")),
        after_script=flatten_script(merged.get("after_script")),
        variables=job_vars,
        needs=normalize_needs(merged.get("needs")),
        dependencies=_normalize_dependencies(merged.get("dependencies")),
        services=_service_names(merged.get("services")),
    )

    if not job.script and not job.before_script:
        job.warnings.append(f"Job '{name}' has no script/before_script after resolution — nothing to run.")
    if job.services:
        job.warnings.append(
            f"Job '{name}' declares services ({', '.join(job.services)}) — not started locally; "
            "start them yourself if the script needs them."
        )
    return job
