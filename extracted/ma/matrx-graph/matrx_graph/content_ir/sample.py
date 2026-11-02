"""Does what an emitter EMITS pass its declared kind's own validator?

WHY THIS EXISTS. A node declares two things independently — the pydantic
``output_schema`` it really returns, and the ``output_kind`` slug consumers bind
to. The first version of ``test_node_output_matches_its_kind`` compared their
FIELD NAMES, and the proxy was wrong in both directions: it counted the
discriminator ``kind_`` as drift on every node whose output schema IS its kind
model (41 false reds on 2026-09-22), and it was blind to anything below the top
level — a nested sub-model that had grown a field sailed straight through.

So ask the runtime's own question instead. Synthesize ONE payload from the
EMITTER's annotations and hand it to the consumer's validator. Registered kinds
are ``extra="forbid"``, so a field the node emits and the kind never declared
fails here exactly as it fails in production (``output_kind_ok = false``), at
any depth.

THE PLACEHOLDER PROBLEM, AND WHY THERE IS NO ALLOWLIST. Synthesized values are
placeholders, so a model with ``min_length=1`` or a
``pattern`` rejects them for reasons that have nothing to do with drift. The
temptation is a hardcoded list of "value-ish" error codes to ignore — an
allowlist that quietly grows into a blindfold. Instead the payload is validated
against BOTH models and the emitter's own complaints are subtracted: an error
the EMITTER raises about its own synthesized payload is the synthesizer's
fault, and only an error the CONSUMER raises and the emitter does not is drift.
Self-calibrating, nothing to maintain, and when emitter and consumer are the
same class the difference is empty by construction.

A type this cannot build raises ``SampleSynthesisError`` — never a silent skip,
because a checker that quietly stops checking is the failure mode this module
was written to end.
"""

from __future__ import annotations

import datetime as _dt
import decimal
import enum
import types
import typing
import uuid
from typing import Any, Literal, Union, get_args, get_origin

from pydantic import BaseModel, JsonValue, ValidationError

__all__ = [
    "SampleSynthesisError",
    "synthesize_payload",
    "contract_drift",
]


class SampleSynthesisError(TypeError):
    """A field annotation the synthesizer cannot build a value for."""


_NoneType = type(None)
_MAX_DEPTH = 12


def _is_union(origin: Any) -> bool:
    return origin is Union or origin is types.UnionType


def _resolve_alias(annotation: Any) -> Any:
    """Unwrap ``TypeAliasType`` (pydantic's ``JsonValue`` and friends)."""
    value = getattr(annotation, "__value__", None)
    return value if value is not None and not isinstance(annotation, type) else annotation


