"""Resolve project names to full GitLab paths, generically (no hardcoded alias table).

A bare name is namespaced under the resolved group (origin / env / default — see
``common.group``); a value that already carries a namespace is passed through. So
``op`` → ``<group>/op`` and ``shift/app`` → ``<group>/shift/app``, while ``pysae/api``
stays as-is. ai-tools holds no per-project alias map.
"""

from ..common.group import ensure_group_namespace, resolve_group


def resolve_project(name: str) -> str:
    """Namespace a bare project name under the resolved group; pass through a full path."""
    return ensure_group_namespace(name, resolve_group())


def resolve_projects(names: list[str]) -> list[str]:
    """Resolve a list, dedup while preserving first-seen order."""
    group = resolve_group()
    seen: set[str] = set()
    out: list[str] = []
    for n in names:
        full = ensure_group_namespace(n, group)
        if full not in seen:
            seen.add(full)
            out.append(full)
    return out
