"""Your benchmarks, their versions, and every eval run on one of them — `seq benchmark ls`, `seq benchmark versions
<name>`, `seq eval ls --benchmark <name>`, and their Python twins `seq.benchmarks()` / `seq.benchmark_evals(name)`; a
benchmark's tasks, `seq benchmark tasks <name>` / `seq.benchmark_tasks(name)`; and an eval's episodes, a page at a
time, `seq eval episodes <eval_id>` / `seq.eval_episodes(eval_id)`.

WHY: your own benchmarks could only be read by name (`seq benchmark status <name>`), and a benchmark's evals only one
policy at a time (`seq eval ls <policy>`); the console listed benchmarks by reading the table directly.



The CLI and the Python functions return the same rows — the gateway's GET /v1/benchmarks and
GET /v1/benchmarks/{name}/evals — one page at a time: `limit` rows (default 50) from the `cursor` the previous page
returned as `next_cursor`, the same pages the console's pager steps through. Each page says where it starts
(`offset`) and how many rows match in all (`total`).
"""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from typing import Any, Callable

from seq import columns
from seq.clock import day_of, stamp
from sequence_ai._core.money import money

PAGE = 50

_SPAN = re.compile(r"(\d+)\s*([dhm])")


def since_iso(value: Any) -> str | None:
    """A `since` as the ISO the gateway takes: a date, a datetime, an ISO string, or a span back from now ("7d", "24h",
    "30m"). A bare date means midnight UTC, the billing day. None stays None."""
    from sequence_ai.errors import InvalidRequest

    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return (value if value.tzinfo else value.replace(tzinfo=timezone.utc)).isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    span = _SPAN.fullmatch(text)
    if span:
        n, unit = int(span.group(1)), span.group(2)
        back = {"d": timedelta(days=n), "h": timedelta(hours=n), "m": timedelta(minutes=n)}[unit]
        return (datetime.now(timezone.utc) - back).isoformat(timespec="seconds")
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise InvalidRequest(f"since takes a date (2026-10-01), a time, or a span back from now (7d, 24h); "
                             f"got {text!r}") from None
    return text


def benchmarks(*, limit: int = PAGE, cursor: str | None = None, api_key: str | None = None,
               base_url: str | None = None) -> dict:
    """Your benchmarks, newest first, one page:

        {"benchmarks": [{"name", "version", "versions", "status", "gpu", "worlds", "created_at",
                         "error", "template": {"name", "version", "channel"} or None, "replay": "3d" or None,
                         "last_eval": {"eval_id", "status", "created_at", "policy", "metric", "value", "low", "high"}
                                      or None}, ...],
         "total": N, "offset": 0, "next_cursor": "50" or None}

    `version` is also how many versions there have been (each re-registration is the next one). `template` is the
    template its code comes from - its version, and "stable" or "beta" (None: neither now) - None for your own code;
    `replay` is "3d" when the version records its 3D replay. `worlds` is how many worlds one call of a vectorized env's
    step takes (@seq.concurrent(sizes=[N])), None for an env of one world an instance."""
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(api_key=api_key, base_url=base_url).benchmarks(limit=limit, cursor=cursor)


def benchmark_evals(name: str, *, policy: str | None = None, since: Any = None, limit: int = PAGE,
                    cursor: str | None = None, api_key: str | None = None, base_url: str | None = None) -> dict:
    """Every eval run on benchmark `name`, across your policies (or only `policy`'s), newest first, one page:

        {"benchmark": name,
         "evals": [{"eval_id", "status", "created_at", "policy", "model_version", "benchmark_version", "adapter",
                    "episodes", "metric", "value", "low", "high", "incomplete", "cost_usd", "cost_settled"}, ...],
         "total": N, "offset": 0, "next_cursor": "50" or None}

    `since` drops evals submitted before it (a date, datetime, ISO string, or "7d"). One eval's full report stays
    `seq eval report <eval_id>`."""
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(api_key=api_key, base_url=base_url).benchmark_evals(
        name, policy=policy, since=since_iso(since), limit=limit, cursor=cursor)


