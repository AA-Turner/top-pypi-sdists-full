"""A script that logs to W&B and Probe makes one run (plan A.5): when `probe.init` opens a run while a `wandb.run`
is active, that W&B run's id goes on the Probe run, so a later W&B import or attachment fills it instead of making
a second one (`foreign_keys.wandb_external_id`, read by the server's claim and mirror)."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from probe.sdk.run.run import Run

#: The foreign key the server's claim and mirror look a W&B run up by (`wandb:entity/project/run_id`).
EXTERNAL_ID_KEY = "wandb_external_id"


def link_active_wandb_run(run: "Run") -> dict[str, str] | None:
    """Record the active `wandb.run` (if this process has one) on `run`; the keys sent, else None. Never imports
    `wandb` (only reads it when the script already did) and never raises: a link is a nicety, not the run."""
    found = read_active_wandb_run()
    if found is None:
        return None
    try:
        run.link(**found)
    except Exception:  # noqa: BLE001 -- best effort: the run goes on without the link
        return None
    return found


def read_active_wandb_run() -> dict[str, str] | None:
    """The active W&B run's keys (`wandb_external_id`, `wandb_run_id`, `wandb_project`, `wandb_entity`), or None
    when `wandb` is not imported, no run is active, or it is offline with no entity yet."""
    wandb = sys.modules.get("wandb")
    active: Any = getattr(wandb, "run", None) if wandb is not None else None
    if active is None:
        return None
    try:
        run_id, project, entity = str(active.id), str(active.project or ""), str(active.entity or "")
    except Exception:  # noqa: BLE001 -- a W&B run object in an odd state reads as none
        return None
    if not (run_id and project and entity):
        return None
    return {EXTERNAL_ID_KEY: f"wandb:{entity}/{project}/{run_id}", "wandb_run_id": run_id,
            "wandb_project": project, "wandb_entity": entity}
