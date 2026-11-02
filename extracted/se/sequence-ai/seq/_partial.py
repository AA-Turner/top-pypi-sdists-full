"""
The `_PartialFunction` + `SeqFlags` bitmask + `.stack()` merge.

WHY one wrapper with a flag bitmask instead of a class per decorator: stacking two lifecycle decorators on
one method must MERGE into a single object carrying both flag bits, not create two competing wrappers: one
`_PartialFunction`, one `IntFlag`, a `.stack()` that ORs flags and merges params.

The flags themselves live in `sequence_base`, imported here — the SDK never redefines them, so the
bits it writes are byte-identical to the bits the harness reads back.


"""
from __future__ import annotations

import contextlib
import contextvars
import inspect
from typing import Any, Callable, Iterator, NoReturn

from seq.errors import PolicyDefinitionError
from sequence_base.by_name import wake_on_refused
from sequence_base.contract import SeqFlags


class _PartialFunction:
    """A lifecycle-decorated method, pre-registration: the raw function + the flag bits it was tagged with
    + any per-binding params (only `@seq.plan` has one: `every_s`). `@seq.policy` consumes these, records
    the bindings, and restores `raw_fn` as the class attribute so the class is a normal, callable class."""

    __slots__ = ("raw_fn", "flags", "params")

    def __init__(self, raw_fn: Callable[..., Any], flags: SeqFlags, params: dict[str, Any]) -> None:
        self.raw_fn = raw_fn
        self.flags = flags

        self.params = dict(params)

    def stack(self, flags: SeqFlags, params: dict[str, Any]) -> "_PartialFunction":
        """Merge another decorator's flags/params into this one.

        WHY OR the flags: two lifecycle decorators on the SAME method mean that one method serves both
        lifecycle roles, so the resulting binding must carry both bits (goal 8). Params are merged too so
        e.g. `@seq.plan(every_s=..)` stacked with `@seq.infer` keeps the cadence.

        """
        self.flags |= flags
        self.params.update(params)
        return self

    def members(self) -> list[SeqFlags]:
        """The single-bit flags set on this method, lowest bit first. Iterating the flag value itself does this only
        from Python 3.11 on, and `seq` runs on 3.10.
"""
        return sorted((m for m in SeqFlags if m in self.flags), key=lambda m: m.value)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calling a partial directly is always a mistake — it means either a bare module-level function
        was decorated (no `@seq.policy` class to consume it) or the class was never decorated. Fail loud
        here rather than silently doing the wrong thing.

        """
        raise PolicyDefinitionError(
            f"{getattr(self.raw_fn, '__name__', self.raw_fn)!r} is a @seq.* lifecycle stub; it only works "
            "as a method of a class decorated with @seq.policy, @seq.planner, @seq.benchmark or @seq.adapter"
        )


_KEPT: contextvars.ContextVar[bool] = contextvars.ContextVar("seq_refusals_kept", default=False)


@contextlib.contextmanager
def refusals_kept() -> Iterator[None]:
    """While seq imports a user's file (seq.loading: `seq deploy`, its dry run, `seq eval`, `seq adapter check`), a
    class whose declaration @seq.policy or @seq.benchmark refuses keeps its refusal (Refused) instead of raising it
    into the import - the file's other classes are defined, and the refusal is raised where that class is used."""
    token = _KEPT.set(True)
    try:
        yield
    finally:
        _KEPT.reset(token)


def keeping() -> bool:
    """Whether a refused declaration is kept on its class rather than raised where it is written: while seq imports a
    file (refusals_kept), and on the platform, which imports the user's module to serve or run one class of it.
    Anywhere else - a test, a notebook, `python file.py` - the decorator raises it at once, as it always has: the
    readable error where the class is written."""
    from seq.image import _on_platform

    return _KEPT.get() or _on_platform()


