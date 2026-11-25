"""`dreamscale sim [<benchmark>] --list`: the benchmarks, their suites and their tasks.

Offline and without a model or login: every row comes from the catalogs `dreamscale sim`
validates against (`benchmarks.py` and the per-benchmark catalogs). Each row's id is exactly
what `--task-suite` or `--task-id` accepts; a task's id is unique across its benchmark
(DSL-611), so `--task-id` never needs a suite.

MolmoSpaces episodes are the one exception: they live in benchmark files MolmoSpaces downloads
on its first run, so its tasks list once they are on disk.
"""

from __future__ import annotations

import glob
import json
import os
import re
from collections.abc import Callable
from dataclasses import asdict, dataclass
from importlib.resources import files
from pathlib import Path

from rich.text import Text

from dreamscale import tables

from .benchmarks import BENCHMARK_LABELS as LOCAL_LABELS
from .benchmarks import robocasa_tasks

# The benchmarks `dreamscale sim` runs on this computer, then RoboLab, which runs on
# Dreamscale's simulators.
BENCHMARK_LABELS = {**LOCAL_LABELS, "robolab": "RoboLab (hosted)"}


@dataclass(frozen=True)
class Suite:
    id: str  # the --task-suite
    tasks: int | None  # None: not known offline (MolmoSpaces before its download)
    description: str = ""


@dataclass(frozen=True)
class Task:
    id: str  # the --task-id
    task: str


class TasksUnavailable(Exception):
    """The suite's tasks can't be listed here; the message says what --task-id takes."""


def _sentence(text: str) -> str:
    text = text.strip().rstrip(".")
    return text[:1].lower() + text[1:]


def _words(name: str) -> str:
    """CamelCase or snake_case to lower-case words: CloseBlenderLid -> close blender lid."""
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", name)
    return spaced.replace("_", " ").lower()


# --- LIBERO: the suites' task names, from LIBERO's own task map (libero_tasks.json).


def _libero_names() -> dict[str, list[str]]:
    data = json.loads(files("dreamscale.sim").joinpath("libero_tasks.json").read_text())
    return data["suites"]


def libero_language(name: str) -> str:
    """The task's instruction, as libero.benchmark derives it from the task's name."""
    if name[0].isupper():  # LIBERO-90/10 names lead with the scene: KITCHEN_SCENE3_...
        skip = 8 if "SCENE10" in name else 7
        return " ".join(name[name.find("SCENE") + skip:].split("_"))
    return " ".join(name.split("_"))


_LIBERO_SUITES = {
    "libero_spatial": "One task, objects laid out differently",
    "libero_object": "Pick and place a different object each task",
    "libero_goal": "One scene, a different goal each task",
    "libero_10": "Long-horizon tasks",
    "libero_90": "Short tasks across many scenes",
}


def _libero_suites() -> list[Suite]:
    return [Suite(suite, len(names), _LIBERO_SUITES.get(suite, ""))
            for suite, names in _libero_names().items()]


def _libero_tasks(suite: str) -> list[Task]:
    names = _libero_names()
    if suite not in names:
        raise ValueError(f"LIBERO --task-suite must be one of {', '.join(names)}.")
    # The SDK loads each suite in LIBERO's default task order: <suite>/i is the i-th name.
    return [Task(f"{suite}/{i}", libero_language(name)) for i, name in enumerate(names[suite])]


# --- RoboCasa365: the task names its suites take (robocasa365_tasks.json).

_ROBOCASA_SUITES = {"atomic": "Single-step tasks", "composite": "Multi-step tasks"}


def _robocasa_suites() -> list[Suite]:
    return [Suite(suite, len(robocasa_tasks(suite)), description)
            for suite, description in _ROBOCASA_SUITES.items()]


def _robocasa_tasks(suite: str) -> list[Task]:
    return [Task(task["name"], _words(task["name"])) for task in robocasa_tasks(suite)]


# --- RoboEval: task families, each a set of environment variants.


def _roboeval_suites() -> list[Suite]:
    from .roboeval_catalog import FAMILIES

    return [Suite(name, len(family.variants), _sentence(family.instruction))
            for name, family in FAMILIES.items()]


def _roboeval_tasks(suite: str) -> list[Task]:
    from .roboeval_catalog import FAMILIES

    if suite not in FAMILIES:
        raise ValueError(f"RoboEval --task-suite must be one of {', '.join(FAMILIES)}.")
    return [Task(variant, _words(variant)) for variant in FAMILIES[suite].variants]


# --- MolmoSpaces: benchmarks whose episodes download on the first run.


