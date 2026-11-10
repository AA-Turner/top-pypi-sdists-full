"""dreamscale train — fine-tune a base model on a LeRobot dataset (see dreamscale.trainings).

`dreamscale train --dataset towels --base pi0.5` reads the dataset, shows the exact quote and asks
once: "Start training?". Then it starts the run and follows it on one live line (Ctrl-C stops
following; training continues). The server checks every dataset before the GPUs start. A folder is
uploaded first (`dreamscale datasets upload`, datasets_cmd.py). `list`, `show`, `cancel`, `rm` and
`deploy` take it from there. Mirrors checkpoints_cmd.py.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dreamscale_transport.training_data import CHECK_SCOPE
from dreamscale_transport.training_recipes import charged_usd
from rich.text import Text

from dreamscale import errors, tables
from dreamscale.checkpoints_cmd import (
    AUTO_REGION,
    _check_region,
    follow_build,
    parse_region,
    region_of,
    robot_line,
)
from dreamscale.control import ControlPlaneClient
from dreamscale.trainings import (
    ACTIVE,
    COMMAND,
    EVAL_CAVEAT,
    _offered_bases_text,
    active_run,
    base_name,
    call,
    check_estimate,
    check_line,
    close_printer,
    dataset_body,
    dataset_line,
    default_name,
    duration,
    estimate_body,
    fingerprint,
    folder_lines,
    follow,
    forget_start,
    held_out_metric,
    live_printer,
    mapping_lines,
    outcome_lines,
    parse_datasets,
    problem_error,
    quote_lines,
    resolve_source,
    run_line,
    run_page,
    run_settings,
    size_text,
    start_run,
    status_text,
    usd,
)

# More than this share removed usually means a calibration or logging fault, not bad demos.
REMOVED_WARNING_SHARE = 0.3
_BAR = 20


def ask(prompt: str, default: bool = True) -> bool:
    import click

    try:
        return click.confirm(prompt, default=default, err=True)
    except click.Abort:
        return False


def _stderr(line: str) -> None:
    print(line, file=sys.stderr)


def _confirm_required(what: str) -> errors.DreamscaleError:
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code="confirm_required",
            problem=f"{what} needs a yes, and there is no terminal to ask in",
            cause="stdin isn't a terminal (a script, a pipe or an agent)",
            fix="rerun with --yes to accept what's shown above",
        )
    )


def _bar(label: str, done: int, total: int, started: float, now: float) -> str:
    filled = round(_BAR * done / total) if total else _BAR
    unit, scale = ("GB", 1e9) if total >= 1e8 else ("MB", 1e6)
    return (
        f"{label} {'━' * filled}{'─' * (_BAR - filled)} {done / scale:.1f} of "
        f"{total / scale:.1f} {unit} · {duration(now - started)}"
    )


def _progress(printer: Callable[[str], None], live: bool, label: str,
              clock: Callable[[], float] = time.monotonic) -> Callable[[int, int], None]:
    """A byte progress bar: redrawn on a terminal, a line per quarter in logs."""
    started, last = clock(), [-1]

    def update(done: int, total: int) -> None:
        if not total:
            return
        quarter = done * 4 // total if total else 4
        if live or quarter != last[0]:
            printer(_bar(label, done, total, started, clock()))
            last[0] = quarter

    return update


def upload_folder(client_factory, local, *, print_fn, kind: str = "dataset",
                  base_model: str | None = None) -> str:
    """Hash then upload ``local``'s files (``root``, ``files`` as (path, size), ``bytes``, and
    optional ``slices``: uploads.Slice by path) with a progress bar; Ctrl-C pauses. Returns
    the complete upload's id."""
    from dreamscale import uploads
    from dreamscale.trainings import _upload as send

    slices = getattr(local, "slices", None) or {}
    printer, live = live_printer(print_fn)
    started = time.monotonic()
    try:
        files = uploads.manifest(
            local.root, local.files, progress=_progress(printer, live, "Reading files"),
            **({"slices": slices} if slices else {}),
        )
        done = asyncio.run(send(
            client_factory, local.root, files, progress=_progress(printer, live, "Uploading"),
            kind=kind,
            **({"base_model": base_model} if base_model is not None else {}),
            **({"slices": slices} if slices else {}),
        ))
    except KeyboardInterrupt:
        close_printer(printer, print_fn)
        print_fn("Upload paused. Run the same command to resume; sent parts aren't resent.")
        raise
    finally:
        close_printer(printer, print_fn)
    took = int(time.monotonic() - started)
    if done.get("sent"):
        print_fn(f"✓ Uploaded {size_text(done['sent'])} in {duration(took)}")
    else:
        print_fn(f"✓ Already uploaded ({size_text(local.bytes)})")
    return done["id"]