class Refused:
    """What @seq.policy or @seq.benchmark kept of a class whose declaration it refused (keeping): the refusal, raised
    again wherever the class is used - its registration read, its deploy, its dry run - and the hooks it had found
    (`found`, flag -> method name), which a class built on it still inherits. Anything else read of it, as of a
    registration (`.spec`, `.bindings`), is the refusal itself.

    WHY not raise in the decorator there: an error at the decorator stops the import of the whole file, so no other
    class in it could be deployed or dry-run either - RoboDojo, beside a RoboDojoEE missing a hook - nor served on the
    platform, which imports the file. Kept on the class, the error is the class's own.
 
"""

    __slots__ = ("error", "found", "found_every_s")

    def __init__(self, error: Exception, found: dict[SeqFlags, str] | None = None,
                 found_every_s: float | None = None) -> None:
        self.error = error
        self.found = dict(found or {})
        self.found_every_s = found_every_s

    def refuse(self) -> NoReturn:
        raise self.error.with_traceback(None)

    def __getattr__(self, name: str) -> Any:
        self.refuse()


def refused(cls: type, attr: str, error: Exception, found: dict[SeqFlags, str] | None = None,
            found_every_s: float | None = None) -> type:
    """`cls`, its declaration's refusal kept under `attr` (Refused), to be raised when it is used."""
    setattr(cls, attr, Refused(error, found, found_every_s))
    return cls


def hooks_along(cls: type, attr: str, refuse: Callable[[str], Exception],
                what: str = "lifecycle") -> tuple[dict[SeqFlags, str], float | None]:
    """`cls`'s lifecycle hooks, found along its classes as Python finds its methods (its MRO), the nearest winning:
    each base registered under `attr` (its registration, or what a refusal found) brings its bindings, a base never
    registered - a mixin - its decorated methods, and `cls` its own; each flag is bound to the name of the nearest
    method declaring it, which an override of that name keeps. Returns (bindings, the PLAN hook's every_s).

    Raw functions are restored on `cls` alone - its own decorated methods, and a mixin's it reaches - never on a base,
    which stays as it was for the next class built on it. Two methods of one class tagged with one flag are `refuse`d.

    WHY along the MRO: `class RoboDojoEE(RoboDojo)` had none of RoboDojo's hooks - only the class's own attributes were
    read, and RoboDojo's decoration had already turned its methods back into plain functions - and `reset =
    RoboDojo.reset` in its body did not count either.
    """
    bindings: dict[SeqFlags, str] = {}
    every_s: float | None = None
    for klass in reversed(cls.__mro__):
        here: dict[SeqFlags, str] = {}
        reg = klass.__dict__.get(attr) if klass is not cls else None
        if reg is not None:
            here.update(reg.found if isinstance(reg, Refused) else reg.bindings)
            if SeqFlags.PLAN in here:
                every_s = reg.found_every_s if isinstance(reg, Refused) else getattr(reg, "plan_every_s", None)
        for name, value in list(klass.__dict__.items()):
            if not isinstance(value, _PartialFunction):
                continue
            for member in value.members():
                if member in here and here[member] != name:
                    raise refuse(f"{klass.__name__}: {member.name} is bound to both {here[member]!r} and {name!r}; "
                                 f"each {what} flag maps to exactly one method")
                here[member] = name
                if member is SeqFlags.PLAN:
                    every_s = value.params.get("every_s")
            if klass is cls:
                setattr(cls, name, value.raw_fn)
        bindings.update(here)
    for name in set(bindings.values()):
        reached = inspect.getattr_static(cls, name, None)
        if isinstance(reached, _PartialFunction):
            setattr(cls, name, reached.raw_fn)
    return bindings, every_s


def hook(cls: type, name: str) -> Any:
    """The method a binding names, as `cls` reaches it - its own, or one it inherits."""
    return inspect.getattr_static(cls, name, None)


def _as_partial(target: Any, flags: SeqFlags, params: dict[str, Any]) -> _PartialFunction:
    """Turn a decoration target into a `_PartialFunction`, or stack onto an existing one.

    WHY the isinstance checks: `@staticmethod`/`@classmethod` objects and non-callables are not valid
    lifecycle entrypoints — the harness calls a bound instance method, so a staticmethod cannot be one.
    Rejecting here (decoration time) is the readable-error contract.

    """

    if isinstance(target, _PartialFunction):
        return target.stack(flags, params)

    if isinstance(target, (staticmethod, classmethod)):
        kind = type(target).__name__
        raise PolicyDefinitionError(
            f"@seq lifecycle decorators cannot be applied to a {kind}; a lifecycle entrypoint must be a "
            "plain instance method"
        )

    if not callable(target):
        raise PolicyDefinitionError(
            f"@seq lifecycle decorators must wrap a method, got {type(target).__name__}"
        )
    return _PartialFunction(target, flags, params)


