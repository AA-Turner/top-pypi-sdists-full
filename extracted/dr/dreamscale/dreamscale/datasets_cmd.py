"""dreamscale datasets — upload, import, list, show, download, rename and rm (see
dreamscale.datasets). Mirrors train_cmd.py."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import threading
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dreamscale_transport.training_data import CHECK_SCOPE, detect_preset

from dreamscale import errors, tables
from dreamscale.control import ControlPlaneClient
from dreamscale.datasets import (
    IMPORT_POLL_S,
    IMPORT_RUNNING,
    _download,
    ensure,
    import_error,
    parse_hf,
    send,
    split_ref,
    start_import,
)
from dreamscale.train_cmd import REMOVED_WARNING_SHARE, _ago, _confirm_required, _stderr, ask
from dreamscale.trainings import (
    _offered_bases_text,
    call,
    check_line,
    close_printer,
    dataset_line,
    dataset_name_for,
    duration,
    folder_lines,
    hours,
    live_printer,
    robot_label,
    size_text,
)

_BAR = 20


def _train_hint(name: str, client_factory: Callable[..., Any]) -> str:
    bases = _offered_bases_text(client_factory)
    return f"Train on it: dreamscale train --dataset {name} --base BASE" + (
        f"   ({bases})" if bases else ""
    )


def _upload_line(checked: int, sent: int, total: int, started: float, now: float) -> str:
    filled = round(_BAR * checked / total) if total else _BAR
    unit, scale = ("GB", 1e9) if total >= 1e8 else ("MB", 1e6)
    return (
        f"Uploading {'━' * filled}{'─' * (_BAR - filled)} {checked / scale:.1f} of "
        f"{total / scale:.1f} {unit} checked · {sent / scale:.1f} {unit} sent · "
        f"{duration(now - started)}"
    )


def _check_alongside(folder, print_lines: list[str]) -> threading.Thread | None:
    """The check beside the upload: informational, so it never holds the upload back."""
    from dreamscale.lerobot_dataset import hardware_check

    def run() -> None:
        try:
            report = hardware_check(folder.local).as_json()
        except errors.DreamscaleError as error:
            print_lines.append(f"! The check couldn't read the recordings: {error.info.problem}")
            return
        except Exception as error:  # noqa: BLE001 - informational
            print_lines.append(f"! The check couldn't read the recordings ({type(error).__name__})")
            return
        print_lines.append(f"  ✓ Auto-clean: {check_line(report)}")
        if report["removed_share"] > REMOVED_WARNING_SHARE:
            print_lines.append(
                f"! The check removed {report['removed_share']:.0%} of the episodes; that "
                "usually means a calibration or logging fault worth fixing first."
            )
        print_lines.append(f"    {CHECK_SCOPE}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread


def _differs(before: dict | None, after: dict | None) -> str | None:
    """A new version recording another robot, fps or features than the latest."""
    if not before or not after:
        return None
    changed = [
        label for key, label in (("robot_type", "robot"), ("fps", "fps"),
                                 ("state_dim", "state width"), ("action_dim", "action width"),
                                 ("cameras", "cameras"))
        if before.get(key) != after.get(key)
    ]
    return ", ".join(changed) if changed else None


def run_upload(
    *,
    folder: str,
    name: str | None = None,
    check: bool = True,
    concurrency: int | None = None,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    """Read the folder, upload what's new and record a version. It never asks: an upload adds a
    version and removes nothing. Ctrl-C pauses; the same command resumes, from any machine."""
    from dreamscale.lerobot_dataset import open_upload

    out = _stderr if json_output and print_fn is print else print_fn
    local = open_upload(folder)
    wanted = name or dataset_name_for(local.root.expanduser().resolve().name)
    if name is None and wanted != local.root.name:
        out(f"Named it {wanted}, from {folder}")
    if local.summary is not None:
        summary = local.summary.as_json()
        out(f"Reading {folder} (LeRobot {local.summary.version})")
        out(f"  ✓ {dataset_line(summary, detect_preset(local.summary))}")
        for line in folder_lines(summary):
            out(f"    {line}")
        for note in summary.get("notes") or []:
            out(f"! {note}")
    else:
        out(f"Reading {folder}")
        out("  Its columns need picking: name them when you train (--state, --action, --camera).")
    dataset = ensure(wanted, client_factory)
    before = dataset.get("summary")
    lines: list[str] = []
    checker = None
    if check and local.local is not None:
        if importlib.util.find_spec("pyarrow") is None:
            out("  Skipping the check here: uv tool install 'dreamscale[train]' adds it. "
                "Training checks again.")
        else:
            checker = _check_alongside(local, lines)
    printer, live = live_printer(out)
    started = time.monotonic()
    last = [-1]

    def progress(checked: int, sent: int, total: int) -> None:
        quarter = (checked * 4 // total) if total else 4
        if live or quarter != last[0]:
            printer(_upload_line(checked, sent, total, started, time.monotonic()))
            last[0] = quarter

    try:
        done = send(client_factory, dataset["id"], local.root, local.files, progress=progress,
                    concurrency=concurrency)
    except KeyboardInterrupt:
        close_printer(printer, out)
        out("Upload paused. Run the same command to resume, from this machine or another; "
            "parts already sent aren't sent again.")
        raise
    finally:
        close_printer(printer, out)
    if checker is not None:
        checker.join()
    for line in lines:
        out(line)
    result = done["dataset"]
    full, version = result["full_name"], done["version"]
    if done.get("unchanged"):
        out(f"✓ {full} v{version} is already up to date")
    else:
        changed = _differs(before, result.get("summary"))
        if changed:
            out(f"! This version differs from the last in: {changed}")
        new = size_text(int(done.get("sent") or 0))
        episodes = (result.get("summary") or {}).get("episodes")
        was = (before or {}).get("episodes")
        shown = f"{int(episodes):,} episodes" if episodes is not None else "no episode count"
        if was is not None and version > 1:
            shown += f" (v{version - 1}: {int(was):,})"
        out(f"✓ {full} v{version} · {shown} · {size_text(local.bytes)}, {new} of it new")
    out(_train_hint(result["name"], client_factory))
    if json_output:
        print_fn(json.dumps({**result, "version": version, "unchanged": done.get("unchanged")},
                            indent=2, sort_keys=True))
    return done


def _import_line(data: dict, started: float) -> str:
    done, total = int(data.get("bytes_done") or 0), int(data.get("bytes_total") or 0)
    filled = round(_BAR * done / total) if total else 0
    unit, scale = ("GB", 1e9) if total >= 1e8 else ("MB", 1e6)
    return (
        f"Importing {'━' * filled}{'─' * (_BAR - filled)} {done / scale:.1f} of "
        f"{total / scale:.1f} {unit} · {duration(time.monotonic() - started)}"
    )


def _follow_import(
    dataset: dict, running: dict, *, client_factory, print_fn, sleep,
) -> dict | None:
    """One live line until the copy finishes; Ctrl-C stops following and it carries on."""
    printer, live = live_printer(print_fn)
    started = time.monotonic()
    last = [-1]
    try:
        while running.get("status") in IMPORT_RUNNING:
            total = int(running.get("bytes_total") or 0)
            quarter = int(running.get("bytes_done") or 0) * 4 // total if total else 0
            if live or quarter != last[0]:
                printer(_import_line(running, started))
                last[0] = quarter
            sleep(IMPORT_POLL_S)
            running = call(client_factory, "get_dataset_import", dataset["id"], running["id"])
    except KeyboardInterrupt:
        close_printer(printer, print_fn)
        print_fn(f"Stopped following; the import continues. Follow it: dreamscale datasets show "
                 f"{dataset['name']}")
        return None
    finally:
        close_printer(printer, print_fn)
    return running


def run_import(
    *,
    source: str,
    name: str | None = None,
    hf_token: str | None = None,
    wait: bool = True,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    out = _stderr if json_output and print_fn is print else print_fn
    parsed = parse_hf(source)
    token = hf_token or os.environ.get("HF_TOKEN") or None
    wanted = name or dataset_name_for(str(parsed["repo"]).rsplit("/", 1)[-1])
    answer, dataset = start_import(wanted, parsed, token, client_factory)
    if answer.get("unchanged"):
        full = answer["dataset"]["full_name"]
        out(f"✓ {full} v{answer['version']} is already up to date")
        if json_output:
            print_fn(json.dumps(answer, indent=2, sort_keys=True))
        return answer
    origin = answer.get("source") or {}
    where = f"hf://{origin.get('repo')}" + (f"/{origin['path']}" if origin.get("path") else "")
    commit = str(origin.get("commit") or "")[:7]
    out(f"Reading {where}@{origin.get('revision')} ({commit}) · "
        f"{int(answer.get('files_total') or 0):,} files · "
        f"{size_text(int(answer.get('bytes_total') or 0))}")
    if not wait:
        out(f"Importing on our side. Follow it: dreamscale datasets show {dataset['name']}")
        if json_output:
            print_fn(json.dumps(answer, indent=2, sort_keys=True))
        return answer
    final = _follow_import(dataset, answer, client_factory=client_factory, print_fn=out,
                           sleep=sleep)
    if final is None:
        return answer
    if final["status"] != "ready":
        raise import_error(final)
    shown = call(client_factory, "get_dataset", dataset["id"])
    summary = shown.get("summary") or {}
    if summary.get("episodes") is not None:
        out(f"  ✓ {_dataset_text(summary)}")
    out(f"✓ {shown['full_name']} v{final['version']} · from {where}@{commit}")
    out(_train_hint(shown["name"], client_factory))
    if json_output:
        print_fn(json.dumps(shown, indent=2, sort_keys=True))
    return shown


def _dataset_text(summary: dict) -> str:
    return dataset_line(summary, summary.get("preset"))


def run_list(
    *,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> list[dict]:
    listed = call(client_factory, "list_datasets")
    if json_output:
        print_fn(json.dumps({"datasets": listed}, indent=2, sort_keys=True))
        return listed
    if not listed:
        print_fn("Datasets")
        print_fn("  None yet. Upload one: dreamscale datasets upload ./my_dataset")
        print_fn("  Or copy one in: dreamscale datasets import hf://owner/name")
        return listed
    for line in list_lines(listed, now=datetime.now(UTC)):
        print_fn(line)
    return listed


def list_lines(rows: list[dict], *, now: datetime, color: bool | None = None,
               width: int | None = None) -> list[str]:
    columns = [
        tables.Column("DATASET", style="bold", shrink=True),
        tables.Column("VERSION", justify="right"),
        tables.Column("ROBOT", drop=1),
        tables.Column("EPISODES", drop=2, justify="right"),
        tables.Column("HOURS", drop=3, justify="right"),
        tables.Column("SIZE", justify="right"),
        tables.Column("LAST USED", drop=4, justify="right", style=tables.DIM),
    ]
    cells = []
    for row in rows:
        summary = row.get("summary") or {}
        running = row.get("import")
        version = (
            f"v{row['latest_version']}" if row.get("latest_version") is not None
            else "importing" if running else tables.none()
        )
        cells.append([
            row.get("name"), version,
            robot_label(summary, summary.get("preset")) if summary else tables.none(),
            f"{int(summary['episodes']):,}" if summary.get("episodes") is not None
            else tables.none(),
            hours(summary.get("demo_hours")) if summary.get("demo_hours") else tables.none(),
            size_text(int(row.get("bytes") or 0)) if row.get("bytes") else tables.none(),
            _ago(row.get("last_used_at"), now) or tables.none(),
        ])
    footer = [tables.hint(
        "Details: ", tables.command("dreamscale datasets show <name>"),
        "   ·   train: ", tables.command("dreamscale train --dataset <name> --base BASE"),
    )]
    return tables.render("Datasets", f"{len(rows)}", columns, cells, footer=footer, color=color,
                         width=width)


def _source_text(source: dict) -> str:
    if source.get("kind") == "huggingface":
        where = f"hf://{source.get('repo')}" + (f"/{source['path']}" if source.get("path") else "")
        return f"from {where}@{str(source.get('commit') or '')[:7]}"
    return "uploaded"


def describe(dataset: dict, pinned: int | None = None) -> list[str]:
    versions = dataset.get("versions") or []
    shown = next((v for v in versions if v["version"] == pinned), None) if pinned else None
    summary = (shown or {}).get("summary") or dataset.get("summary") or {}
    lines = [dataset["full_name"]]
    if summary.get("episodes") is not None:
        lines.append(f"  {_dataset_text(summary)}")
    if summary.get("cameras"):
        lines.append("  cameras: " + ", ".join(
            str(c).removeprefix("observation.images.") for c in summary["cameras"]
        ))
    if summary.get("state_dim"):
        lines.append(f"  widths:  state {summary['state_dim']} · action {summary['action_dim']}")
    if versions:
        lines.append("  versions:")
        for version in versions:
            mark = "*" if version["version"] == (pinned or dataset.get("latest_version")) else " "
            when = str(version.get("created_at") or "")[:10]
            who = f" · {version['created_by']}" if version.get("created_by") else ""
            lines.append(
                f"   {mark} v{version['version']} · {size_text(int(version.get('bytes') or 0))} · "
                f"{when}{who} · {_source_text(version.get('source') or {})}"
            )
    runs = [r for r in dataset.get("runs") or [] if not pinned or r.get("version") == pinned]
    if runs:
        lines.append("  runs:")
        lines += [f"    {r['id']}  {r['name']}  {r['status']}  (v{r['version']})" for r in runs]
    return lines


def run_show(
    *,
    name: str,
    json_output: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    ref, pinned = split_ref(name)
    dataset = call(client_factory, "get_dataset", ref)
    if pinned is not None and not any(
        v["version"] == pinned for v in dataset.get("versions") or []
    ):
        raise errors.DreamscaleError(
            errors.ErrorInfo(
                code="dataset_version_not_found",
                problem=f"dataset {dataset['full_name']} has no version {pinned}",
                cause="it was deleted, or never existed",
                fix=f"dreamscale datasets show {dataset['name']} lists its versions",
            )
        )
    if json_output:
        print_fn(json.dumps(dataset, indent=2, sort_keys=True))
        return dataset
    for line in describe(dataset, pinned):
        print_fn(line)
    failed = (dataset.get("failed_import") or {}).get("error")
    if failed:
        print_fn(f"  last import failed: {failed.get('message')}")
        print_fn(f"  fix: {failed.get('fix')}")
    running = dataset.get("import")
    if running is not None:
        final = _follow_import(dataset, running, client_factory=client_factory,
                               print_fn=print_fn, sleep=sleep)
        if final is not None:
            if final["status"] != "ready":
                raise import_error(final)
            print_fn(f"✓ {dataset['full_name']} v{final['version']}")
    return dataset


def run_download(
    *,
    name: str,
    folder: str | None = None,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> Path:
    ref, pinned = split_ref(name)
    dataset = call(client_factory, "get_dataset", ref)
    version = pinned or dataset.get("latest_version")
    if version is None:
        from dreamscale.datasets import _empty

        raise _empty(dataset["name"])
    dest = Path(folder).expanduser() if folder else Path(dataset["name"])
    printer, live = live_printer(print_fn)
    started = time.monotonic()
    last = [-1]

    def progress(done: int, total: int) -> None:
        quarter = done * 4 // total if total else 4
        if live or quarter != last[0]:
            unit, scale = ("GB", 1e9) if total >= 1e8 else ("MB", 1e6)
            filled = round(_BAR * done / total) if total else _BAR
            printer(f"Downloading {'━' * filled}{'─' * (_BAR - filled)} {done / scale:.1f} of "
                    f"{total / scale:.1f} {unit} · {duration(time.monotonic() - started)}")
            last[0] = quarter

    try:
        _download(client_factory, dataset["id"], version, dest, progress=progress)
    except KeyboardInterrupt:
        close_printer(printer, print_fn)
        print_fn("Download paused. Run the same command to resume.")
        raise
    finally:
        close_printer(printer, print_fn)
    print_fn(f"✓ {dataset['full_name']} v{version} in {dest}")
    return dest


def run_rename(
    *,
    name: str,
    new_name: str,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
) -> dict:
    renamed = call(client_factory, "rename_dataset", name, new_name)
    print_fn(f"Renamed {name} to {renamed['full_name']}.")
    if not name.startswith("ds_"):
        print_fn(f"{name} still names it until another dataset takes that name.")
    return renamed


def run_rm(
    *,
    name: str,
    yes: bool = False,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    confirm_fn: Callable[..., bool] = ask,
    interactive: bool | None = None,
) -> dict:
    interactive = sys.stdin.isatty() if interactive is None else interactive
    ref, pinned = split_ref(name)
    dataset = call(client_factory, "get_dataset", ref)
    versions = dataset.get("versions") or []
    if pinned is not None:
        what = f"{dataset['full_name']} v{pinned}"
    else:
        count = len(versions)
        size = int(dataset.get("bytes") or 0)
        what = (f"{dataset['full_name']} ({count} version{'s' if count != 1 else ''}"
                + (f", {size_text(size)})" if size else ")"))
    if not yes:
        if not interactive:
            raise _confirm_required("Deleting a dataset")
        question = f"Delete {what}? Runs and deployments made from it keep working."
        if not confirm_fn(question, default=False):
            print_fn("Not deleted.")
            return dataset
    if pinned is not None:
        result = call(client_factory, "delete_dataset_version", dataset["id"], pinned)
    else:
        result = call(client_factory, "delete_dataset", dataset["id"])
    print_fn(f"Deleted {what} permanently.")
    return result
