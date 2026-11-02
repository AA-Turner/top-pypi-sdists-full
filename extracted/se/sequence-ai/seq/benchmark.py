"""
`@seq.benchmark` - a benchmark is the env you already have, run as it is.

In one sentence: your class is built by its own constructor after the machine's snapshot - init= its arguments,
"{num_worlds}" how many worlds this eval builds and "{policy.hz}" the evaluated policy's rate - and you mark two of its
methods, @seq.reset starting an episode of a task at a seed and returning its first observation, @seq.step playing one
action and returning (observation, done, success), and declare its tasks, its seeds and how long an episode may run
→ `seq deploy` registers it → an eval resets each episode, hands every observation to the policy as a robot's own code
would and steps the env with the actions that come back. The platform reads none of the observations or actions: they
go to the policy, and come from it, as a robot's do.
WHY a black box: "think from a black box perspective for the benchmarks as well, like the policies." (the user 10-24) -
the platform has no types of its own for a benchmark's observations or actions.

Introspection → `BenchmarkRegistration` lives in `benchmark_registry.py`, symmetric to `registry.py` for policies.
"""
from __future__ import annotations

from typing import Any, Callable, TypeVar

from seq.errors import BenchmarkDefinitionError

_T = TypeVar("_T", bound=type)


_ALLOWED_KWARGS = frozenset({
    "name", "image", "gpu", "cpu", "memory", "secrets",

    "freeze",

    "assets",


    "replay", "engine",




    "driver",



    "tasks", "seeds", "max_seconds",


    "init",
})

def _reject_bad_kwargs(kwargs: dict[str, Any]) -> None:
    for name in kwargs:
        if name not in _ALLOWED_KWARGS:
            raise BenchmarkDefinitionError(
                f"@seq.benchmark got unknown argument {name!r}; allowed: {', '.join(sorted(_ALLOWED_KWARGS))}"
            )


def benchmark(*args: Any, **kwargs: Any) -> Callable[[_T], _T]:
    """`@seq.benchmark(tasks={name: description}, seeds=range(50), max_seconds=15.0, gpu="L4", ...)` on your class -
    the env as it is, or a short one built on it - capture the declaration and register.

    - `tasks`: each task an episode can be of, by the name @seq.reset is handed and an eval chooses it by (--tasks),
      with what it asks of the robot, shown beside it ("" for none): what a name means is your env's own.
    - `seeds`: the seeds an episode starts at; trial k of a task runs seeds[k % len(seeds)].
    - `max_seconds`: how long an episode may run on the robot's clock, the same for every task or {task: seconds}.

    - `init`: its constructor's arguments, a dict by name or a list by position - "{num_worlds}" how many worlds this eval
      builds, "{policy.<field>}" what the evaluated policy declares (hz, action_chunk_valid_len, action_chunk_replan_at; at
      the registration check none is, and a keyword argument that is one alone is left out, its default holding).

    Its class is built by its constructor after the machine's snapshot, its cameras opened there too; its file is
    imported before, so work alike for every eval goes at its module's top. Its methods: `@seq.reset def start(self,
    task, seed)` returns an episode's first observation; `@seq.step def play(self, action)` returns (observation,
    done, success), or (observation, done, success, metrics). Its constructor's other arguments with a default are the
    settings an eval may change (--param benchmark.NAME=VALUE). A vectorized env puts `@seq.concurrent(sizes=[N])` on
    its step, N the most worlds one call steps: its reset is then `start(self, worlds, tasks, seeds)`, its step
    `play(self, worlds, actions)` returning one tuple a world, and init= hands its constructor how many worlds to
    build, "{num_worlds}".

    WHY it must be called with parens (never bare `@seq.benchmark`): a benchmark has no valid zero-arg form (tasks,
    seeds and max_seconds are required), so a bare application is always a mistake - same discipline as `@seq.policy`.
    """
    from seq._partial import keeping, refused



    if args:
        error = BenchmarkDefinitionError(
            "@seq.benchmark must be called with arguments: @seq.benchmark(tasks={name: description}, seeds=[...], "
            "max_seconds=...)"
        )
        if len(args) == 1 and isinstance(args[0], type) and not kwargs and keeping():
            from seq.benchmark_registry import _BENCH_ATTR

            return refused(args[0], _BENCH_ATTR, error)
        raise error
    try:
        _reject_bad_kwargs(kwargs)
        bad = None
    except BenchmarkDefinitionError as exc:
        if not keeping():
            raise
        bad = exc

    def decorator(cls: _T) -> _T:

        from seq.benchmark_registry import _BENCH_ATTR, build_benchmark_registration

        if bad is not None:
            return refused(cls, _BENCH_ATTR, bad)
        from seq.freeze import declare

        return build_benchmark_registration(declare(cls, kwargs, BenchmarkDefinitionError),
                                            {k: v for k, v in kwargs.items() if k != "freeze"})

    return decorator