def _molmospaces_episodes(suite: str) -> list[dict] | None:
    """The suite's episodes from MolmoSpaces' download cache, or None before it's there."""
    from .molmospaces_catalog import BENCHMARKS

    cache = Path(os.environ.get("MLSPACES_CACHE_DIR",
                                Path("~/.cache/molmo-spaces-resources").expanduser()))
    version, rest = BENCHMARKS[suite].path.split("/", 1)
    hits = sorted(glob.glob(str(cache / "benchmarks" / version / "*" / rest / "benchmark.json")))
    if not hits:
        return None
    try:
        with open(hits[-1]) as source:
            return json.load(source)
    except (OSError, ValueError):
        return None


def _molmospaces_suites() -> list[Suite]:
    from .molmospaces_catalog import BENCHMARKS

    rows = []
    for name, benchmark in BENCHMARKS.items():
        episodes = _molmospaces_episodes(name)
        rows.append(Suite(name, None if episodes is None else len(episodes),
                          f"{benchmark.horizon_s} s per episode"))
    return rows


def _molmospaces_tasks(suite: str) -> list[Task]:
    from .molmospaces_catalog import BENCHMARKS

    if suite not in BENCHMARKS:
        raise ValueError(f"MolmoSpaces --task-suite must be one of {', '.join(BENCHMARKS)}.")
    episodes = _molmospaces_episodes(suite)
    if episodes is None:
        raise TasksUnavailable(
            f"MolmoSpaces downloads {suite}'s episodes on its first run; list them after "
            f"`dreamscale sim molmospaces --task-id {suite}/0` has run once. A task's id is "
            f"{suite}/<episode number>.")
    return [Task(f"{suite}/{i}", _sentence(episode["language"]["task_description"]))
            for i, episode in enumerate(episodes)]


# --- RoboLab (hosted): suites are its competency axes; a task can be in several.


def _robolab_suites() -> list[Suite]:
    from .robolab_catalog import SUITES

    described = {"visual": "Color, semantics and size",
                 "relational": "Spatial, counting and conjunction",
                 "procedural": "Affordance, reorientation, sorting and stacking"}
    return [Suite(name, len(SUITES[name]), text) for name, text in described.items()]


def _robolab_tasks(suite: str) -> list[Task]:
    from .robolab_catalog import SUITES

    if suite not in SUITES or suite == "all":
        raise ValueError("RoboLab --task-suite must be one of visual, relational, procedural.")
    return [Task(name, _words(name)) for name in SUITES[suite]]


# --- ABC: the station's tasks, in no suite; --task-seed picks the scene.


def _abc_suites() -> list[Suite]:
    return []


def _abc_tasks(suite: str) -> list[Task]:
    raise ValueError("ABC has no suites: --task-id is one of its tasks, or use --all.")


def _abc_all() -> list[Task]:
    from .abc_catalog import TASKS

    return [Task(name, _words(name)) for name in TASKS]


_SUITES: dict[str, Callable[[], list[Suite]]] = {
    "libero": _libero_suites, "robocasa365": _robocasa_suites,
    "molmospaces": _molmospaces_suites, "roboeval": _roboeval_suites, "abc": _abc_suites,
    "robolab": _robolab_suites,
}
_TASKS: dict[str, Callable[[str], list[Task]]] = {
    "libero": _libero_tasks, "robocasa365": _robocasa_tasks,
    "molmospaces": _molmospaces_tasks, "roboeval": _roboeval_tasks, "abc": _abc_tasks,
    "robolab": _robolab_tasks,
}
# What each benchmark's --task-id is, for the suite list's footer.
_TASK_ID = {
    "libero": "<suite>/<number>, such as libero_spatial/0",
    "robocasa365": "a task's name",
    "molmospaces": "<benchmark>/<episode>, such as pick-v1.5/0",
    "roboeval": "a variant's name",
    "abc": "a task's name",
    "robolab": "a task's name",
}


def suites(benchmark: str) -> list[Suite]:
    return _SUITES[benchmark]()


def tasks(benchmark: str, suite: str) -> list[Task]:
    """Raises ValueError for an unknown suite, TasksUnavailable when they can't be listed."""
    return _TASKS[benchmark](suite)


def all_tasks(benchmark: str) -> list[Task]:
    """Every task in the benchmark, each once, in suite order. MolmoSpaces raises
    TasksUnavailable for a benchmark whose episodes aren't downloaded yet."""
    if benchmark == "abc":
        return _abc_all()
    if benchmark == "robolab":
        from .robolab_catalog import ROBOLAB_TASKS

        return [Task(name, _words(name)) for name in ROBOLAB_TASKS]
    listed = [task for suite in suites(benchmark) for task in tasks(benchmark, suite.id)]
    return list({task.id: task for task in listed}.values())


