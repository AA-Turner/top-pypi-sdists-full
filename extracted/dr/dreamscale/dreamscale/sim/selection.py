"""Which tasks a `dreamscale sim` run runs (DSL-611).

Exactly one of ``--all`` (every task in the benchmark), ``--task-suite`` (every task in a
suite), ``--task-id`` (one task) or ``--random`` (one task at random). A task's id is unique
across its benchmark (``task_list``), so it never needs a suite; each ``Pick`` turns it back
into the suite and task the benchmark's runner takes.
"""

from __future__ import annotations

import random as _random
from dataclasses import dataclass

from . import task_list

SELECTORS = "--all, --task-suite <suite>, --task-id <id> or --random"


@dataclass(frozen=True)
class Pick:
    id: str  # the task's --task-id (MolmoSpaces: a benchmark, when its runner picks episodes)
    suite: str  # what the benchmark's runner takes as task_suite
    task: str | int  # ... and as task_id ("all" or "random": MolmoSpaces picks the episodes)


def selector_error(benchmark: str) -> str:
    return (f"choose one: {SELECTORS}. `dreamscale sim {benchmark} --list` lists the suites "
            "and tasks.")


def _unknown(benchmark: str, task_id: str, form: str = "") -> ValueError:
    label = task_list.BENCHMARK_LABELS[benchmark].removesuffix(" (hosted)")
    return ValueError(f"Unknown {label} task {task_id!r}{form}. `dreamscale sim {benchmark} "
                      "--list` lists the suites, and --task-suite <suite> --list their tasks.")


def pick(benchmark: str, task_id: str) -> Pick:
    """The task an id names; ValueError when it names none."""
    value = str(task_id)
    if benchmark == "libero":
        suite, _, index = value.rpartition("/")
        known = task_list.suites("libero")
        sizes = {s.id: s.tasks for s in known}
        if suite in sizes and index.isdecimal() and int(index) < (sizes[suite] or 0):
            return Pick(value, suite, int(index))
        raise _unknown(benchmark, value, " (ids look like libero_spatial/0)")
    if benchmark == "molmospaces":
        from .molmospaces_catalog import BENCHMARKS

        suite, _, index = value.rpartition("/")
        if suite in BENCHMARKS and index.isdecimal() and str(int(index)) == index:
            return Pick(value, suite, int(index))
        raise _unknown(benchmark, value, " (ids look like pick-v1.5/0)")
    if benchmark == "robolab":
        from .robolab_catalog import TASK_ATTRIBUTES

        name = value.removesuffix("Task") if value.removesuffix("Task") in TASK_ATTRIBUTES \
            else value
        if name in TASK_ATTRIBUTES:
            return Pick(name, "", name)
        raise _unknown(benchmark, value)
    if benchmark == "robotwin":
        from .robotwin_catalog import STEP_LIMITS

        if value in STEP_LIMITS:
            return Pick(value, "", value)
        raise _unknown(benchmark, value)
    if benchmark == "abc":
        from .abc_catalog import TASKS

        if value in TASKS:
            return Pick(value, value, 0)  # the runner's suite is the task; --task-seed its scene
        raise _unknown(benchmark, value)
    for suite in task_list.suites(benchmark):  # robocasa365, roboeval: names in suites
        if value in {task.id for task in task_list.tasks(benchmark, suite.id)}:
            return Pick(value, suite.id, value)
    raise _unknown(benchmark, value)


def _suite_ids(benchmark: str) -> list[str]:
    return [suite.id for suite in task_list.suites(benchmark)]


def select(benchmark: str, *, every: bool = False, suite: str | None = None,
           task_id: str | None = None, random_task: bool = False,
           rng: _random.Random | None = None) -> list[Pick]:
    """The run's tasks, in order. ValueError for no selector, two, or an unknown name."""
    chosen = sum((every, suite is not None, task_id is not None, random_task))
    if chosen != 1:
        raise ValueError(selector_error(benchmark))
    rng = rng or _random.Random()
    if task_id is not None:
        return [pick(benchmark, task_id)]
    if suite is not None and suite not in _suite_ids(benchmark):
        names = _suite_ids(benchmark)
        label = task_list.BENCHMARK_LABELS[benchmark].removesuffix(" (hosted)")
        raise ValueError(
            f"{label} has no suites: use --all or --task-id <task>." if not names else
            f"{label} --task-suite must be one of {', '.join(names)}"
            + (" (every task: --all)." if suite == "all" else "."))
    if benchmark == "molmospaces":  # its runner loads the episodes, and picks among them
        if every:
            return [Pick("all", "all", "all")]
        if suite is not None:
            return [Pick(suite, suite, "all")]
        name = rng.choice(_suite_ids(benchmark))
        return [Pick(name, name, "random")]
    if benchmark == "robolab":  # the hosted run takes a suite or task ids
        if every:
            return [Pick("all", "all", "all")]
        if suite is not None:
            return [Pick(suite, suite, "all")]
    if random_task:
        return [pick(benchmark, rng.choice(task_list.all_tasks(benchmark)).id)]
    if benchmark == "abc":  # no suites: --all is every task
        return [Pick(task.id, task.id, 0) for task in task_list.all_tasks(benchmark)]
    if benchmark == "robotwin":  # no suites: --all is every task, sent by id
        return [Pick(task.id, "", task.id) for task in task_list.all_tasks(benchmark)]
    picks: dict[str, Pick] = {}
    for name in ([suite] if suite is not None else _suite_ids(benchmark)):
        for task in task_list.tasks(benchmark, name):
            runner_task = int(task.id.rpartition("/")[2]) if benchmark == "libero" else task.id
            picks.setdefault(task.id, Pick(task.id, name, runner_task))
    return list(picks.values())
