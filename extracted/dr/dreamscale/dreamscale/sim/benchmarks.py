"""Benchmark selection and task validation, without importing a native simulator."""

from __future__ import annotations

import json
from importlib.resources import files
from math import ceil

from dreamscale_transport import catalog

from dreamscale import errors
from dreamscale.model_names import public_model

from .abc_catalog import MODELS as ABC_MODELS

BENCHMARK_LABELS = {"libero": "LIBERO", "robocasa365": "RoboCasa365",
                    "molmospaces": "MolmoSpaces", "roboeval": "RoboEval", "abc": "ABC"}
# The models each benchmark runs: the catalog's (each entry's ``client.sim.benchmarks``). ABC
# is the YAM robot's simulator, not a model's sim: it runs the robot's joint models through
# the robot's own run loop (``sim/abc.py``).
BENCHMARK_MODELS = {
    benchmark: tuple(entry.id for entry in catalog.CATALOG
                     if entry.client.sim is not None and benchmark in entry.client.sim.benchmarks)
    for benchmark in BENCHMARK_LABELS
}
BENCHMARK_MODELS["abc"] = ABC_MODELS
LIBERO_MODELS = BENCHMARK_MODELS["libero"]
LIBERO_SUITES = {"libero_spatial": 10, "libero_object": 10, "libero_goal": 10,
                 "libero_10": 10, "libero_90": 90}


def robocasa_tasks(suite: str) -> list[dict]:
    catalog = json.loads(files("dreamscale.sim").joinpath("robocasa365_tasks.json").read_text())
    if suite not in catalog["suites"]:
        raise ValueError("RoboCasa365 --task-suite must be atomic or composite.")
    return catalog["suites"][suite]


def resolve_task(benchmark: str, suite: str, task_id: str | int) -> str | int:
    if benchmark == "libero":
        if suite not in LIBERO_SUITES:
            raise ValueError(f"LIBERO --task-suite must be one of {', '.join(LIBERO_SUITES)}.")
        try:
            index = int(task_id)
        except (ValueError, TypeError) as exc:
            raise ValueError("LIBERO --task-id must be an integer.") from exc
        if not 0 <= index < LIBERO_SUITES[suite]:
            raise ValueError(f"{suite} --task-id must be 0–{LIBERO_SUITES[suite] - 1}.")
        return index
    if benchmark == "robocasa365":
        tasks = robocasa_tasks(suite)
        value = str(task_id)
        if value in {task["name"] for task in tasks}:
            return value
        if value.isdecimal() and int(value) < len(tasks):
            return tasks[int(value)]["name"]
        raise ValueError(f"Unknown {suite} task {value!r}. "
                         f"Use a task name or index 0–{len(tasks)-1}.")
    if benchmark == "molmospaces":
        from .molmospaces_catalog import episode_selection, selected_suites

        selected_suites(suite)
        return episode_selection(task_id)
    if benchmark == "roboeval":
        from .roboeval_catalog import resolve_variant

        return resolve_variant(suite, task_id)
    if benchmark == "abc":
        from .abc_catalog import resolve_task as resolve_abc_task

        return resolve_abc_task(suite, task_id)
    raise ValueError("benchmark must be libero, robocasa365, molmospaces, roboeval or abc")


def validate_selection(benchmark: str, model: str, suite: str, task_id: str | int) -> str | int:
    task = resolve_task(benchmark, suite, task_id)
    if model not in BENCHMARK_MODELS[benchmark]:
        raise ValueError(f"{public_model(model)} doesn't run on {benchmark}. {errors.SEE_MODELS}")
    from dreamscale.policy.runtime import served

    # A model trained on one suite refuses the others (its wire's ``sim_task``).
    sim_task = served.hook(model, "sim_task")
    if sim_task is not None:
        sim_task(model, benchmark, suite)
    return task


ROBOCASA_TASK_HZ = 20  # RoboCasa365 task horizons count steps at its default control rate


def default_task_horizon(
    benchmark: str, suite: str, task: str | int, *, action_hz: float | None = None
) -> int:
    """The task's step budget, kept to the same wall-clock span at ``action_hz``."""
    if benchmark == "libero":
        from .timing import DEFAULT_SIM_MAX_STEPS

        return DEFAULT_SIM_MAX_STEPS
    if benchmark == "molmospaces":
        from .molmospaces_catalog import BENCHMARKS, selected_suites

        return max(BENCHMARKS[name].horizon_s * 15 for name in selected_suites(suite))
    if benchmark == "roboeval":
        from .roboeval_catalog import FAMILIES

        return FAMILIES[suite].horizon
    if benchmark == "abc":
        from .abc_catalog import HORIZON_STEPS

        return HORIZON_STEPS
    record = next(item for item in robocasa_tasks(suite) if item["name"] == task)
    steps = record.get("horizon") or 2400
    if action_hz is None or action_hz == ROBOCASA_TASK_HZ:
        return steps
    return max(1, ceil(steps * action_hz / ROBOCASA_TASK_HZ))
