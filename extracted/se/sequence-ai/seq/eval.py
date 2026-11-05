"""
`seq.eval(policy, benchmark, ...)` — evaluate a deployed policy on a registered benchmark, on the platform.

In one sentence: `seq.eval` posts the eval (`POST /v1/eval`) → the platform runs the selected episodes of the
benchmark against the deployed policy on its own machines → by default it polls until the eval completes or fails and
returns the platform's `EvalReport`; `dry_run=True` returns the estimate and starts nothing, and `wait=False` returns
the started eval's id at once (`seq eval report <id>` reads it later). `seq eval run` posts the same body.

Nothing runs on this machine. The local engine this module used to drive — a mock platform that ran the sim and the
policy on the caller's laptop — is gone: a Mac cannot run the sims, and a second, local way to evaluate meant a second
set of answers.
"""
from __future__ import annotations

import warnings as _warnings
from dataclasses import dataclass
from typing import Any

from sequence_base.contract import EvalReport

from sequence_ai.errors import InvalidRequest


@dataclass
class EvalEstimate:
    """What `dry_run=True` returns: the estimated wall-clock time, cost and chat-model calls; the layout as it would run
    (per side the machines and card — the numbers you wrote, or the fixed defaults — and the worlds each benchmark
    machine runs, the platform's own); the account's
    cards against the eval's (`cards`: how many, how many are free, whether it would wait, and why); and hints
    (`notes`) such as a policy that does not declare @seq.concurrent; `warnings`, what the platform sees will not fit
    between the policy and the benchmark - each {reason, model, sentence, adapters, needs, stops, start_usd}: the eval
    starts all the same, and one that `stops` it at its first act costs `start_usd`, its machines' start. The platform
    never changes your numbers.
    `cost_usd` prices each machine on its card (a policy's one card; a benchmark that names several, its first);
    `held_usd` is what a real run holds from the balance while it runs - with a reserve, and such a benchmark on its
    costliest card - when that differs (None when it is the estimate). `cost_parts` is `cost_usd` by machine and by what
    it is billed for, {"policy": {"gpu", "cpu", "memory"}, "benchmark": {...}}, each the whole eval's.
    `layout["selection"]` is which episodes would run: their number, each chosen task's seeds
    ("0-9") and episodes, and each arm's time limit beside the benchmark's own (`max_seconds`: {"default", "arms":
    [{"arm", "value", "standard"}]}); `repeats`, in all and per task, the episodes that run a start again past a task's
    last seed."""

    gpus_granted: int
    wall_clock_s: float
    cost_usd: float
    vlm_calls: int
    layout: dict | None = None
    cards: dict | None = None
    notes: list | None = None
    breakdown: dict | None = None
    default_timing: bool | None = None
    held_usd: float | None = None
    warnings: list | None = None
    cost_parts: dict | None = None


def at_least_one(*counts: tuple[str, Any]) -> None:
    """Each (name, value) a count of at least 1 when given - machines as an eval takes them, said where they are
    written: `seq eval run --policy-machines 0` and `seq.eval(..., policy_machines=0)` alike. Before: the Python call ran
    a 0 as the default with no word, where the CLI refused it."""
    for name, value in counts:
        if value is not None and value < 1:
            raise InvalidRequest(f"{name} is a count of at least 1, got {value}")


