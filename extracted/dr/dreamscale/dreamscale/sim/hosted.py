"""Hosted benchmarks: `dreamscale sim robolab` (DSL-444) and `dreamscale sim robotwin`
(DSL-612) run on Dreamscale's simulators.

Nothing runs locally and no simulator is installed: the control plane's ``/v1/sim-runs`` API
creates the run, launches sim units for it and terminates them when it ends
(``mvp/docs/plans/2026-11-17-hosted-robolab-phase1.md``). This module creates the run, follows it
with one line per stage, cancels it on Ctrl-C, saves each episode's video and result, and prints
the success rate and the contract the score was measured under.

The control-plane calls take an open ``ControlPlaneClient`` (tests pass one over a fake
transport); ``run_hosted`` opens one per call from the saved config, like ``dreamscale train``.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import httpx

from dreamscale import errors
from dreamscale.config import load_config
from dreamscale.control import (
    ControlPlaneClient,
    _error_code,
    _raise_for_status,
    user_agent,
)

# Benchmarks that run on Dreamscale's simulators, not this computer.
HOSTED_BENCHMARKS = {"robolab": "RoboLab", "robotwin": "RoboTwin"}
EPISODES_MAX = {"robolab": 50, "robotwin": 100}
DEFAULT_EPISODES = 4
DEFAULT_MAX_UNITS = 1
SIM_RUNS_PATH = "/v1/sim-runs"
POLL_S = 3.0
ACTIVE = frozenset({"queued", "running"})
# Polls that may fail in a row (a dropped connection, a 5xx) before following gives up.
_POLL_FAILURES = 5
CANCELED_EXIT = 130

# The run's ``phase`` by stage. Unknown phases keep the stage already shown. ``launching``
# reads as Starting Isaac Sim once a unit is live (its machine is up and booting).
_WAITING = frozenset({"queued", "pending", "provisioning", "capacity"})
_STARTING = frozenset({"booting", "starting", "registering", "ready", "loading", "warming"})
_RUNNING = frozenset({"running", "evaluating", "finishing"})

GETTING = "Getting a simulator"
WAITING = "Waiting for L4 capacity"
STARTING = "Starting Isaac Sim"
STARTING_ROBOTWIN = "Starting RoboTwin"
PREPARING = "Preparing scene"
BOOT_STAGES = frozenset({GETTING, WAITING, STARTING, STARTING_ROBOTWIN, PREPARING})
DONE = "Done"


# --- the request ----------------------------------------------------------------------------


def run_body(
    benchmark: str,
    model: str,
    *,
    task_id: str | None = None,
    task_suite: str | None = None,
    task_ids: list[str] | None = None,
    episodes: int = DEFAULT_EPISODES,
    max_units: int = DEFAULT_MAX_UNITS,
) -> dict[str, Any]:
    """``POST /v1/sim-runs``'s body: one task by id, several (a benchmark without suites:
    ``--all``), or a suite (``all``: every task)."""
    if sum(x is not None for x in (task_id, task_suite, task_ids)) != 1:
        raise ValueError("choose one: a task id, task ids or a suite")
    body: dict[str, Any] = {"benchmark": benchmark, "model": model}
    if task_id is not None:
        body["tasks"] = [task_id]
    elif task_ids is not None:
        body["tasks"] = list(task_ids)
    else:
        body["suite"] = task_suite
    return {**body, "episodes": episodes, "max_units": max_units}


# --- the control plane ----------------------------------------------------------------------


def _refusal(resp: httpx.Response, benchmark: str | None) -> errors.DreamscaleError | None:
    label = HOSTED_BENCHMARKS.get(benchmark or "", "this benchmark")
    if resp.status_code == 403:
        return errors.DreamscaleError(errors.ErrorInfo(
            code="sim_run_not_entitled",
            problem=f"Hosted {label} isn't available to your organization",
            cause="this Dreamscale server doesn't run it for your organization, or not with "
            "that model",
            fix="email team@dreamscalelabs.com to ask for access",
        ))
    if resp.status_code == 404:
        return errors.DreamscaleError(errors.ErrorInfo(
            code="sim_runs_unavailable",
            problem="Hosted benchmarks aren't available here",
            cause="this Dreamscale server doesn't run hosted benchmarks",
            fix="check which server you're signed in to (dreamscale auth whoami), or email "
            "team@dreamscalelabs.com",
        ))
    if resp.status_code == 409 and _error_code(resp) in ("", "capacity"):
        return errors.CapacityError(errors.ErrorInfo(
            code="sim_capacity",
            problem="All simulators are busy",
            cause="every simulator this server runs is in use",
            fix="try again shortly",
        ))
    return None


def _answer(resp: httpx.Response, benchmark: str | None = None) -> dict[str, Any]:
    refusal = _refusal(resp, benchmark)
    if refusal is not None:
        raise refusal
    _raise_for_status(resp)
    return resp.json()


async def create_run(
    client: ControlPlaneClient, body: dict[str, Any], preview: bool = False,
) -> dict[str, Any]:
    headers = {"Prefer": "preview=robolab"} if preview else None
    resp = await client.sim_runs_request("POST", SIM_RUNS_PATH, json=body, headers=headers)
    return _answer(resp, body.get("benchmark"))


async def get_run(client: ControlPlaneClient, run_id: str) -> dict[str, Any]:
    return _answer(await client.sim_runs_request("GET", f"{SIM_RUNS_PATH}/{run_id}"))


async def cancel_run(client: ControlPlaneClient, run_id: str) -> dict[str, Any]:
    return _answer(await client.sim_runs_request("DELETE", f"{SIM_RUNS_PATH}/{run_id}"))


def call(client_factory: Callable[..., Any], fn: Callable[..., Any], *args: Any) -> Any:
    """``fn(client, *args)`` on a client opened from the saved config (key and server)."""
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")

    async def go() -> Any:
        client = client_factory(config.control_plane_url, config.api_key)
        try:
            return await fn(client, *args)
        finally:
            await client.close()

    return asyncio.run(go())


# --- following a run ------------------------------------------------------------------------


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _progress(run: dict[str, Any]) -> dict[str, Any]:
    """``tasks_done``/``tasks_total``/``episodes_done``/``episodes_total``: under
    ``progress``, or on the run itself."""
    progress = run.get("progress")
    return progress if isinstance(progress, dict) else run


def _error_text(run: dict[str, Any]) -> str:
    error = run.get("error")
    if isinstance(error, dict):
        error = error.get("problem") or error.get("message") or error.get("code")
    return str(error) if error else ""


def stage(run: dict[str, Any], previous: str | None = None) -> str:
    """The run's stage as one line: Getting a simulator · Starting Isaac Sim · Running k/n
    tasks · Done (or Failed / Canceled)."""
    status = run.get("status")
    if status == "succeeded":
        return DONE
    if status in ("failed", "canceled"):
        error = _error_text(run)
        return status.capitalize() + (f": {error}" if error else "")
    phase = str(run.get("phase") or "").lower()
    if phase == "waiting_for_capacity":
        return WAITING
    activity = run.get("activity") or {}
    unit_phase = activity.get("phase")
    starting = STARTING_ROBOTWIN if run.get("benchmark") == "robotwin" else STARTING
    if unit_phase == "starting_isaac_sim":
        return starting
    if unit_phase in ("claiming", "creating_env", "env_created"):
        return PREPARING
    if unit_phase == "running" and isinstance(activity.get("episode"), int):
        episode = activity["episode"] + 1
        total_episodes = (run.get("settings") or {}).get("episodes")
        return (f"Running · {activity.get('task') or run['benchmark']} · "
                f"episode {episode}/{total_episodes}" if total_episodes else
                f"Running · episode {episode}")
    if unit_phase == "saving":
        return "Saving episode artifacts"
    progress = _progress(run)
    done, total = _int(progress.get("tasks_done")), _int(progress.get("tasks_total"))
    if phase in _RUNNING or done or _int(progress.get("episodes_done")):
        return f"Running {done}/{total} tasks" if total else "Running tasks"
    units = run.get("units") if isinstance(run.get("units"), dict) else {}
    if phase in _STARTING or (phase == "launching" and _int(units.get("live"))):
        return starting
    if phase in _WAITING or phase == "launching" or status == "queued":
        return GETTING
    return previous or GETTING


def follow(
    run: dict[str, Any],
    *,
    fetch: Callable[[str], dict[str, Any]],
    print_fn: Callable[[str], None] = print,
    sleep: Callable[[float], None] = time.sleep,
    wait_started_at: float | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Poll the run every ``POLL_S`` until it finishes, printing its stage when it changes."""
    shown: str | None = None
    failures = 0
    while True:
        line = stage(run, shown)
        if line != shown:
            if wait_started_at is not None and line in BOOT_STAGES:
                print_fn(f"{line}: {int(clock() - wait_started_at)}s elapsed")
            else:
                if (
                    wait_started_at is not None
                    and shown in BOOT_STAGES
                    and (line.startswith("Running") or line == "Saving episode artifacts"
                         or run.get("status") == "succeeded")
                ):
                    print_fn("✓ Simulator ready")
                    wait_started_at = None
                print_fn(line)
            shown = line
        if run.get("status") not in ACTIVE:
            return run
        sleep(POLL_S)
        try:
            run = fetch(run["id"])
        except (httpx.TransportError, errors.ServerError):
            failures += 1
            if failures >= _POLL_FAILURES:
                raise
            continue
        failures = 0