def benchmark_tasks(name: str, *, version: int | None = None, api_key: str | None = None,
                    base_url: str | None = None) -> dict:
    """A registered benchmark's tasks - its current version's, or `version`'s:

        {"benchmark", "version", "template": {"name", "version", "channel"} or None, "replay": "3d" or None,
         "tasks": [{"task", "description", "max_seconds", "seeds": "0-49", "seed_count", "episodes"}, ...]}

    What seq.eval(tasks=, trials=, seeds=) and `seq eval run --tasks / --trials / --seeds` choose from: a task or a
    seed not listed here is refused. `description` is what the benchmark's tasks={name: description} says of the task
    ("" or None when it says nothing), `max_seconds` how long its episode may run on the robot's clock.
    """
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(api_key=api_key, base_url=base_url).benchmark_tasks(name, version=version)


def benchmark_io(name: str, *, api_key: str | None = None, base_url: str | None = None) -> dict:
    """What a benchmark's latest version hands an adapter and takes back:

        {"benchmark", "version", "observation": {key: {"shape": [...], "dtype": "..."}} or None,
         "obs_contract": {...} or None, "templates": [...]}

    `observation` is the first observation its registration check read - its keys and each entry's shape and dtype, no
    data (None for a version checked before this was recorded); `obs_contract` the observation contract it declared;
    `templates` the official templates it is made from. What `seq adapter check --benchmark` builds a sample from, and
    what `seq benchmark status` shows under the status."""
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(api_key=api_key, base_url=base_url).benchmark_io(name)


def print_benchmark_io(io: dict, *, echo: Callable[[str], None] = print) -> None:
    """The inputs a benchmark hands an adapter, under `seq benchmark status`: each observation key with its shape and
    dtype, then the templates it is made from. Nothing when the version recorded no observation."""
    obs = io.get("observation") or {}
    if obs:
        echo("  observation:")
        for key, spec in obs.items():
            shape = "×".join(str(d) for d in (spec or {}).get("shape") or []) or "?"
            echo(f"    {key}  {shape}  {(spec or {}).get('dtype') or ''}".rstrip())
    tmpl = io.get("templates") or []
    if tmpl:
        echo(f"  from template{'' if len(tmpl) == 1 else 's'}: " + ", ".join(tmpl))


def eval_episodes(eval_id: str, *, task: str | list[str] | None = None, outcome: str | None = None,
                  arm: int | None = None, limit: int = PAGE, cursor: str | None = None,
                  api_key: str | None = None, base_url: str | None = None) -> dict:
    """One page of an eval's episodes, as far as they have reported (a running eval's too):

        {"eval_id", "episodes": [{"index", "task", "seed", "start", "repeat", "success", "steps", "wall_s",
                                  "terminated", "truncated", "timed_out", "error", "metrics", ...}, ...],
         "total": N, "offset": 0, "next_cursor": "50" or None}

    `task` one task or several; `outcome` success, failure, error, truncated or timed_out; `arm` one arm's. An
    episode's `success` is what the benchmark's @seq.step said of its last step - None for one that errored - what the
    outcome filter reads; `metrics` the dict its steps returned beside it. `wall_s` is its seconds from reset to end;
    `start` the start it ran - its seed - and `repeat` how many times that start ran before it (0 the first).
    """
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(api_key=api_key, base_url=base_url).eval_episodes(
        eval_id, task=task, outcome=outcome, arm=arm, limit=limit, cursor=cursor)



def ls(*, limit: int = PAGE, cursor: str | None = None, base_url: str | None = None,
       echo: Callable[[str], None] = print) -> dict:
    """`seq benchmark ls [--limit N] [--cursor C]`: one page of your benchmarks, printed."""
    out = benchmarks(limit=limit, cursor=cursor, base_url=base_url)
    print_benchmarks(out, echo=echo)
    return out


def evals(name: str, *, policy: str | None = None, since: Any = None, limit: int = PAGE, cursor: str | None = None,
          base_url: str | None = None, echo: Callable[[str], None] = print) -> dict:
    """`seq eval ls --benchmark <name> [<policy>] [--since S] [--limit N] [--cursor C]`: one page of the evals run on a
    benchmark, printed."""
    out = benchmark_evals(name, policy=policy, since=since, limit=limit, cursor=cursor, base_url=base_url)
    print_benchmark_evals(out, echo=echo)
    return out


