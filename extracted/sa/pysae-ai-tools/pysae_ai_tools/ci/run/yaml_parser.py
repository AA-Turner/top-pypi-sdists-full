"""Extract the effective ``needs:`` per job from GitLab CI YAML.

The YAML parsing itself (custom-tag tolerance, ``!reference`` handling) lives in
the shared :mod:`pysae_ai_tools.ci.common.gitlab_yaml` loader; this module only
adds the ``ci run`` concerns: merging documents into a jobs map, following
``extends:`` chains, and reading the ``include:`` block.
"""

from typing import Any

from ..common.gitlab_yaml import RESERVED_TOP_LEVEL, normalize_needs, parse


def parse_yaml(content: str) -> dict[str, Any]:
    """Parse a GitLab YAML document, flattening ``!reference`` into plain data."""
    return parse(content, reference_mode="flatten")


def merge_jobs(documents: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Merge multiple parsed YAML docs into a single jobs map.

    Documents are merged in order; later ones override earlier ones. Callers
    must order ``documents`` so the highest-precedence document (the local
    ``.gitlab-ci.yml``) comes last — see :func:`gather_yaml_documents`. Reserved
    top-level keys are excluded. Hidden templates (``.foo``) are kept so that
    ``extends:`` resolution can follow them.
    """
    jobs: dict[str, dict[str, Any]] = {}
    for doc in documents:
        if not isinstance(doc, dict):
            continue
        for name, body in doc.items():
            if not isinstance(name, str) or name in RESERVED_TOP_LEVEL:
                continue
            if not isinstance(body, dict):
                continue
            jobs[name] = body
    return jobs


def effective_needs(name: str, jobs: dict[str, dict[str, Any]]) -> list[str]:
    """Return the effective ``needs:`` list for a job, following ``extends:``.

    Returns an empty list when the job has no ``needs:`` (directly or
    through any ``extends:`` parent).
    """
    resolved = _resolve_needs(name, jobs, set())
    return resolved if resolved is not None else []


def _resolve_needs(name: str, jobs: dict[str, dict[str, Any]], visited: set[str]) -> list[str] | None:
    if name in visited or name not in jobs:
        return None
    visited.add(name)
    job = jobs[name]

    if "needs" in job:
        return normalize_needs(job["needs"])

    extends = job.get("extends")
    parents: list[str] = []
    if isinstance(extends, str):
        parents = [extends]
    elif isinstance(extends, list):
        parents = [p for p in extends if isinstance(p, str)]

    for parent in parents:
        inherited = _resolve_needs(parent, jobs, visited)
        if inherited is not None:
            return inherited
    return None


def parse_includes(content: str) -> list[dict[str, Any]]:
    """Extract the ``include:`` block of a GitLab YAML as a normalized list.

    Supported entry forms:
        - string ``"path/to/file.yml"`` → ``{"local": ...}``
        - mapping with ``project`` + ``file`` + optional ``ref``
        - mapping with ``local`` (path inside the current repo)
        - mapping with ``remote`` (HTTP URL — recorded but not fetched here)
        - mapping with ``template`` (GitLab-managed templates — recorded only)
    """
    data = parse_yaml(content)
    raw = data.get("include")
    if raw is None:
        return []
    if isinstance(raw, (str, dict)):
        raw = [raw]
    if not isinstance(raw, list):
        return []

    out: list[dict[str, Any]] = []
    for entry in raw:
        if isinstance(entry, str):
            out.append({"local": entry})
        elif isinstance(entry, dict):
            out.append(dict(entry))
    return out
