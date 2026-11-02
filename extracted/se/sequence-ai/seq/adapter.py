"""
`@seq.adapter` - the robot's own code, in the eval's loop: two conversions between a benchmark's env and a policy
.

In one sentence: an adapter is a plain class with two methods - `@seq.observation` turns the env's observation into what
the policy's observe is sent, `@seq.action` turns the policy's answer into the actions the env's step plays, a list, one
a step - and the benchmark → policy pairs it is for (`@seq.adapter(pairs=[...])`) → `seq deploy` registers it as a
version of its own → an eval of a pair it names runs it in the benchmark's container, between the two.
WHY two functions and not a pipeline of named transforms: every adapter in use wrapped a plain function in seq.tf.custom
;
the conversion is what the robot's own code does, so the adapter is that code. (the user 10-24: "The adapter is
basically transforming the observations and the acts, right?")
"""
from __future__ import annotations

import inspect
import re
from typing import Any, TypeVar

from seq.errors import AdapterDefinitionError
from sequence_base.contract import SeqFlags
from sequence_base.contract.adapters import Pairs, parse_pairs

_T = TypeVar("_T", bound=type)

_ADAPTER_ATTR = "__seq_adapter__"
_NAME = re.compile(r"[A-Za-z][A-Za-z0-9._-]{0,63}")


ADAPTER_MARKS = {SeqFlags.OBSERVE: ("@seq.observation", "def to_policy(self, obs)", "the env's observation"),
                 SeqFlags.ACTION: ("@seq.action", "def to_env(self, answer)", "the policy's answer")}



GONE_ATTRS = {
    "obs_transforms": "obs_transforms is gone: one method converts the env's observation into what the policy is sent "
                      "- @seq.observation def to_policy(self, obs)",
    "action_transforms": "action_transforms is gone: one method converts the policy's answer into the actions the env "
                         "plays, one a step - @seq.action def to_env(self, answer)",
    "policy_io": "policy_io is gone: @seq.observation returns whatever the policy's observe takes, and @seq.action is "
                 "handed whatever the policy answers",
}


class AdapterRegistration:
    """What `@seq.adapter` attaches: the name it registers under, the benchmark → policy pairs it converts between, its
    two methods (`bindings`: SeqFlags.OBSERVE → its @seq.observation, SeqFlags.ACTION → its @seq.action) and the ref an
    eval's machine importlib-loads the class by."""

    __slots__ = ("cls", "handler_ref", "bindings", "name", "pairs")

    def __init__(self, cls: type, handler_ref: str, bindings: dict[SeqFlags, str], name: str | None = None,
                 pairs: Pairs | None = None) -> None:
        self.cls = cls
        self.handler_ref = handler_ref
        self.bindings = dict(bindings)

        self.name = name or default_name(cls.__name__)


        self.pairs = pairs


def default_name(class_name: str) -> str:
    """The name an adapter registers under when it gives none: its class name, lower-case with hyphens —
    ToyAdapter → toy-adapter, _To_Arm → to-arm."""
    kebab = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "-", class_name.strip("_"))
    return re.sub(r"[_-]+", "-", kebab).lower()


def adapter(cls: _T | None = None, *, name: str | None = None, pairs: Any = None) -> Any:
    """`@seq.adapter(name="libero-openpi", pairs=[("template:libero-10", "template:pi05-libero")])` on a plain class
    with two methods - `@seq.observation def to_policy(self, obs)`, the env's observation → what the policy's observe
    is sent, and `@seq.action def to_env(self, answer)`, the policy's answer → the actions the env's step plays, a list,
    one a step - records them and the pairs, and attaches the registration.

    `pairs`: each pair (benchmark, policy), each side a name in your account, `template:<name>` (anything made from
    that template) or `*` (any one); or `pairs="any"` for every pair. An eval with any other pair is refused before
    anything runs, and `seq deploy` refuses an adapter that declares none. `seq deploy` registers
    the class under `name` (default: the class name, kebab-cased) as a version of its own, chosen when an eval runs
    (`--adapter name@vN`). Its `__init__`'s keyword parameters, each with a default, an eval may set (--param
    adapter.NAME=VALUE).
    """
    if cls is None:
        return lambda c: _adapter(c, name=name, pairs=pairs)
    return _adapter(cls, name=name, pairs=pairs)