# --- results --------------------------------------------------------------------------------


def task_episodes(run: dict[str, Any]) -> Iterator[tuple[str, list[tuple[int, dict]]]]:
    """Each task's name and its episodes as (episode number, row). ``tasks`` is a list of
    ``{"name", "episodes": [...]}`` or a map of name to that row (or to its episodes)."""
    tasks = run.get("tasks") or []
    if isinstance(tasks, dict):
        tasks = [
            {"name": name, **(row if isinstance(row, dict) else {"episodes": row})}
            for name, row in tasks.items()
        ]
    for task in tasks:
        if not isinstance(task, dict):
            continue
        name = str(task.get("name") or task.get("task") or "")
        rows = [row for row in task.get("episodes") or [] if isinstance(row, dict)]
        yield name, [
            (_int(row["episode"]) if "episode" in row else index, row)
            for index, row in enumerate(rows)
        ]


def task_rates(run: dict[str, Any]) -> list[tuple[str, int, int]]:
    """(task, successes, episodes) per task: the run's summary when it has one per task,
    else counted from the episodes."""
    per_task = (run.get("summary") or {}).get("tasks")
    if isinstance(per_task, dict):
        per_task = [{"name": name, **row} for name, row in per_task.items()
                    if isinstance(row, dict)]
    if isinstance(per_task, list) and per_task:
        return [
            (str(row.get("name") or row.get("task") or ""), _int(row.get("successes")),
             _int(row.get("episodes")))
            for row in per_task if isinstance(row, dict)
        ]
    return [
        (name, sum(1 for _, row in rows if row.get("success") is True), len(rows))
        for name, rows in task_episodes(run)
    ]


