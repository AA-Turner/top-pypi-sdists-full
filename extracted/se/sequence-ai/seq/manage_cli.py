"""
The commands of `seq policy | benchmark | eval | adapter | volume` and `seq audit` that had no function of their own,
as functions: `seq.policy_list`, `policy_status`, `policy_stop`, `policy_start`, `policy_rm`, `policy_upgrade`,
`policy_versions`, `policy_rollback`, `policy_source`; `seq.benchmark_status`, `benchmark_cancel`, `benchmark_rm`,
`benchmark_upgrade`, `benchmark_versions`, `benchmark_source`; `seq.eval_status`,
`eval_report`, `eval_cancel`, `eval_list`; `seq.adapter_list`, `adapter_rm`; `seq.volume_list`, `volume_show`;
`seq.audit`.


In one sentence: each calls the very function its command runs - which says its lines through `echo` and returns what
it read - with the arguments the command has, written as `seq.robot_add(policy=...)` and `seq.policy_settings(name)`
are (what the call names first, the rest by keyword, `base_url` and `echo` last) → it says nothing unless given `echo`
(`echo=print` says what the command says), so a script's log stays its own → it returns what `seq --json <command>`
prints, so a script reads the data the command shows → a refusal raises the library's typed error, as the command
reports it (`sequence_ai.errors`). A version the command writes NAME@vN is `version=N` here.

    seq.policy_stop("kitchen_user")                      # {"name": "kitchen_user", "workers_stopped": 2, ...}
    seq.policy_rollback("kitchen_user", version=2)       # serves v2 again, no rebuild
    seq.eval_list("kitchen_user", benchmark="reach_user")   # one page of the evals that policy ran on that benchmark
"""
from __future__ import annotations

from typing import Any, Callable

Echo = Callable[[str], Any] | None


def _quiet(*_args: Any, **_kwargs: Any) -> None:
    """The `echo` of a call given none: what the command would say goes nowhere."""


def _say(echo: Echo) -> Callable[..., Any]:
    return echo if echo is not None else _quiet


def _page(limit: int | None, cursor: str | None) -> dict:
    """The paging that was given, as keyword arguments (the list call's own defaults fill the rest)."""
    return {k: v for k, v in (("limit", limit), ("cursor", cursor)) if v is not None}


def _ref(name: str, version: int | None) -> str:
    """`NAME@vN` as the commands that take a version write it, or the bare NAME for the version they would choose."""
    return name if version is None else f"{name}@v{int(version)}"



def policy_list(*, limit: int | None = None, cursor: str | None = None, base_url: str | None = None,
                echo: Echo = None) -> dict:
    """Your deployed policies, newest first, one page (`seq policy ls`): {"data": [{name, status, version, gpu,
    weights, stopped, latest, ...}, ...], "total", "offset", "next_cursor"}; `limit` rows (default 50) from the
    `cursor` the page before returned as `next_cursor`."""
    from seq import deployments_cli

    return deployments_cli.list_remote(base_url, _say(echo), limit=limit, cursor=cursor)


def policy_metrics(name: str, *, hours: int = 24, base_url: str | None = None, echo: Echo = None) -> dict:
    """A policy's workers' readings over the last `hours` (24 by default, 336 at most) - GPU utilization, GPU memory
    used of its total, CPU cores and memory, one a minute each, oldest first, each worker by its handle's short hash -
    as its console page charts them (GET /v1/deployments/{name}/metrics): {"name", "hours", "readings": [{"handle",
    "ts", "gpu_util_pct", "gpu_mem_used_mb", "gpu_mem_total_mb", "cpu_cores", "mem_gib"}, ...]}. With `echo`, each
    worker's GPU over the window in a line, as `seq policy status` ends with it."""
    from seq.deployments_cli import _call
    from sequence_ai._core.names import segment

    out = _call("GET", f"/v1/deployments/{segment(name)}/metrics?hours={int(hours)}", base_url) or {}
    if echo is not None:
        for line in gpu_lines(out):
            echo(line)
    return out