def versions(name: str, *, base_url: str | None = None, echo: Callable[[str], None] = print) -> dict:
    """`seq benchmark versions <name>`: a benchmark's versions, newest first, as a policy's are listed - each one's build:
    its state, how long it took and the step a failed one stopped in - and the one evals run, "in use" (GET
    /v1/benchmarks/{name}/builds: its newest 20). A version's build log: `seq benchmark logs <name>@vN --build`.


    The one in use is the platform's word (`serving`): the latest once it passed its check, else the latest that did -
    which evals run until a newer one passes; a version canceled, or stopped before it finished, says so.
    """
    from seq.deploy_cli import elapsed
    from seq.deployments_cli import _call, copy_line, error_line
    from sequence_ai._core.names import segment

    out = _call("GET", f"/v1/benchmarks/{segment(name)}/builds", base_url)
    rows = out.get("builds") or []
    if not rows:
        echo(f"{name} has no version yet")
        return out
    newest = rows[0]
    cells = []
    for r in rows:
        note = ""
        if r.get("serving"):

            note = (f"evals run v{r.get('version')} until v{newest.get('version')} passes its check"
                    if newest.get("state") == "building" and r is not newest else "new evals run this one")
        cells.append(["v" + str(r.get("version")), "in use" if r.get("serving") else str(r.get("state") or "-"),
                      elapsed(r["duration_s"]) if isinstance(r.get("duration_s"), (int, float)) else "-", note])

    widths = columns.widths([["ver", "state", "took", ""], *cells])
    echo(columns.line(["ver", "state", "took", ""], widths).rstrip())
    for r, row in zip(rows, cells):
        echo(columns.line(row, widths).rstrip())


        replaced = f"; replaced by v{r['replaced_by']}" if r.get("replaced_by") is not None else ""
        if r.get("failed_stage") or replaced:
            first = error_line(r.get("error"), r.get("failed_stage"))
            how = {"canceled": "canceled", "stopped": "stopped"}.get(str(r.get("state")), "failed")
            if how == "canceled":
                first = first.removeprefix("canceled: ")
            where = f"{how} in its {r['failed_stage']} step" if r.get("failed_stage") else how
            echo(f"{'':{widths[0]}}  ↳ {where}" + (f": {first}" if first else "")
                 + (", before it finished" if how == "stopped" else "") + replaced)
        if copy := copy_line(r):
            echo(f"{'':6}  ↳ {copy}")
    echo(f"a version's build: seq benchmark logs {name}@v<ver> --build")
    if any(r.get("state") == "kept" for r in rows):

        echo(f"a kept version: evals run it with --benchmark {name}@v<ver>, and seq benchmark rm {name}@v<ver> deletes it")
    from seq.freeze import footer

    if said := footer("benchmark", name, rows):
        echo(said)
    return out


def eval_list(policy: str | None = None, *, benchmark: str | None = None, since: Any = None, limit: int | None = None,
              cursor: str | None = None, base_url: str | None = None, echo: Callable[[str], Any] | None = None) -> dict:
    """`seq eval ls`: with `benchmark`, that benchmark's evals - only the named policy's if one is named - the one way
    to list them: {"benchmark", "evals", "total", "offset", "next_cursor"}; with a policy alone, its evals over time:
    {"deployment", "history", ...}. One page, newest first; `limit` rows from the `cursor` the page before returned
    as `next_cursor`. `since` (a benchmark's evals only) drops the evals submitted before a date, a time or a span
    back from now ("7d"). Says the page as the command does only when given `echo`.
    
"""
    from seq import ops_cli
    from sequence_ai.errors import InvalidRequest

    say = echo if echo is not None else _silent
    page = {k: v for k, v in (("limit", limit), ("cursor", cursor)) if v is not None}
    if benchmark:
        return evals(benchmark, policy=policy, since=since, base_url=base_url, echo=say, **page)
    if not policy:
        raise InvalidRequest("name a deployed policy, or a benchmark: seq eval ls --benchmark <name>")

    if since is not None:
        raise InvalidRequest("--since filters a benchmark's evals: add --benchmark <name>")
    return ops_cli.evals(policy, base_url=base_url, echo=say, **page)


def _silent(*_args: Any, **_kwargs: Any) -> None:
    """The `echo` of a call given none: what it would say goes nowhere."""


