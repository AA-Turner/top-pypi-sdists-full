"""
The class-level decorators: `@seq.policy(...)` (infra spec + registration) and `@seq.concurrent(...)` (the
sole concurrency entrypoint).

WHY `@seq.policy` is where registration happens: applying it is the "registration time" the goal keeps
referring to — the moment we introspect the class, validate everything, and attach a `PolicyRegistration`.
Everything that is malformed is rejected HERE, not deferred to when the harness loads the class.



"""
from __future__ import annotations

import sys
from typing import Any, Callable, TypeVar



from sequence_base.constants.limits import MAX_ENVS

from seq.errors import PolicyDefinitionError

_T = TypeVar("_T", bound=type)






_ALLOWED_KWARGS = frozenset({
    "gpu", "image", "weights", "secrets", "deps",


    "freeze",



    "min_workers", "buffer_workers", "max_gpus",


    "region",






    "hz", "action_chunk_valid_len", "action_chunk_replan_at",



    "cpu", "memory",

    "timeouts",




    "name", "io",


    "models",


    "family",




    "gpus_per_replica", "replica_start",


    "tensors",



    "init",
})


_NOT_A_KWARG = {
    "concurrency": "@seq.concurrent(sizes=[1, 2, 4, 8]) on the @seq.infer method",
}



PLAYS_HOW = ("@seq.policy(hz=15, action_chunk_valid_len=15, action_chunk_replan_at=8) - hz the steps a second its "
             "answers play at, action_chunk_valid_len the steps of an answer that are valid, action_chunk_replan_at the "
             "step, counted from when its act is sent, at which its robot asks for the next answer (its last valid "
             "step when unset)")


HZ_NEEDED = f"@seq.policy needs hz=, the steps a second its answers play at: {PLAYS_HOW}"


def _reject_bad_kwarg_names(kwargs: dict[str, Any]) -> None:
    """Raise a readable error for any not-a-kwarg / unknown name, BEFORE building the spec.

    WHY name-check before pydantic: pydantic's `extra=forbid` would also reject unknowns, but with a generic message. A
    user who typed `gpuu=` deserves to be told the names there are. region= names the platform's regions now
    (registry.region_of), never a provider's.
    """
    for name in kwargs:

        if name in _NOT_A_KWARG:
            raise PolicyDefinitionError(
                f"{name!r} is not a @seq.policy argument; use {_NOT_A_KWARG[name]}"
            )


        if name not in _ALLOWED_KWARGS:
            raise PolicyDefinitionError(
                f"@seq.policy got unknown argument {name!r}; "
                f"allowed: {', '.join(sorted(_ALLOWED_KWARGS))}"
            )





CONCURRENT_WHAT = ("the batch sizes its infer is called with, ascending, 1 first: a copy seats as many robots as the "
                   "largest of them whose batch answers within the time one answer plays")
CONCURRENT_HOW = f"write @seq.concurrent(sizes=[1, 2, 4, 8]) on the @seq.infer method - {CONCURRENT_WHAT}"
_MOST = 256

def policy_sizes(sizes: Any) -> list[int]:
    """A policy's batch sizes as `@seq.concurrent(sizes=...)` lists them on its infer: whole numbers from 1 to _MOST,
    each once, ascending, 1 first - an act that finds no other robot's to join goes as a batch of 1."""
    if (not isinstance(sizes, (list, tuple)) or not sizes
            or any(isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= _MOST for n in sizes)):
        raise PolicyDefinitionError(f"@seq.concurrent(sizes=...) lists whole numbers from 1 to {_MOST}, got {sizes!r}: "
                                    f"{CONCURRENT_HOW}")
    listed = list(sizes)
    if listed != sorted(set(listed)) or listed[0] != 1:
        raise PolicyDefinitionError(
            f"@seq.concurrent(sizes={listed!r}) lists each size once, ascending, 1 first - sizes="
            f"{sorted({1, *listed})}: an act that finds no other robot's to join goes as a batch of 1")
    return listed