def _adapter(cls: Any, *, name: str | None, pairs: Any = None) -> Any:
    from seq._partial import hooks_along
    from seq.registry import _ref_kept

    if not isinstance(cls, type):
        raise AdapterDefinitionError("@seq.adapter goes on a class, with an @seq.observation and an @seq.action method")
    if name is not None and _NAME.fullmatch(name) is None:
        raise AdapterDefinitionError(f"@seq.adapter(name={name!r}): 1-64 letters, digits, '.', '_' or '-', starting "
                                     "with a letter")
    for attr, said in GONE_ATTRS.items():
        if any(attr in vars(k) for k in cls.__mro__):
            raise AdapterDefinitionError(f"{cls.__name__}: {said}")
    if pairs is not None:
        try:
            pairs = parse_pairs(pairs)
        except ValueError as exc:
            raise AdapterDefinitionError(f"@seq.adapter(pairs=...): {exc}") from None
    bindings, _ = hooks_along(cls, _ADAPTER_ATTR, AdapterDefinitionError, "adapter")
    _check(cls, bindings)
    setattr(cls, _ADAPTER_ATTR, AdapterRegistration(cls=cls, handler_ref=_ref_kept(cls), bindings=bindings,
                                                    name=name, pairs=pairs))
    return cls


def _check(cls: type, bindings: dict[SeqFlags, str]) -> None:
    """Both methods marked, nothing else, and each taking the one value it is handed."""
    for flag, method in bindings.items():
        if flag not in ADAPTER_MARKS:
            raise AdapterDefinitionError(f"{cls.__name__}.{method} is marked @seq.{(flag.name or '').lower()}: an "
                                         "adapter marks @seq.observation and @seq.action")
    for flag, (mark, example, what) in ADAPTER_MARKS.items():
        method = bindings.get(flag)
        if method is None:
            raise AdapterDefinitionError(f"{cls.__name__} has no {mark} method: an adapter converts both ways - "
                                         f"{mark} {example}, handed {what}")
        try:
            params = list(inspect.signature(inspect.getattr_static(cls, method)).parameters.values())[1:]
        except (TypeError, ValueError):
            continue
        positional = [p for p in params if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                                      inspect.Parameter.POSITIONAL_OR_KEYWORD)]
        star = any(p.kind is inspect.Parameter.VAR_POSITIONAL for p in params)
        required = [p for p in positional if p.default is inspect.Parameter.empty]
        keyword_required = [p for p in params
                            if p.kind is inspect.Parameter.KEYWORD_ONLY and p.default is inspect.Parameter.empty]
        if (not positional and not star) or len(required) > 1 or keyword_required:
            raise AdapterDefinitionError(f"{cls.__name__}.{method} is the {mark} method: it is handed {what} alone - "
                                         f"{example.replace('to_policy', method).replace('to_env', method)}")


def adapter_registration(cls: type) -> AdapterRegistration:
    """Return the `AdapterRegistration` `@seq.adapter` attached, or raise if the class was never decorated."""
    reg = cls.__dict__.get(_ADAPTER_ATTR)
    if reg is None:
        raise AdapterDefinitionError(
            f"{cls.__name__} is not a @seq.adapter class; decorate it with @seq.adapter"
        )
    return reg


def adapter_bindings(cls: type) -> dict[SeqFlags, str]:
    """An adapter's two methods by name: {SeqFlags.OBSERVE: its @seq.observation, SeqFlags.ACTION: its @seq.action} -
    what an eval's machine calls, `getattr(adapter, bindings[SeqFlags.OBSERVE])(obs)` and `getattr(adapter,
    bindings[SeqFlags.ACTION])(answer)`. Raises AdapterDefinitionError for a class @seq.adapter did not register, or one
    without either method."""
    reg = adapter_registration(cls)
    for flag, (mark, example, what) in ADAPTER_MARKS.items():
        if flag not in reg.bindings:
            raise AdapterDefinitionError(f"{cls.__name__} has no {mark} method: an adapter converts both ways - "
                                         f"{mark} {example}, handed {what}")
    return {flag: reg.bindings[flag] for flag in ADAPTER_MARKS}
