"""probe trial ...: Harbor/Miles rollout trials (list, get, set, stage, add, reconcile, export, drain, watch, expand)."""

from __future__ import annotations
import json
from typing import Any, Optional

import typer
from probe.cli.commands.entity_text import description_opt
from probe.cli.commands.json_print import _FIELDS_OPTION, _print_json, _select_fields
from probe.cli.commands.refs import _ref, run_ref


# -- Trials: the entity, and the Harbor capture that produces them ------------
#
# ONE GROUP, two halves, and they are not parallel. `stage/add/reconcile/export/
# drain/watch/expand` CAPTURE trials out of a Harbor sandbox; `list/get/set` read
# and author the rows that capture produced (research-os 0135). They share a noun
# because they are the same noun -- a second `probe rollout` group would have made
# a researcher learn which word this lab uses for the thing they are looking at,
# and the dashboard already answered that question with "trial".
trial_app = typer.Typer(
    no_args_is_help=True, help="rollout trials: read and author them, and capture Harbor's"
)


@trial_app.command("list")
def trial_list(
    run: str = run_ref(),
    limit: int = typer.Option(None, "--limit", help="rows per page (server max 200)"),
    cursor: str = typer.Option(None, "--cursor", help="continue from a previous page"),
) -> None:
    """List a run's trials, newest step first.

    This is the AUTHORED inventory, not `probe span list --type rollout`: the
    span is what the producer emitted and the trial is the row beside it that
    holds a title, a description and a note. A trial also survives outside a
    bounded span slice, so this finds ones a span listing reports as absent.
    """
    with _client() as c:
        page = c.list_run_trials(_ref(c, "run", run).id, cursor=cursor, limit=limit)
    _print_json({"trials": page.items, "next_cursor": page.next_cursor})