def gpu_lines(out: dict) -> list[str]:
    """Each worker's GPU over a window of readings: its utilization's median and peak, the most memory it held of its
    card's; a worker with no GPU reading (a CPU worker) said as one."""
    readings = out.get("readings") or []
    hours = out.get("hours") or 24
    if not readings:
        return [f"GPU, last {hours} h: no reading"]
    workers: dict[str, list[dict]] = {}
    for r in readings:
        workers.setdefault(str(r.get("handle") or "?"), []).append(r)
    lines = [f"GPU, last {hours} h:"]
    for handle, rows in workers.items():
        util = sorted(float(r["gpu_util_pct"]) for r in rows if r.get("gpu_util_pct") is not None)
        used = [float(r["gpu_mem_used_mb"]) for r in rows if r.get("gpu_mem_used_mb") is not None]
        total = next((float(r["gpu_mem_total_mb"]) for r in rows if r.get("gpu_mem_total_mb")), None)
        if not util:
            lines.append(f"  worker {handle}: no GPU reading ({len(rows)} reading{'' if len(rows) == 1 else 's'}: a "
                         "CPU worker)")
            continue
        memory = (f" · memory at most {max(used) / 1024:.1f} of {total / 1024:.1f} GiB" if used and total else "")
        lines.append(f"  worker {handle}: utilization {util[len(util) // 2]:.0f}% median, {util[-1]:.0f}% at most"
                     f"{memory} ({len(rows)} reading{'' if len(rows) == 1 else 's'})")
    return lines


def policy_status(name: str, *, wait: bool = False, timeout_s: float | None = None, base_url: str | None = None,
                  echo: Echo = None) -> dict:
    """A deployment's state - building, ready or failed, and why - with its fleet (`seq policy status`): {"status",
    "model", "error", "reason", "fleet": {workers, queue, scaling, ...}}. `wait` polls until the build is ready or
    failed, and then until robots can connect (up to `timeout_s`). A deployment whose build failed raises, and so does
    a wait that ended with the build still going - as the command ends - except a new version that failed beside the
    one serving: that is news, and the state returned is the new version's. With `echo`, each state it waits through
    and the fleet are said, and so are the warnings the command puts on stderr."""
    from seq import deploy_cli

    return deploy_cli.status(name, wait=wait, timeout=timeout_s, base_url=base_url, echo=echo, warn=echo)


