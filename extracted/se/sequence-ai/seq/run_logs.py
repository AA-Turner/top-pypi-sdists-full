"""A benchmark's logs and an eval's — `seq benchmark logs <name>[@vN] [--worker RUN] [--since WHEN] [--before WHEN|SEQ]
[--build]` and `seq eval logs <id> [--side benchmark|policy] [--arm A] [--machine NAME] [--before WHEN|SEQ] [--follow]`
.

A benchmark's logs read as a policy's do: its eval runs are its workers - the lines their machines
printed, the newest runs merged by time or one alone - and --build is a version's build.

In one sentence: the gateway keeps what a benchmark's build reported of itself (its phases, the image build's output,
then the check's own: the setup's prints, which renderer it got) and every line an eval's machines printed (each
benchmark machine's stdout and stderr, each policy machine's structured lines) → these read them back, a version or a
page at a time, and `--follow` polls for the lines after the last one until the eval ends.

WHY: an eval's machines and a benchmark's check printed only where the owner could not read them, so "which renderer
did my sim get" or "why did episode 12 fail" had no answer outside the report's one-line errors.


Lines are kept by their kind - acts and prints 7 days, refused requests 14, the rest 30 - as each page the platform
answers says (its retention_days_by_kind).
"""
from __future__ import annotations

import time
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from datetime import datetime

from seq import clock

Echo = Optional[Callable[[str], None]]

FOLLOW_S = 2.0

RUN_LINES = 500


ENDED = ("settled", "completed", "failed", "canceled")


SAID = {"settled": "completed"}


def status_said(status: str | None) -> str | None:
    """An eval's state as its report names it (queued, running, completed, failed, canceled)."""
    return SAID.get(status, status) if status else status


def _client(base_url: str | None):
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(base_url=base_url)


def _quiet(_line: str) -> None:
    """The echo of a call made with none: its lines dropped, what it read returned."""


def _t(line: dict) -> Optional[float]:
    """A line's time, epoch seconds; None for one without."""
    t = clock.instant(line.get("ts"))
    return t.timestamp() if t else None



SCAN = 2000


def _forward(client, eval_id: str, **filters):
    """An eval's lines in the order the platform kept them, read forward from its start a page at a time (`after`, the
    `next` each page hands on): each page, as it answered it."""
    cursor = 0
    while True:
        page = client.eval_logs(eval_id, after=cursor, limit=SCAN, **filters)
        yield page
        if not page.get("lines") or page.get("next") in (None, cursor):
            return
        cursor = page["next"]


def _first_at(client, eval_id: str, when: float, **filters) -> Optional[int]:
    """The number of the first line the platform kept that was printed at or after `when` - the line a page before
    `when` ends at, as a policy's log is paged (logs_cli.policy_logs) - or None when no line was. Read forward: an
    eval's machines' lines are kept as they are sent, and a benchmark's can come minutes after it printed them
, so read back no page can be said to
    hold none printed later."""
    for page in _forward(client, eval_id, **filters):
        at = [ln["id"] for ln in page.get("lines") or [] if (t := _t(ln)) is not None and t >= when]
        if at:
            return min(at)
    return None


def _lines_back(client, eval_id: str, *, before=None, since: Optional[float] = None, limit: int = 500,
                **filters) -> tuple[list[dict], Optional[int], dict]:
    """An eval's lines: the newest `limit` before `before` - a line's number, or a time: the page before the first line
    kept that was printed at or after it (_first_at) - or every one printed since `since` (and before `before`), read
    forward from the log's start. Returns them, the cursor of the lines before them (a page's `older`: None when there
    are none, or with `since`) and the last page the platform answered.
"""
    from seq.logs_cli import before_point

    end, when = before_point(before) if before is not None else (None, None)
    if when is not None:
        end = _first_at(client, eval_id, when, **filters)
    if since is not None:
        kept: list[dict] = []
        page: dict = {}
        for page in _forward(client, eval_id, **filters):
            kept += [ln for ln in page.get("lines") or []
                     if (t := _t(ln)) is not None and t >= since and (end is None or ln["id"] < end)]
        return sorted(kept, key=lambda ln: _t(ln) or 0.0), None, page
    page = client.eval_logs(eval_id, before=end, limit=limit, **filters)
    return list(page.get("lines") or []), page.get("older"), page


def _kept(page: dict) -> Optional[str]:
    """How long the platform keeps an eval's lines, kind by kind, as its page says (retention_days_by_kind): "kept: acts
    and prints 7 days, refused requests 14 days, everything else 30 days". Before, "lines are kept 7 days", where an
    error, a machine's start and its setup are kept 30."""
    from seq.logs_cli import _kept_said

    return _kept_said(page.get("retention_days_by_kind") or {})



RUNS = 5
_ASKED = 50


