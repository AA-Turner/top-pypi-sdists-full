"""
A policy class's methods as the worker calls them, and how it builds the class: what the decorators mark is held to
what the worker hands each method, init= is how the class is built, and naming methods on @seq.policy is refused,
saying how it is written now.

    @seq.policy(hz=15, gpu="L4", weights="hf://org/model",
                init={"cfg": seq.config("deploy.yml", ckpt_dir="{weights}")})
    class Policy(Model):                   # your repository's class, as it is, subclassed in seq_policy.py
        @seq.observe
        def update_obs(self, obs):
            return super().update_obs(obs)

        @seq.infer
        def get_action(self):
            return super().get_action()

In one sentence: `refuse(cls, kw)` turns away infer= / observe= / reset= / end= / sample= - methods named on
@seq.policy - and make=, each with how it is written now → `constructor(cls, kw)` reads init=, the constructor's
arguments, config files read and "{weights}" filled where it runs (sequence_base.construct) - without it, a constructor
that needs arguments refused, as the worker builds it with none → `check(cls, bindings)` holds each marked
method to what the worker hands it: observe each observation - whole, or each key by name to a method of two or more
arguments without a default (sequence_base.by_name), with the platform's step= and episode= by name - infer nothing for a
class that observes, reset and sample nothing.

WHY decorators alone: one way to mark a method, and the numbers a method carries (sizes, every_s) fit only on a
decorator - a name on @seq.policy could not hold them, so the two ways ended up mixed. A class of a repository is
subclassed in seq_policy.py and stays as it is.

"""
from __future__ import annotations

import inspect
import os
import sys
from typing import Any

from sequence_base import SeqFlags
from sequence_base.by_name import INFER_PLATFORM, OBSERVE_PLATFORM, ByName, ends, takes_by_name
from sequence_base.construct import CONFIG_KEY, FORMS, POLICY_FIELDS, SET_KEY, is_config
from sequence_base.contract.policy import PolicyConstructor

from seq.errors import PolicyDefinitionError

__all__ = ["PER_STEP", "check", "constructor", "inputs_by_name", "per_step"]


_DECORATOR = {"infer": "seq.infer", "observe": "seq.observe", "end": "seq.on_episode",
              "sample": "seq.sample"}


_BY_NAME = {"infer": INFER_PLATFORM, "observe": OBSERVE_PLATFORM}





PER_STEP = {"select_action": "predict_action_chunk"}

def constructor(cls: type, kw: dict[str, Any], *, benchmark: bool = False, worlds: int | None = None,
                error: type[Exception] = PolicyDefinitionError) -> PolicyConstructor | None:
    """init=: the arguments the worker builds the class with - a dict by name or a list by position - held to its
    constructor, each seq.config(...) a file beside its file; a policy's "{weights}" only with weights= declared, a
    benchmark's "{num_worlds}" only when it is vectorized (`worlds`: N of @seq.concurrent(sizes=[N]) on its step) - which
    must name it - and "{policy.<field>}" only of what a policy declares (sequence_base.construct.POLICY_FIELDS). None
    without init=: the worker builds it with no arguments, refused here for a constructor that needs some - a policy
    loads its model in the constructor, so a class written to take its weights' directory and declared without init=
    is the mistake to catch before a build. Refused with `error`, the declaration's own.

"""
    if "init" not in kw:
        if benchmark and worlds is not None:
            raise error(_vectorized(cls, worlds))
        try:
            inspect.signature(cls).bind()
        except TypeError:
            needed = ", ".join(f'"{p.name}": ...' for p in inspect.signature(cls).parameters.values()
                               if p.default is p.empty and p.kind not in (p.VAR_POSITIONAL, p.VAR_KEYWORD))
            fills = ('"{policy.hz}" the evaluated policy\'s rate' if benchmark
                     else '"{weights}" its weights\' directory where it runs')
            raise error(f"{cls.__name__}{_signature(cls)}: the worker builds it with no arguments unless init= hands "
                        f"it some - init={{{needed}}}, {fills}") from None
        except ValueError:
            pass
        return None
    init = kw.get("init")
    if isinstance(init, dict) and not is_config(init):
        if not all(isinstance(k, str) for k in init):
            raise error(f"{cls.__name__}: init= keys are its constructor's argument names")
        args, kwargs = [], dict(init)
    elif isinstance(init, (list, tuple)):
        args, kwargs = list(init), {}
    else:
        raise error(f"{cls.__name__}: init= is its constructor's arguments - a dict by name (init={{\"cfg\": ...}}) or "
                    f"a list by position (init=[seq.config(\"deploy.yml\")]); got {type(init).__name__}")
    if benchmark:
        _check_benchmark_forms(cls, [args, kwargs], worlds, error)
    try:
        inspect.signature(cls).bind(*args, **kwargs)
    except TypeError as exc:
        raise error(f"{cls.__name__}: init= does not fit {cls.__name__}{_signature(cls)}: {exc}") from None
    except ValueError:
        pass
    folder = _folder(cls)
    for ref in _configs([args, kwargs]):
        path = os.path.join(folder, ref[CONFIG_KEY])
        if not os.path.isfile(path):
            raise error(f"{cls.__name__}: seq.config({ref[CONFIG_KEY]!r}) - no such file beside its file ({path}); "
                        "the worker reads it from where the upload puts it")
    if not benchmark:
        _check_weights(cls, [args, kwargs], kw.get("weights"))
    try:
        return PolicyConstructor(args=args, kwargs=kwargs)
    except ValueError as exc:
        raise error(f"{cls.__name__}: init=: {exc}") from None