def benchmark_status(name: str, *, wait: bool = False, timeout: float | None = None, base_url: str | None = None,
                     echo: Callable[[str], Any] | None = None, on_retry: Callable[..., Any] | None = None,
                     on_more: Callable[[float], Any] | None = None, on_data: Callable[[dict], Any] | None = None) -> dict:
    """`seq benchmark status <name> [--wait]` / seq.benchmark_status: a benchmark's build - building, ready or failed,
    with the failure - as `seq --json benchmark status` prints it: {name, status, error}. `wait` polls until it is ready
    or failed (up to `timeout` seconds; a build whose log still moves is waited on past the default hour). A ready
    one is said with the template its code comes from, its card and its tasks (template_line).
    A registration its owner canceled is said as it is - no error, it ended as asked - and returned; a build that
    failed is raised, and so is a wait that ended with the build going on. `echo` says it, `on_retry` hears a platform
    lost and asked again, `on_more` a wait that goes on past its window, `on_data` the data before a refusal ends the
    call (the command prints it there)."""
    from seq._eval_gateway import BENCHMARK_WAIT_S, BUILD_MOVED_S, EvalGatewayClient
    from seq.errors import CANCELED, build_failed, canceled, still_building

    client = EvalGatewayClient(base_url=base_url)
    stalled: list[float] = []
    if wait:
        resp = client.wait_benchmark(name, timeout_s=timeout or BENCHMARK_WAIT_S, on_retry=on_retry,
                                     while_moving=timeout is None, on_more=on_more, on_stall=stalled.append)
    else:
        resp = client.benchmark(name)


    stopped = resp.status.value == "failed" and canceled(resp.error)
    data = resp.model_dump(mode="json")
    if on_data is not None:
        on_data(data)
    if echo is not None:
        if stopped:
            echo(f"{resp.name}: canceled — {str(resp.error).removeprefix(CANCELED)}")
        else:
            echo(f"{resp.name}: {resp.status.value}" + (f" — {resp.error}" if resp.error else ""))
            if resp.status.value == "ready":


                tasks = _tasks(client, resp.name)
                line = template_line(client, resp.name, tasks) if tasks is not None else None
                if line:
                    echo(line)


                if tasks and tasks.get("note"):
                    echo(f"  {tasks['note']}")


                u = (tasks or {}).get("template_update")
                if u:
                    echo(f"  {u['name']} {u['version']} is available"
                         + (f": {notes_said(u['notes'])}" if u.get("notes") else "")
                         + f" — seq benchmark upgrade {resp.name}")

                print_benchmark_io(benchmark_io(resp.name, base_url=base_url), echo=echo)
    if stopped:
        return data
    if resp.status.value == "failed":
        raise build_failed(f"benchmark {resp.name}", resp.error)
    if wait and resp.status.value != "ready":
        raise still_building(f"benchmark {resp.name}", f"seq benchmark status {resp.name} --wait",
                             stalled_s=BUILD_MOVED_S if stalled else None)
    return data


def _tasks(client: Any, name: str) -> dict | None:
    """The benchmark's tasks as GET /v1/benchmarks/{name}/tasks answers them, None when they cannot be read."""
    from sequence_ai.errors import SequencesError

    try:
        return client.benchmark_tasks(name)
    except SequencesError:
        return None


def template_line(client: Any, name: str, out: dict | None = None) -> str | None:
    """`seq benchmark status`'s second line: the template the benchmark's code comes from (its version and channel),
    its card and driver when it names one (card_label), whether it records its 3D replay, and how many tasks it has -
    None when its tasks cannot be read. All of it is read from the tasks (`out`, when already read): GET
    /v1/benchmarks/{name} is a strict contract that carries none of it."""
    if out is None:
        out = _tasks(client, name)
        if out is None:
            return None
    code = (f"template {template_label(out.get('template'), out.get('edited_from'))}"
            if out.get("template") or out.get("edited_from") else "your own code")
    many = len(out.get("tasks") or [])

    card = f", {card_label(out.get('gpu'), out['driver'])}" if out.get("driver") else ""
    return (f"  {code}" + card + (", records its 3D replay" if out.get("replay") else "")
            + f", {many} task{'s' if many != 1 else ''} (seq benchmark tasks {name})")


def card_label(gpu: Any, driver: Any = None) -> str:
    """A benchmark's card as `seq benchmark ls` and `status` write it: "L4", and for a benchmark that names its driver
    (driver=) the version it runs with, "L4 · driver 580.178.04" - the full version its registration check saw, the
    one it names until a check has said - the version alone, never where it runs.
    
"""
    card = _cell(gpu)
    return f"{card} · driver {driver}" if driver else card


