"""`probe import wandb` — deterministic W&B history mirror into an existing run.

Built because its absence was improvised badly once (the 2026-08-13 Anthrogen
'crashed' incident): with only the raw metrics API available, an agent dumped
two weeks of W&B history with INGEST-TIME wall clocks (a fictional time axis),
PATCHed the runs to 'running' (arming the reaper), and left them to be
declared crashed 15 minutes after the session ended. This command is what that
session needed:

  * wall clocks BACKDATED from W&B's own per-row timestamps; a row missing
    its timestamp is SKIPPED rather than stamped with ingest time -- the
    fictional time axis is the bug this tool exists to prevent;
  * incremental resume from a watermark stored on the run's own foreign keys
    (`wandb_last_step`, written only on successful completion) -- a crashed
    import re-sends its tail and the server's point-identity dedupe absorbs
    the overlap, so a cron re-mirror converges instead of duplicating;
  * `wandb_*` linkage merged onto the run's foreign keys;
  * an HONEST final status: a finished W&B run lands 'completed', a crashed
    one 'crashed' -- and a still-running one lands 'untracked' (mirrored,
    nothing attached), never 'running', because 'running' is a promise that a
    live process owns the run and a mirror is not that process. The owner
    check re-reads the run AFTER the (possibly long) history stream, so an
    owner that attached mid-import keeps its status untouched.

Deterministic by design: no agent in the loop, one W&B run in, one probe run
updated, counts printed. The `wandb` package is an optional dependency of this
command only.
"""

from __future__ import annotations

import math
from datetime import datetime
from probe._compat import UTC

import typer

from ..models import MetricPointIn
from ..sdk.run import Run, _metric_batch_body

import_app = typer.Typer(no_args_is_help=True, help="Import history from external trackers.")

#: Points per POST, flushed at ROW boundaries only -- a chunk that split one
#: W&B row across requests would, on a crash between them, leave a watermark
#: past the unflushed keys and lose them forever. (Purely a request-size
#: bound; each point carries its own step_index and wall_clock.)
_CHUNK = 500

#: W&B run states -> probe statuses. 'running' (and anything unrecognized)
#: maps to 'untracked' on purpose -- see the module docstring.
_STATE_MAP = {
    "finished": "completed",
    "crashed": "crashed",
    "failed": "failed",
    "killed": "canceled",
}


def _client():
    # Late import so tests monkeypatching `probe.cli.Client` reach this too.
    # importlib, not `from . import main`: the package __init__ re-exports the
    # entry FUNCTION under the name `main`, shadowing the submodule attribute.
    import importlib

    return importlib.import_module("probe.cli.main")._client()


def _load_wandb():
    try:
        import wandb  # noqa: PLC0415 -- optional, this command only

        return wandb
    except ImportError as exc:
        raise typer.BadParameter(
            "the `wandb` package is required for `probe import wandb` "
            "(pip install wandb); it is deliberately not a probe-research dependency"
        ) from exc


def _row_points(row: dict, step: int, wall_clock: str) -> list[MetricPointIn]:
    points = []
    for key, value in row.items():
        # bool is an int subclass; NaN/Inf poison series min/max and strict
        # JSON consumers. Both are W&B-history regulars.
        if key.startswith("_") or isinstance(value, bool):
            continue
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            continue
        points.append(
            MetricPointIn(
                key=key,
                kind="model",
                value=float(value),
                step_index=step,
                wall_clock=wall_clock,
            )
        )
    return points


@import_app.command("wandb")
def import_wandb(
    wandb_path: str = typer.Argument(
        ..., help="entity/project/run_id of the W&B run to mirror"
    ),
    run: str = typer.Option(
        ..., "--run", help="Probe run to import into (id, slug, or slug)"
    ),
) -> None:
    """Mirror one W&B run's metric history into an existing probe run."""
    if wandb_path.count("/") != 2:
        raise typer.BadParameter("wandb path must be entity/project/run_id")
    wandb = _load_wandb()
    client = _client()

    data = client.get_run(run)
    run_id = data["id"]

    wandb_run = wandb.Api().run(wandb_path)
    entity, project, wandb_run_id = wandb_path.split("/")

    # Watermark: OUR OWN previous import's high step, never a max over the
    # run's series catalog -- an unrelated SDK/derived series with a high step
    # would silently skip the whole mirror forever.
    raw_watermark = (data.get("foreign_keys") or {}).get("wandb_last_step")
    since = int(raw_watermark) if raw_watermark is not None else None

    def _flush(chunk: list[MetricPointIn]) -> None:
        # strict: an import must fail loudly, never spool -- a spooled replay
        # hours later would interleave with a live re-run.
        client.write(
            "POST", f"/v1/runs/{run_id}/metrics", _metric_batch_body(chunk), strict=True
        )

    points: list[MetricPointIn] = []
    imported = 0
    skipped_unstamped = 0
    last_step: int | None = None
    for row in wandb_run.scan_history():
        step = row.get("_step")
        if step is None or (since is not None and step <= since):
            continue
        stamp = row.get("_timestamp")
        if stamp is None:
            skipped_unstamped += 1
            continue
        row_points = _row_points(
            row, int(step), datetime.fromtimestamp(stamp, UTC).isoformat()
        )
        if not row_points:
            continue
        if points and len(points) + len(row_points) > _CHUNK:
            _flush(points)
            imported += len(points)
            points = []
        points.extend(row_points)
        last_step = int(step)
    if points:
        _flush(points)
        imported += len(points)

    # Linkage + watermark ride the run's foreign keys (per-key new-wins merge
    # server-side). strict for the same reason as the metric writes: a spooled
    # watermark replayed later could mask points a rerun still needs to send.
    link_keys: dict = {
        "wandb_entity": entity,
        "wandb_project": project,
        "wandb_run_id": wandb_run_id,
    }
    if last_step is not None:
        link_keys["wandb_last_step"] = last_step
    Run(client, data).link(strict=True, **link_keys)

    # Owner check on FRESH data: the history stream above can run for minutes,
    # and an owner that attached during it must keep its status.
    data = client.get_run(run_id)
    status_note = "left alone (a live owner has beaten on this run)"
    if data.get("last_heartbeat_at") is None:
        status = _STATE_MAP.get(getattr(wandb_run, "state", None), "untracked")
        # strict=True: the line printed below CLAIMS the status was set. Every
        # other write in this command is already strict for that reason; this
        # one was left bare, and set_status stopped propagating transport
        # errors, so a failure would journal and still print success.
        Run(client, data).set_status(status, strict=True)
        status_note = f"set to {status!r} (wandb state {getattr(wandb_run, 'state', None)!r})"

    resumed = f" (resumed above step {since})" if since is not None else ""
    unstamped = (
        f"; skipped {skipped_unstamped} row(s) without a W&B timestamp"
        if skipped_unstamped
        else ""
    )
    typer.echo(
        f"imported {imported} points from {wandb_path}"
        f"{f' up to step {last_step}' if last_step is not None else ''}{resumed}"
        f"{unstamped}; status {status_note}"
    )