def _vectorized(cls: type, worlds: int) -> str:
    """What a vectorized benchmark whose init= hands it no "{num_worlds}" is told: its constructor's own first argument
    handed how many, the way it builds them."""
    try:
        first = next((p.name for p in inspect.signature(cls).parameters.values()
                      if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)), "worlds")
    except (TypeError, ValueError):
        first = "worlds"
    return (f"{cls.__name__} is vectorized (@seq.concurrent(sizes=[{worlds}]) on its @seq.step): its constructor "
            f"builds the worlds an eval runs, at most {worlds}, after the machine's snapshot, handed how many by init= "
            f'- init={{"{first}": "{{num_worlds}}"}}')


def _check_benchmark_forms(cls: type, value: Any, worlds: int | None, error: type[Exception]) -> None:
    """Each form in a benchmark's init= held to what the eval fills it with (sequence_base.construct): "{num_worlds}" only
    when it is vectorized - and then named somewhere - "{policy.<field>}" a field a policy declares, no "{weights}".
"""
    named = False
    for form in _forms(value):
        if form.group("worlds"):
            if worlds is None:
                raise error(f"{cls.__name__}: init= names {{num_worlds}}, how many worlds one call of a vectorized env's "
                            "@seq.step takes - mark it @seq.concurrent(sizes=[N]), N the most it takes; an env of one "
                            "world an instance takes none")
            named = True
        elif form.group("field") is not None:
            if form.group("field") not in POLICY_FIELDS:
                raise error(f"{cls.__name__}: init= names {form.group(0)}, and a policy declares "
                            f"{', '.join(POLICY_FIELDS)} - \"{{policy.hz}}\" its control rate")
        else:
            raise error(f"{cls.__name__}: init= names {form.group(0)}, and a benchmark has no weights - its assets= "
                        "volumes are mounted at /assets")
    if worlds is not None and not named:
        raise error(_vectorized(cls, worlds))


def check(cls: type, bindings: dict[SeqFlags, str], *, planner: bool = False) -> None:
    """Each marked method held to what the worker hands it: @seq.on_episode the episode alone, as the episode begins
    and as it ends (ends); observe each observation, infer nothing in a class that observes (its observations went to
    observe), sample nothing. An infer of a class that does not observe is held by the registry's own check, to an observation
    (registry._check_infer_signature). The words are sequence-base's, the worker's own when it loads a class.
    """
    name = bindings.get(SeqFlags.ON_EPISODE)
    params = _params(cls, name) if name else None
    why = ends(params, f"{cls.__name__}.{name}") if params is not None else None
    if why:
        raise PolicyDefinitionError(why)
    _takes(cls, "observe", bindings.get(SeqFlags.OBSERVE), 1)
    if SeqFlags.OBSERVE in bindings:
        _takes(cls, "infer", bindings.get(SeqFlags.INFER), 0)
    _takes(cls, "sample", bindings.get(SeqFlags.SAMPLE), 0, planner=planner)


def per_step(cls: type) -> str | None:
    """What `seq deploy` says, once, of a class whose @seq.infer method is one of PER_STEP's - one that answers an action
    a control step - and which to mark instead: the method beside it that returns the whole chunk, when the class has
    it. None for any other.
"""
    from seq.registry import registration

    name = registration(cls).bindings.get(SeqFlags.INFER)
    chunk = PER_STEP.get(name)
    if chunk is None:
        return None
    instead = chunk if callable(getattr(cls, chunk, None)) else "the method that returns a whole chunk"
    return (f"@seq.infer marks {name}, which answers one action a control step from a queue it keeps, so every step "
            f"would wait out a round trip to the worker; mark {instead} instead and let the robot play its rows in its "
            "own loop.")


def inputs_by_name(cls: type, arg: str, name: str) -> ByName | None:
    """How the method `name` (@seq.infer's or @seq.observe's) takes what it is handed: by name - each key of the inputs
    to its argument of that name - when it takes two or more without a default beside the platform's, else None
    (whole)."""
    params = _params(cls, name)
    return None if params is None else takes_by_name(params, _BY_NAME[arg])