def _rate(successes: int, episodes: int) -> str:
    return f"{successes}/{episodes} ({successes / episodes:.0%})" if episodes else "no episodes"


def result_lines(run: dict[str, Any]) -> list[str]:
    """The success rate per task and overall, then the contract."""
    rates = task_rates(run)
    lines = []
    if rates:
        width = max(len(name) for name, _, _ in rates)
        lines += [f"  {name:<{width}}  {_rate(s, n)}" for name, s, n in rates]
    summary = run.get("summary") or {}
    if "episodes" in summary:
        successes, episodes = _int(summary.get("successes")), _int(summary.get("episodes"))
    else:
        successes, episodes = sum(r[1] for r in rates), sum(r[2] for r in rates)
    lines.append(f"Success rate: {_rate(successes, episodes)}")
    contract = run.get("contract") or {}
    parts = [
        f"{label} {str(contract[key])[:12] if key == 'seed_list_sha256' else contract[key]}"
        for key, label in (("gpu", "GPU"), ("isaac_sim", "Isaac Sim"),
                           ("robolab_commit", "RoboLab"), ("robotwin_commit", "RoboTwin"),
                           ("setting", "setting"), ("seed_list_sha256", "seeds"),
                           ("bundle", "bundle"))
        if contract.get(key) and (key != "bundle" or contract.get("benchmark") == "robotwin")
    ]
    if parts:
        lines.append("Contract: " + " · ".join(parts))
    return lines


# --- artifacts ------------------------------------------------------------------------------


def _safe_name(name: str) -> str:
    """A task name as one directory name (the server's text never escapes the folder)."""
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", name).strip("._")
    return safe or "task"