def eval(
    policy: Any,
    benchmark: Any,
    *,
    adapter: Any = None,
    tasks: list[str] | str | None = None,
    trials: int | dict[str, int] | str | None = None,
    seeds: Any = None,
    policy_machines: int = 1,
    benchmark_machines: int = 1,
    sweep: dict[str, list[Any]] | None = None,
    params: dict[str, Any] | None = None,
    spend_cap_usd: float | None = None,
    replay: str | None = None,
    dry_run: bool = False,
    wait: bool = True,
    timeout_s: float | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> EvalReport | EvalEstimate | str:
    """Evaluate the deployed `policy` on the registered `benchmark`.

    A policy with a `@seq.plan` plans in the eval on the robot's clock - every_s of the episode's own time, however
    fast it runs - and its plans are kept in the report's episodes and their replays; the report's `plan` says how many
    and what their model calls cost.

    `policy` is a deployment name (or what `seq.deploy` returned); `benchmark` a registered benchmark's name or its
    `@seq.benchmark` class. `adapter` maps the sim to the policy's own inputs and outputs: a registered adapter
    ("name@vN", or "name" for its latest), or a `@seq.adapter` class or "./my_adapter_user.py:MyAdapter_user" file,
    registered first (the same code is the version it already is). The other arguments select and bound the run exactly
    as the `seq eval run` flags of the same names do.

    Which episodes run (`seq.benchmark_tasks(benchmark)` lists the tasks and their seeds): `tasks` only these of the
    benchmark's tasks (all of them when left out); then each chosen task's seeds - `trials` how many times it runs:
    its declared seeds in order, and past the last the same seeds again as repeated starts, marked so - or
    `seeds` the ones named (a list, `range(10, 20)`, or "10-19") - given once for every chosen task, or per task as
    {task: ...} with "*" for the rest: `trials={"libero_spatial/3": 20, "*": 5}`. With no `tasks`, per-task dicts
    without "*" run just the tasks they name; a "*", or one count or seed list for every task, runs every task. The
    platform refuses a task or seed the benchmark does not declare, naming the ones it does.

    How the eval runs is yours to write, the same way on both sides: `policy_machines` copies of the policy (each on
    the deployment's own card) and `benchmark_machines` benchmark machines per arm (each on the card the benchmark was
    registered on); each benchmark machine builds the worlds the eval needs - the fewest of the
    benchmark's @seq.concurrent size, the eval's episodes and what the policy takes at once. Both sides run wherever
    there are cards. `sweep` ({param: [values]}) adds arms that run side by side on the same episodes; the report has one table
    per arm. Another policy is an eval of its own. `spend_cap_usd` is the eval's spend
    cap: it stops once its machines (GPU, CPU and memory) have cost that much, and the report covers what ran.

    `params` and `sweep` name any side's parameter: the policy's @seq.infer
    (`"replan_steps"` or `"policy.replan_steps"`), the adapter's __init__ (`"adapter.image_size"`), the benchmark's
    __init__ (`"benchmark.noise_std"`) or the eval's own `"eval.max_seconds"` — how long an episode may run on the
    robot's clock (default: the benchmark's max_seconds); an eval that changes it is not a standard one, and its report
    says so. A bare name works when only one side declares it. The report's `arm_params` gives every parameter's value
    per arm and where it came from.

    Each episode plays the policy's answers on the robot's clock: it asks for the next answer at the policy's
    action_chunk_replan_at step and switches to it at its action_chunk_valid_len step, the world held still until it
    arrives - it models no network, so there is no latency to set.

    Returns the `EvalReport` once the eval completes or fails (with `wait=True`; past `timeout_s` the last, still-running
    report), the eval id with `wait=False`, or an `EvalEstimate` with `dry_run=True`. A refusal raises the platform's
    one error hierarchy (`sequence_ai.errors`): an unknown policy or benchmark is NotFound, no balance OutOfCredit, no
    GPU free Conflict."""
    from seq import selection
    from seq._eval_gateway import EVAL_WAIT_S, EvalGatewayClient
    at_least_one(("policy_machines=", policy_machines), ("benchmark_machines=", benchmark_machines))
    body = {

        "model": _policy_name(policy),
        "benchmark": _benchmark_name(benchmark),
        "adapter": _adapter_ref(adapter, api_key=api_key, base_url=base_url),

        "tasks": selection.tasks_value(tasks),
        "trials": selection.trials_value(trials),
        "seeds": selection.seeds_value(seeds),

        "policy_machines": int(policy_machines or 1),
        "benchmark_machines": int(benchmark_machines or 1),
        "sweep": {k: list(v) for k, v in sweep.items()} if sweep else None,
        "params": dict(params) if params else None,
        "spend_cap_usd": spend_cap_usd,
        "replay": replay,
        "dry_run": dry_run or None,
    }
    client = EvalGatewayClient(api_key=api_key, base_url=base_url)
    started = client.start_eval(body)
    if dry_run:
        return estimate_of(started)
    eval_id = started["eval_id"]

    for w in started.get("warnings") or []:
        _warnings.warn(str(w.get("sentence") or w), stacklevel=2)
    if not wait:
        return eval_id
    return client.wait_report(eval_id, timeout_s=timeout_s or EVAL_WAIT_S)


def estimate_of(started: dict) -> EvalEstimate:
    """The estimate in a `POST /v1/eval` answer — a dry run's, or the one a started eval is held against."""
    est = started.get("estimate") or {}
    layout = started.get("layout") or None
    granted = started.get("gpus_granted") or ((layout or {}).get("cards") or {}).get("total") or 0
    return EvalEstimate(gpus_granted=int(granted),
                        wall_clock_s=float(est.get("wall_clock_s") or 0.0),
                        cost_usd=float(est.get("cost_usd") or 0.0),
                        vlm_calls=int(est.get("vlm_calls") or 0),
                        layout=layout, cards=started.get("cards") or None, notes=started.get("notes") or None,
                        breakdown=est.get("breakdown"), default_timing=est.get("default_timing"),
                        held_usd=float(est["held_usd"]) if est.get("held_usd") is not None else None,
                        warnings=started.get("warnings") or None, cost_parts=started.get("cost_parts") or None)


def cancel(eval_id: str, *, base_url: str | None = None, api_key: str | None = None) -> dict:
    """Stop a running eval: it takes no new episode, its machines stop within a minute, and what ran is billed and
    reported (`seq eval report <id>` shows it, status canceled)."""
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(api_key=api_key, base_url=base_url).cancel(eval_id)


def _policy_name(policy: Any) -> str:
    """A deployment name: a string, what `seq.deploy` returned, or a `@seq.policy` class (its declared name)."""
    if isinstance(policy, type):
        from seq.registry import registration

        return registration(policy).spec.name
    name = str(policy or "").strip()
    if not name:
        raise InvalidRequest("name the deployed policy to evaluate (see `seq policy ls`)")
    return name


def _benchmark_name(benchmark: Any) -> str:
    if isinstance(benchmark, type):
        from seq.benchmark_registry import benchmark_registration

        return benchmark_registration(benchmark).name
    name = str(benchmark or "").strip()
    if not name:
        raise InvalidRequest("name the registered benchmark to evaluate on (register one with `seq deploy`)")
    return name


def _adapter_ref(adapter: Any, *, api_key: str | None = None, base_url: str | None = None) -> str | None:
    """The adapter as the eval names it: name@vN — a class or a local file is registered first
. A registered name goes as written."""
    from seq import adapter_cli

    return adapter_cli.resolve(adapter, api_key=api_key, base_url=base_url, echo=lambda _line: None)
