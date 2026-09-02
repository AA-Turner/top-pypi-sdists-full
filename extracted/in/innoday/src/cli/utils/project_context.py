"""
Auto-discovery of org/project context from a workspace's .innoday/project.yml.

Mirrors the _find_project_root() pattern pixelfuel-claude skills already use
(walk up from cwd looking for .innoday/project.yml), so a bare `innoday
tickets create ...` run from inside a project workspace resolves the same
org/project context those skills already read manually. This is the sole
mechanism for org/project resolution -- there is no persistent `orgs switch`
/ `projects switch` command; pass --organization explicitly for one-shot
overrides outside any project directory.
"""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# The .innoday/project.yml format version this build reads/writes. Bump when the
# schema changes incompatibly. Files without this stamp (or with an older one)
# predate the alias/versioning migration and must be regenerated via
# `innoday refresh`.
PROJECT_YML_SCHEMA_VERSION = 2


class LegacyProjectFileError(Exception):
    """Raised when a .innoday/project.yml exists but is an outdated format
    (missing `schema_version`/`org.alias`, or an older schema version). The
    remedy is always `innoday refresh` to regenerate it. Distinct from "no
    project.yml found at all", which is a normal None result.

    `org_name`/`project_name` are best-effort human-readable labels pulled from
    the legacy file when present (they survive across schema versions), so the
    message can name the workspace the user is standing in rather than only its
    path."""

    def __init__(
        self,
        path: Path,
        reason: str,
        org_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ):
        self.path = path
        self.reason = reason
        self.org_name = org_name
        self.project_name = project_name

        # Name the workspace when we can read it — "the PixelFuel project
        # (Haviland Software)" is friendlier and more actionable than a bare
        # path, and confirms to the user which project.yml is stale.
        if project_name and org_name:
            where = f"the {project_name} project ({org_name})"
        elif project_name:
            where = f"the {project_name} project"
        elif org_name:
            where = f"the {org_name} workspace"
        else:
            where = "this workspace"

        super().__init__(
            f"{where} needs a quick refresh — its project file is an older "
            f"format ({reason}).\n"
            f"  Run `innoday refresh` here to bring it up to schema "
            f"v{PROJECT_YML_SCHEMA_VERSION}.\n"
            f"  File: {path}"
        )


def find_project_yml(start: Optional[Path] = None) -> Optional[Path]:
    """Walk up from `start` (default: cwd) looking for .innoday/project.yml."""
    current = (start or Path.cwd()).resolve()
    for directory in [current, *current.parents]:
        candidate = directory / ".innoday" / "project.yml"
        if candidate.is_file():
            return candidate
    return None


def load_project_context(start: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """
    Discover and parse .innoday/project.yml, returning the org/project fields
    needed for CLI context resolution.

    Returns None if no project.yml is found or it can't be parsed. Raises
    LegacyProjectFileError if a file IS found but is an outdated format
    (missing the `schema_version` stamp or `org.alias`) — the caller should
    surface that so the user runs `innoday refresh`.
    """
    path = find_project_yml(start)
    if path is None:
        return None

    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return None

    schema_version = data.get("schema_version")
    org = data.get("org") or {}
    project = data.get("project") or {}
    org_alias = org.get("alias")

    # A file that predates versioning/alias — has content but no stamp or the
    # legacy `slug` key instead of `alias` — is an explicit upgrade prompt, not
    # a silent fallback.
    if schema_version is None or not org_alias:
        if "slug" in org or schema_version is None:
            reason = (
                "missing schema_version"
                if schema_version is None
                else "uses legacy org.slug instead of org.alias"
            )
            raise LegacyProjectFileError(
                path,
                reason,
                org_name=org.get("name"),
                project_name=project.get("name"),
            )
        return None
    if schema_version != PROJECT_YML_SCHEMA_VERSION:
        raise LegacyProjectFileError(
            path,
            f"schema_version {schema_version} != {PROJECT_YML_SCHEMA_VERSION}",
            org_name=org.get("name"),
            project_name=project.get("name"),
        )

    org_id = org.get("innoday_id")
    project_id = project.get("innoday_id")
    if not org_id:
        return None

    resolved_project_id = project_id if project_id and project_id != "~" else None
    return {
        "org_alias": org_alias,
        "org_id": org_id,
        "org_name": org.get("name") or org_alias,
        "project_id": resolved_project_id,
        # The org's human name was already here; the project's was not, so any
        # caller wanting to *show* which project it resolved had only the UUID
        # to print. `innoday summary` did exactly that -- "Team · last 3d ·
        # 4f61ff9f-8138-..." where it should read "BPAI".
        "project_alias": project.get("alias"),
        "project_name": project.get("name"),
        "source_path": str(path),
    }
