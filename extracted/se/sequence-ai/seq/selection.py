"""
Which episodes an eval runs, as `seq eval run` and `seq.eval()` take it: the tasks, a count of each task's declared
seeds (`trials`, the first N) or the seeds by name (`seeds`) - once for every chosen task, or per task, "*" for the
rest - turned into the request's own types. Ranges are expanded into lists here, so the platform sees one shape.

In one sentence: `--trials 10` / `--trials libero_spatial/3=20,*=5` → an int or {task: int}; `--seeds 10-19` /
`--seeds libero_spatial/3=10-19,libero_spatial/7=0,4` → a list or {task: [seed]} → the request's `trials` and `seeds` →
the platform picks each chosen task's seeds by its rules and refuses a task or seed the benchmark does not declare,
naming the ones it does. Whether a task or a seed is the benchmark's is the platform's to say: only the shape is
checked here.

"""
from __future__ import annotations

import re
from typing import Any

from sequence_ai.errors import InvalidRequest


MAX_SEEDS = 5000
MAX_TASKS = 1000
MAX_TRIALS = 100000
_SPAN = re.compile(r"^\s*(\d+)\s*(?:-\s*(\d+)\s*)?$")
TRIALS_FORM = "a count (10), or TASK=COUNT entries with '*' for the rest (libero_spatial/3=20,*=5)"
SEEDS_FORM = ("seeds for every task (10-19, or 0,4,10-19), or TASK=SEEDS entries with '*' for the rest "
              "(libero_spatial/3=10-19,libero_spatial/7=0,4)")


def _span(text: str, where: str) -> list[int]:
    """'10-19' → [10, ..., 19]; '7' → [7]. A range runs low to high, both ends in."""
    m = _SPAN.match(text)
    if not m:
        raise InvalidRequest(f"{where}: {text.strip()!r} is not a seed or a range of seeds (10, 10-19)")
    low, high = int(m.group(1)), int(m.group(2) if m.group(2) is not None else m.group(1))
    if high < low:
        raise InvalidRequest(f"{where}: {text.strip()!r} runs backwards; write the low seed first ({high}-{low})")
    if high - low + 1 > MAX_SEEDS:
        raise InvalidRequest(f"{where}: {text.strip()!r} is {high - low + 1} seeds; at most {MAX_SEEDS}")
    return list(range(low, high + 1))


def seed_list(parts: list[str], where: str) -> list[int]:
    """Seeds and ranges in the order written, each seed once, at most MAX_SEEDS."""
    out: list[int] = []
    for part in parts:
        for seed in _span(part, where):
            if seed not in out:
                out.append(seed)
    if len(out) > MAX_SEEDS:
        raise InvalidRequest(f"{where}: {len(out)} seeds; at most {MAX_SEEDS}")
    return out


def _entries(text: str, flag: str, form: str) -> list[tuple[str, list[str]]]:
    """'a=1,b=2' → [("a", ["1"]), ("b", ["2"])]; a part without '=' goes on the entry before it (a seed list).
    Each task once."""
    out: list[tuple[str, list[str]]] = []
    for part in text.split(","):
        key, sep, value = part.partition("=")
        if sep:
            if not key.strip():
                raise InvalidRequest(f"{flag}: {part!r} names no task; {flag} takes {form}")
            if any(k == key.strip() for k, _ in out):
                raise InvalidRequest(f"{flag}: {key.strip()} is given twice")
            out.append((key.strip(), [value]))
        elif out and part.strip():
            out[-1][1].append(part)
        else:
            raise InvalidRequest(f"{flag}: {text!r} mixes a value for every task with TASK=... entries; {flag} takes "
                                 f"{form}")
    if len(out) > MAX_TASKS:
        raise InvalidRequest(f"{flag}: {len(out)} tasks; at most {MAX_TASKS}")
    return out


