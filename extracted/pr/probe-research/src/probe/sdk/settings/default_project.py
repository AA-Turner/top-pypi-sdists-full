"""This computer's default project (`probe project use`): saved in the context file, beside the
workspace it is filed in. One writer for the CLI command and a run's project prompt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from probe.sdk.settings import workspace_pin
from probe.sdk.settings.settings import load_context, resolve, save_context


@dataclass
class DefaultProjectSave:
    """What `save_default_project` did. `refused`: why nothing was saved (a workspace limit);
    `moved_to`: the workspace the pin moved to (its name, else its id), when it moved."""

    project: dict
    refused: str | None = None
    moved_to: str | None = None


def save_default_project(client: Any, project: dict, *, what: str) -> DefaultProjectSave:
    """Make `project` (a project row) this computer's default, pinned under the workspace that
    owns it, not the ambient one. `what` names the caller in a workspace-limit refusal."""
    saved = load_context().get("workspace")
    before = _strip_id_prefix(saved.get("id")) if isinstance(saved, dict) else None
    if before is None and not project.get("workspace_id"):
        before = client.workspace_id_for(resolve(workspace=None).workspace)
    # Pin the project under the workspace that actually owns it: selecting a project from another
    # workspace moves the anchor. workspace_id is nullable on legacy rows: fall back to ambient.
    owner = project.get("workspace_id") or before
    moved = owner is not None and str(owner) != str(before or "")
    refused = workspace_pin.refusal_for_pin_move(str(owner) if owner else None, what=what)
    if refused:
        return DefaultProjectSave(project, refused=refused)
    name = client.get_workspace(str(owner)).get("name") if moved else None
    # Stored as `id:<uuid>`: an id survives a rename where a slug does not, and a BARE id would
    # read as a slug when it flows back in as a default.
    save_context(
        {"workspace": workspace_pin.keep_limit_keys({"id": str(owner) if owner else None, "project": f"id:{project['id']}"})}
    )
    return DefaultProjectSave(project, moved_to=(name or str(owner)) if moved else None)


def _strip_id_prefix(ref: object) -> str | None:
    """`id:<uuid>` -> `<uuid>`; any other ref unchanged (`refs.split_selector`'s id case)."""
    if not isinstance(ref, str):
        return None
    return ref[3:] if ref.startswith("id:") else ref
