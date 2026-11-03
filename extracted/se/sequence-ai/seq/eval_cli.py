"""
`seq eval run`, `seq eval status`, `seq eval report` and `seq eval cancel`: start an eval on the platform, wait for it,
print and export what it found.

In one sentence: the CLI posts the eval — its scope, its spend cap, how it is laid out on cards (policy and benchmark
machines, their cards, environments per benchmark machine), and its arms (every combination of swept parameter values
with --sweep), or the errored episodes of an earlier one to run again → polls the report → prints the benchmark's own
metrics, each with its n, the run's manifest from `/v1/eval/{id}/details` and a table per arm → `--gate` turns the
result into an exit code for CI, and `seq eval report --csv [-o PATH]` gives one row per episode. When the account is short of GPUs the
platform puts the whole eval in line (up to 10 minutes, nothing held or billed) and the CLI says what it waits for;
`--dry-run` prints the card report the real submit acts on, and `seq eval status <id>` shows the wait.

WHY a sweep's arms run in one eval: the platform runs every arm on the same episodes (task, seed) side by side, so their tables need no second run and no matching across evals. Another policy is an eval of its own (the user
10-19 had --compare taken out).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import operator
import os
import re
import sys
import time
from typing import Any, Callable

from sequence_ai.errors import InvalidRequest, SequencesError, Unavailable

from sequence_ai._core.money import money
from seq.units import UNITS, shown



GATE_FAILED = 8
_GATE = re.compile(r"^\s*([A-Za-z0-9_./:-]+?)\s*(>=|<=|==|>|<)\s*(-?\d+(?:\.\d*)?(?:[eE]-?\d+)?)\s*$")
_OPS = {">=": operator.ge, "<=": operator.le, ">": operator.gt, "<": operator.lt, "==": operator.eq}


def add_arguments(p_eval: argparse.ArgumentParser, p_report: argparse.ArgumentParser) -> None:
    p_eval.add_argument("--tasks", default=None,
                        help="only these of the benchmark's tasks, comma-separated (`seq benchmark tasks <name>` "
                             "lists them; default: every task)")
    p_eval.add_argument("--seeds", default=None, metavar="SEEDS",
                        help="which of each task's seeds run, instead of --trials' first N: 10-19 or 0,4,10-19 for "
                             "every chosen task, or per task: libero_spatial/3=10-19,libero_spatial/7=0,4 ('*' for "
                             "the rest)")
    p_eval.add_argument("--spend-cap", type=float, default=None, metavar="USD",
                        help="the eval's spend cap: it stops once its machines (GPU, CPU and memory) have cost this "
                             "much, and the report covers what ran")
    p_eval.add_argument("--rerun-failed", default=None, metavar="EVAL_ID",
                        help="run only the episodes that errored in that eval again; the report "
                             "covers both runs")
    p_eval.add_argument("--rerun-unsuccessful", default=None, metavar="EVAL_ID",
                        help="run the episodes that eval ran without error and did not succeed on again, as an eval "
                             "of their own; never merged into its report")
    p_eval.add_argument("--gate", action="append", default=None, metavar="METRIC>=X",
                        help="exit 8 unless the completed eval's overall METRIC passes (repeatable; with --no-wait "
                             "none is checked)")
    p_eval.add_argument("--param", action="append", default=None, metavar="[SIDE.]NAME=VALUE",
                        help="set a parameter for the whole eval (repeatable): the policy's @seq.infer, the "
                             "adapter's __init__, the benchmark's __init__, or the eval's own max_seconds (how long "
                             "an episode may run on the robot's clock; an eval that changes it is not a standard one) "
                             "- policy.replan_steps=3, adapter.image_size=128, benchmark.noise_std=0, "
                             "eval.max_seconds=20; the bare name when only one side declares it")
    p_eval.add_argument("--sweep", action="append", default=None, metavar="[SIDE.]NAME=V1,V2,...",
                        help="an arm per value of any parameter --param sets, run side by side in one eval "
                             "(repeatable: every combination is an arm)")

    p_eval.add_argument("--replay", default=None, choices=("3d", "none"),
                        help="whether the eval records its 3D replay when the benchmark declares replay= - 3d, every "
                             "episode, drawn in the console after the eval; none, no replay (default: the platform's, "
                             "which the report says)")
    p_report.add_argument("--csv", action="store_true",
                          help="the eval's episodes as CSV, a row per episode - the file the console downloads - "
                               "printed in place of the report, or written to -o PATH beside it")
    p_report.add_argument("-o", "--out", default=None, metavar="PATH", help="with --csv: the file to write it to")
    p_report.add_argument("--records", default=None, metavar="DIR",
                          help="save every episode's record - what its policy was sent, its cameras as video, and "
                               "each answer (.rec.zst) - into DIR")
    p_report.add_argument("--replays", default=None, metavar="DIR",
                          help="save every episode's 3D replay (.seqreplay) and the scenes they are drawn in "
                               "(scenes/<sha256>.glb) into DIR")


def parse_value(text: str) -> int | float | bool | str:
    """A parameter value as typed: true/false, an int, a float, else the text itself (the worker casts it to the
    declared type and refuses what does not fit)."""
    low = text.strip().lower()
    if low in ("true", "false"):
        return low == "true"
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


def parse_param(text: str) -> tuple[str, int | float | bool | str]:
    """`replan_steps=3` or `adapter.image_size=128` → (the key as written, its value); which side a bare name belongs
    to, and whether that side declares it, is the platform's to decide (it knows every side's declarations)."""
    from seq.params import split

    name, sep, value = (text or "").partition("=")
    try:
        split(name)
    except ValueError:
        sep = ""
    if not sep:
        raise ValueError(f"{text!r} is not NAME=VALUE or SIDE.NAME=VALUE, SIDE one of policy / adapter / benchmark / "
                         "eval (e.g. replan_steps=3, adapter.image_size=128, eval.max_seconds=20)")
    return name.strip(), parse_value(value)


def parse_sweep(text: str) -> tuple[str, list]:
    name, value = parse_param(text)
    values = [parse_value(v) for v in str(text.partition("=")[2]).split(",") if v.strip()]
    if len(values) < 2:
        raise ValueError(f"{text!r}: a sweep needs at least two values (NAME=V1,V2)")
    return name, values



def eval_remote(args: argparse.Namespace) -> int:
    """POST /v1/eval for a deployed policy on a registered benchmark, then (default) wait for the report. Every arm —
    each combination of swept parameter values (--sweep) — runs side by side in this one eval, on the same episodes;
    the report has a table per arm."""
    from seq._eval_gateway import EvalGatewayClient

    from seq import selection


    chosen = {"tasks": selection.tasks_value(args.tasks),
              "trials": selection.parse_trials(args.trials) if args.trials is not None else None,
              "seeds": selection.parse_seeds(args.seeds) if args.seeds is not None else None}
    try:
        gates = [parse_gate(g) for g in args.gate or []]
        params = dict(parse_param(p) for p in args.param or []) or None
        sweep = dict(parse_sweep(x) for x in args.sweep or []) or None
    except ValueError as exc:
        raise InvalidRequest(f"--gate / --param / --sweep: {exc}") from None
    if gates and not args.wait:

        raise InvalidRequest("--gate checks the eval once it has finished; it takes no --no-wait")
    if sweep and args.rerun_failed:
        raise InvalidRequest("--rerun-failed repeats one eval's errored episodes; it takes no --sweep")
    if args.rerun_unsuccessful and (args.rerun_failed or sweep):
        raise InvalidRequest("--rerun-unsuccessful runs one eval's unsuccessful episodes as an eval of their own; it "
                             "takes no --rerun-failed or --sweep")
    from seq.eval import at_least_one

    at_least_one(("--policy-machines", args.policy_machines), ("--benchmark-machines", args.benchmark_machines))
    from seq import adapter_cli


    adapter = adapter_cli.resolve(args.adapter, base_url=args.base_url,
                                  echo=(lambda _line: None) if args.json else print)


    body = {"model": args.policy, "benchmark": args.benchmark, "adapter": adapter, **chosen,
            **({"policy": args.member} if getattr(args, "member", None) else {}),
            "dry_run": args.dry_run or None,
            "spend_cap_usd": args.spend_cap, "rerun_of": args.rerun_failed, "params": params,
            "rerun_unsuccessful_of": args.rerun_unsuccessful, "replay": args.replay, "sweep": sweep,


            "policy_machines": args.policy_machines, "benchmark_machines": args.benchmark_machines}
    client = EvalGatewayClient(base_url=args.base_url)
    started = client.start_eval(body)
    if args.dry_run:
        if args.json:
            print(json.dumps(started, indent=2, default=str))
        else:
            print_dry_run(started)
        return 0
    eval_id = started["eval_id"]
    _say_started(eval_id, started)
    if not args.wait:
        print(f"read it with: seq eval report {eval_id} --wait   stop it with: seq eval cancel {eval_id}")
        return 0

    report, details = _finished(client, eval_id, math.inf)
    print_report(report, details, earlier_cost=earlier_cost(client, details), eval_id=eval_id)
    rc = 0 if report.status.value == "completed" else 1
    if gates:
        rc = rc or check_gates(report, gates)
    return rc


def eval_cancel(eval_id: str, *, base_url: str | None = None, echo: Callable[[str], Any] | None = None) -> dict:
    """POST /v1/eval/{id}/cancel: no new episodes; the machines stop within a minute; what ran is billed and reported.
    Returns the platform's answer, {eval_id, status}: "canceling" while the machines stop. Says its line only when
    given `echo`."""
    from seq._eval_gateway import EvalGatewayClient

    out = EvalGatewayClient(base_url=base_url).cancel(eval_id)
    if echo is not None:
        echo(f"eval {out.get('eval_id')}: {out.get('status')}")
    return out


def eval_rm(eval_ids: str | list[str], *, base_url: str | None = None,
            echo: Callable[[str], Any] | None = None) -> dict:
    """DELETE /v1/eval/{id}, each id in turn: ended evals deleted for good - their reports, episodes and recordings -
    as the console's Eval runs tab deletes them; a queued or running one is refused (cancel it first), and the ones
    before it stay deleted. Returns {"deleted": [ids]}."""
    from seq.deployments_cli import _call
    from sequence_ai._core.names import segment

    gone: list[str] = []
    for eid in [eval_ids] if isinstance(eval_ids, str) else list(eval_ids):
        out = _call("DELETE", f"/v1/eval/{segment(eid, 'eval id')}", base_url) or {}
        gone.append(out.get("deleted") or eid)
        if echo is not None:
            echo(f"eval {gone[-1]}: deleted, with its report, episodes and recordings")
    return {"deleted": gone}


def cancel(args: argparse.Namespace) -> int:
    """`seq eval cancel <id>`: eval_cancel, its line printed - or, with `seq --json`, the platform's answer, as every
    command with a JSON form prints what it read (it printed the line under `--json` too).
    """
    out = eval_cancel(args.eval_id, base_url=args.base_url, echo=None if args.json else print)
    if args.json:
        print(json.dumps(out, indent=2, default=str))
    return 0


def _estimate(started: dict) -> str:
    est = started.get("estimate") or {}
    cards = int(started.get("gpus_granted") or ((started.get("layout") or {}).get("cards") or {}).get("total")
                or (started.get("cards") or {}).get("total") or 0)
    guess = " (a first guess: nothing of this benchmark has been measured yet)" if est.get("default_timing") else ""
    return (f"~{float(est.get('wall_clock_s') or 0):.0f}s, ~{money(est.get('cost_usd'))} on {cards} "
            f"card{'s' if cards != 1 else ''}{guess}")



_ESTIMATED = {"forward": "the policy's time for a batch", "network": "an act's network time"}


def fastest_line(fastest: dict | None, *, arms: int = 1) -> None:
    """The fastest layout within the account's GPUs, as the platform worked it out (gateway eval/basis.py fastest) and
    said as it is: the benchmark machines (and the worlds each runs, the platform's own), the policy machines, the GPUs
    of the limit, the time and the cost, and the flags that run it - beside what no measurement gave. Nothing where the
    platform sends none: a CPU benchmark, or an unmeasured one.
    
"""
    if not fastest:
        return
    bench, policy, worlds = fastest["benchmark_machines"], fastest["policy_machines"], fastest.get("worlds")
    guessed = [_ESTIMATED.get(k, k) for k in fastest.get("estimated") or []]
    print(f"fastest: {bench} benchmark machine{'s' if bench != 1 else ''}{' per arm' if arms > 1 else ''}"
          + (f" x {worlds} world{'s' if worlds != 1 else ''}" if worlds else "")
          + f" + {policy} policy machine{'s' if policy != 1 else ''}, "
          f"{fastest['cards']} of your {fastest['limit']} GPUs: ~{float(fastest['wall_clock_s']):.0f}s, "
          f"~{money(fastest['cost_usd'])}" + (f" (estimated: {', '.join(guessed)})" if guessed else ""))
    print(f"  --benchmark-machines {bench} --policy-machines {policy}")


def parts_lines(parts: dict | None) -> None:
    """The estimate's cost by machine and by what it is billed for - GPU, CPU, memory - each the whole eval's, as the
    platform worked it out (gateway eval/estimate.py burn_parts): a line for the policy machines and one for the
    benchmark machines - and a composite eval's planner, its containers on those machines - a part with nothing in it
    left out (a CPU machine has no GPU)."""
    for role, label in (("policy", "policy machines"), ("benchmark", "benchmark machines"), ("planner", "planner")):
        kinds = (parts or {}).get(role)
        if not kinds:
            continue
        said = [f"{name} ~{money(kinds[kind])}" for kind, name in (("gpu", "GPU"), ("cpu", "CPU"), ("memory", "memory"))
                if kinds.get(kind)]
        print(f"  {label}: {', '.join(said) or '~$0.00'}")


def about_time(seconds) -> str:
    """A time as the dry run says it: seconds under a minute and a half, else whole minutes."""
    s = float(seconds or 0)
    return f"{s:.0f} s" if s < 90 else f"{s / 60:.0f} min"


def _held(started: dict) -> float | None:
    """What a real run holds from the balance, when the platform says it differs from the estimate (the hold adds a
    reserve, and prices a benchmark that names several cards on its costliest); None when it is the estimate."""
    held = (started.get("estimate") or {}).get("held_usd")
    return float(held) if held is not None else None


_FROM = {"cli": "set", "policy": "policy's default", "adapter": "adapter's default",
         "benchmark": "benchmark's default", "platform": "platform's default",
         "deployment": "deployment's default"}


def params_line(settings: dict) -> str:
    """An arm's parameters, side by side — `policy.replan_steps=5 (policy's default) · eval.max_seconds=20 (set)` —
    each with where its value came from."""
    cells = []
    for side in ("policy", "adapter", "benchmark", "eval"):
        for name, used in (settings.get(side) or {}).items():
            used = used if isinstance(used, dict) else used.model_dump()
            cells.append(f"{side}.{name}={used.get('value')!r} ({_FROM.get(used.get('source'), used.get('source'))})")
    return " · ".join(cells) or "none declared"


def print_dry_run(started: dict) -> None:
    """The dry run: what would run (your numbers, or the fixed defaults), the cards against the account, the estimate
    and any hints. Nothing was started or held."""
    lay = started["layout"]
    for g in lay.get("policy") or []:



        print(f"policy: {g['model']} x {g['machines']} machine(s) on " + ("CPU" if g["gpu"] == "cpu" else str(g["gpu"]))
              + (f" ({g['cards_each']} cards each)" if int(g.get("cards_each") or 1) > 1 else ""))
    planner = lay.get("planner")
    if planner:

        print(f"planner: {planner['name']} plans for {planner['policy']} every {planner['every_s']:g} s of each "
              f"episode, on CPU beside it")
    b = lay.get("benchmark") or {}


    worlds = f", {b['worlds']} world{'s' if b['worlds'] != 1 else ''} each" if b.get("worlds") else ""
    if b:
        print(f"benchmark: {b.get('machines_per_arm')} machine(s) per arm on "
              + ("CPU" if b.get("gpu") == "cpu" else str(b.get("gpu")))
              + (f" (then {', '.join(b['fallback'])})" if b.get("fallback") else "") + worlds)
    arms = lay.get("arms") or []
    if len(arms) > 1:
        for a in arms:
            print(f"  arm {a['arm']}: {a['model']}" + (f" {a['params']}" if a.get("params") else ""))
    for a in arms:
        if a.get("settings"):
            print(("params: " if len(arms) == 1 else f"params, arm {a['arm']}: ") + params_line(a["settings"]))
    print_selection(lay["selection"], arms=len(arms) or 1)
    print_cards(started.get("cards"))


    est = started.get("estimate") or {}
    print(f"cost: about {money(est.get('cost_usd'))}")
    held = _held(started)
    if held is not None:
        print(f"      up to {money(held)} held")
    parts_lines(started.get("cost_parts"))


    calls = (est.get("breakdown") or {}).get("planner_calls_usd")
    if calls:
        print(f"  model calls: ~{money(calls)} (up to {int(est.get('vlm_calls') or 0)} plans)")
    print(f"time: about {about_time(est.get('wall_clock_s'))}")
    slow = started.get("wall_clock_slow_s")
    if slow and float(slow) > float(est.get("wall_clock_s") or 0):
        print(f"      up to {about_time(slow)} when GPUs are slow to come")
    fastest_line(started.get("fastest"), arms=len(arms))
    print_notes(started)
    print_warnings(started)


def print_notes(started: dict) -> None:
    """The platform's hints on the eval, its dry run's and its start's alike - a policy that takes one episode at a
    time (no @seq.concurrent) has the episodes wait their turn, and what more policy machines would take
."""
    for n in started.get("notes") or []:
        print(f"note: {n}")


    up = started.get("benchmark_upgrade")
    if up:
        print(f"upgrade: seq benchmark upgrade {up['benchmark']} ({up['template']} "
              + (f"{up['from']} → " if up.get("from") else "") + f"{up['to']})")


def print_warnings(started: dict) -> None:
    """What the platform says will not fit between the policy and the benchmark - the eval starts all the same
 - each with the adapter to run it with; one that stops the eval at its first act if they really do not
    fit says what that costs: its machines' start."""
    for w in started.get("warnings") or []:
        print(f"warning: {w.get('sentence')}")
        if w.get("stops") and w.get("start_usd") is not None:
            print("  if they do not fit, the eval stops at its first act: "
                  f"~{money(w['start_usd'])}, its machines' start")



_SHOWN_TASKS = 12


def print_selection(picked: dict, *, arms: int = 1) -> None:
    """Which episodes run (a dry run's layout.selection): how many, each chosen task's seeds and episodes - the first
    twelve tasks, then how many more - and each arm's time limit beside the benchmark's own.

    {the user 10-17: "each task how many trials and also the seed and aslo total eps"}"""
    tasks = picked.get("tasks") or []
    n = int(picked.get("episodes") or 0)
    head = f"episodes: {n} ({len(tasks)} task{'s' if len(tasks) != 1 else ''})"
    print(head + (f" per arm, {n * arms} in all over {arms} arms" if arms > 1 else ""))
    for t in tasks[:_SHOWN_TASKS]:
        many, again = int(t.get("episodes") or 0), int(t.get("repeats") or 0)
        print(f"  {t.get('task')}: seeds {t.get('seeds')}, {many} episode{'s' if many != 1 else ''}"
              + (f", {again} of them repeated starts" if again else ""))
    if len(tasks) > _SHOWN_TASKS:
        print(f"  ... and {len(tasks) - _SHOWN_TASKS} more tasks (`seq --json eval run ... --dry-run` lists them all)")


    again = int(picked.get("repeats") or 0)
    if again:
        print(f"repeated starts: {again} episode{'s' if again != 1 else ''} run a start again - not a standard eval, "
              "so its success rates do not compare with standard runs'")
    limit_lines(picked.get("max_seconds"))


def limit_lines(limits: dict | None, *, echo: Callable[[str], Any] = print) -> None:
    """Each arm's time limit beside the benchmark's, as the dry run's layout.selection and /details both give it:
    {"default", "arms": [{"arm", "value", "standard"}]}; the arm is named when there are several."""
    arms = (limits or {}).get("arms") or []
    for a in arms:
        seconds_line({"value": a.get("value"), "default": limits.get("default"), "standard": a.get("standard")},
                     arm=a.get("arm") if len(arms) > 1 else None, echo=echo)


def repeats_lines(repeats: dict | None, *, echo: Callable[[str], Any] = print) -> None:
    """The episodes that ran a start again (/details' repeats): how many - not a standard eval - and the starts run more
    than once by their success rate, as the report page draws them."""
    again = int((repeats or {}).get("episodes") or 0)
    if not again:
        return
    echo(f"repeated starts: {again} episode{'s' if again != 1 else ''} ran a start again (not a standard eval)")
    starts, dist = repeats.get("starts") or [], repeats.get("distribution") or []
    if starts:
        rates = ", ".join(f"{shown(float(d.get('rate') or 0), 'rate')} ({d.get('starts')} start"
                          f"{'s' if d.get('starts') != 1 else ''})" for d in dist)

        by = f", by {repeats['metric']} rate" if repeats.get("metric") else ""
        echo(f"  the {len(starts)} start{'s' if len(starts) != 1 else ''} run more than once{by}: {rates}")


def seconds_line(limit: dict | None, *, arm: int | None = None, echo: Callable[[str], Any] = print) -> None:
    """How long an episode may run on the robot's clock, beside the benchmark's own: an eval that changes it is not a
    standard one, and its success rates do not compare with standard runs'.
"""
    if not limit or limit.get("value") is None:
        return
    where = f" (arm {arm})" if arm is not None else ""
    if limit.get("standard", limit.get("value") == limit.get("default")):
        echo(f"max seconds: {limit['value']}{where}, the benchmark's default")
    else:
        echo(f"max seconds: {limit['value']}{where} this run, the benchmark's default {limit.get('default')}: not a "
             "standard eval, so its success rates do not compare with standard runs'")


def print_cards(cards: dict | None) -> None:
    """The dry run's card report — the same check a real submit runs: both sides' machines × cards each, the total
    against the account's limit and what serving and evals hold now, what is free, how many are short and why, and
    whether a real submit would wait in line. A count the platform could not read says unknown, never full.
    """
    from sequence_ai._core.capacity import count, held

    if not cards:
        return
    sides = []
    for side in ("policy", "benchmark"):
        g = cards.get(side) or {}
        each = g.get("cards_each")
        if g.get("gpu") == "cpu":
            sides.append(f"{side} {count(g.get('machines'))} × CPU machine (no GPU)")
            continue
        sides.append(f"{side} {count(g.get('machines'))} × {g.get('gpu')}"
                     + (f" ({each} cards each)" if isinstance(each, int) and each > 1 else ""))
    print(f"cards: {' + '.join(sides)} = {count(cards.get('total'))} GPUs at once")
    print(f"  your account: limit {count(cards.get('limit'))}, in use {held(cards.get('in_use'))}, "
          f"{count(cards.get('available'))} available")
    reason, wait = cards.get("reason"), cards.get("queue_timeout_s") or 600
    if reason is None:
        print("  fits: no wait for GPUs")
    elif reason == "gpu_limit_reached" and not cards.get("would_queue"):
        print(f"  never fits: {count(cards.get('total'))} at once is more than your account's limit — lay it out on "
              "fewer --policy-machines / --benchmark-machines")
    else:
        why = {"gpu_limit_reached": "your account's GPUs are in use", "gpu_busy": "the platform's GPUs are all busy",
               "gpu_low_stock": "the card is out of stock"}.get(reason, reason)
        print(f"  {count(cards.get('short'))} short ({why}, {reason})"
              + (f": submitted, it would wait in line up to {wait:.0f} s for them, then fail (queue_timeout)"
                 if cards.get("would_queue") else ": submitted, it would be refused"))


def _say_started(eval_id: str, started: dict) -> None:
    """One line for a submitted eval: started, or in line for the account's GPUs (what it needs, what is free, when it
    gives up)."""
    queue = started.get("queue")
    if queue or started.get("status") == "queued":
        est = started.get("estimate") or {}
        print(f"queued: eval {eval_id} (~{float(est.get('wall_clock_s') or 0):.0f}s, "
              f"~{money(est.get('cost_usd'))}) waits for {queued_for(queue or {})} — {queue_line(queue or {})}")
        print_notes(started)
        print_warnings(started)
        return
    held = _held(started)
    print(f"started: eval {eval_id} ({_estimate(started)}; "
          + (f"{money(held)} is held against this month's limit" if held is not None
             else "the estimate is held against this month's limit")
          + ", the time your machines actually run is what you pay)")
    print_notes(started)
    print_warnings(started)


def queued_for(queue: dict) -> str:
    """What a queued eval is in line for: the account's GPUs, or its compute, held for its spend limit (reason
    "account_held")."""
    return "compute" if queue.get("reason") == "account_held" else "GPUs"


def queue_line(queue: dict) -> str:
    """What a queued eval waits for and when it is expected to clear. For GPUs: 'needs 5 GPUs, 2 free now; waited 42 s;
    gives up at 17:10 EDT'. For its compute held on a spend limit: 'waiting for compute to free up; expected back by
    17:10 EDT; gives up at 17:40 EDT' (or 'expected time not known yet' when the platform cannot say). Nothing is held
    or billed while it waits; it starts on its own when the wait clears."""
    from sequence_ai._core.capacity import count

    waited = queue.get("waited_s")
    if queue.get("reason") == "account_held":

        parts = ["waiting for compute to free up"]
        parts.append(f"expected back by {_clock(queue['expected_at'])}" if queue.get("expected_at")
                     else "expected time not known yet")
    else:
        parts = [f"needs {count(queue.get('cards'))} GPUs, {count(queue.get('available'))} available now"]
    if isinstance(waited, (int, float)) and waited:
        parts.append(f"waited {waited:.0f} s")
    if queue.get("gives_up_at"):
        parts.append(f"gives up at {_clock(queue['gives_up_at'])}")
    clears = "the hold lifts" if queue.get("reason") == "account_held" else "they free up"
    return "; ".join(parts) + f" (it starts on its own when {clears}; nothing is held or billed meanwhile)"


def _clock(at: str) -> str:
    """'2026-10-03T21:10:00+00:00' → '17:10 EDT' on this machine's clock (the date too when it is not today here)."""
    from seq.clock import stamp

    return stamp(at)



def eval_status(eval_id: str, *, watch: bool = False, every: float | None = None, base_url: str | None = None,
                echo: Callable[[str], Any] | None = None) -> dict:
    """Where an eval is — in line for GPUs (what it needs, what is free, how long it has waited, when it gives up),
    running, or ended — and how far it has got: episodes done of the total (per arm when it has several) and every
    metric so far with its mean and n. Returns it as `seq --json eval status` prints it: {eval_id, status, queue,
    progress, incomplete, errors, time_limit, units, and before its first episode starting, what it waits on}. `watch` reads
    it again every `every` seconds (5, and at least 1)
    until the eval ends, and returns what it read last. Says each reading when it moved, only when given `echo`.

    
"""
    from seq._eval_gateway import EVAL_TERMINAL, EvalGatewayClient

    client = EvalGatewayClient(base_url=base_url)
    shown = None
    while True:
        report = client.report(eval_id)
        state = report.status.value



        try:
            details = client.details(eval_id)
        except SequencesError:
            details = {}
        snap = {"eval_id": eval_id, "status": state, "queue": details.get("queue") if state == "queued" else None,
                "progress": details.get("progress"), "incomplete": report.incomplete, "errors": report.errors,
                "time_limit": details.get("time_limit"), "units": UNITS,
                **({"starting": details["starting"]} if details.get("starting") else {})}
        waits = snap.get("starting") or {}
        moved = (state, *(((snap["progress"] or {}).get(k) for k in ("done", "running", "pending"))),
                 (snap["time_limit"] or {}).get("note"), waits.get("what"),
                 int(waits.get("since_s") or 0) // STARTING_AGAIN_S)
        if echo is not None and moved != shown:
            print_status(snap, echo=echo)
        shown = moved
        if not watch or state in EVAL_TERMINAL:
            break
        time.sleep(max(1.0, float(every or 5.0)))
    return snap


def status(args: argparse.Namespace) -> int:
    """`seq eval status <id> [--watch [--every S]]`: eval_status, printed - with --json, what it read last; exit 1 for
    an eval that failed."""
    snap = eval_status(args.eval_id, watch=getattr(args, "watch", False), every=getattr(args, "every", None),
                       base_url=args.base_url, echo=None if args.json else print)
    if args.json:
        print(json.dumps(snap, indent=2, default=str))
    return 1 if snap["status"] == "failed" else 0


def print_status(snap: dict, *, echo: Callable[[str], Any] = print) -> None:
    """One status: the line — state, then episodes done of the total and what the rest are doing — and under it each
    metric so far, per arm when there are several. An ended eval that did not complete says its results are partial;
    the report keeps every episode that ran."""
    eid, state, p = snap["eval_id"], snap["status"], snap.get("progress")
    if state == "queued":
        q = snap.get("queue") or {}
        echo(f"eval {eid}: queued for {queued_for(q)} — {queue_line(q)}")
        return
    if not p or not p.get("total"):

        if state == "completed":
            echo(f"eval {eid}: completed — `seq eval report {eid}` prints it")
        elif state == "failed":
            echo(f"eval {eid}: failed — " + ("; ".join(snap.get("errors") or []) or f"`seq eval report {eid}`"))
        else:
            echo(f"eval {eid}: {state}")
        return
    done = f"{p['done']} / {p['total']} episodes done{progress_counts(p)}"
    if state == "completed":
        echo(f"eval {eid}: completed — {done} — `seq eval report {eid}` prints it")
    elif state in ("failed", "canceled"):
        echo(f"eval {eid}: {state} — partial results: {done}; the report keeps what ran")
    else:
        echo(f"eval {eid}: {state} — {done}")
        if (starting := starting_said(snap)) is not None:
            echo(f"  {starting}")
    arms = p.get("arms") or []
    for a in arms:
        indent = "  "
        if len(arms) > 1:
            label = a["model"] + "".join(f" {k}={v}" for k, v in (a.get("params") or {}).items())
            echo(f"  arm {a['arm']} {label}: {a['done']} / {a['total']}{progress_counts(a)}")
            indent = "    "
        for key, m in (a.get("means") or {}).items():
            echo(f"{indent}{key}: {shown(m['mean'], (snap.get('units') or {}).get(key))} (n={m['n']})")
    if state == "failed":
        for e in snap.get("errors") or []:
            echo(f"  error: {e}")
    time_note(snap.get("time_limit"), echo)


def starting_said(snap: dict | None) -> str | None:
    """The platform's word on what an eval waits on before its first episode - a card, its machine's start, its benchmark's -
    and about how long is left (gateway eval/machine_start.view), printed as it comes; None once an episode has begun.
    """
    starting = (snap or {}).get("starting")
    said = starting.get("sentence") if isinstance(starting, dict) else None
    return said if isinstance(said, str) and said else None


def start_said(timing: Any) -> str | None:
    """The report's word on its machines' start: its wait for a card, which is not billed, and its machines' own - their
    boot, image and weights - billed as the rest of their time, each as long as the longest of its machines'; None when it
    had neither.
"""
    cold = getattr(timing, "cold_start_s", None) or {}
    parts = [(f"waited {about_time(cold['card_wait_s'])} for a card (not billed)") if cold.get("card_wait_s") else None,
             (f"its machines took {about_time(cold['machine_start_s'])} to start (billed)")
             if cold.get("machine_start_s") else None]
    said = [p for p in parts if p]
    return f"before its first episode: {', '.join(said)}" if said else None


def time_note(limit: dict | None, echo: Callable[[str], Any] = print) -> None:
    """The platform's word on an eval's time limit, when it has one: that its pace moved the limit on within its spend
    cap, or that it will not finish by it (gateway runtime.time_view).
 
"""
    note = (limit or {}).get("note")
    if note:
        echo(f"  time limit: {note}")


def progress_counts(p: dict) -> str:
    """' (1 failed, 4 running, 24 pending, 28 not run)': what the episodes not cleanly done are doing — only the states
    that have any, each in the platform's word for it (its progress keys), none of the CLI's own.
"""
    parts = [f"{p[k]} {label}" for k, label in (("failed", "failed"), ("running", "running"), ("pending", "pending"),
                                                ("not_run", "not run")) if p.get(k)]
    return f" ({', '.join(parts)})" if parts else ""


STARTING_AGAIN_S = 120


def _live(line: str) -> None:
    """A wait's progress line, flushed: on a pipe too it appears as it happens."""
    print(line, flush=True)


def _finished(client: Any, eval_id: str, timeout: float | None, *,
              echo: Callable[[str], Any] | None = _live) -> tuple[Any, dict]:
    """The finished report and its details. One still running at the deadline is Unavailable (`timeout`): it was not
    abandoned, and the hint says how to read it later. Each state it passes is said through `echo` (and a platform it
    loses and asks again, on stderr); with None nothing is said."""
    from seq._eval_gateway import EVAL_WAIT_S

    from seq._eval_gateway import EVAL_TERMINAL

    seen: list[tuple] = []
    noted: list[str] = []

    def _show(rep: Any) -> None:
        state, done, limit, waits = rep.status.value, None, None, None
        line = f"  eval {eval_id}: {state}"
        try:
            if state == "queued":
                queue = client.details(eval_id).get("queue") or {}
                line += f" for {queued_for(queue)} — {queue_line(queue)}"
            elif state == "running":

                d = client.details(eval_id)
                p, limit = d.get("progress") or {}, d.get("time_limit")
                if p.get("total"):
                    done = p["done"]
                    line += f" — {p['done']} / {p['total']} episodes done{progress_counts(p)}"

                if (starting := starting_said(d)) is not None:
                    line += f" — {starting}"
                    waits = (d["starting"].get("what"), int(d["starting"].get("since_s") or 0) // STARTING_AGAIN_S)
        except SequencesError:
            pass
        if not seen or seen[-1] != (state, done, waits):
            seen.append((state, done, waits))
            echo(line)

        note = (limit or {}).get("note")
        if note and (not noted or noted[-1] != note):
            noted.append(note)
            time_note(limit, echo)

    said = echo is not None
    report = client.wait_report(eval_id, timeout_s=timeout or EVAL_WAIT_S, on_poll=_show if said else None,
                                on_retry=lost_line if said else None)
    if report.status.value not in EVAL_TERMINAL:
        raise Unavailable(f"eval {eval_id} is still running after the wait window", code="timeout",
                          details={"state": report.status.value}, hint=f"seq eval report {eval_id} --wait")
    return report, client.patiently(lambda: client.details(eval_id), on_retry=lost_line if said else None,
                                    going_on=f"eval {eval_id} is done on the platform",
                                    hint=f"seq eval report {eval_id}")


def lost_line(exc: SequencesError, pause: float) -> None:
    """A wait's word that it lost the platform and asks again, on stderr beside the progress it interrupts."""
    print(f"  {exc.message} — asking again in {pause:.0f}s", file=sys.stderr, flush=True)



def _read_report(client: Any, eval_id: str, wait: bool, timeout: float | None,
                 echo: Callable[[str], Any] | None) -> tuple[Any, dict]:
    """The eval's report and its details: as they stand, or - `wait` - once it has ended, each state it passes said
    through `echo` (_finished)."""
    if wait:
        return _finished(client, eval_id, timeout, echo=echo)
    return client.report(eval_id), client.details(eval_id)


def _report_data(rep: Any, details: dict) -> dict:
    """The report and its details as `seq --json eval report` prints them."""
    return {"report": rep.model_dump(mode="json"), "details": details}


def eval_report(eval_id: str, *, wait: bool = False, timeout_s: float | None = None, base_url: str | None = None,
                echo: Callable[[str], Any] | None = None) -> dict:
    """An eval's report, with its details: {"report": the benchmark's own metrics overall and per task with the cost and
    the arms, "details": the manifest, the progress, the load of its machines, the episodes and what else the
    platform sends of it} - what `seq --json eval report` prints. `wait` waits until the eval has ended (up to
    `timeout_s`; one still running then is Unavailable, as the command ends); without it, the report so far.
    Prints the report as the command does, and each state it waits through, only when given `echo`. The files the
    command saves beside it - `--records`, `--replays`, `--csv` - are its alone."""
    from seq._eval_gateway import EvalGatewayClient

    client = EvalGatewayClient(base_url=base_url)
    rep, details = _read_report(client, eval_id, wait, timeout_s, echo)
    if echo is not None:
        print_report(rep, details, earlier_cost=earlier_cost(client, details), echo=echo, eval_id=eval_id)
    return _report_data(rep, details)


def report(args: argparse.Namespace) -> int:
    """`seq eval report <id> [--wait] [--csv [-o PATH]] [--records DIR] [--replays DIR]`:
    eval_report, printed - or, with --json, as data - and the files saved."""
    from seq._eval_gateway import EvalGatewayClient

    out_only(args.csv, args.out)
    client = EvalGatewayClient(base_url=args.base_url)
    rep, details = _read_report(client, args.eval_id, args.wait, args.timeout, _live)
    if args.json:
        print(json.dumps(_report_data(rep, details), indent=2, default=str))
    elif not (args.csv and args.out is None):
        print_report(rep, details, earlier_cost=earlier_cost(client, details), eval_id=args.eval_id)
    if details and (getattr(args, "records", None) or getattr(args, "replays", None)):

        details = {**details, "episodes": client.all_episodes(args.eval_id, details)}
    if getattr(args, "records", None) and not save_records(client, args.eval_id, details, args.records):
        return 1
    if getattr(args, "replays", None) and not save_replays(client, args.eval_id, details, args.replays):
        return 1
    if args.csv and not save_csv(client, args.eval_id, args.out):
        return 1
    return 0 if rep.status.value == "completed" else 1


def out_only(csv_on: bool, out: str | None) -> None:
    """`-o PATH` says where --csv writes, and nothing else: given without --csv it is refused, not ignored. One flag,
    one meaning - --csv the format, -o the place."""
    if out is not None and not csv_on:
        raise InvalidRequest("-o PATH is where --csv writes the episodes: add --csv")


def save_records(client: Any, eval_id: str, details: dict | None, dest: str) -> bool:
    """Download every episode's record the details mark into `dest` (eval-<id8>-<n>.rec.zst): the one copy an eval keeps
    of what its policy was sent - its cameras as video - and what it answered, step by step, where its own recordings
    and trajectories were before. False when one failed. Before, --videos and --trajectories
    read what no eval has made since then and said every eval kept none.
"""
    episodes = [e for e in ((details or {}).get("episodes") or []) if e.get("record")]
    if not episodes:
        print("  no records (the eval kept none, has not finished, or its recordings were deleted)")
        return True
    os.makedirs(dest, exist_ok=True)
    ok = True
    for e in episodes:
        name = f"eval-{eval_id[:8]}-{e['index']}.rec.zst"
        try:
            data = client.record(eval_id, int(e["index"]))
        except SequencesError as exc:
            print(f"  {name}: failed: {exc}", file=sys.stderr)
            ok = False
            continue
        with open(os.path.join(dest, name), "wb") as f:
            f.write(data)
    print(f"  saved {len(episodes) if ok else 'some'} records into {dest}")
    return ok


def save_replays(client: Any, eval_id: str, details: dict | None, dest: str) -> bool:
    """Download every episode's 3D replay the details mark into `dest` (eval-<id8>-<n>.seqreplay) and each scene they
    name once (scenes/<sha256>.glb). False when one failed."""
    episodes = [e for e in ((details or {}).get("episodes") or []) if e.get("replay")]
    if not episodes:
        print("  no 3D replays (the benchmark declares no replay=, the eval ran with --replay none, or it has not "
              "finished)")
        return True
    os.makedirs(os.path.join(dest, "scenes"), exist_ok=True)
    ok, saved = True, 0
    for e in episodes:
        name = f"eval-{eval_id[:8]}-{e['index']}.seqreplay"
        try:
            data = client.replay(eval_id, int(e["index"]))
        except SequencesError as exc:
            print(f"  {name}: failed: {exc}", file=sys.stderr)
            ok = False
            continue
        with open(os.path.join(dest, name), "wb") as f:
            f.write(data)
        saved += 1
    for sha in sorted({str(e["scene_sha256"]) for e in episodes if e.get("scene_sha256")}):
        if not re.fullmatch(r"[0-9a-f]{64}", sha):

            print(f"  scene {sha[:80]!r}: failed: not a sha256, so not written", file=sys.stderr)
            ok = False
            continue
        try:
            data = client.scene(eval_id, sha)
        except SequencesError as exc:
            print(f"  scene {sha[:12]}: failed: {exc}", file=sys.stderr)
            ok = False
            continue
        with open(os.path.join(dest, "scenes", f"{sha}.glb"), "wb") as f:
            f.write(data)
    print(f"  saved {saved} replays into {dest}")
    return ok


def earlier_cost(client: Any, details: dict | None) -> float | None:
    """What the eval a rerun completes cost (its manifest's rerun_of), for the report's cost line; None for an eval that
    is no rerun, or when that one cannot be read - the line then says this run's alone, as before."""
    of = ((details or {}).get("manifest") or {}).get("rerun_of")
    if not of:
        return None
    try:
        return float(client.report(of).cost_usd)
    except (SequencesError, TypeError, ValueError):
        return None


def print_report(report: Any, details: dict | None = None, *, earlier_cost: float | None = None,
                 echo: Callable[[str], Any] = print, eval_id: str | None = None) -> None:
    """The report as the platform returned it: every metric is the benchmark's own (user-named), aggregated
    overall and per task — the platform names none of them — each with its n;
    and the time limit each arm ran with, beside the benchmark's own. A rerun's
    (`earlier_cost`: what the eval it completes cost) says both runs' cost: it covers both runs' episodes, and
    "$2.0269" alone read as what all 500 had cost, where the eval it reran had cost $6.7830 more.
    """
    details = details or {}
    m = details.get("manifest") or {}
    units = UNITS
    if m:
        seeds = m.get("seeds") or []
        from seq.adapter_cli import label






        adapter = m.get("adapter")


        bench = f"{m.get('benchmark')}" + (" (deleted)" if m.get("benchmark_deleted") else "")
        echo(f"ran: benchmark {bench} v{m.get('benchmark_version')} + "
             f"{'adapter ' if isinstance(adapter, dict) else ''}{label(adapter, at=' v')} + "
             f"policy {m.get('model')} v{m.get('model_version')}  {m.get('episodes')} episode(s), seeds "
             f"{_span(seeds)}" + (f"  (reran the errors of {m['rerun_of']})" if m.get("rerun_of") else "")
             + (f"  (the episodes {m['rerun_unsuccessful_of']} ran and did not succeed on"
                 + (f", by {m['metric']}" if m.get("metric") else "") + " - an eval of their own)"
                 if m.get("rerun_unsuccessful_of") else ""))
        if m.get("params") and not report.arm_params:
            echo("params: " + ", ".join(f"{k}={v}" for k, v in m["params"].items()))
    used = report.arm_params or []
    for a in used:
        echo(("params: " if len(used) == 1 else f"params, arm {a.arm}: ") + params_line(a.model_dump()))
        if a.queries and a.steps:
            echo(f"  asked the policy at {a.queries:,} of {a.steps:,} steps (1 in {a.steps / a.queries:.1f})")
    cost = f"cost {money(report.cost_usd)}"
    if earlier_cost is not None:
        of = str((details.get("manifest") or {}).get("rerun_of"))[:8]
        cost += (f" this run, with the {money(earlier_cost)} eval {of} cost before it: "
                 f"{money(report.cost_usd + earlier_cost)} for the episodes this report covers")
    echo(f"report: {report.status.value}  {cost}")
    planner = getattr(report, "planner", None)
    if planner is not None:


        calls = money(planner.model_calls_usd) if planner.model_calls_usd is not None else "unknown"
        echo(f"planner: {planner.name} planned for {planner.policy} every {planner.every_s:g} s of each episode, "
             f"{planner.plans:,} plan(s); its model calls {calls}")
    time_note(details.get("time_limit"), echo)
    limit_lines(details.get("max_seconds"), echo=echo)
    repeats_lines(details.get("repeats"), echo=echo)
    for key, agg in report.metrics.items():
        unit = units.get(key)
        echo(f"  {key}: overall {shown(agg.overall, unit)} (n={agg.n})")
        for t in agg.per_task:
            echo(f"    task {t.task}: {shown(t.value, unit)} (n={t.n})")
    if report.incomplete:
        p = details.get("progress") or {}
        if p.get("total"):


            echo(f"  partial results: {p['done'] - p['failed']} of {p['total']} episodes scored{progress_counts(p)}")
        else:
            echo("  incomplete: not every selected episode produced a result")
    for e in report.errors:
        echo(f"  error: {e}")
    arms = report.arms or []
    if len(arms) > 1:
        echo("arms:")
        for a in arms:
            label = a.model + ("" if not a.params else " " + ", ".join(f"{k}={v}" for k, v in a.params.items()))
            cells = [f"{k} {shown(agg.overall, units.get(k))}" for k, agg in a.metrics.items()]


            ran_out = f", {stop_said(report.stop_reason) or 'its spend cap or the monthly limit was reached'}" \
                if a.budget_stopped else ""
            echo(f"  arm {a.arm} {label}: " + "  ".join(cells) + f"  ({a.episodes} ran, {a.failed} failed, "
                 f"{a.not_run} not run{ran_out})")
    timing = report.timing
    load = details.get("load") or []
    if timing and timing.step_ms:
        legs = "  ".join(f"{k.removesuffix('_ms')} {v:.1f} ms" for k, v in timing.step_ms.items())


        echo(f"time per occurrence: {legs}" + (f"  (policy batch {timing.batch_size_mean:.1f} on average)"
                                              if timing.batch_size_mean and not load else ""))
    if (started := start_said(timing)) is not None:
        echo(started)
    _print_load(load, echo)
    _print_link(details.get("link") or [], echo)
    _print_usage(details.get("usage") or [], echo)
    if (place := placement_line(details.get("placement"))) is not None:
        echo(place)
    _print_warning(details.get("warning") or [], echo)
    if (taken := taken_line(details.get("taken"))) is not None:
        echo(taken)



    from seq.capacity_cli import show_hints

    show_hints(details.get("hints"), "load", echo)
    show_hints(details.get("hints"), None, echo)
    if report.stop_reason:
        said = stop_said(report.stop_reason)
        echo(f"stopped: {said} ({report.stop_reason})" if said else f"stopped: {report.stop_reason}")


        if report.stop_reason in RERUN_STOPS and eval_id and not (details.get("policy_deleted")
                                                                   or m.get("benchmark_deleted")):
            echo(rerun_line(eval_id, details))





STOP_SAID = {"canceled": "the eval was canceled", "spend_cap": "its spend cap ran out",
             "balance": "the account reached this month's limit, or its credit with no payment method",
             "deadline": "the eval reached its time limit",
             "refused": "the policy refused this eval's requests",
             "mismatch": "the benchmark and the policy do not fit",
             "no_gpu_render": "the benchmark's cameras could not be drawn on its GPU",
             "queue_timeout": "it waited in line for GPUs and they did not free up"}


def stop_said(reason: str | None) -> str | None:
    """A stop_reason in words, or None for none (or one this client has no words for: printed as it came)."""
    return STOP_SAID.get(reason) if reason else None





RERUN_STOPS = ("deadline", "balance")


def rerun_line(eval_id: str, details: dict | None) -> str:
    """The command that runs the episodes an eval's stop left unrun, as this CLI spells it."""
    m = (details or {}).get("manifest") or {}
    return (f"run the episodes it did not run: seq eval run {m.get('model') or '<policy>'} --benchmark "
            f"{m.get('benchmark') or '<benchmark>'} --rerun-failed {eval_id}")


def taken_line(taken: Any) -> str | None:
    """The eval's machines taken back while it ran (details["taken"]: {machines, episodes}) - each started again, the
    episodes they held run again - and that what was lost there is not charged; None when none was.
"""
    if not isinstance(taken, dict):
        return None
    n, eps = taken.get("machines"), taken.get("episodes")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        return None
    line = f"{n} machine{'' if n == 1 else 's'} {'was' if n == 1 else 'were'} reclaimed mid-run and started again"
    if isinstance(eps, int) and not isinstance(eps, bool) and eps > 0:
        line += f"; {eps} episode{'' if eps == 1 else 's'} ran again"
    return line + " — the lost part is not charged"


def _print_load(load: list[dict], echo: Callable[[str], Any] = print) -> None:
    """How each arm used its policy machines (details["load"]): per machine its requests, batches, average batch and
    batches per round, the share of its time spent computing, and the rounds that waited for it; per arm, the sim's
    share of time busy and waiting on the policy."""
    for a in load:
        policies = a.get("policies") or []
        head = "policy load" + (f" (arm {a.get('arm')})" if len(load) > 1 else "")
        head += f": {len(policies)} machine(s), {a.get('rounds') or 0} round(s)"
        if a.get("benchmark_busy") is not None:
            head += (f"; the sim was busy {a['benchmark_busy']:.0%} of the time and waited on the policy "
                     f"{a.get('policy_wait') or 0:.0%}")
        echo(head)
        for p in policies:
            line = f"  machine {p.get('machine')}: {p.get('requests') or 0} request(s)"


            if p.get("batches"):
                line += f" in {p['batches']:g} batch(es)"
                if p.get("batch_size_mean") is not None:
                    line += f", {p['batch_size_mean']:.1f} per batch"
                if p.get("batches_per_round") is not None:
                    line += f", {p['batches_per_round']:.2f} per round"
            if p.get("busy") is not None:
                line += f", busy {p['busy']:.0%}"
            if p.get("slowest_rounds"):
                line += f", the last to answer in {p['slowest_rounds']} round(s) (+{p.get('lag_ms_mean') or 0:.0f} ms)"
            echo(line)
        serving = a.get("serving") or {}
        if serving.get("act_ms") is not None:


            echo(f"  online: a robot's acts run one per batch, about {float(serving['act_ms']):.0f} ms each "
                 "(its build check)")
        moved, rerun = a.get("episodes_moved") or 0, a.get("episodes_rerun") or 0
        if moved or rerun:
            echo(f"  a policy machine ended mid-episode: {moved} episode(s) went on on another one, {rerun} ran again "
                 "from their reset (a stateful policy's)")


def _print_link(link: list[dict], echo: Callable[[str], Any] = print) -> None:
    """The link between each arm's benchmark machines and its policy machines (details["link"]): its pings' round
    trips on an open connection - the network alone - and each request's time outside the policy's worker, its
    observation's upload with it: a request, as the load lines above say the policy's acts, and as the console says it.
    Where only the benchmark's eval.lane log line said it.

 """
    def ms(v) -> str:
        v = float(v or 0)
        return f"{v:.1f} ms" if round(v, 1) < 10 else f"{v:.0f} ms"

    for a in link:
        parts = []
        if a.get("ping_p50_ms") is not None:
            parts.append(f"ping p50 {ms(a['ping_p50_ms'])}, p90 {ms(a.get('ping_p90_ms'))}, "
                         f"max {ms(a.get('ping_max_ms'))} ({a.get('pings') or 0} ping(s))")
        if a.get("outside_p50_ms") is not None:
            parts.append(f"a request's time outside the policy's worker p50 {ms(a['outside_p50_ms'])}, "
                         f"p90 {ms(a.get('outside_p90_ms'))} ({a.get('acts') or 0} request(s))")
        if parts:
            echo("link between the benchmark and policy machines" + (f" (arm {a.get('arm')})" if len(link) > 1
                                                                      else "") + ": " + "; ".join(parts))


def _print_usage(usage: list[dict], echo: Callable[[str], Any] = print) -> None:
    """Each side's machines' resource use (details["usage"]): the benchmark's and the policy's - the most any used and
    the mean of their uses, against what it requested. The policy's is what it carried back with its answers (the
    policy cannot report to the gateway itself)."""
    multi = len({a.get("arm") for a in usage}) > 1
    for a in usage:
        side = "policy" if a.get("role") == "policy" else "benchmark"
        head = f"{side} usage" + (f" (arm {a.get('arm')})" if multi else "")
        parts = []
        if a.get("cpu_cores_peak") is not None:
            of = f" of {a['cpu_request']:g}" if a.get("cpu_request") else ""
            avg = f", {a['cpu_cores_avg']:g} average" if a.get("cpu_cores_avg") is not None else ""
            parts.append(f"CPU {a['cpu_cores_peak']:g}{of} core(s) at peak{avg}")
        if a.get("ram_mb_peak") is not None:
            of = f" of {a['mem_request_mb']:g}" if a.get("mem_request_mb") else ""
            parts.append(f"RAM {a['ram_mb_peak']:g}{of} MiB")
        if a.get("gpu_util_pct_peak") is not None:
            avg = f", {a['gpu_util_pct_avg']:g}% average" if a.get("gpu_util_pct_avg") is not None else ""
            parts.append(f"GPU {a['gpu_util_pct_peak']:g}% busy at peak{avg}")
        if a.get("vram_mb") is not None:
            parts.append(f"{a['vram_mb']:g} MiB VRAM")
        if parts:
            echo(f"{head}: " + "; ".join(parts))


def placement_line(place: Any) -> str | None:
    """Where the eval's machines ran (details["placement"]): on one machine or apart, and the region(s) - never the
    provider's name. None when it is not known. {the user 11-02: "are these two machines just next to each other"}"""
    if not isinstance(place, dict):
        return None
    region = place.get("region")
    if place.get("same_machine"):
        return "placement: the policy and benchmark ran on one machine" + (f" in {region}" if isinstance(region, str)
                                                                            else "")
    where = ""
    if isinstance(region, str):
        where = f" in {region}"
    elif isinstance(region, dict) and region.get("policy") and region.get("benchmark"):
        pol, ben = region["policy"], region["benchmark"]
        where = f" both in {pol}" if pol == ben else f" (policy in {pol}, benchmark in {ben})"
    return "placement: the policy and benchmark ran on separate machines" + where


def _print_warning(warnings: list[dict], echo: Callable[[str], Any] = print) -> None:
    """A warning per arm whose acts ran clearly slower than its policy's build check (details["warning"]), naming the
    resource that was its bottleneck and what to change. {the user 11-02: "also send warning fro these if needed so
    seru know"}"""
    for w in warnings:
        arm = f" (arm {w['arm']})" if len(warnings) > 1 else ""
        echo(f"warning{arm}: {w.get('note')}")
        if w.get("act_ms") is not None and w.get("check_p95_ms") is not None:
            echo(f"  its acts took about {float(w['act_ms']):.0f} ms each against the build check's "
                 f"{float(w['check_p95_ms']):.0f} ms ({w.get('slower_x')}x slower)")


def _span(seeds: list) -> str:
    if not seeds:
        return "-"
    return str(seeds[0]) if len(seeds) == 1 else f"{seeds[0]}..{seeds[-1]} ({len(seeds)})"



def parse_gate(text: str) -> tuple[str, str, float]:
    match = _GATE.match(text or "")
    if not match:
        raise ValueError(f"{text!r} is not METRIC OP NUMBER (e.g. \"success>=0.9\"; OP is one of >= <= > < ==)")
    return match.group(1), match.group(2), float(match.group(3))


def check_gates(report: Any, gates: list[tuple[str, str, float]]) -> int:
    """0 when the eval completed with every selected episode and every gate passes, else GATE_FAILED."""
    if report.status.value != "completed" or report.incomplete:
        why = "the eval did not complete" if report.status.value != "completed" else \
            "not every selected episode produced a result"
        print(f"gate: failed — {why}", file=sys.stderr)
        return GATE_FAILED
    failed = False
    for key, op, want in gates:
        agg = report.metrics.get(key)
        if agg is None:
            print(f"gate: {key} {op} {want:g} — failed: the report has no metric {key!r}", file=sys.stderr)
            failed = True
            continue
        ok = _OPS[op](agg.overall, want)
        failed |= not ok
        print(f"gate: {key} {agg.overall:.3f} {op} {want:g} — {'passed' if ok else 'failed'}",
              file=sys.stdout if ok else sys.stderr)
    return GATE_FAILED if failed else 0


def save_csv(client: Any, eval_id: str, path: str | None, *, task: list[str] | None = None,
             outcome: str | None = None, arm: int | None = None) -> int:
    """The eval's episodes - every one, or those the filters take - as the platform's one CSV file, the one the console
    downloads (GET /v1/eval/{id}/episodes.csv: a row per episode, its condition, its success as the eval judged it,
    each metric under "metrics.<name>", its cells guarded against spreadsheet formulas), written to `path` (-o), or to
    stdout without one. How many episodes it wrote; 0, and nothing written, when none has reported or none passes the
    filters."""
    text = client.episodes_csv(eval_id, task=task, outcome=outcome, arm=arm)
    rows = max(0, sum(1 for _ in csv.reader(io.StringIO(text))) - 1)
    if not rows:
        print("csv: no episode of this eval to write: none has reported yet, or none passes the filters",
              file=sys.stderr)
        return 0
    if path is None:
        sys.stdout.write(text)
    else:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write(text)
        print(f"  wrote {rows} episode(s) to {path}")
    return rows
