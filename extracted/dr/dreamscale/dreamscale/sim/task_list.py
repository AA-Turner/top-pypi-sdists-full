"""`dreamscale sim [<benchmark>] --list`: the benchmarks, their suites and their tasks.

Offline and without a model or login: every row comes from the catalogs `dreamscale sim`
validates against (`benchmarks.py` and the per-benchmark catalogs). Each row's id is exactly
what `--task-suite` or `--task-id` accepts.

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

from .benchmarks import BENCHMARK_LABELS, DEFAULT_SUITES, robocasa_tasks


@dataclass(frozen=True)
class Suite:
    id: str  # the --task-suite
    tasks: int | None  # None: not known offline (MolmoSpaces before download, ABC's episodes)
    description: str = ""
    default: bool = False


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
    # The SDK loads each suite in LIBERO's default task order, so --task-id i is the i-th name.
    return [Task(str(i), libero_language(name)) for i, name in enumerate(names[suite])]


# --- RoboCasa365: the task names its suites take (robocasa365_tasks.json).

_ROBOCASA_SUITES = {"atomic": "Single-step tasks", "composite": "Multi-step tasks"}


def _robocasa_suites() -> list[Suite]:
    return [Suite(suite, len(robocasa_tasks(suite)), description)
            for suite, description in _ROBOCASA_SUITES.items()]


def _robocasa_tasks(suite: str) -> list[Task]:
    # --task-id takes the name or its index; the name says what the task is.
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
    return [Task(str(i), variant) for i, variant in enumerate(FAMILIES[suite].variants)]


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

    rows = [Suite("all", None, "Every benchmark below")]
    for name, benchmark in BENCHMARKS.items():
        episodes = _molmospaces_episodes(name)
        rows.append(Suite(name, None if episodes is None else len(episodes),
                          f"{benchmark.horizon_s} s per episode"))
    return rows


def _molmospaces_tasks(suite: str) -> list[Task]:
    from .molmospaces_catalog import selected_suites

    if suite.lower() == "all":
        raise TasksUnavailable(
            "MolmoSpaces --task-suite all runs the same --task-id (an episode number, or all) "
            "in every benchmark. List one benchmark's episodes with --task-suite <benchmark>.")
    (name,) = selected_suites(suite)
    episodes = _molmospaces_episodes(name)
    if episodes is None:
        raise TasksUnavailable(
            f"MolmoSpaces downloads {name}'s episodes on its first run; list them after "
            f"`dreamscale sim molmospaces --task-suite {name}` has run once. --task-id is an "
            "episode number, or all.")
    return [Task(str(i), _sentence(episode["language"]["task_description"]))
            for i, episode in enumerate(episodes)]


# --- ABC: the station's tasks; --task-id is an episode (a seeded scene), any number.


def _abc_suites() -> list[Suite]:
    from .abc_catalog import TASKS

    return [Suite(name, None, _words(name)) for name in TASKS]


def _abc_tasks(suite: str) -> list[Task]:
    from .abc_catalog import SEED, TASKS

    if suite not in TASKS:
        raise ValueError(f"ABC --task-suite must be one of {', '.join(TASKS)}.")
    raise TasksUnavailable(
        f"ABC's --task-id is an episode number, 0 or more: episode N is {suite} in the scene "
        f"seeded {SEED} + N.")


_SUITES: dict[str, Callable[[], list[Suite]]] = {
    "libero": _libero_suites, "robocasa365": _robocasa_suites,
    "molmospaces": _molmospaces_suites, "roboeval": _roboeval_suites, "abc": _abc_suites,
}
_TASKS: dict[str, Callable[[str], list[Task]]] = {
    "libero": _libero_tasks, "robocasa365": _robocasa_tasks,
    "molmospaces": _molmospaces_tasks, "roboeval": _roboeval_tasks, "abc": _abc_tasks,
}
# What each benchmark's --task-id is, for the suite list's footer.
_TASK_ID = {
    "libero": "the task's number in its suite",
    "robocasa365": "a task's name, or its number in the suite",
    "molmospaces": "an episode number, or all",
    "roboeval": "the variant's number or name",
    "abc": "an episode number, 0 or more",
}


def suites(benchmark: str) -> list[Suite]:
    default = DEFAULT_SUITES.get(benchmark)
    return [Suite(s.id, s.tasks, s.description, s.id == default) for s in _SUITES[benchmark]()]


def tasks(benchmark: str, suite: str) -> list[Task]:
    """Raises ValueError for an unknown suite, TasksUnavailable when they can't be listed."""
    return _TASKS[benchmark](suite)


# --- Rendering.

_SUITE_COLUMNS = [tables.Column("--task-suite"), tables.Column("Tasks", justify="right"),
                  tables.Column("Description", drop=1, shrink=True)]
_TASK_COLUMNS = [tables.Column("--task-id"), tables.Column("Task", shrink=True)]


def _count(suite: Suite, benchmark: str) -> str | None:
    if suite.tasks is not None:
        return str(suite.tasks)
    return "any" if benchmark == "abc" else None  # MolmoSpaces before its download: —


def render_benchmarks(*, color: bool | None = None, width: int | None = None) -> list[str]:
    rows = []
    for benchmark, label in BENCHMARK_LABELS.items():
        listed = suites(benchmark)
        rows.append([benchmark, label, str(len([s for s in listed if s.id != "all"]))])
    columns = [tables.Column("Benchmark"), tables.Column("Name"),
               tables.Column("Suites", justify="right")]
    footer = [tables.hint("Suites: ", tables.command("dreamscale sim <benchmark> --list"))]
    return tables.render("Benchmarks", str(len(rows)), columns, rows, footer=footer,
                         color=color, width=width)


def render_suites(benchmark: str, *, color: bool | None = None,
                  width: int | None = None) -> list[str]:
    listed = suites(benchmark)
    rows = [[s.id, _count(s, benchmark),
             Text(s.description).append("  (default)" if s.default else "",
                                               style=tables.DIM)]
            for s in listed]
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
        f"dreamscale sim {benchmark} --task-suite {suite} --task-id <id> --model <model>"))]
    return tables.render(f"{BENCHMARK_LABELS[benchmark]} {suite}", str(len(listed)),
                         _TASK_COLUMNS, [[t.id, t.task] for t in listed], footer=footer,
                         color=color, width=width)


def run_list(benchmark: str | None, suite: str | None, *, json_output: bool = False,
             print_fn: Callable[[str], None] = print) -> None:
    if benchmark is None:
        if json_output:
            print_fn(json.dumps({"benchmarks": [
                {"benchmark": b, "name": label, "suites": [asdict(s) for s in suites(b)]}
                for b, label in BENCHMARK_LABELS.items()]}, indent=2))
            return
        for line in render_benchmarks():
            print_fn(line)
        return
    if suite is None:
        if json_output:
            print_fn(json.dumps({"benchmark": benchmark,
                                 "suites": [asdict(s) for s in suites(benchmark)]}, indent=2))
            return
        for line in render_suites(benchmark):
            print_fn(line)
        return
    try:
        lines = render_tasks(benchmark, suite) if not json_output else None
        listed = tasks(benchmark, suite) if json_output else None
    except TasksUnavailable as exc:
        if json_output:
            print_fn(json.dumps({"benchmark": benchmark, "suite": suite, "tasks": None,
                                 "task_id": str(exc)}, indent=2))
        else:
            print_fn(str(exc))
        return
    if listed is not None:
        print_fn(json.dumps({"benchmark": benchmark, "suite": suite,
                             "tasks": [asdict(t) for t in listed]}, indent=2))
        return
    for line in lines:
        print_fn(line)
