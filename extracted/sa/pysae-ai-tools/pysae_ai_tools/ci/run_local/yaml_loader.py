"""Deep-merge GitLab CI YAML documents for local job resolution.

The YAML parsing itself (custom-tag tolerance, ``!reference`` kept as a
:class:`Reference` sentinel) lives in the shared
:mod:`pysae_ai_tools.ci.common.gitlab_yaml` loader; this module only adds the
``ci run-local`` concerns: deep-merging documents and splitting out jobs.
"""

from typing import Any

from ..common.gitlab_yaml import RESERVED_TOP_LEVEL
from ..common.gitlab_yaml import parse as _parse


def parse(content: str) -> dict[str, Any]:
    """Parse a GitLab YAML document, keeping ``!reference`` as a sentinel."""
    return _parse(content, reference_mode="keep")


def _merge_into(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep-merge ``override`` into ``base``: mappings recurse, lists/scalars replace."""
    for key, value in override.items():
        if not isinstance(key, str):
            continue
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _merge_into(base[key], value)
        else:
            base[key] = value
    return base


def merge_documents(contents: list[str]) -> dict[str, Any]:
    """Parse and **deep-merge** raw YAML contents into a single top-level mapping.

    Documents are merged in order; later documents win on conflicts. Mappings
    (e.g. the ``variables:`` and ``default:`` blocks, same-named jobs) merge
    key-by-key — GitLab's ``include:`` semantics — so a value defined in one
    file is not wiped by another file that only redefines a sibling key. Lists
    and scalars are replaced wholesale. Callers must order ``contents`` so the
    highest-precedence document (the local ``.gitlab-ci.yml``) comes last.

    Both jobs *and* reserved keys (``variables``, ``default``, ``image``,
    ``services``) are kept — the resolver needs the reserved blocks too. Hidden
    templates (``.foo``) are preserved so ``extends:`` / ``!reference`` follow.
    """
    merged: dict[str, Any] = {}
    for content in contents:
        _merge_into(merged, parse(content))
    return merged


def split_jobs(full_map: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return only the job entries (named mappings, excluding reserved keys)."""
    jobs: dict[str, dict[str, Any]] = {}
    for name, body in full_map.items():
        if not isinstance(name, str) or name in RESERVED_TOP_LEVEL:
            continue
        if isinstance(body, dict):
            jobs[name] = body
    return jobs