def edited_label(edited: dict) -> str:
    """A folder `seq init` wrote and its owner edited, as `seq policy versions`, `status` and `seq benchmark ls` say it:
    the template its image installs, "toy-policy v3 (edited)" (the platform's edited_from) - the version left out when
    the platform names none."""
    version = f" {edited['version']}" if edited.get("version") else ""
    return f"{edited.get('name')}{version} (edited)"


def template_label(template: dict | None, edited: dict | None = None) -> str:
    """A benchmark's template as `seq benchmark ls` and `status` write it - "libero-spatial v2 (stable)", the channel
    left out when the version is in neither - its code edited since `seq init`, "libero-spatial v2 (edited)" - or a
    dash for a benchmark of your own code."""
    if not template:
        return edited_label(edited) if edited else "—"
    label = f"{template.get('name')} {template.get('version')}"
    return label + (f" ({template['channel']})" if template.get("channel") else "")


def notes_said(notes: list[str] | None) -> str:
    """A newer template version's notes in one run of text, as the line saying it is available writes them, each as it
    is: a space after one that ends its sentence, "; " after any other - a "; " after a note's own stop read
    "...toy-benchmark.; The env ..."."""
    said = ""
    for note in (n.strip() for n in notes or [] if n and n.strip()):
        if said:
            said += " " if said[-1] in ".!?" else "; "
        said += note
    return said


def print_benchmarks(out: dict, *, echo: Callable[[str], None] = print) -> None:
    """`seq benchmark ls`: one line per benchmark - the template its code comes from too, its card (and the driver it
    names, card_label), and how many worlds one call of its step takes (— for an env of one world an instance) - then
    where this page sits in the whole list."""
    rows = out.get("benchmarks") or []
    if not rows:
        echo("you have no benchmarks yet: register one with `seq deploy <file>`")
        return

    cards = [card_label(b.get("gpu"), b.get("driver")) for b in rows]
    gw = max([12, *(len(c) for c in cards)])
    echo(f"{'NAME':<24} {'VER':>3}  {'STATUS':<8}  {'TEMPLATE':<28} {'GPU':<{gw}} {'WORLDS':>6}  "
         f"{'REGISTERED':<10}  LAST EVAL")
    for b, card in zip(rows, cards):
        last = b.get("last_eval")
        last_text = "—" if not last else f"{last['eval_id'][:8]}  {last.get('policy') or '?'}  {_metric(last)}"
        tpl = template_label(b.get("template"), b.get("edited_from"))
        echo(f"{b['name']:<24} {_cell(b.get('version')):>3}  {b['status']:<8}  {tpl:<28} "
             f"{card:<{gw}} {_cell(b.get('worlds')):>6}  "
             f"{_day(b.get('created_at')):<10}  {last_text}")

        u, t = b.get("template_update"), b.get("template")
        if u and t:
            echo(f"{'':<24}   ↳ runs {t['name']} {t['version']}; {u['version']} is available"
                 + (f": {notes_said(u['notes'])}" if u.get("notes") else "") + f" — seq benchmark upgrade {b['name']}")
    _footer(out, len(rows), echo)


def print_benchmark_evals(out: dict, *, echo: Callable[[str], None] = print) -> None:
    """`seq eval ls --benchmark <name>`: one line per eval — when, which policy and version, on which benchmark version
    and adapter, its success rate, and the cost — then where this page sits."""
    rows = out.get("evals") or []
    if not rows:
        echo(f"no evals on {out.get('benchmark')} yet: run one with "
             f"`seq eval run <policy> --benchmark {out.get('benchmark')}`")
        return
    echo(f"{'EVAL':<8}  {'SUBMITTED':<20}  {'STATUS':<9}  {'POLICY':<22} {'BENCH':>5}  {'ADAPTER':<16} {'EPS':>4}  "
         f"{'COST':>8}  {_metric_head(rows)}")
    for e in rows:
        policy = f"{e.get('policy') or '?'}@v{_cell(e.get('model_version'))}"
        adapter = _adapter(e.get("adapter"))
        cost = "—" if e.get("cost_usd") is None else money(e["cost_usd"]) + ("" if e.get("cost_settled") else "*")
        echo(f"{e['eval_id'][:8]:<8}  {_minute(e.get('created_at')):<20}  {e['status']:<9}  {policy:<22} "
             f"{'v' + _cell(e.get('benchmark_version')):>5}  {adapter:<16} {_cell(e.get('episodes')):>4}  "
             f"{cost:>8}  {_metric(e)}" + ("  (incomplete)" if e.get("incomplete") else ""))
    if any(e.get("cost_usd") is not None and not e.get("cost_settled") for e in rows):
        echo("  * held while running; the settled cost replaces it when the eval ends")
    _footer(out, len(rows), echo)


