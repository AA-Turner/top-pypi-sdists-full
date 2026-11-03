"""
What a policy's declarations make of it, said by `seq deploy` and its --dry-run before anything is built: whose its
episodes are, what its build check plays, and how a worker seats robots
- and, once, what is missing when a policy that could seat several robots a copy seats one.


In one sentence: the class's registration - its spec, and the methods it marks (@seq.sample, @seq.observe, ...) → one line a
part (episodes, check, seats), each as the worker will act on it
 → printed under the request.

WHY here and not the platform's hints: the deploy request does not carry its sample episode (@seq.sample) - the
platform learns of it at the build check - so what the declarations make of a policy is said where all of them are.
The platform's hints say what it measured, after the build and once robots act; none of
these lines is one of theirs.
"""
from __future__ import annotations

from typing import Any

from sequence_base.contract import SeqFlags

from sequence_ai._core.capacity import LOAD_MAX, wait_steps


_COLUMN = 12


_OWN_HOOKS = (SeqFlags.OBSERVE, SeqFlags.ON_EPISODE)


def _line(label: str, text: str) -> str:
    return f"{label:<{_COLUMN}}{text}"


def _and(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _method(bindings: dict, flag: SeqFlags) -> str | None:
    name = bindings.get(flag)
    return f"{name}()" if name else None


def episodes(spec: Any, bindings: dict) -> str:
    """Whose an episode's state is (PolicySpec.episodes, worked out from how the policy is written) - and, a policy that
    keeps none, takes one act a call and plans nothing, where its episode's observations go: its worker
    keeps the latest on one copy for act()
."""
    if spec.episodes == "shared":
        if getattr(spec.concurrency, "sizes", None):


            return "batched (@seq.concurrent): a copy serves several robots' episodes together"


        handed = "observe and infer" if SeqFlags.OBSERVE in bindings else "infer"
        return f"handed to {handed} (seq.Episode): each copy serves one robot's episode"
    if spec.episodes == "own":
        hooks = [m for m in (_method(bindings, f) for f in _OWN_HOOKS) if m]
        return f"kept on the class by {_and(hooks)}: each episode holds a copy of its own"
    if spec.concurrency is None and SeqFlags.PLAN not in bindings:


        return ("kept on one copy: each episode's observe() and act() go to the same copy, which keeps its latest "
                "observation")
    return "none kept: any copy answers any act"


def _timing(spec: Any, bindings: dict) -> str | None:
    """What its version's build check times each batch size on: its sample episode, or nothing - a worker on the check's
    card seats by those timings, one on another card times them beside its first robots.

"""
    return "its sample episode" if SeqFlags.SAMPLE in bindings else None


def check(spec: Any, bindings: dict) -> str:
    """What the build check plays: its sample episode, call by call."""
    if SeqFlags.SAMPLE in bindings:
        return f"plays its sample episode, {_method(bindings, SeqFlags.SAMPLE)}, call by call"
    return "loads it and calls nothing: it names no sample episode (@seq.sample)"


def seats(spec: Any, bindings: dict) -> str:
    """How a worker seats robots on a copy: a policy whose infer takes a
    batch (@seq.concurrent(sizes=[...])) as many as the largest listed size whose batch answers within the time its
    robots can wait for an answer (wait_steps at hz), as long as their batches fill at most LOAD_MAX of the time between
    a robot's asks (its replan step at hz), each size timed by its version's build check; one that asks at its last valid
    step, or declares no action_chunk_valid_len, one robot a copy, its robots waiting for every answer or nothing saying
    how long they can; any other one robot a copy - several robots never take turns on one copy (the user 10-24: "We
    just want to do the batching").
"""
    listed = getattr(spec.concurrency, "sizes", None)
    if spec.episodes == "own":
        return "one robot a copy: an episode holds its copy"
    if listed:
        steps = wait_steps(spec.action_chunk_valid_len, spec.action_chunk_replan_at)
        if steps is None:
            return ("one robot a copy: it declares no action_chunk_valid_len, so nothing says how long its robots can "
                    "wait for a batch")
        wait = getattr(spec, "max_wait_for_batch", None)
        if wait is not None:
            ask = spec.action_chunk_valid_len - steps
            return (f"as many robots a copy as the largest of its batches of {_and([str(n) for n in listed])} that "
                    f"answers within its max_wait_for_batch of {wait:g} s, each robot waiting up to that long for an "
                    f"answer, as long as their batches fill at most {LOAD_MAX:.0%} of a robot's time between asks (its "
                    f"{ask} steps at {spec.hz:g} Hz and its wait for the answer) - each warmed and timed on "
                    f"{_timing(spec, bindings) or 'nothing'} before it serves")
        if not steps:
            return ("one robot a copy: it asks for each answer at its last valid step, so its robots wait for every "
                    "answer and none can wait for a batch - an action_chunk_replan_at below action_chunk_valid_len "
                    "gives them the time, or a max_wait_for_batch lets them wait that long for one")
        ask = spec.action_chunk_valid_len - steps
        return (f"as many robots a copy as the largest of its batches of {_and([str(n) for n in listed])} that answers "
                f"within {steps / spec.hz:.3g} s, the {steps} steps a robot plays between asking for an answer and "
                f"needing it at {spec.hz:g} Hz, as long as their batches fill at most {LOAD_MAX:.0%} of the "
                f"{ask / spec.hz:.3g} s between a robot's asks (its {ask} steps) - each timed on "
                f"{_timing(spec, bindings) or 'nothing'} by its build check")
    return "one robot a copy"


def names_sample(cls: type) -> bool:
    """Whether a policy class marks a method returning a sample episode (@seq.sample), which the deploy request does
    not carry."""
    from seq.registry import registration

    return SeqFlags.SAMPLE in registration(cls).bindings


def planner(cls: type, spec: Any, bindings: dict, plan_every_s: float | None) -> list[str]:
    """The lines `seq deploy` says of a planner (@seq.planner), which answers no act: what it plans for and when - its
    clock, and wake_on: a key of what is observed into it or by a policy member's robots, or "seq.plans", a plan from
    the planner above - and what its build check plans."""
    plan = getattr(cls, bindings[SeqFlags.PLAN], None)
    wake = list(getattr(getattr(plan, "raw_fn", plan), "__seq_plan_wake_on__", None) or [])
    keys = [k for k in wake if k != "seq.plans"]
    woken = ([f"an observation holds {_and(keys)}"] if keys else []) + (
        ["the planner above writes it a plan"] if "seq.plans" in wake else [])
    when = f"every {plan_every_s:g} s" + (f", and at once when {' or '.join(woken)}" if woken else "")
    sample = _method(bindings, SeqFlags.SAMPLE)
    return [_line("plans", f"for its members {_and(spec.planner.members)}, {when}"),
            _line("check", f"plans its sample group once, {sample}" if sample
                  else "loads it and plans nothing: it names no sample group (@seq.sample)")]


def of(cls: type) -> list[str]:
    """The lines `seq deploy` says of a policy class's parts - reads for a policy of its own inputs, then episodes,
    check and seats; a planner's own (planner)."""
    from seq.registry import registration

    reg = registration(cls)
    spec, bindings = reg.spec, dict(reg.bindings)
    if spec.planner is not None:
        return planner(cls, spec, bindings, reg.plan_every_s)
    lines = [_line("episodes", episodes(spec, bindings)), _line("check", check(spec, bindings)),
              _line("seats", seats(spec, bindings))]
    return lines