@trial_app.command("get")
def trial_get(
    trial_id: str = typer.Argument(..., help="the trial's rollout span id"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """Show one trial.

    The id is the ROLLOUT SPAN id -- the last segment of a dashboard
    `/runs/<run>/trials/<id>` link, so a URL a teammate pasted works here
    unedited. `probe trial list` is where it comes from otherwise.
    """
    with _client() as c:
        _print_json(_select_fields(c.get_trial(trial_id), fields))


@trial_app.command("set")
def trial_set(
    trial_id: str = typer.Argument(..., help="the trial's rollout span id"),
    name: str = typer.Option(None, "--name"),
    description: str = description_opt(),
) -> None:
    """Give one trial a human title and/or a description.

    Both are STICKY once set: the producer keeps writing its own benchmark name
    on every retry and will not overwrite yours. That is the point of the verb --
    a rollout worth talking about gets a name a person can say, instead of the
    Harbor join key it was born with.

    NO `--notes` here, and there is no notes door for a trial anywhere: it is
    the one research entity with no notes document. A rollout ran once and is
    immutable afterwards, so what went wrong in it goes in `--description`, and
    anything about the harness belongs once on the RUN's notes.
    """
    if name is None and description is None:
        raise typer.BadParameter("pass at least one of --name/--description")
    with _client() as c:
        _print_json(c.update_trial(trial_id, name=name, description=_text_value(description)))


def _trial_result_summary(result: dict) -> dict:
    manifest = result.get("manifest") or {}
    return {
        "trial": result["trial"],
        "span_id": result["span_id"],
        "reward": result["reward"],
        "manifest_artifact_id": manifest.get("id") if isinstance(manifest, dict) else None,
        "files": len(result["files"]),
        "uploaded": sum(1 for item in result["files"] if item.get("uploaded")),
        "trajectory": result.get("trajectory"),
        "capture": result.get("capture"),
    }


@trial_app.command("stage")
def trial_stage(
    trial_dir: str = typer.Argument(..., help="live Harbor trial output directory"),
    destination: str = typer.Option(
        ..., "--to", help="durable destination outside the sandbox (for example a shared PVC)"
    ),
    expect: list[str] = typer.Option(
        None, "--expect", metavar="RELATIVE_PATH", help="repeatable required producer output"
    ),
) -> None:
    """Copy + checksum Harbor's host trial output; performs no network writes."""
    from ....connectors.harbor import stage_trial

    staged = stage_trial(trial_dir, destination, expected_paths=expect or ())
    _print_json(
        {
            "trial_dir": str(staged.trial_dir),
            "ledger": str(staged.ledger.path),
            "durable_collection_complete": staged.durable_collection_complete,
            "completeness": staged.ledger.report(),
        }
    )
    if not staged.durable_collection_complete:
        raise typer.Exit(2)


@trial_app.command("add")
def trial_add(
    run: str = typer.Argument(...),
    trial_dir: str = typer.Argument(..., help="a Harbor trial output directory"),
    step: int = typer.Option(
        None, "--step", help="training step / Miles rollout_id — the join key"
    ),
    env_type: str = typer.Option(
        None, "--env-type", help="opaque environment label (e.g. skypilot-fork)"
    ),
    expand: bool = typer.Option(
        True, "--expand/--no-expand", help="expand a recognized trajectory format into spans"
    ),
    max_spans: int = typer.Option(
        None, "--max-spans", help="eager expansion window (0 = unlimited)"
    ),
) -> None:
    """Capture one Harbor trial: rollout span + reward metric + labeled file
    uploads + a kind=harbor_trial manifest, all keyed by --step."""
    from ....connectors.harbor import capture_trial

    with _client() as c:
        result = capture_trial(
            _run_handle(c, run),
            trial_dir,
            step_index=step,
            environment={"type": env_type} if env_type else None,
            source_mode="cli",
            expand=expand,
            max_trajectory_spans=max_spans,
        )
    _print_json(_trial_result_summary(result))


@trial_app.command("reconcile")
def trial_reconcile(
    run: str = typer.Argument(...),
    trial_dir: str = typer.Argument(..., help="a directory created by `probe trial stage`"),
    step: int = typer.Option(None, "--step", help="override the step recorded in the ledger"),
    env_type: str = typer.Option(None, "--env-type", help="opaque environment label"),
) -> None:
    """Retry unconfirmed staged bytes and publish the latest completeness manifest."""
    from ....connectors.harbor import reconcile_staged_trial

    kwargs: dict[str, Any] = {
        "environment": {"type": env_type} if env_type else None,
        "source_mode": "cli-reconcile",
    }
    if step is not None:
        kwargs["step_index"] = step
    with _client() as client:
        result = reconcile_staged_trial(_run_handle(client, run), trial_dir, **kwargs)
    _print_json(_trial_result_summary(result))


@trial_app.command("export")
def trial_export(
    request: str = typer.Argument(..., help="a probe-harbor-export/1 export-request.json"),
    run: Optional[str] = typer.Option(None, "--run", help="later-resolved Probe run ID"),
) -> None:
    """Consume one durable Miles/Harbor export request; retry safe."""
    from ....connectors.harbor_export import consume_export_request

    try:
        with _client() as client:
            result = consume_export_request(client, request, run_id=run)
    except Exception as exc:
        typer.echo(f"export failed (staged bytes retained): {type(exc).__name__}: {exc}", err=True)
        raise typer.Exit(1) from exc
    _print_json(result)


@trial_app.command("drain")
def trial_drain(
    capture_root: str = typer.Argument(..., help="root containing export-request.json files"),
    run: Optional[str] = typer.Option(None, "--run", help="later-resolved Probe run ID"),
) -> None:
    """Retry every non-completed Miles/Harbor export request below a capture root."""
    from ....connectors.harbor_export import drain_export_requests

    with _client() as client:
        result = drain_export_requests(client, capture_root, run_id=run)
    _print_json(result)
    if result["failed"]:
        raise typer.Exit(2)


@trial_app.command("watch")
def trial_watch(
    capture_root: str = typer.Argument(..., help="root containing export-request.json files"),
    interval: float = typer.Option(5.0, "--interval", min=0.1, help="poll interval in seconds"),
    once: bool = typer.Option(False, "--once", help="drain once and exit (deployment smoke check)"),
    run: Optional[str] = typer.Option(None, "--run", help="later-resolved Probe run ID"),
) -> None:
    """Continuously export newly staged Harbor trials from a durable capture root."""
    from ....connectors.harbor_export import drain_export_requests
    from .watch_loop import watch

    with _client() as client:
        watch(
            lambda: drain_export_requests(client, capture_root, run_id=run),
            interval=interval,
            once=once,
            report=_print_json,
        )


@trial_app.command("expand")
def trial_expand(
    run: str = typer.Argument(...),
    manifest_id: str = typer.Argument(..., help="a kind=harbor_trial manifest artifact id"),
    max_spans: int = typer.Option(
        0, "--max-spans", help="eager expansion window (default 0 = full)"
    ),
) -> None:
    """Retroactively expand a captured trial's stored trajectory into spans —
    e.g. after a parser for its format shipped. Idempotent (deterministic span
    ids), so re-running only upserts."""
    from ....connectors.atif import expand_trajectory

    with _client() as c:
        manifests = {a["id"]: a for a in c.list_run_artifacts(run, kind="harbor_trial")}
        manifest = manifests.get(manifest_id)
        if manifest is None:
            typer.echo(f"no kind=harbor_trial artifact {manifest_id} on run {run}", err=True)
            raise typer.Exit(1)
        meta = manifest.get("meta") or {}
        traj_entry = next(
            (
                f
                for f in meta.get("files") or []
                if f.get("role") == "trajectory" and f.get("artifact_id")
            ),
            None,
        )
        if traj_entry is None:
            typer.echo("manifest has no uploaded trajectory file", err=True)
            raise typer.Exit(1)
        doc = json.loads(c.transport.get_url(c.presign_download(traj_entry["artifact_id"])))
        report = expand_trajectory(
            _run_handle(c, run),
            doc,
            root_span_id=str(manifest["span_id"]),
            trial=(meta.get("trial") or {}).get("name") or manifest.get("name"),
            step_index=manifest.get("step_index"),
            max_spans=max_spans,
        )
    _print_json(report)
from probe.cli.commands.flag_values import _text_value  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