def _adapter(a: Any) -> str:
    """The adapter as the eval ran it, {name, version, sha256} → name@vN."""
    if isinstance(a, dict):
        return f"{a.get('name') or '?'}" + (f"@v{a['version']}" if a.get("version") is not None else "")
    return "—"


def _metric(p: dict) -> str:
    """The eval's metric as `seq eval ls` and `seq benchmark ls` print it: its value alone - success the share of its
    episodes that succeeded, any other metric the benchmark's own number; which metric it is heads the column
    (_metric_head)."""
    from seq.units import UNITS, shown

    if str(p.get("status")) == "failed":
        return "Fail"
    if p.get("value") is None:
        return "—"
    return shown(p["value"], UNITS.get(p.get("metric")))


def _metric_head(rows: list[dict]) -> str:
    """The metric column's head: the metric every row with a value names - its benchmark's own word, in upper case as
    the other heads are - or METRIC where they name more than one, or none."""
    names = {r.get("metric") for r in rows if r.get("value") is not None and r.get("metric")}
    return next(iter(names)).upper() if len(names) == 1 else "METRIC"


def _footer(out: dict, shown: int, echo: Callable[[str], None]) -> None:
    """Where this page sits — "51–100 of 120", the console pager's label — and the flag that fetches the next one."""

    offset, total, nxt = out.get("offset") or 0, out.get("total") or shown, out.get("next_cursor")
    echo(f"\n{offset + 1}–{offset + shown} of {total}" + (f" — next page: --cursor {nxt}" if nxt else ""))


def _cell(v: Any) -> str:
    """A table cell: the value, or a dash where the platform has none."""
    return "—" if v is None else str(v)


def _day(iso: str | None) -> str:
    """An ISO timestamp as the day it falls on here, 2026-10-06 (seq/clock.py)."""
    return day_of(iso)


def _minute(iso: str | None) -> str:
    """An ISO timestamp to the minute on this machine's clock, with the zone: 2026-10-06 08:30 EDT (seq/clock.py)."""
    return stamp(iso, day="always")



def tasks(name: str, *, version: int | None = None, base_url: str | None = None,
          echo: Callable[[str], None] = print) -> dict:
    """`seq benchmark tasks <name>[@vN]`: a benchmark's tasks, printed - each with its description, seeds, episodes and
    time limit - under the template, channel and replay of that version."""
    out = benchmark_tasks(name, version=version, base_url=base_url)
    print_benchmark_tasks(out, echo=echo)
    return out


def print_benchmark_tasks(out: dict, *, echo: Callable[[str], None] = print) -> None:
    """One line per task - its name, its seeds, its episodes, how long one may run and what it asks (the description
    tasks={name: description} gives it) - then how many tasks and episodes in all and how an eval chooses among them.
    """
    head = (f"{out.get('benchmark')} v{_cell(out.get('version'))}: template "
            f"{template_label(out.get('template'), out.get('edited_from'))}")
    if out.get("replay"):
        head += ", records its 3D replay"
    echo(head)
    rows = out.get("tasks") or []
    width = max([len("TASK")] + [len(str(t.get("task"))) for t in rows])
    echo(f"{'TASK':<{width}}  {'SEEDS':<12} {'EPISODES':>8}  {'MAX SECONDS':>11}  DESCRIPTION")
    for t in rows:
        limit = t.get("max_seconds")
        echo(f"{str(t.get('task')):<{width}}  {_cell(t.get('seeds')):<12} {_cell(t.get('episodes')):>8}  "
             f"{(f'{float(limit):g}' if limit is not None else '—'):>11}  {t.get('description') or '—'}")
    total = sum(int(t.get("episodes") or 0) for t in rows)

    echo(f"\n{len(rows)} task{'s' if len(rows) != 1 else ''}, {total} episodes in all; an eval chooses with "
         "--tasks, then --trials (past a task's last seed, its seeds run again: repeated starts) or --seeds")


