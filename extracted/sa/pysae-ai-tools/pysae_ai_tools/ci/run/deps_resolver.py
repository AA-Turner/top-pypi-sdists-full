"""Pure dependency-graph resolution for the CI job runner.

Everything here operates on data already in memory (a list of :class:`Job`
objects, the ``.gitlab-ci.yml`` text) and never plays, retries, waits or sleeps.
The only I/O is reading the local ``.gitlab-ci.yml`` (and, transitively,
fetching ``include:`` templates) in :func:`resolve_deps_from_yaml`; the graph
functions it delegates to (:func:`_resolve_chain`, :func:`fuzzy_match_job`,
:func:`resolve_target_job`, the stage-order helpers) are side-effect free and
directly unit-testable.
"""

import re
from difflib import SequenceMatcher
from pathlib import Path

from .gitlab_api import Job
from .include_resolver import gather_yaml_documents
from .yaml_parser import effective_needs, merge_jobs, parse_yaml


def fuzzy_match_job(query: str, jobs: list[Job]) -> list[Job]:
    """Find jobs matching a query string (exact, prefix, or fuzzy)."""
    query_lower = query.lower().replace(" ", "_").replace("-", "_")

    # Exact match
    for job in jobs:
        if job.name.lower() == query_lower:
            return [job]

    # Prefix/substring match
    matches = [j for j in jobs if query_lower in j.name.lower().replace("-", "_")]
    if matches:
        return matches

    # Fuzzy match (similarity > 0.5)
    scored = []
    for job in jobs:
        ratio = SequenceMatcher(None, query_lower, job.name.lower().replace("-", "_")).ratio()
        if ratio > 0.5:
            scored.append((ratio, job))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [j for _, j in scored[:5]]


def resolve_target_job(target_name: str, jobs: list[Job]) -> tuple[Job | None, str]:
    """Resolve a single target job from a name, disambiguating fuzzy matches.

    Returns ``(job, "")`` on a unique match, or ``(None, error)`` when the name
    matches no job or several with no exact winner. The error message lists the
    available or conflicting job names, ready to surface to the user.
    """
    matches = fuzzy_match_job(target_name, jobs)
    if not matches:
        available = ", ".join(j.name for j in sorted(jobs, key=lambda x: x.id))
        return None, f"Job '{target_name}' non trouvé. Jobs disponibles : {available}"
    if len(matches) > 1:
        exact = [m for m in matches if m.name.lower() == target_name.lower()]
        if len(exact) == 1:
            return exact[0], ""
        names = ", ".join(m.name for m in matches)
        return None, f"Plusieurs jobs correspondent à '{target_name}' : {names}"
    return matches[0], ""


def resolve_deps_from_yaml(target_job_name: str, jobs: list[Job]) -> tuple[list[str], dict[str, list[str]]]:
    """Resolve the dependency chain for a job by parsing ``.gitlab-ci.yml``.

    Walks ``include:`` to fetch remote templates from GitLab (cached by ref),
    then merges every reachable YAML document into a single jobs map and
    follows the ``extends:`` chain to compute effective ``needs:`` per job.

    Falls back to a regex-based parse of the local file (and finally to
    stage-order ordering) when YAML parsing fails or the target is absent
    from the merged map — for example because templates couldn't be fetched.

    Returns ``(chain, needs_map)``. ``needs_map`` is the effective ``needs:``
    per job and is consumed by :func:`add_manual_gates` to distinguish DAG
    dependencies (no stage-order gating) from stage-ordered jobs (gated by
    earlier stages). It is empty when the stage-order fallback was used —
    callers should then assume nothing is known about explicit needs.
    """
    yaml_content = _read_ci_yaml()
    if not yaml_content:
        return _stage_order_fallback(target_job_name, jobs), {}

    documents_text = gather_yaml_documents(yaml_content)
    parsed_docs = [parse_yaml(text) for text in documents_text]
    merged = merge_jobs(parsed_docs)

    if target_job_name in merged:
        needs_map = {name: effective_needs(name, merged) for name in merged if not name.startswith(".")}
        return _resolve_chain(target_job_name, needs_map), needs_map

    # YAML parsing didn't surface the target — try the regex parser on the
    # local file alone (may still find inline ``needs:`` declarations).
    fallback_needs = _parse_needs_from_yaml(yaml_content)
    if target_job_name in fallback_needs:
        return _resolve_chain(target_job_name, fallback_needs), fallback_needs

    return _stage_order_fallback(target_job_name, jobs), {}