def _count(text: str, where: str) -> int:
    try:
        n = int(text.strip())
    except ValueError:
        raise InvalidRequest(f"{where}: {text.strip()!r} is not a count; it takes {TRIALS_FORM}") from None
    if not 1 <= n <= MAX_TRIALS:
        raise InvalidRequest(f"{where}: {n} is not a count of 1 to {MAX_TRIALS}")
    return n


def parse_trials(text: str) -> int | dict[str, int]:
    """`--trials`: '10' → 10 (every chosen task ten times: its declared seeds in order, then again as repeated
    starts); 'libero_spatial/3=20,*=5' → {"libero_spatial/3": 20, "*": 5} (task 3 twenty, every other
    chosen task five)."""
    if "=" not in text:
        return _count(text, "--trials")
    return {task: _count(",".join(values), f"--trials {task}") for task, values in _entries(text, "--trials",
                                                                                             TRIALS_FORM)}


def parse_seeds(text: str) -> list[int] | dict[str, list[int]]:
    """`--seeds`: '10-19' or '0,4,10-19' → those seeds of every chosen task;
    'libero_spatial/3=10-19,libero_spatial/7=0,4' → per task (a part with no '=' goes on listing the seeds of the task
    before it)."""
    if "=" not in text:
        return seed_list(text.split(","), "--seeds")
    return {task: seed_list(values, f"--seeds {task}") for task, values in _entries(text, "--seeds", SEEDS_FORM)}


def _ints(value: Any, where: str) -> list[int]:
    """Seeds as given to seq.eval(): a list or range of ints, or the CLI's text ('10-19', '0,4,10-19')."""
    if isinstance(value, str):
        return seed_list(value.split(","), where)
    try:
        seeds = list(value)
    except TypeError:
        raise InvalidRequest(f"{where} is a list of seeds (or '10-19'), got {type(value).__name__}") from None
    if any(isinstance(s, bool) or not isinstance(s, int) for s in seeds):
        raise InvalidRequest(f"{where}: every seed is an int")
    if len(seeds) > MAX_SEEDS:
        raise InvalidRequest(f"{where}: {len(seeds)} seeds; at most {MAX_SEEDS}")
    return seeds


def trials_value(value: Any) -> int | dict[str, int] | None:
    """seq.eval(trials=): an int, {task: int} ('*' for the rest), or the CLI's text."""
    if value is None:
        return None
    if isinstance(value, str):
        return parse_trials(value)
    if isinstance(value, dict):
        if len(value) > MAX_TASKS:
            raise InvalidRequest(f"trials names {len(value)} tasks; at most {MAX_TASKS}")
        return {str(k): _count(str(v), f"trials[{k!r}]") if not isinstance(v, bool) else _count("x", "trials")
                for k, v in value.items()}
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidRequest(f"trials is a count or {{task: count}}, got {type(value).__name__}")
    return _count(str(value), "trials")


def seeds_value(value: Any) -> list[int] | dict[str, list[int]] | None:
    """seq.eval(seeds=): a list or range of seeds, {task: seeds} ('*' for the rest), or the CLI's text."""
    if value is None:
        return None
    if isinstance(value, str):
        return parse_seeds(value)
    if isinstance(value, dict):
        if len(value) > MAX_TASKS:
            raise InvalidRequest(f"seeds names {len(value)} tasks; at most {MAX_TASKS}")
        return {str(k): _ints(v, f"seeds[{k!r}]") for k, v in value.items()}
    return _ints(value, "seeds")


def tasks_value(value: Any) -> list[str] | None:
    """seq.eval(tasks=) / --tasks: the tasks to run, each once ('a,b' or a list)."""
    if value is None:
        return None
    tasks = [t.strip() for t in value.split(",")] if isinstance(value, str) else [str(t).strip() for t in value]
    tasks = [t for t in tasks if t]
    if len(set(tasks)) != len(tasks):
        raise InvalidRequest("tasks: a task is named twice")
    if len(tasks) > MAX_TASKS:
        raise InvalidRequest(f"tasks: {len(tasks)} tasks; at most {MAX_TASKS}")
    return tasks or None