def episodes(eval_id: str, *, task: list[str] | None = None, outcome: str | None = None, arm: int | None = None,
             csv: bool = False, out: str | None = None, limit: int | None = None, cursor: str | None = None,
             base_url: str | None = None, echo: Callable[[str], None] = print) -> dict:
    """`seq eval episodes <eval_id> [--task T]... [--outcome O] [--arm N] [--csv [-o PATH]]`: one page of an eval's
    episodes, printed - or, with --csv, every episode the filters take as the platform's CSV file, the one
    `seq eval report --csv` and the console save: on stdout, or written to `out` (-o PATH)."""
    from seq.eval_cli import out_only

    out_only(csv, out)
    if csv:
        from seq._eval_gateway import EvalGatewayClient
        from seq.eval_cli import save_csv

        n = save_csv(EvalGatewayClient(base_url=base_url), eval_id, out, task=task, outcome=outcome, arm=arm)
        return {"eval_id": eval_id, "csv": out or "stdout", "episodes": n}
    out = eval_episodes(eval_id, task=task, outcome=outcome, arm=arm, limit=limit or PAGE, cursor=cursor,
                        base_url=base_url)
    print_episodes(out, echo=echo)
    return out


def _result(e: dict) -> str:
    """How an episode ended: an error, out of time, at its time limit, or ended by the benchmark (done)."""
    if e.get("error"):
        return "error"
    if e.get("timed_out"):
        return "timed out"
    return "truncated" if e.get("truncated") else "ended"


def _answer(v: Any) -> bool:
    """Whether one episode's value is a success's answer - true or false, 1 or 0 - rather than a measure."""
    return isinstance(v, bool) or (isinstance(v, (int, float)) and v in (0, 1))


def _value(v: Any) -> str:
    """One episode's value of a metric - the benchmark's own number, which declares no unit: yes or no for a true or
    false, else the number as it is."""
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f"{v:.4g}"
    return str(v)


def _succeeded(e: dict) -> str:
    """Whether an episode succeeded, as the benchmark's @seq.step said of its last step: yes, no, or — (it errored)."""
    return {True: "yes", False: "no"}.get(e.get("success"), "—")


def print_episodes(out: dict, *, echo: Callable[[str], None] = print) -> None:
    """One line per episode - its task and seed, its steps, the seconds it ran on the robot's clock and the steps it
    paused waiting for an answer, how it ended, whether it succeeded and every other metric its steps returned - then
    where this page sits. A `success` metric is left out when its every value is a success's answer (1 or 0, true or
    false) beside SUCCEEDED, which says each then."""
    rows = out.get("episodes") or []
    if not rows:
        echo("no episode of this eval matches yet: none has reported, or none passes the filters")
        return
    keys = sorted({k for e in rows for k in (e.get("metrics") or {})})
    had = [e for e in rows if (e.get("metrics") or {}).get("success") is not None]
    if "success" in keys and all(_answer(e["metrics"]["success"]) and isinstance(e.get("success"), bool) for e in had):
        keys.remove("success")
    arms = any(e.get("arm") for e in rows)
    again = any(e.get("repeat") for e in rows)
    width = max([len("TASK")] + [len(str(e.get("task"))) for e in rows])
    echo(f"{'#':>5}  " + ("ARM  " if arms else "") + f"{'TASK':<{width}}  {'SEED':>6}  "
         + (f"{'REPEAT':>6}  " if again else "") + f"{'STEPS':>6}  {'SECONDS':>7}  {'PAUSED':>6}  "
         f"{'ENDED':<9}  {'SUCCEEDED':<9}" + "".join(f"  {k}" for k in keys))
    for e in rows:
        seconds = "—" if e.get("seconds") is None else f"{float(e['seconds']):.1f}"
        echo(f"{_cell(e.get('index')):>5}  " + (f"{_cell(e.get('arm')):>3}  " if arms else "")
             + f"{str(e.get('task')):<{width}}  {_cell(e.get('seed')):>6}  "
             + (f"{_cell(e.get('repeat')):>6}  " if again else "")
             + f"{_cell(e.get('steps')):>6}  {seconds:>7}  {_cell(e.get('paused')):>6}  {_result(e):<9}  "
             f"{_succeeded(e):<9}" + "".join(f"  {_value((e.get('metrics') or {}).get(k))}" for k in keys))
    _footer(out, len(rows), echo)