def benchmark_runs_logs(name: str, *, worker: str | None = None, since: str | float | datetime | None = None,
                        before: int | str | float | datetime | None = None, limit: int | None = None,
                        base_url: str | None = None, echo: Echo = None) -> dict:
    """`seq benchmark logs <name> [--worker RUN] [--since WHEN] [--before WHEN|SEQ]`: a benchmark's eval runs - each run
    a worker, as a policy's machines are its log's - the lines their machines printed, the benchmark's machines and the
    policy's (GET /v1/eval/{id}/logs): the newest RUNS runs merged by time, each line under its run's policy, or one run
    alone (`worker`: its eval id or the start of it) - each run's newest page (RUN_LINES), its page before `before` (a
    time, or a line's number, which orders every eval's lines), or every line since `since`, each run read back a page
    at a time. A version's build is --build's, as a policy's is.



    """
    from seq.logs_cli import before_point, since_epoch
    from sequence_ai.errors import InvalidRequest, NotFound

    echo = echo or _quiet
    if before is not None:
        before_point(before)
    client = _client(base_url)
    runs = list(client.benchmark_evals(name, limit=_ASKED if worker else RUNS).get("evals") or [])
    if worker:
        runs = [e for e in runs if str(e.get("eval_id") or "").startswith(worker)]
        if not runs:
            raise NotFound(f"no eval run of {name} starts with {worker!r}",
                           hint=f"seq eval ls --benchmark {name} lists its runs")
        if len(runs) > 1:
            raise InvalidRequest(f"{worker!r} is the start of {len(runs)} eval runs of {name}: give more of its id")
    if not runs:
        echo(f"no eval runs on {name} yet: run one with `seq eval run <policy> --benchmark {name}` "
             f"(its build: seq benchmark logs {name} --build)")
        return {"benchmark": name, "runs": [], "lines": [], "older": None}
    after = since_epoch(since) if since not in (None, "") else None
    lines: list[dict] = []



    on: Optional[int] = None
    kept: Optional[str] = None
    for e in runs:
        run = f"{e.get('policy') or '?'}@v{e.get('model_version') if e.get('model_version') is not None else '?'}"
        echo(f"{str(e.get('eval_id'))[:8]}  {run:<24} {status_said(e.get('status')) or '—':<10} "
             f"{clock.stamp(e.get('created_at'), unit='minute')}")
        got, older, page = _lines_back(client, str(e["eval_id"]), before=before, since=after, limit=limit or RUN_LINES)
        kept = _kept(page) or kept
        if older is not None:
            on = max(on or 0, int(older))
        for ln in got:
            lines.append({**ln, "run": run, "eval_id": e["eval_id"], "_t": _t(ln) or 0.0})
    lines.sort(key=lambda ln: ln["_t"])
    days = clock.Days()
    for ln in lines:
        t = clock.instant(ln.get("ts"))
        head = days.head(t) if t else None
        if head:
            echo(head)
        where = ln.get("machine_name") or (f"arm {ln['arm']}" if ln.get("arm") is not None else "")
        echo(f"{clock.stamp(ln.get('ts'), unit='second', day='never', zone=False)}  {ln['run']:<24} "
             f"{ln.get('side', ''):<9} {where:<10} {ln.get('line', '')}")
    if not lines:
        echo("no lines from these runs" + (" since then" if after is not None else "") + (f" ({kept})" if kept else ""))
    if on is not None:
        echo(f"older lines are kept: seq benchmark logs {name}" + (f" --worker {worker}" if worker else "")
             + f" --before {on}")
    return {"benchmark": name, "runs": runs, "lines": [{k: v for k, v in ln.items() if k != "_t"} for ln in lines],
            "older": on}


def benchmark_logs(name: str, *, build: bool = False, version: int | None = None, worker: str | None = None,
                   since: str | float | datetime | None = None, before: int | str | float | datetime | None = None,
                   base_url: str | None = None, echo: Echo = None) -> dict:
    """`seq benchmark logs <name>[@vN] [--worker RUN] [--since WHEN] [--before WHEN|SEQ] [--build]`, its own function:
    its eval runs' lines (benchmark_runs_logs), or with `build` a version's build and check log (benchmark_build_log,
    the latest version's unless `version`). A time is --since's words, epoch seconds or a datetime. Printed only
    through `echo`."""
    from sequence_ai.errors import InvalidRequest

    if build:
        if worker or since not in (None, "") or before is not None:
            raise InvalidRequest("build is a version's build: worker, since and before read its eval runs' lines")
        return benchmark_build_log(name, version=version, base_url=base_url, echo=echo)
    if version is not None:
        raise InvalidRequest("a version names its build: build=True reads it")
    return benchmark_runs_logs(name, worker=worker, since=since, before=before, base_url=base_url, echo=echo)