def _value_for(annotation: Any, *, path: str, depth: int) -> Any:
    if depth > _MAX_DEPTH:
        # Recursive aliases (JsonValue) legitimately bottom out; a scalar keeps
        # the payload valid without pretending to model infinite nesting.
        return None

    if annotation is Any or annotation is None or annotation is _NoneType:
        return None

    # JsonValue is intentionally structure-free and recursively refers to
    # itself by name; a scalar is a valid sample without unresolved forwards.
    if annotation is JsonValue:
        return ""

    annotation = _resolve_alias(annotation)
    origin = get_origin(annotation)

    if origin is Literal:
        return get_args(annotation)[0]
    if origin is typing.Annotated:
        return _value_for(get_args(annotation)[0], path=path, depth=depth + 1)
    if _is_union(origin):
        args = [a for a in get_args(annotation) if a is not _NoneType]
        if not args:
            return None
        return _value_for(args[0], path=path, depth=depth + 1)
    if origin in (list, set, frozenset, tuple):
        args = get_args(annotation)
        if not args:
            return []
        # Empty containers never exercise their element contracts. Use a wire
        # array for all sequence types, including one value per fixed tuple slot.
        elements = args if origin is tuple and args[-1] is not Ellipsis else args[:1]
        return [
            _value_for(item, path=f"{path}[{index}]", depth=depth + 1)
            for index, item in enumerate(elements)
        ]
    if origin is dict:
        args = get_args(annotation)
        if not args:
            return {}
        key = _value_for(args[0], path=f"{path}.<key>", depth=depth + 1)
        return {
            key: _value_for(args[1], path=f"{path}[{key!r}]", depth=depth + 1)
        }

    if isinstance(annotation, type):
        if issubclass(annotation, BaseModel):
            return synthesize_payload(annotation, path=path, depth=depth + 1)
        if issubclass(annotation, enum.Enum):
            return next(iter(annotation)).value
        if issubclass(annotation, bool):
            return False
        if issubclass(annotation, int):
            # 0/1 also validate as booleans and hide an int -> bool mismatch.
            return 2
        if issubclass(annotation, float):
            # Whole-valued floats also validate as integers.
            return 0.5
        if issubclass(annotation, decimal.Decimal):
            return "0.5"
        if issubclass(annotation, str):
            return ""
        if issubclass(annotation, bytes):
            return ""
        if issubclass(annotation, _dt.datetime):
            # Midnight also validates as a date, hiding loss of time precision.
            return "2026-01-01T12:34:56+00:00"
        if issubclass(annotation, _dt.date):
            return "2026-01-01"
        if issubclass(annotation, uuid.UUID):
            return str(uuid.UUID(int=0))
        if issubclass(annotation, (list, set, frozenset, tuple)):
            return []
        if issubclass(annotation, dict):
            return {}

    raise SampleSynthesisError(f"{path}: cannot synthesize a value for {annotation!r}")


def synthesize_payload(
    model: type[BaseModel], *, path: str = "", depth: int = 0
) -> dict[str, Any]:
    """The wire payload an emitter of ``model`` puts out, with placeholder values.

    Keys are SERIALIZATION names (so ``kind_`` lands as ``__kind``, exactly as
    ``serialize_by_alias=True`` sends it) and EVERY field is present, optional
    ones included: the point is to exercise the whole emitted shape against the
    consuming kind, not the smallest legal subset.
    """
    by_alias = bool(model.model_config.get("serialize_by_alias"))
    payload: dict[str, Any] = {}
    for name, field in model.model_fields.items():
        where = f"{path}.{name}" if path else f"{model.__name__}.{name}"
        # EXACTLY the key pydantic would put on the wire: the alias ONLY
        # when the model opted into ``serialize_by_alias`` (what ``KindModel``
        # does), the plain field name otherwise — pydantic populates
        # ``serialization_alias`` from ``alias`` whether or not it will ever
        # use it, so reading that field alone invents a wire shape nobody
        # emits. It is how a real drift hides: ``GscSiteIntakeProposal``
        # declares ``kind`` with ``alias="__kind"`` and does NOT serialize by
        # alias, so it emits ``kind`` — which its declared kind's sub-model
        # forbids.
        key = (field.serialization_alias or field.alias or name) if by_alias else name
        payload[key] = _value_for(field.annotation, path=where, depth=depth + 1)
    return payload


def _errors(model: type[BaseModel], payload: dict[str, Any]) -> set[tuple[str, str]]:
    try:
        model.model_validate(payload)
    except ValidationError as exc:
        return {
            (".".join(str(p) for p in err["loc"]), err["type"]) for err in exc.errors()
        }
    return set()


def contract_drift(
    emitter: type[BaseModel], consumer: type[BaseModel]
) -> list[tuple[str, str]]:
    """Ways ``consumer`` refuses what ``emitter`` emits, and ``emitter`` does not.

    Returns ``(location, pydantic error type)`` pairs, sorted. Empty means this
    sample exposes no additional consumer refusals, not that all possible
    emitter values are accepted. See the module docstring for
    why the emitter's own complaints are subtracted rather than allowlisted.
    """
    payload = synthesize_payload(emitter)
    return sorted(_errors(consumer, payload) - _errors(emitter, payload))