# --- Rendering.

_SUITE_COLUMNS = [tables.Column("--task-suite"), tables.Column("Tasks", justify="right"),
                  tables.Column("Description", drop=1, shrink=True)]
_TASK_COLUMNS = [tables.Column("--task-id"), tables.Column("Task", shrink=True)]


def _count(suite: Suite) -> str | None:
    return None if suite.tasks is None else str(suite.tasks)  # MolmoSpaces before download: —


def render_benchmarks(*, color: bool | None = None, width: int | None = None) -> list[str]:
    rows = []
    for benchmark, label in BENCHMARK_LABELS.items():
        rows.append([benchmark, label, str(len(suites(benchmark)))])
    columns = [tables.Column("Benchmark"), tables.Column("Name"),
               tables.Column("Suites", justify="right")]
    footer = [tables.hint("Suites: ", tables.command("dreamscale sim <benchmark> --list"))]
    return tables.render("Benchmarks", str(len(rows)), columns, rows, footer=footer,
                         color=color, width=width)


def render_suites(benchmark: str, *, color: bool | None = None,
                  width: int | None = None) -> list[str]:
    listed = suites(benchmark)
    if not listed:  # ABC: no suites, so its tasks
        return render_all_tasks(benchmark, color=color, width=width)
    rows = [[s.id, _count(s), Text(s.description)] for s in listed]
    footer = [
        tables.hint("Tasks: ", tables.command(
            f"dreamscale sim {benchmark} --task-suite <suite> --list")),
        tables.hint(f"--task-id is {_TASK_ID[benchmark]}."),
    ]
    return tables.render(f"{BENCHMARK_LABELS[benchmark]} suites", str(len(listed)),
                         _SUITE_COLUMNS, rows, footer=footer, color=color, width=width)


def render_tasks(benchmark: str, suite: str, *, color: bool | None = None,
                 width: int | None = None) -> list[str]:
    listed = tasks(benchmark, suite)
    footer = [tables.hint("Run one: ", tables.command(
        f"dreamscale sim {benchmark} --task-id <id> --model <model>")),
              tables.hint("Run them all: ", tables.command(
        f"dreamscale sim {benchmark} --task-suite {suite} --model <model>"))]
    return tables.render(f"{BENCHMARK_LABELS[benchmark]} {suite}", str(len(listed)),
                         _TASK_COLUMNS, [[t.id, t.task] for t in listed], footer=footer,
                         color=color, width=width)


def render_all_tasks(benchmark: str, *, color: bool | None = None,
                     width: int | None = None) -> list[str]:
    listed = all_tasks(benchmark)
    footer = [tables.hint("Run one: ", tables.command(
        f"dreamscale sim {benchmark} --task-id <id> --model <model>")),
              tables.hint("Run them all: ", tables.command(
        f"dreamscale sim {benchmark} --all --model <model>"))]
    return tables.render(f"{BENCHMARK_LABELS[benchmark]} tasks", str(len(listed)),
                         _TASK_COLUMNS, [[t.id, t.task] for t in listed], footer=footer,
                         color=color, width=width)


def run_list(benchmark: str | None, suite: str | None, *, json_output: bool = False,
             every: bool = False, print_fn: Callable[[str], None] = print) -> None:
    """``every``: the benchmark's tasks (``--list --all``); a benchmark with no suites lists
    its tasks in place of them."""
    if benchmark is None:
        if json_output:
            print_fn(json.dumps({"benchmarks": [
                {"benchmark": b, "name": label, "suites": [asdict(s) for s in suites(b)]}
                for b, label in BENCHMARK_LABELS.items()]}, indent=2))
            return
        for line in render_benchmarks():
            print_fn(line)
        return
    try:
        if suite is not None:
            listed, render = tasks(benchmark, suite), lambda: render_tasks(benchmark, suite)
        elif every or not suites(benchmark):
            listed, render = all_tasks(benchmark), lambda: render_all_tasks(benchmark)
        else:
            if json_output:
                print_fn(json.dumps({"benchmark": benchmark,
                                     "suites": [asdict(s) for s in suites(benchmark)]},
                                    indent=2))
                return
            for line in render_suites(benchmark):
                print_fn(line)
            return
    except TasksUnavailable as exc:
        if json_output:
            print_fn(json.dumps({"benchmark": benchmark, "suite": suite, "tasks": None,
                                 "task_id": str(exc)}, indent=2))
        else:
            print_fn(str(exc))
        return
    if json_output:
        print_fn(json.dumps({"benchmark": benchmark, "suite": suite,
                             "tasks": [asdict(t) for t in listed]}, indent=2))
        return
    for line in render():
        print_fn(line)
