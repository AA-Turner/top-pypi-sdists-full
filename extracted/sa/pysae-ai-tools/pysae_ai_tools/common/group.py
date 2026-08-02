"""Resolve the GitLab **group** ai-tools operates on — generically, not hardcoded.

The group identity is org-wide, not per-repo, so it cannot live in a repo's
``.pysae-ai-tools.yaml``. It is resolved through a precedence chain that keeps the
current behaviour as a last-resort default while making the tool generic:

1. an explicit value (``--group`` / function arg);
2. the **current repo's origin namespace** (top segment of ``group/repo``) — zero-config,
   so the tool follows whatever org the checkout belongs to;
3. the ``PYSAE_AI_TOOLS_GROUP`` environment variable (for out-of-repo runs: cron,
   managed agents, …);
4. ``"pysae"`` — schema default, the only Pysae-specific value, kept so nothing breaks
   when none of the above resolves.

The numeric group ID (needed by the Epics REST API) is resolved **live** from the group
path via ``glab`` and cached on disk — there is no hardcoded ID anywhere.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from .glab_cache import _cache_read, _cache_write, _glab_api, current_project_path

GROUP_ENV_VAR = "PYSAE_AI_TOOLS_GROUP"
"""Environment variable overriding the group when no repo origin is available."""

DEFAULT_GROUP = "pysae"
"""Last-resort group (schema default) when nothing else resolves."""


@dataclass
class GroupIdentity:
    """The resolved group path plus where it came from (for visibility/debug)."""

    path: str
    source: str  # "explicit" | "origin" | "env" | "default"


def resolve_group_identity(explicit: str | None = None, root: Path | None = None) -> GroupIdentity:
    """Resolve the group path and its source following the documented precedence."""
    if explicit:
        return GroupIdentity(explicit.strip("/"), "explicit")
    project_path = current_project_path(root)
    if project_path:
        return GroupIdentity(project_path.split("/", 1)[0], "origin")
    env = os.environ.get(GROUP_ENV_VAR, "").strip()
    if env:
        return GroupIdentity(env.strip("/"), "env")
    return GroupIdentity(DEFAULT_GROUP, "default")


def resolve_group(explicit: str | None = None, root: Path | None = None) -> str:
    """Resolve just the group path (see :func:`resolve_group_identity`)."""
    return resolve_group_identity(explicit, root).path


def ensure_group_namespace(path: str, group: str | None = None) -> str:
    """Prefix a bare project name with the group when it lacks a namespace.

    ``op`` → ``<group>/op`` while an already-namespaced ``<group>/op`` or
    ``<group>/infra/foo`` is left untouched. ``group`` defaults to :func:`resolve_group`
    — resolve it once and pass it in when calling this in a loop.
    """
    g = group or resolve_group()
    return path if path.split("/", 1)[0] == g else f"{g}/{path}"


def resolve_group_id(group: str | None = None, *, refresh: bool = False) -> int:
    """Numeric ID of ``group`` (default: :func:`resolve_group`), via ``glab``, cached.

    Looks up ``glab api groups/<path>`` → ``.id`` and caches the result on disk
    (``refresh=True`` bypasses). Raises ``RuntimeError`` when glab is unavailable or the
    group can't be resolved — there is no hardcoded fallback ID.
    """
    path = group or resolve_group()
    cache_key = f"groupid:{path}"
    if not refresh:
        cached = _cache_read(cache_key)
        if cached is not None:
            cached_id = cached.get("id")
            if isinstance(cached_id, int):
                return cached_id
    rc, out, err = _glab_api(f"groups/{quote(path, safe='')}")
    if rc != 0:
        raise RuntimeError(f"cannot resolve group id for {path}: {err.strip() or 'glab error'}")
    try:
        gid = int(json.loads(out)["id"])
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
        raise RuntimeError(f"cannot parse group id for {path} from glab: {exc}") from exc
    _cache_write(cache_key, {"id": gid})
    return gid