def follow_run(
    run: dict,
    *,
    client_factory: Callable[..., Any],
    print_fn: Callable[[str], None],
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Follow until the run finishes; Ctrl-C detaches with the commands to come back."""
    print_fn(
        "Ctrl-C stops following; training continues. "
        f"Stop it: {COMMAND} stop {run['id']}"
    )
    try:
        run = follow(run, client_factory=client_factory, print_fn=print_fn, sleep=sleep)
    except KeyboardInterrupt:
        print_fn(f"Stopped following {run['id']}; training continues. "
                 f"Follow again: {COMMAND} show {run['id']}")
        return run
    for line in outcome_lines(run):
        print_fn(line)
    return run


def run_create(
    *,
    dataset: str | list[str],
    base: str | None = None,
    steps: int | None = None,
    max_usd: Any = None,
    rtc: bool | None = None,
    name: str | None = None,
    hf_token: str | None = None,
    learning_rate: float | None = None,
    prompt: str | None = None,
    hardware_check: bool = True,
    trim_idle: bool = True,
    mapping: dict | None = None,
    inputs: dict | None = None,
    eval_fraction: float | None = None,
    base_step: int | None = None,
    normalization: str | None = None,
    batch_size: int | None = None,
    warmup_steps: int | None = None,
    lr_schedule: str | None = None,
    checkpoint_every: int | None = None,
    yes: bool = False,
    wait: bool = True,
    json_output: bool = False,
    quote_only: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    confirm_fn: Callable[[str], bool] = ask,
    interactive: bool | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Read, quote, one confirm, start, follow. ``quote_only`` stops at the quote (``--yes`` or
    not) and returns the estimate: nothing is started."""
    out = _stderr if json_output and print_fn is print else print_fn
    interactive = sys.stdin.isatty() if interactive is None else interactive
    if not base:
        raise errors.catalog("base_required", bases=_offered_bases_text(client_factory))
    source = resolve_source(
        parse_datasets(dataset if isinstance(dataset, list) else [dataset]), client_factory
    )
    body = run_settings(
        base=base, steps=steps, max_usd=max_usd, rtc=rtc, name=name or default_name(source),
        learning_rate=learning_rate, prompt=prompt, hardware_check=hardware_check,
        trim_idle=trim_idle, mapping=mapping, eval_fraction=eval_fraction,
        base_step=base_step, normalization=normalization, batch_size=batch_size,
        warmup_steps=warmup_steps, lr_schedule=lr_schedule, checkpoint_every=checkpoint_every,
        inputs=inputs,
    )
    fp = fingerprint(source, body)

    def finish(run: dict) -> dict:
        if wait and run.get("status") in ACTIVE:
            run = follow_run(run, client_factory=client_factory, print_fn=out, sleep=sleep)
        if json_output:
            print_fn(json.dumps(run, indent=2, sort_keys=True))
        return run

    existing = None if quote_only else active_run(client_factory, fp)
    if existing is not None:
        out(f"{existing['id']} is already training this dataset with these settings.")
        return finish(existing)
    token = hf_token or os.environ.get("HF_TOKEN") or None
    extra = {"hf_token": token} if token else {}
    request = {**body, **extra, "dataset": dataset_body(source)}

    def quote() -> dict:
        estimate = call(client_factory, "estimate_training", estimate_body(request))
        # A quote alone is still shown when something would stop the run (the balance, say).
        if not (quote_only and estimate.get("quote")):
            check_estimate(estimate, f"the estimate for {source.label}")
        return estimate

    estimate = quote()
    summary = estimate.get("summary") or {}
    preset = (estimate.get("contract") or {}).get("preset")
    out(f"Reading {source.label} (LeRobot {summary.get('version', '?')})")
    out(f"  ✓ {dataset_line(summary, None if preset == 'custom' else preset)}")
    for line in [*folder_lines(summary, several=source.kind == "several"),
                 *mapping_lines(summary, picked=bool(mapping))]:
        out(f"    {line}")
    for note in summary.get("notes") or []:
        out(f"! {note}")
    if hardware_check:
        out("  Auto-clean: runs on our side before training starts (free)")
        out(f"    {CHECK_SCOPE}")
    else:
        out("  Auto-clean: off (every episode trains as recorded)")
    demo_hours = summary.get("demo_hours")
    question = "Start training?"
    if quote_only:
        for line in quote_lines(estimate, demo_hours, rtc=request.get("rtc")):
            out(line)
        if not estimate.get("can_start", True):
            for problem in estimate.get("problems") or []:
                error = problem_error(problem, f"the estimate for {source.label}")
                out(f"! Can't start yet: {error.info.problem.rstrip('.')}. {error.fix}")
        out("Quote only: nothing started.")
        if json_output:
            print_fn(json.dumps(estimate, indent=2, sort_keys=True))
        return estimate

    def accept(estimate: dict) -> None:
        for line in quote_lines(estimate, demo_hours, rtc=request.get("rtc")):
            out(line)
        if yes:
            return
        if not interactive:
            raise _confirm_required("Starting a training run")
        if not confirm_fn(question):
            raise KeyboardInterrupt

    try:
        accept(estimate)
    except KeyboardInterrupt:
        out("Nothing started.")
        return {}
    for attempt in range(2):
        try:
            run = start_run(
                client_factory, {**request, "accept_usd": estimate["quote"]["usd"]}, fp,
                sleep=sleep,
            )
            break
        except errors.DreamscaleError as error:
            if error.code != "quote_changed" or attempt:
                raise
            forget_start(fp)
            out("The price changed since the quote:")
            estimate = quote()
            try:
                accept(estimate)
            except KeyboardInterrupt:
                out("Nothing started.")
                return {}
    quoted = run.get("quote") or estimate["quote"]
    out(
        f"Started {run['id']} · {base_name(quoted.get('base'))} · "
        f"{int(quoted.get('steps') or 0):,} steps · ~{usd(quoted.get('usd'))}, charged as it "
        "trains"
    )
    link = run_page(run["id"])
    if link:
        out(f"  {link}")
    if not wait:
        out(f"Follow it: {COMMAND} show {run['id']}")
    return finish(run)


def describe(run: dict) -> list[str]:
    dataset = run.get("dataset") or {}
    source = dataset.get("source") or {}
    summary = dataset.get("summary") or {}
    preset = (run.get("contract") or {}).get("preset")
    quote = run.get("quote") or {}
    cost = run.get("cost") or {}
    def hub(part: dict) -> str:
        return (f"hf://{part.get('repo')}{'/' + part['path'] if part.get('path') else ''}"
                f"@{part.get('revision') or 'main'}")

    where = (
        hub(source) if source.get("kind") == "huggingface"
        else " + ".join(hub(part) for part in source.get("datasets") or [])
        if source.get("kind") == "several"
        else f"{source.get('name')} v{source.get('version')}"
        + (" (deleted)" if source.get("deleted") else "")
        if source.get("kind") == "dataset"
        else f"uploaded ({source.get('upload_id')})"
    )
    settings = run.get("settings") or {}
    lines = [
        f"{run['id']}  {run.get('name')}  ({base_name(run.get('base') or quote.get('base'))})",
        f"  status:   {status_text(run)}",
        f"  dataset:  {where} · {dataset_line(summary, None if preset == 'custom' else preset)}",
    ]
    parent = settings.get("parent") or {}
    if parent:
        if parent.get("artifact_id"):  # an imported deployment: no run, no step
            source = f" (imported from {parent['source']})" if parent.get("source") else ""
            lines.append(f"  from:     deployment {parent.get('deployment')}{source}")
        else:
            lines.append(
                (f"  from:     deployment {parent['deployment']} · " if parent.get("deployment")
                 else "  from:     ")
                + f"{parent.get('name')} · step {int(parent.get('step') or 0):,} "
                f"({parent.get('run_id')})"
            )
    if dataset.get("check"):
        lines.append(f"  check:    {check_line(dataset['check'])}")
        note = (dataset["check"].get("normalization") or {}).get("note")
        if note:
            lines.append(f"            {note}")
    lines += [
        f"  length:   {int(quote.get('steps') or 0):,} steps · {quote.get('samples', 0):,} "
        f"samples · RTC {'on' if settings.get('rtc', True) else 'off'}",
        f"  cost:     {usd(cost.get('held_usd', 0))} taken · {usd(cost.get('charged_usd', 0))} "
        f"charged" + (f" · {usd(cost['refunded_usd'])} refunded"
                      if float(cost.get("refunded_usd") or 0) else ""),
    ]
    held = settings.get("eval_fraction")  # opt-in: only a run that held episodes out
    label, field, point = held_out_metric(run)
    if held:
        evals = [e for e in run.get("eval_metrics") or [] if isinstance(e.get(point), int | float)]
        latest = f" · {label} {evals[-1][point]:.3g}" if evals else ""
        lines.append(f"  eval:     {float(held):.0%} of episodes held out{latest}")
    shown = "held-out" if field == "eval_loss" else label
    for checkpoint in run.get("checkpoints") or []:
        loss = checkpoint.get("loss")
        held_out = checkpoint.get(field)  # shown, never used to mark a checkpoint best
        lines.append(
            f"  checkpoint: step {int(checkpoint.get('step') or 0):,}"
            + (f" · loss {loss:.3g}" if isinstance(loss, int | float) else "")
            + (f" · {shown} {held_out:.3g}" if isinstance(held_out, int | float) else "")
            + (" · RTC trained" if checkpoint.get("rtc_trained") else "")
            + (f" · deployed {checkpoint['deployment_id']}"
               if checkpoint.get("deployment_id") else "")
        )
    if held:
        lines.append(f"  {EVAL_CAVEAT}")
    return lines


def run_show(
    *,
    run_id: str,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    run = call(client_factory, "get_training", run_id)
    if json_output:
        print_fn(json.dumps(run, indent=2, sort_keys=True))
        return run
    for line in describe(run):
        print_fn(line)
    if run.get("status") in ACTIVE:
        return follow_run(run, client_factory=client_factory, print_fn=print_fn, sleep=sleep)
    for line in outcome_lines(run):
        print_fn(line)
    return run


def run_list(
    *,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    listed = call(client_factory, "list_trainings")
    if json_output:
        print_fn(json.dumps(listed, indent=2, sort_keys=True))
        return listed
    runs = listed.get("trainings") or []
    if not runs:
        print_fn("Training runs")
        print_fn("  None yet. Upload a dataset: dreamscale datasets upload ./my_dataset")
        print_fn(f"  Then train on it: {COMMAND} --dataset my_dataset --base BASE")
        return listed
    for line in list_lines(runs, now=_now()):
        print_fn(line)
    return listed


# A run's status as `train list` shows it: (label, tables kind).
_LIST_STATUSES = {
    "queued": ("Queued", "active"), "preparing": ("Preparing", "active"),
    "training": ("Training", "active"), "ready": ("Ready", "ok"),
    "stopped": ("Stopped", "idle"), "canceled": ("Canceled", "idle"), "failed": ("Failed", "bad"),
}


def _list_status(run: dict) -> Text:
    """`● Training · ~2 h 10 m left`, `○ Stopped · resume by Nov 23`, `● Ready`."""
    status = str(run.get("status") or "")
    label, kind = _LIST_STATUSES.get(status, (status.capitalize(), "idle"))
    progress, detail = run.get("progress") or {}, ""
    if status in ACTIVE:
        # The phase names what an active run is doing (`Checking data`, `Saving`).
        label = status_text(run).split(" · ")[0]
        if label.startswith("Training") and progress.get("eta_seconds") is not None:
            detail = f"~{duration(progress['eta_seconds'])} left"
    elif status == "stopped":
        resume = run.get("resume") or {}
        until = resume.get("resumable_until")
        if resume.get("can_resume") and isinstance(until, str):
            when = datetime.fromisoformat(until.replace("Z", "+00:00"))
            detail = f"resume by {when:%b} {when.day}"
            if resume.get("reason") == "credits":
                detail = f"out of credits · {detail}"
    return tables.status(label, kind, detail)


def _list_steps(run: dict) -> Text:
    """`33,517`, or `961 / 3,000` for a run that hasn't reached its last step."""
    progress, resume = run.get("progress") or {}, run.get("resume") or {}
    step = progress.get("step") if progress.get("step") is not None else resume.get("steps_done")
    total = progress.get("total_steps") or (run.get("quote") or {}).get("steps")
    if step is None:
        return tables.none()
    if not total or int(step) >= int(total):
        return Text(f"{int(step):,}")
    return Text.assemble(f"{int(step):,}", (f" / {int(total):,}", tables.DIM))


def _list_checkpoints(run: dict) -> Text:
    """`5`, or `5 · 1 deployed`."""
    checkpoints = [c for c in run.get("checkpoints") or [] if isinstance(c, dict)]
    if not checkpoints:
        return tables.none()
    deployed = sum(1 for c in checkpoints if c.get("deployment_id"))
    cell = Text(str(len(checkpoints)))
    if deployed:
        cell.append(f" · {deployed} deployed", style="green")
    return cell


def _ago(value: Any, now: datetime) -> str:
    if not isinstance(value, str):
        return ""
    seconds = (now - datetime.fromisoformat(value.replace("Z", "+00:00"))).total_seconds()
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if seconds >= size:
            return f"{int(seconds // size)}{unit} ago"
    return "just now"


def _now() -> datetime:
    return datetime.now(UTC)


def list_lines(runs: list[dict], *, now: datetime, color: bool | None = None,
               width: int | None = None) -> list[str]:
    columns = [
        tables.Column("RUN", style="bold", shrink=True),
        tables.Column("BASE", drop=1),
        tables.Column("STATUS"),
        tables.Column("STEPS", drop=2, justify="right"),
        tables.Column("CHECKPOINTS", drop=3),
        tables.Column("COST", drop=4, justify="right"),
        tables.Column("STARTED", drop=5, justify="right", style=tables.DIM),
        # Names repeat; the id is what `show` and `deploy` take.
        tables.Column("ID", style=tables.DIM),
    ]
    rows = [[
        run.get("name"), base_name(run.get("base")).removesuffix(" base"), _list_status(run),
        _list_steps(run), _list_checkpoints(run),
        usd((run.get("cost") or {}).get("charged_usd", 0)),
        _ago(run.get("created_at"), now), run.get("id"),
    ] for run in runs]
    footer = [tables.hint(
        "Details: ", tables.command(f"{COMMAND} show <id>"),
        "   ·   deploy a checkpoint: ", tables.command(f"{COMMAND} deploy <id> --step N"),
    )]
    return tables.render("Training runs", f"{len(runs)}, newest first", columns, rows,
                         footer=footer, color=color, width=width)


def run_cancel(
    *,
    run_id: str,
    yes: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    confirm_fn: Callable[..., bool] = ask,
    interactive: bool | None = None,
) -> dict:
    """Stop a run (``cancel`` is its older name). One still training saves at its current
    step; when the run can resume, that is said and how."""
    interactive = sys.stdin.isatty() if interactive is None else interactive
    run = call(client_factory, "get_training", run_id)
    if run.get("status") not in ACTIVE:
        print_fn(f"{run_id} is already {run.get('status')}; nothing to stop.")
        return run
    held = (run.get("cost") or {}).get("held_usd", 0)
    resumable = bool(run.get("resumable"))
    if run.get("status") == "training":
        step = int((run.get("progress") or {}).get("step") or 0)
        pay = charged_usd(run, step)
        question = (
            f"Stop {run_id}? "
            + ("It saves at its current step and releases the GPUs. " if resumable else "")
            + f"You pay {usd(pay)} for the {step:,} completed steps (and the steps until it "
            "stops); credits it didn't use come back."
            + (" Resume within 30 days." if resumable else "")
        )
    else:
        question = f"Stop {run_id}? It hasn't started training: you pay nothing."
    print_fn(question.split("? ", 1)[1])
    if not yes:
        if not interactive:
            raise _confirm_required("Stopping a training run")
        if not confirm_fn(f"Stop {run_id}?", default=False):
            print_fn("Not stopped.")
            return run
    # /cancel is /stop's older name: every control plane answers it.
    run = call(client_factory, "cancel_training", run_id)
    cost = run.get("cost") or {}
    if run.get("status") in ("canceled", "stopped"):
        print_fn(
            f"{run.get('status').capitalize()} {run_id} · charged "
            f"{usd(cost.get('charged_usd', 0))} · refunded {usd(cost.get('refunded_usd', held))}"
        )
    else:
        print_fn(
            f"Stopping {run_id} after its current step; saved checkpoints stay deployable."
            + (f" Resume it later: {COMMAND} resume {run_id}." if resumable else "")
            + f" See it: {COMMAND} show {run_id}"
        )
    return run


def run_resume(
    *,
    run_id: str,
    yes: bool = False,
    wait: bool = True,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    confirm_fn: Callable[..., bool] = ask,
    interactive: bool | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Resume a stopped run for its remaining steps at its own rate (one confirm)."""
    import uuid

    out = _stderr if json_output and print_fn is print else print_fn
    interactive = sys.stdin.isatty() if interactive is None else interactive
    run = call(client_factory, "get_training", run_id)
    resume = run.get("resume") or {}
    if run.get("status") != "stopped" or not resume.get("can_resume"):
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="training_not_resumable",
                problem=f"{run_id} can't resume",
                cause=status_text(run) if run.get("status") == "stopped"
                else f"it is {run.get('status')}, not stopped",
                fix=f"start a new run from its latest checkpoint: {COMMAND} --dataset <dataset> "
                f"--base {run_id}",
            )
        )
    left = int(resume.get("steps_left") or 0)
    eta = resume.get("eta_seconds")
    out(
        f"Resume {run_id} from step {int(resume.get('steps_done') or 0):,}: {left:,} steps · "
        + (f"~{duration(eta)} · " if eta else "") + f"~{usd(resume.get('usd', 0))}, charged as "
        "it trains"
    )
    if not yes:
        if not interactive:
            raise _confirm_required("Resuming a training run")
        if not confirm_fn(f"Resume {run_id}?", default=True):
            out("Not resumed.")
            return run
    run = call(client_factory, "resume_training", run_id, accept_usd=str(resume.get("usd")),
               idempotency_key=f"cli-resume-{uuid.uuid4()}")
    if json_output:
        print(json.dumps(run, indent=2, sort_keys=True))
    if wait and run.get("status") in ACTIVE:
        run = follow_run(run, client_factory=client_factory, print_fn=out, sleep=sleep)
    elif not wait:
        out(f"Resuming {run_id}. Follow it: {COMMAND} show {run_id}")
    return run


def run_rm(
    *,
    run_id: str,
    yes: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    confirm_fn: Callable[..., bool] = ask,
    interactive: bool | None = None,
) -> dict:
    """Delete a run for good, after one question; one still going is canceled first."""
    interactive = sys.stdin.isatty() if interactive is None else interactive
    run = call(client_factory, "get_training", run_id)
    if run.get("status") == "training":
        step = int((run.get("progress") or {}).get("step") or 0)
        pay = charged_usd(run, step)
        consequence = (
            f"It stops now: you pay {usd(pay)} for the {step:,} steps it completed; credits "
            "it didn't use come back."
        )
    elif run.get("status") in ACTIVE:
        consequence = "It's canceled first; it hasn't started training, so you pay nothing."
    else:
        consequence = "This can't be undone."
    if run.get("checkpoints"):
        consequence += " Its checkpoints go with it"
        deployed = any(c.get("deployment_id") for c in run["checkpoints"])
        consequence += "; deployments made from them keep running." if deployed else "."
    print_fn(consequence)
    if not yes:
        if not interactive:
            raise _confirm_required("Deleting a training run")
        if not confirm_fn(f"Delete {run_id} permanently?", default=False):
            print_fn("Not deleted.")
            return run
    result = call(client_factory, "delete_training", run_id)
    print_fn(f"Deleted training run {run_id} permanently.")
    return result


def run_deploy(
    *,
    run_id: str,
    step: int | None = None,
    region: str | None = None,
    region_fallback: bool | None = None,
    wait: bool = True,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Deploy a checkpoint (default the latest) and follow its GPU check like
    `deployments create`. ``region_fallback``: whether its server may start in the
    next-closest region when its own is full (None: the server's default, on)."""
    region = parse_region(region)
    if region == AUTO_REGION:
        # The nearest region the run's base serves (None: the server's default).
        base = call(client_factory, "get_training", run_id).get("base")
        region = (_check_region(client_factory, base, base, region, print_fn=print_fn)
                  if isinstance(base, str) else None)
    result = call(
        client_factory, "deploy_training", run_id, step=step, region=region,
        **({"region_fallback": region_fallback} if region_fallback is not None else {}),
    )
    deployment = result.get("deployment") or result
    which = f"{run_id} step {step:,}" if step else f"{run_id}'s latest checkpoint"
    print_fn(
        f"Building {deployment['id']} (deployment) from {which} for "
        f"{robot_line(deployment)} in {region_of(deployment)} (one-time build and GPU check)."
    )
    deployment = follow_build(
        deployment, wait=wait, client_factory=client_factory, print_fn=print_fn, sleep=sleep
    )
    if deployment.get("status") == "failed":
        return deployment
    for line in _state_lines(client_factory, run_id):
        print_fn(line)
    prefix = "Run it" if deployment.get("status") == "ready" else "Once it's ready, run it"
    print_fn(f"{prefix}: {run_line(deployment)}")
    return deployment


def _state_lines(client_factory: Callable[..., Any], run_id: str) -> list[str]:
    """What the robot must send, when the run trained on some of its state's values."""
    try:
        run = call(client_factory, "get_training", run_id)
    except errors.DreamscaleError:
        return []
    names = (run.get("contract") or {}).get("state_names") or []
    state = (((run.get("dataset") or {}).get("summary") or {}).get("mapping") or {}).get("state")
    if not names or not any("[" in str(entry) for entry in state or []):
        return []
    return [f"The robot sends its state as these {len(names)} values, in order: {', '.join(names)}"]


DOWNLOAD_POLL_S = 10
DOWNLOAD_WAIT_S = 3600


def run_download(
    *,
    run_id: str,
    step: int | None = None,
    output: str | None = None,
    link: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    fetch: Callable[..., None] | None = None,
) -> dict:
    """Download a checkpoint (default the latest) and its dreamscale.json in one tar.
    The first ask packs it (a few minutes); ``link`` prints the signed link
    (valid an hour) instead of downloading."""
    started = clock()
    said = False
    while True:
        answer = call(client_factory, "download_training", run_id, step=step)
        status = answer.get("status")
        if status == "ready":
            break
        if status == "failed":
            error = answer.get("error") or {}
            raise errors.DreamscaleError(
                errors.ErrorInfo(
                    code=error.get("code") or "download_failed",
                    problem=error.get("message") or "packing the checkpoint failed",
                    cause=f"{run_id} step {answer.get('step')}",
                    fix=error.get("fix")
                    or f"run the same command again: {COMMAND} download {run_id}",
                )
            )
        if not said:
            print_fn(f"Packing {run_id} step {answer.get('step'):,} for download (a few minutes)…")
            said = True
        if clock() - started > DOWNLOAD_WAIT_S:
            raise errors.DreamscaleError(
                errors.ErrorInfo(
                    code="download_timeout",
                    problem="the checkpoint is still being packed",
                    cause=f"{run_id} step {answer.get('step')}",
                    fix=f"run the same command again later: {COMMAND} download {run_id}",
                )
            )
        sleep(DOWNLOAD_POLL_S)
    if link:
        print_fn(answer["url"])
        return answer
    path = Path(output).expanduser() if output else Path(answer["filename"])
    if path.is_dir():
        path = path / answer["filename"]
    (fetch or _fetch_file)(answer["url"], path, int(answer.get("size_bytes") or 0), print_fn)
    print_fn(
        f"✓ Downloaded {path} ({size_text(path.stat().st_size)})"
    )
    return {**answer, "path": str(path)}


def _fetch_file(url: str, path: Path, size: int, print_fn: Callable[[str], None]) -> None:
    """Stream ``url`` to ``path`` with a progress bar (written beside it, then renamed). An
    interrupted download keeps its ``.part`` (and the object's ETag beside it), and the next one
    continues from it only if the object is still the same (``If-Range``)."""
    import httpx

    printer, live = live_printer(print_fn)
    update = _progress(printer, live, "Downloading")
    partial = path.with_name(path.name + ".part")
    etag_file = path.with_name(path.name + ".part.etag")
    etag = etag_file.read_text().strip() if etag_file.exists() else ""
    done = partial.stat().st_size if partial.exists() and etag else 0
    headers = {"Range": f"bytes={done}-", "If-Range": etag} if done else {}
    try:
        with httpx.stream(
            "GET", url, headers=headers, timeout=60.0, follow_redirects=True
        ) as response:
            if not (response.status_code == 416 and size and done == size):  # else: whole
                response.raise_for_status()
                if response.status_code != 206:
                    done = 0  # a different object, or the server sent it all again
                    if response.headers.get("etag"):
                        etag_file.write_text(response.headers["etag"])
                total = done + int(response.headers.get("content-length") or 0) or size
                with partial.open("ab" if done else "wb") as out:
                    for chunk in response.iter_bytes(8 << 20):
                        out.write(chunk)
                        done += len(chunk)
                        update(done, total)
        if size and done != size:
            partial.unlink(missing_ok=True)
            raise httpx.HTTPError(f"received {done:,} of {size:,} bytes")
        partial.replace(path)
        etag_file.unlink(missing_ok=True)
    except httpx.HTTPError as error:
        if isinstance(error, httpx.HTTPStatusError) and error.response.status_code == 416:
            partial.unlink(missing_ok=True)  # not a prefix of this file: start again
            done = 0
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="download_failed",
                problem="the download stopped",
                cause=f"{type(error).__name__}: {error}",
                fix=f"run the same command again; it continues from {size_text(done)}",
            )
        ) from None
    finally:
        close_printer(printer, print_fn)