def policy_stop(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """End every worker of a deployment now and refuse connects until `policy_start` (`seq policy stop`); a version
    still building finishes. {"name", "version", "stopped", "workers_stopped", ...}"""
    from seq import deployments_cli

    return deployments_cli.stop(name, base_url, _say(echo))


def policy_start(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Let robots connect to a stopped deployment again (`seq policy start`): {"name", "version", "stopped", ...}."""
    from seq import deployments_cli

    return deployments_cli.start(name, base_url, _say(echo))


def policy_rm(name: str, *, force: bool = False, dry_run: bool = False, base_url: str | None = None,
              echo: Echo = None) -> dict:
    """Delete a deployment for good (`seq policy rm`): its workers end now, its robot keys and what it stores go, its name
    and quota place are free, and nothing can bring it back. Refused while robots are connected or evals run on it unless
    `force`; `dry_run` deletes nothing and returns what deleting it would touch. {"deleted", "workers_stopped", ...} A
    `name@vN` deletes that version alone: {"name", "version", "state": "deleting" | "deleted"}."""
    from seq import deployments_cli

    return deployments_cli.rm(name, base_url, _say(echo), force=force, dry_run=dry_run)


def policy_upgrade(name: str, *, to: str | None = None, dry_run: bool = False, wait: bool = True,
                   timeout_s: float | None = None, base_url: str | None = None, echo: Echo = None) -> dict:
    """Move a deployment made from a template to the template's newer version (`seq policy upgrade`), built beside
    the one serving, your changes and its scaling kept. `to` names a version of the template it was made from,
    "toy-policy@v3"; the stable one without it. `dry_run` changes nothing and returns what the upgrade would change,
    keep and cost; `wait` follows the new version's build to ready (up to `timeout_s`). Returns the platform's plan."""
    from seq import upgrade_cli

    return upgrade_cli.upgrade(name, kind="policy", to=to, dry_run=dry_run, wait=wait, timeout=timeout_s,
                               base_url=base_url, echo=_say(echo))


def policy_versions(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """A deployment's versions, newest first - building, serving, kept for rollback - each with its card, template and
    weights, and the builds of versions no longer kept (`seq policy versions`): {"versions": [...], "builds": [...]}."""
    from seq import deployments_cli

    return deployments_cli.versions(name, base_url, _say(echo))


def policy_rollback(name: str, *, version: int | None = None, base_url: str | None = None,
                    echo: Echo = None) -> dict:
    """Serve a kept earlier version again, with no rebuild (`seq policy rollback`): `version`, or the version before the
    one serving. It serves from now on; robots on another version are disconnected, and each connects again to reach it,
    after a cold start when none of its workers is running. {"name", "version", "kept_versions", "dropped", ...}"""
    from seq import deployments_cli

    return deployments_cli.rollback(name, version, base_url, _say(echo))


def policy_source(name: str, *, version: int | None = None, out: str | None = None, base_url: str | None = None,
                  echo: Echo = None) -> dict:
    """The code a version runs, as it deployed it - `version`, or the one serving - downloaded and unpacked into the
    folder `out` (default ./<name>-v<N>; one that holds anything is refused) (`seq policy source`):
    {"name", "version", "dir", "files"}."""
    from seq import deployments_cli

    return deployments_cli.source(name, version, out, base_url, _say(echo))



def benchmark_status(name: str, *, wait: bool = False, timeout_s: float | None = None, base_url: str | None = None,
                     echo: Echo = None) -> dict:
    """A benchmark's build (`seq benchmark status`): {"name", "status": "building" | "ready" | "failed", "error"}.
    `wait` polls until it is ready or failed (up to `timeout_s`). A build that failed raises, and so does a wait that
    ended with the build still going; a registration its owner canceled is returned as failed, with its error."""
    from seq import listing

    return listing.benchmark_status(name, wait=wait, timeout=timeout_s, base_url=base_url, echo=echo)


def benchmark_cancel(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Stop a benchmark's registration in flight (`seq benchmark cancel`): its check's machine ends now, none of its
    check is billed, and evals run the version before it. {"name", "version", "status", "runs", "stage",
    "check_started"}"""
    from seq import benchmark_cancel_cli

    return benchmark_cancel_cli.cancel(name, base_url=base_url, echo=_say(echo))


def benchmark_rm(name: str, *, force: bool = False, dry_run: bool = False, base_url: str | None = None,
                 echo: Echo = None) -> dict:
    """Delete a benchmark for good (`seq benchmark rm`): what it stores goes, its name and quota place are free at once, a
    build in flight stops, the evals that ran it keep their reports, and nothing can bring it back. Refused while an eval
    runs on it unless `force` cancels those; `dry_run` deletes nothing and returns what deleting it would touch."""
    from seq import benchmark_rm_cli

    return benchmark_rm_cli.rm(name, dry_run=dry_run, force=force, base_url=base_url, echo=_say(echo))


def benchmark_upgrade(name: str, *, to: str | None = None, dry_run: bool = False, wait: bool = True,
                      timeout_s: float | None = None, base_url: str | None = None, echo: Echo = None) -> dict:
    """Move a benchmark registered from a template to the template's newer version, or back to an earlier one with
    `to` ("libero-10@v8"), your changes kept (`seq benchmark upgrade`). `dry_run` changes nothing and returns the plan;
    `wait` follows the new version's build to ready (up to `timeout_s`)."""
    from seq import upgrade_cli

    return upgrade_cli.upgrade(name, kind="benchmark", to=to, dry_run=dry_run, wait=wait, timeout=timeout_s,
                               base_url=base_url, echo=_say(echo))


def benchmark_versions(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """A benchmark's versions, newest first - each one's build: its state, how long it took, the step a failed one
    stopped in - and the one new evals run (`seq benchmark versions`): {"builds": [{version, state, serving,
    duration_s, ...}, ...]}."""
    from seq import listing

    return listing.versions(name, base_url=base_url, echo=_say(echo))


def benchmark_source(name: str, *, version: int | None = None, out: str | None = None, base_url: str | None = None,
                     echo: Echo = None) -> dict:
    """The code a benchmark version runs, as it was registered - `version`, or the one new evals run - downloaded and
    unpacked into the folder `out` (default ./<name>-v<N>; one that holds anything is refused) (`seq benchmark
    source`): {"name", "version", "dir", "files"}."""
    from seq import benchmark_source_cli

    return benchmark_source_cli.source(name, version, out, base_url, _say(echo))



def eval_status(eval_id: str, *, watch: bool = False, every: float | None = None, base_url: str | None = None,
                echo: Echo = None) -> dict:
    """Where an eval is - in line for GPUs, running or ended - and how far it has got (`seq eval status`):
    {"eval_id", "status", "queue", "progress": {done, total, arms, ...}, "incomplete", "errors", "time_limit",
    "units"}. `watch` reads it again every `every` seconds (5) until it ends, and returns what it read last."""
    from seq import eval_cli

    return eval_cli.eval_status(eval_id, watch=watch, every=every, base_url=base_url, echo=echo)


def eval_report(eval_id: str, *, wait: bool = False, timeout_s: float | None = None, base_url: str | None = None,
                echo: Echo = None) -> dict:
    """An eval's report and its details (`seq eval report`): {"report": {status, metrics, cost_usd, arms, ...},
    "details": {manifest, progress, episodes, ...}}. `wait` waits until the eval has ended (up to `timeout_s`; one
    still running then raises). The recordings, trajectories, replays and CSV the command saves beside it are its
    alone: `seq.eval_episodes` pages the episodes."""
    from seq import eval_cli

    return eval_cli.eval_report(eval_id, wait=wait, timeout_s=timeout_s, base_url=base_url, echo=echo)


def eval_cancel(eval_id: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Stop a running eval (`seq eval cancel`): no new episodes, its machines stop within a minute, what ran is billed
    and reported. {"eval_id", "status"}: "canceling" while the machines stop."""
    from seq import eval_cli

    return eval_cli.eval_cancel(eval_id, base_url=base_url, echo=echo)


def eval_rm(eval_ids: str | list[str], *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Delete ended evals for good (`seq eval rm`): their reports, episodes and recordings, as the console's Eval runs tab
    does; a queued or running one is refused - cancel it first. {"deleted": [ids]}."""
    from seq import eval_cli

    return eval_cli.eval_rm(eval_ids, base_url=base_url, echo=echo)


def eval_list(policy: str | None = None, *, benchmark: str | None = None, since: Any = None, limit: int | None = None,
              cursor: str | None = None, base_url: str | None = None, echo: Echo = None) -> dict:
    """Evals, newest first, one page (`seq eval ls`): with `benchmark`, every eval on it across your policies - only
    `policy`'s if one is named - {"benchmark", "evals", "total", "offset", "next_cursor"}; with a policy alone, its
    evals over time, {"deployment", "history", ...}. `since` drops a benchmark's evals submitted before a date, a time
    or a span back from now ("7d"). `seq.benchmark_evals` is the benchmark's list without a policy."""
    from seq import listing

    return listing.eval_list(policy, benchmark=benchmark, since=since, limit=limit, cursor=cursor, base_url=base_url,
                             echo=echo)



def adapter_list(*, limit: int | None = None, cursor: str | None = None, base_url: str | None = None,
                 echo: Echo = None) -> dict:
    """Your registered adapters, one page (`seq adapter ls`): {"adapters": [{name, latest, versions, pairs,
    last_eval, ...}, ...], "total", "offset", "next_cursor"}."""
    from seq import adapter_cli

    return adapter_cli.ls(base_url=base_url, echo=_say(echo), **_page(limit, cursor))


def adapter_rm(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Delete an adapter for good, every version of it (`seq adapter rm`); refused while an eval that runs it waits or runs.
    {"name", "deleted_versions"}"""
    from seq import adapter_cli

    return adapter_cli.rm(name, base_url=base_url, echo=_say(echo))


def volume_list(*, limit: int | None = None, cursor: str | None = None, base_url: str | None = None,
                echo: Echo = None) -> dict:
    """Your volumes and what uses each, one page (`seq volume ls`): {"data": [{name, kind, state, version,
    size_bytes, referenced_by, ...}, ...], "total", "offset", "next_cursor"}."""
    from seq import storage_cli

    return storage_cli.volume_list(limit=limit, cursor=cursor, base_url=base_url, echo=echo)


def volume_show(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """One volume (`seq volume show`): its kind, state, version and size, and what uses it - the policies whose
    weights and the benchmarks whose assets it is."""
    from seq import storage_cli

    return storage_cli.volume_show(name, base_url=base_url, echo=echo)


def audit(*, limit: int = 50, before: int | None = None, base_url: str | None = None, echo: Echo = None) -> list[dict]:
    """Who did what to your account, newest first, one page of `limit` events, 1-200 (`seq audit`): [{id, created_at,
    action, target, actor_email, actor_key, actor_kind, detail}, ...]. `before` continues below an event id: the id of
    the last event of the page before."""
    from seq import audit_cli

    return audit_cli.audit(limit=limit, before=before, base_url=base_url, echo=echo)