def _params(cls: type, name: str) -> list[inspect.Parameter] | None:
    """The arguments of the method `name` the worker hands something, its instance left out; None for a builtin's or
    one the class does not have."""
    try:
        params = list(inspect.signature(getattr(cls, name)).parameters.values())
    except (AttributeError, TypeError, ValueError):
        return None
    if params and inspect.isfunction(inspect.getattr_static(cls, name)):
        params = params[1:]
    return params


def _takes(cls: type, arg: str, name: str | None, positional: int, *, planner: bool = False) -> None:
    """That the method `name` takes `positional` arguments besides self and no more required ones, the platform's by
    name: the worker hands observe one observation - with step= and episode= when it takes them - infer the act's
    inputs, or nothing in a class that observes (with episode= and its other platform arguments), reset and sample
    nothing. An observe or infer method handed one that takes two or more arguments without a default takes it by name
    instead, each key to its argument (sequence_base.by_name)."""
    if name is None:
        return
    params = _params(cls, name)
    if params is None:
        return
    if positional == 1 and arg in _BY_NAME and takes_by_name(params, _BY_NAME[arg]) is not None:
        return
    sig = inspect.signature(getattr(cls, name))

    keywords = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params)
    named = {p.name for p in params if p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                                  inspect.Parameter.KEYWORD_ONLY)}
    by_name = {k: None for k in sorted(_BY_NAME.get(arg, ())) if keywords or k in named}
    positionals = [p.name for p in params if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                                        inspect.Parameter.POSITIONAL_OR_KEYWORD)][:positional]
    try:
        inspect.Signature(params).bind(*([None] * positional), **{k: v for k, v in by_name.items()
                                                                  if k not in positionals})
    except TypeError:
        hands = {0: "nothing", 1: "one argument"}[positional]
        why = {"observe": "each observation - with step=, its step in the episode from 0, and episode= when it takes "
                          "them - or each of its keys by name, to a method that takes two or more arguments without a "
                          "default",
               "infer": "the act's inputs - or each of them by name, to a method that takes two or more arguments "
                        "without a default" if positional else
               "nothing but its platform arguments (episode=) - its observations went to @seq.observe",
               "sample": "nothing - it returns its sample group, each member's robots' observations or a member "
                         "planner's state" if planner else "nothing - it returns the episode's calls"}[arg]
        raise PolicyDefinitionError(f"{cls.__name__}.{name}{sig} (@{_DECORATOR[arg]}): the worker hands it {hands} "
                                    f"({why})") from None


def _signature(fn: Any) -> str:
    try:
        return str(inspect.signature(fn))
    except (TypeError, ValueError):
        return "(...)"


def _folder(cls: type) -> str:
    module = sys.modules.get(cls.__module__)
    return os.path.dirname(os.path.abspath(module.__file__)) if getattr(module, "__file__", None) else os.getcwd()


def _configs(value: Any):
    """Every seq.config(...) in `value`, at any depth (one inside another's keys too)."""
    if is_config(value):
        yield value
        yield from _configs(value[SET_KEY])
    elif isinstance(value, dict):
        for v in value.values():
            yield from _configs(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from _configs(v)


def _check_weights(cls: type, value: Any, weights: Any) -> None:
    """Each "{weights}" and "{weights.<part>}" in init= against the weights= it is filled from, refused here as the
    worker would refuse it building the class (sequence_base.construct), after a build: none declared, a part the
    weights do not have - its parts named - a part of weights that come whole, or the whole of weights in parts.
    """
    for form in _forms(value):
        if form.group("worlds") or form.group("field") is not None:
            raise PolicyDefinitionError(f"{cls.__name__}: init= names {form.group(0)}, which a benchmark's init= is "
                                        'handed - a policy\'s names "{weights}", its weights\' directory')
        part = form.group("part")
        named = "{weights}" if part is None else f"{{weights.{part}}}"
        if weights is None:
            raise PolicyDefinitionError(f"{cls.__name__}: init= names {named}, and it declares no weights= to fill it")
        if isinstance(weights, dict):
            parts = ", ".join(weights)
            if part is None:
                raise PolicyDefinitionError(f"{cls.__name__}: init= names {{weights}}, and its weights come in named "
                                            f"parts ({parts}): name one, {{weights.<part>}}")
            if part not in weights:
                raise PolicyDefinitionError(f"{cls.__name__}: init= names {named}, and its weights have no part "
                                            f"{part!r} - its parts are {parts}")
        elif part is not None:
            raise PolicyDefinitionError(f"{cls.__name__}: init= names {named}, a part of its weights, and they come "
                                        "whole (weights= names no parts): write {weights}")


def _forms(value: Any):
    """Each form a string in `value` holds, at any depth, by sequence_base construct's own pattern (FORMS): a policy's
    "{weights}" / "{weights.<part>}", a benchmark's "{num_worlds}" / "{policy.<field>}"."""
    if isinstance(value, str):
        yield from FORMS.finditer(value)
    elif isinstance(value, dict):
        for v in value.values():
            yield from _forms(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from _forms(v)