def _lifecycle(flag: SeqFlags) -> Callable[[Any], _PartialFunction]:
    """Build a bare lifecycle decorator (`@seq.infer`, `@seq.shutdown`, ...) for one flag."""

    def decorator(target: Any) -> _PartialFunction:
        return _as_partial(target, flag, {})

    return decorator




infer = _lifecycle(SeqFlags.INFER)
on_episode = _lifecycle(SeqFlags.ON_EPISODE)




observe = _lifecycle(SeqFlags.OBSERVE)
sample = _lifecycle(SeqFlags.SAMPLE)
shutdown = _lifecycle(SeqFlags.SHUTDOWN)







reset = _lifecycle(SeqFlags.RESET)
step = _lifecycle(SeqFlags.STEP)






observation = _lifecycle(SeqFlags.OBSERVE)
action = _lifecycle(SeqFlags.ACTION)

def _validate_every_s(every_s: Any) -> float:
    """`@seq.plan(every_s=..)` cadence must be a positive number; reject non-numeric / <=0 at decoration.

    WHY reject `bool`: `bool` is a subclass of `int`, so `True` would sneak through an `isinstance(_, int)`
    check and become `every_s=1.0` silently — a cadence is never a boolean.

    """
    if isinstance(every_s, bool) or not isinstance(every_s, (int, float)):
        raise PolicyDefinitionError(
            f"@seq.plan(every_s=...) must be a number, got {type(every_s).__name__}"
        )
    if every_s <= 0:
        raise PolicyDefinitionError(f"@seq.plan(every_s=...) must be > 0, got {every_s}")
    return float(every_s)


def plan(fn: Any = None, *, every_s: Any = None, wake_on: Any = None) -> Callable[[Any], _PartialFunction]:
    """`@seq.plan(every_s=SECONDS, wake_on=[KEY, ...])` — a planner's one method (@seq.planner), `def plan(self, group)`,
    plain or async. The platform calls it on the planner's own clock - every_s from one plan's start to the next, one
    plan at a time (one that runs past its tick is followed by the next the moment it returns) - handed the group:
    group.members, each a policy (m.robots, each robot's id and episode, r.id and r.state) or a planner below (m.state,
    what it hands up), and group.state, the planner's own record. What it returns, {id: value} keyed by a robot's r.id
    or a planner member's m.id, is written where that robot's policy reads it, its episode.state["seq.plans"], or into
    that planner's group.state["seq.plans"]; None writes nothing. A plan that raises is noted in the worker's log and
    called again at the next tick. `wake_on`: top-level keys whose arrival plans at once, the clock going on beside as
    the fallback - of what is observed into the planner, or by a policy member's robots, and "seq.plans", a plan from the
    planner above. The worker reads wake_on off the method, where it is stashed as `__seq_plan_wake_on__`. On a
    @seq.policy it is refused: a policy is planned by a planner that names it.


    WHY a separate binding from `@seq.infer`, never used bare: a planner's VLM runs at a slow cadence and MUST NOT sit
    on a robot's per-step hot path — a plan call is hundreds of ms to seconds. So `plan` only sets what a policy reads;
    its `infer` remains the sole per-step entrypoint. Requiring `every_s` makes the cadence explicit and un-omittable.




    """

    if fn is not None:
        raise PolicyDefinitionError(
            "@seq.plan requires a cadence: write @seq.plan(every_s=SECONDS), not a bare @seq.plan"
        )

    if every_s is None:
        raise PolicyDefinitionError("@seq.plan(every_s=...) is required (seconds from one plan's start to the next)")
    cadence = _validate_every_s(every_s)
    said = wake_on_refused(wake_on)
    if said:
        raise PolicyDefinitionError(said)

    def decorator(target: Any) -> _PartialFunction:


        if wake_on:
            getattr(target, "raw_fn", target).__seq_plan_wake_on__ = list(wake_on)


        return _as_partial(target, SeqFlags.PLAN, {"every_s": cadence})

    return decorator