def benchmark_build_log(name: str, *, version: int | None = None, base_url: str | None = None,
                        echo: Echo = None) -> dict:
    """One version's build (the latest unless `version`): its state, the phases it went through, what its check
    measured, and its log — the image build, then the check's output."""
    echo = echo or _quiet
    out = _client(base_url).benchmark_logs(name, version=version)
    state = f": {out['status']}" if out.get("status") else ""
    echo(f"{out['benchmark']} v{out['version']} (latest v{out.get('latest')}){state}"
         + (f" — {out['error']}" if out.get("error") else ""))
    if out.get("stages"):
        _steps(out["stages"], echo)
    elif out.get("phases"):
        echo(f"phases ({clock.zone_name(out['phases'][0].get('at'))}): " + " → ".join(_phases(out["phases"])))
    check = out.get("check") or {}
    if check:

        seen = [f"{check['steps']} steps" if check.get("steps") is not None else None,
                f"GPU use median {check['util_median']:.0f}%" if check.get("util_median") is not None else None,
                "on CPU" if check.get("on") == "cpu" else None, check.get("reason")]
        echo("check: " + ("passed" if check.get("ok") else "failed") + "".join(f", {s}" for s in seen if s))
    log = (out.get("log") or "").strip("\n")
    echo(log if log else "no build log was kept for this version (it was built before builds reported one)")
    return out


def _steps(stages: list, echo: Echo) -> None:
    """Its build step by step, as `seq policy logs --build` says a policy's (deploy_cli._print_steps): each with its
    state, its time - a running one's so far - and what it did; a step it never reached, or passed by with nothing to
    say, left out.
"""
    from seq.deploy_cli import _MARKS, _STAGE_SHORT, elapsed

    for s in stages:
        if not isinstance(s, dict):
            continue
        name, state = s.get("stage"), s.get("state")
        if state == "pending" or (state == "skipped" and not s.get("summary")):
            continue
        took = elapsed(s["duration_s"]) if isinstance(s.get("duration_s"), (int, float)) else ""
        echo(f"  {_MARKS.get(state, '?')} {_STAGE_SHORT.get(name, name):<12}{took:>10}  {s.get('summary') or ''}"
             .rstrip())


def _phases(phases: list[dict]) -> list[str]:
    """Each phase with its start (epoch seconds, as the build wrote it) on this machine's clock - `image 16:53:20` - the
    date in front of the first one that is not today's or not the day of the one before, the zone in the heading."""
    out, last = [], None
    for p in phases:
        t = clock.instant(p.get("at"))
        if t is None:
            out.append(f"{p['phase']} —")
            continue
        new_day = t.date() != (last or clock.instant(time.time())).date()
        out.append(f"{p['phase']} " + (f"{t:%Y-%m-%d} " if new_day else "") + f"{t:%H:%M:%S}")
        last = t
    return out



def eval_logs(eval_id: str, *, side: str | None = None, arm: int | None = None, machine: str | None = None,
              before=None, follow: bool = False, limit: int = 500, base_url: str | None = None,
              echo: Echo = None, sleep: Callable[[float], None] = time.sleep) -> dict:
    """`seq eval logs <id>`, its own function - an eval's lines, oldest first: the newest `limit`, or the `limit` before
    `before` (a line's number, or a time), then with `follow` every new one as it arrives, until the eval has ended and
    a last read brings nothing new; while older lines are kept, the last line said is the --before that reads the page
    before. Returns what it read: {eval_id, status, lines, next, older}."""
    from sequence_ai.errors import InvalidRequest

    if follow and before is not None:
        raise InvalidRequest("--follow reads on from the newest line and --before back from a point: one or the other")
    echo = echo or _quiet
    client = _client(base_url)
    filters = {"side": side, "arm": arm, "machine": machine}
    if before is None:
        page = client.eval_logs(eval_id, limit=limit, **filters)
        lines, older = list(page.get("lines") or []), page.get("older")
    else:
        lines, older, page = _lines_back(client, eval_id, before=before, limit=limit, **filters)
    days = clock.Days()
    _print_lines(lines, echo, days)
    if not lines and not follow:
        kept = _kept(page) if page.get("status") in ENDED else None
        echo(f"no lines yet from eval {eval_id}" + (f" ({kept})" if kept else ""))
    if older is not None and not follow:
        echo(f"older lines are kept: seq eval logs {eval_id}"
             + "".join(f" --{k} {v}" for k, v in filters.items() if v is not None) + f" --before {older}")
    while follow:
        ended = page.get("status") in ENDED
        sleep(FOLLOW_S)
        page = client.eval_logs(eval_id, side=side, arm=arm, machine=machine, after=page.get("next"), limit=limit)
        fresh = list(page.get("lines") or [])
        _print_lines(fresh, echo, days)
        lines += fresh

        if ended and not fresh:
            echo(f"eval {eval_id} {status_said(page.get('status'))}")
            break
    return {"eval_id": eval_id, "status": page.get("status"), "lines": lines, "next": page.get("next"), "older": older}


def _print_lines(lines: list[dict], echo: Callable[[str], None], days: clock.Days) -> None:
    """Each line as `14:05:09  benchmark a0-1  <text>` — its time on this machine's clock, the side and the machine it
    came from, then what it printed — after a line naming the day and the zone whenever the day changes."""
    for ln in lines:
        t = clock.instant(ln.get("ts"))
        head = days.head(t) if t else None
        if head:
            echo(head)
        where = ln.get("machine_name") or (f"arm {ln['arm']}" if ln.get("arm") is not None else "")
        echo(f"{clock.stamp(ln.get('ts'), unit='second', day='never', zone=False)}  {ln.get('side', ''):<9} "
             f"{where:<10} {ln.get('line', '')}")