def concurrent(fn: Any = None, *, sizes: Any = None) -> Callable[[Any], Any]:
    """`@seq.concurrent(sizes=[1, 2, 4, 8])` on the `@seq.infer` method (above or below it) - how one worker serves
    robots. Without it a worker serves one robot a copy, infer taking one observation, as ever. With it infer takes a
    list - the acts that run together, in the sizes it lists alone (each 1 to 256, ascending, 1 first: what its own
    code is built for, which only its author knows; a JAX policy compiles each) - and returns a list of chunks in the
    same order. Its worker warms each listed size before it serves, timing it and the GPU memory it holds, on the class's
    sample episode (@seq.sample), which it needs. A copy seats as many robots as the largest listed size whose batch
    answers within the time its robots can wait for an answer - the steps from action_chunk_replan_at to
    action_chunk_valid_len, at hz (@seq.policy) - and holds an early act within that time, so they fall into one batch;
    acts that fill no listed size go as the sizes that fit them (3 of [1, 2, 4] as 2, then 1); a policy that asks at
    its last valid step, or declares no action_chunk_valid_len, batches no robots, one robot a copy. When no copy can take a new robot, another worker starts within
    max_gpus. An eval batches its environments' acts in the listed sizes. On a vectorized benchmark's `@seq.step` it is
    one number, `@seq.concurrent(sizes=[N])`: the most worlds one call steps.

    The declaration rides on the function (`__seq_concurrent__`) and `@seq.policy` puts it into the deploy request
    (PolicySpec.concurrency). gpus_per_replica and replica_start are `@seq.policy(...)` arguments.


"""

    if fn is not None or sizes is None:
        raise PolicyDefinitionError(f"@seq.concurrent needs sizes: {CONCURRENT_HOW}")
    if (not isinstance(sizes, (list, tuple)) or not sizes
            or any(isinstance(n, bool) or not isinstance(n, int) or n < 1 for n in sizes)):

        raise PolicyDefinitionError(f"@seq.concurrent(sizes=...) on a policy's infer lists whole numbers from 1 to "
                                    f"{_MOST}, got {sizes!r}: {CONCURRENT_HOW}. On a vectorized benchmark's @seq.step "
                                    f"it is one number from 1 to {MAX_ENVS}, the most worlds one call steps: "
                                    "@seq.concurrent(sizes=[64])")



    declared = {"sizes": list(sizes)}

    def decorator(target: Any) -> Any:

        if isinstance(target, type):
            raise PolicyDefinitionError(f"@seq.concurrent goes on the @seq.infer method, not on the class "
                                        f"{target.__name__}: {CONCURRENT_HOW}. gpus_per_replica and replica_start are "
                                        "@seq.policy(...) arguments")

        getattr(target, "raw_fn", target).__seq_concurrent__ = dict(declared)
        return target

    return decorator


def _first_error(exc: Exception) -> str:
    """A pydantic ValidationError's first message, without pydantic's URL footer; any other exception as itself."""
    errors = getattr(exc, "errors", None)
    if callable(errors):
        try:
            first = errors()[0]
            where = ".".join(str(p) for p in first.get("loc") or ())
            return f"{where}: {first['msg']}" if where else str(first["msg"])
        except Exception:
            pass
    return str(exc)



def policy(*args: Any, **kwargs: Any) -> Callable[[_T], _T]:
    """`@seq.policy(gpu=..., weights=..., ...)` — capture the infra declaration and register the class.

    WHY it must be called with parens (never bare `@seq.policy`): a policy has no valid zero-arg form — at
    minimum `gpu` is required — so a bare application is always a mistake.
    """
    from seq._partial import keeping, refused



    if args:
        error = PolicyDefinitionError(
            "@seq.policy must be called with arguments: @seq.policy(gpu=..., weights=..., ...)"
        )
        if len(args) == 1 and isinstance(args[0], type) and not kwargs and keeping():
            from seq.registry import _REG_ATTR

            return refused(args[0], _REG_ATTR, error)
        raise error
    try:
        _reject_bad_kwarg_names(kwargs)
        if "hz" not in kwargs:
            raise PolicyDefinitionError(HZ_NEEDED)
        bad = None
    except PolicyDefinitionError as exc:
        if not keeping():
            raise
        bad = exc

    def decorator(cls: _T) -> _T:


        from seq.registry import _REG_ATTR, applied_by, build_registration

        if bad is not None:
            return refused(cls, _REG_ATTR, bad)
        from seq.freeze import declare



        return build_registration(declare(cls, kwargs, PolicyDefinitionError), {k: v for k, v in kwargs.items()
                                                                                if k != "freeze"},
                                  applied=applied_by(sys._getframe(1)))

    return decorator