def _read_ci_yaml() -> str:
    """Read .gitlab-ci.yml from the repo root."""
    for candidate in [Path(".gitlab-ci.yml"), Path(".gitlab-ci.yaml")]:
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    return ""


def _parse_needs_from_yaml(content: str) -> dict[str, list[str]]:
    """Extract needs: directives from YAML content (lightweight parsing).

    We do a simple regex-based parse to avoid a PyYAML dependency.
    Handles:
    - needs: [job1, job2]
    - needs:\n  - job1\n  - job2
    - needs:\n  - job: job1
    """
    needs_map: dict[str, list[str]] = {}
    current_job: str | None = None
    in_needs = False
    indent_level = 0

    for line in content.splitlines():
        stripped = line.lstrip()

        # Top-level job definition (not indented, ends with :, not a keyword)
        if line and not line[0].isspace() and line.rstrip().endswith(":") and not stripped.startswith(("#", ".")):
            job_name = line.rstrip().rstrip(":")
            if job_name not in ("stages", "variables", "default", "include", "workflow", "image", "services", "cache"):
                current_job = job_name
                in_needs = False
            continue

        if not current_job:
            continue

        # Detect needs: directive
        if stripped.startswith("needs:"):
            in_needs = True
            indent_level = len(line) - len(stripped)
            # Inline array: needs: [job1, job2]
            inline = stripped[len("needs:") :].strip()
            if inline.startswith("["):
                items = re.findall(r"[\w][\w./-]*", inline)
                needs_map[current_job] = items
                in_needs = False
            else:
                needs_map.setdefault(current_job, [])
            continue

        # Inside a needs: block
        if in_needs and current_job:
            line_indent = len(line) - len(stripped)
            if line_indent <= indent_level and stripped and not stripped.startswith("-"):
                in_needs = False
                continue
            if stripped.startswith("- job:"):
                job_ref = stripped[len("- job:") :].strip().strip("\"'")
                needs_map[current_job].append(job_ref)
            elif stripped.startswith("- "):
                job_ref = stripped[2:].strip().strip("\"'")
                if job_ref and not job_ref.startswith("{"):
                    needs_map[current_job].append(job_ref)

    return needs_map


def _resolve_chain(target: str, needs_map: dict[str, list[str]]) -> list[str]:
    """Recursively resolve the dependency chain, returning execution order."""
    visited: set[str] = set()
    order: list[str] = []

    def _visit(name: str) -> None:
        if name in visited:
            return
        visited.add(name)
        for dep in needs_map.get(name, []):
            _visit(dep)
        order.append(name)

    _visit(target)
    return order


def _stage_order_from_jobs(jobs: list[Job]) -> list[str]:
    """Derive stage order from the pipeline's jobs (sorted by id)."""
    order: list[str] = []
    for j in sorted(jobs, key=lambda x: x.id):
        if j.stage not in order:
            order.append(j.stage)
    return order


def _stage_order_fallback(target_name: str, jobs: list[Job]) -> list[str]:
    """Fall back to running all jobs from earlier stages (when no needs: found)."""
    target_job = next((j for j in jobs if j.name == target_name), None)
    if not target_job:
        return [target_name]

    stage_order = _stage_order_from_jobs(jobs)
    target_stage_idx = stage_order.index(target_job.stage) if target_job.stage in stage_order else -1
    if target_stage_idx < 0:
        return [target_name]

    # All jobs from earlier stages + target
    chain = [j.name for j in jobs if j.stage in stage_order[:target_stage_idx]]
    chain.append(target_name)
    return chain