def _fetch(http: httpx.Client, url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_name(path.name + ".part")
    with http.stream("GET", url) as resp:
        resp.raise_for_status()
        with part.open("wb") as out:
            for chunk in resp.iter_bytes():
                out.write(chunk)
    part.replace(path)


def download_artifacts(
    run: dict[str, Any],
    dest: Path,
    *,
    http: httpx.Client | None = None,
    warn: Callable[[str], None] = print,
) -> list[Path]:
    """Save the run to ``dest/run.json`` and each episode's video (and result, when the run
    links one) to ``dest/<task>/episode_<k>.mp4`` (``.json``). A link that fails is named in a
    warning and skipped. Returns the files saved."""
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "run.json").write_text(json.dumps(run, indent=2) + "\n")
    saved = [dest / "run.json"]
    # Presigned links: no API key goes with them.
    own = http is None
    http = http or httpx.Client(
        timeout=httpx.Timeout(120.0, connect=10.0),
        follow_redirects=True,
        headers={"User-Agent": user_agent()},
    )
    try:
        for task, rows in task_episodes(run):
            folder = dest / _safe_name(task)
            for k, row in rows:
                for key, suffix in (("video_url", ".mp4"), ("result_url", ".json")):
                    url = row.get(key)
                    if not isinstance(url, str) or not url:
                        continue
                    path = folder / f"episode_{k}{suffix}"
                    try:
                        _fetch(http, url, path)
                    except httpx.HTTPError as exc:
                        warn(f"Couldn't save {task} episode {k}'s {key[:-4]}: {exc}")
                        continue
                    saved.append(path)
    finally:
        if own:
            http.close()
    return saved


# --- the command ----------------------------------------------------------------------------


def run_hosted(
    *,
    benchmark: str,
    model: str,
    task_id: str | None = None,
    task_suite: str | None = None,
    task_ids: list[str] | None = None,
    episodes: int = DEFAULT_EPISODES,
    max_units: int = DEFAULT_MAX_UNITS,
    json_output: bool = False,
    artifacts: Path | None = None,
    client_factory: Callable[..., Any] | None = None,
    print_fn: Callable[[str], None] = print,
    err_fn: Callable[[str], None] | None = None,
    live_wait: bool = False,
    view: bool = False,
    sleep: Callable[[float], None] = time.sleep,
    http: httpx.Client | None = None,
) -> int:
    """`dreamscale sim robolab`: create the run, follow it, save its artifacts, print the
    result. Returns the exit code: 0 when the run succeeded, 1 when it didn't, 130 when
    Ctrl-C canceled it. With ``json_output`` only the final run's JSON is printed."""
    if err_fn is None:
        def err_fn(line: str) -> None:
            print(line, file=sys.stderr)

    say = err_fn if json_output else print_fn
    client_factory = client_factory or ControlPlaneClient
    body = run_body(benchmark, model, task_id=task_id, task_suite=task_suite,
                    task_ids=task_ids, episodes=episodes, max_units=max_units)
    started = time.monotonic()
    if live_wait:
        say(f"{GETTING}: 0s elapsed")
    run = call(client_factory, create_run, body, view)
    run_id = run["id"]
    what = (f"task {task_id}" if task_id is not None
            else f"{len(task_ids)} tasks" if task_ids is not None
            else "every task" if body["suite"] == "all" else f"suite {body['suite']}")
    if not json_output:
        print_fn(f"{HOSTED_BENCHMARKS[benchmark]} run {run_id}: {model} · {what} · "
                 f"{episodes} episode{'s' if episodes != 1 else ''} per task")
    viewer = None
    try:
        if view and (run.get("settings") or {}).get("preview"):
            from dreamscale.sim.live_view import LiveView

            config = load_config()
            viewer = LiveView(config.control_plane_url, config.api_key, run_id)
        elif view:
            say("Live preview is unavailable for this run.")
        run = follow(
            run,
            fetch=lambda rid: call(client_factory, get_run, rid),
            print_fn=(lambda _line: None) if json_output else print_fn,
            sleep=sleep,
            wait_started_at=started if live_wait else None,
        )
    except KeyboardInterrupt:
        try:
            call(client_factory, cancel_run, run_id)
        except (KeyboardInterrupt, errors.DreamscaleError, httpx.HTTPError) as exc:
            say(f"Couldn't cancel {run_id} ({str(exc) or type(exc).__name__}); "
                "its simulators stop at the run's time limit.")
        else:
            say(f"Canceled {run_id}; its simulators are shutting down.")
        return CANCELED_EXIT
    finally:
        if viewer is not None:
            viewer.close()
    if artifacts is not None:
        saved = download_artifacts(run, artifacts, http=http, warn=err_fn)
        say(f"Saved {len(saved)} file{'s' if len(saved) != 1 else ''} to {artifacts}")
    if json_output:
        print_fn(json.dumps(run, indent=2))
    else:
        for line in result_lines(run):
            print_fn(line)
    return 0 if run.get("status") == "succeeded" else 1
