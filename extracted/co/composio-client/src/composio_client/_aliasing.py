"""Rename a dict request body's keys and materialize declared array iterables.

The spec gives a handful of request fields a wire name that is not their
pythonic one (``auth_scheme`` -> ``authScheme``, ``your_domain`` ->
``your-domain``, ...). A caller who hands us a plain mapping writes the pythonic
spelling, so something has to apply those renames before the body is
serialized.

This module is that something, and it is deliberately *only* that. It walks the
endpoint's generated request model as a **name map** — for each key the caller
wrote, look up the field it names and emit that field's alias — and copies every
scalar value through untouched. It never validates or coerces. Array iterables
become lists so the JSON transport can serialize them.

## Why not validate-and-dump

The obvious implementation is ``model.model_validate(mapping).model_dump(
mode="json", by_alias=True, exclude_unset=True)``, and that is what this package
did until now. It renames correctly, but it also *rewrites values*, because
pydantic's lax validation mode coerces on the way in and its JSON dump
serializes on the way out. Against the pinned Stainless 1.43.0 oracle — whose
``maybe_transform`` walks unchecked ``TypedDict`` annotations and remaps aliases
and nothing more — that produced four separate wire divergences on this surface:

| caller writes | oracle sends | validate-and-dump sent |
| --- | --- | --- |
| ``expires_in: 3600`` (a spec ``number``) | ``3600`` | ``3600.0`` |
| ``auto_offload_threshold: "20000"`` | ``"20000"`` | ``20000.0`` |
| ``binary_body.url: "https://example.com"`` | as written | ``"https://example.com/"`` |
| any field the model rejects | body aliased | **whole body unaliased** |

The last one is the sharpest: a single out-of-model value anywhere in the body
raised ``ValidationError``, and the lenient fallback then sent the entire
mapping unrenamed — narrowly reinstating the bug the aliasing was introduced to
fix. A rename that cannot fail has no failure mode to fall back from.

## The one place a model still has to be *chosen*

``custom_connection_data`` on ``session.proxy_execute`` is an eleven-member
``oneOf`` and the members do not agree on their field names: ``redirect_url`` ->
``redirectUrl`` is declared on the OAUTH1 member alone. Renaming against "the
union" would smear that alias across every member and emit ``redirectUrl`` on a
connection whose schema has no such field — which is exactly what Stainless
does, and exactly the one behavior this client deliberately does not copy (see
MIGRATION.md §1 and
``tests/test_tool_router.py::test_proxy_execute_aliases_resolve_per_variant_not_across_the_union``).

So the member is resolved first and the rename runs against that member only.
:func:`_select_variant` resolves it, in order:

1. **By discriminator.** Each member declares a single-valued enum (or
   ``Literal``) field — ``authScheme`` here — and the eleven values are
   distinct. Matching on it needs nothing but that one key, so a member is still
   resolved when some *other* field of the body is something the model would
   reject. This is what keeps a bad ``expires_in`` from costing the body its
   ``authScheme`` rename.
2. **By trial validation**, for a union with no discriminator (``toolkits``,
   ``binary_body``): the first member that validates wins. Validation is used
   purely as a selector here — the coerced model it produces is discarded, and
   the values that reach the wire are still the caller's.
3. **Not at all**: no member matched, so no rename is applied to that subtree.
   Its keys and values are forwarded exactly as written. This is the only
   remaining "leave it alone" path, and it is scoped to the one subtree that
   could not be resolved rather than to the whole body.

## ``RootModel`` is transparent

A ``RootModel`` declares one field, ``root``, holding the whole payload — so
walked as a plain name map it recognizes exactly one key (``"root"``), which no
caller writes, and every key of the body would be forwarded unrenamed. That is
the worst failure mode this module can have: it looks like it worked.

:func:`_alternatives` therefore peels a ``RootModel`` the same way it peels
``Annotated`` and unions, replacing it with the annotation it wraps, everywhere
an annotation is expanded. ``RootModel[Foo]`` renames against ``Foo``,
``RootModel[list[Foo]]`` against each element, ``RootModel[dict[str, Foo]]``
against each value. Unwrapping is preferred over raising because it is what the
caller meant: the wrapper is a codegen artifact of a body whose schema has no
object at its top level, not a shape the caller chose. Raising would trade a
silent under-rename for a hard failure on a body the server would have accepted,
and this function's contract is that it cannot fail on a caller's body.

No request body is a ``RootModel`` in the current spec snapshot; three list
*responses* are (``config_history``, ``toolkits``, ``tools``). Responses are
parsed by ``model_validate`` in the kernel and never reach this module, so the
unwrap is invisible to them.
"""

from __future__ import annotations

import types
import typing
from collections.abc import Callable, Iterable, Mapping
from enum import Enum
from typing import Any, TypeVar, cast

from pydantic import BaseModel, RootModel, ValidationError

__all__ = ["rename_to_wire_names"]

#: Sentinel for "this field has no constant value" / "this key is absent".
_MISSING = object()

_UNION_ORIGINS = (typing.Union, types.UnionType)

_T = TypeVar("_T")


def _root_annotation(node: Any) -> Any:
    """What a ``RootModel`` wraps, or ``_MISSING`` when ``node`` is not one."""
    if not (isinstance(node, type) and issubclass(node, RootModel)):
        return _MISSING
    field = node.model_fields.get("root")
    return _MISSING if field is None else field.annotation


def _alternatives(annotation: Any) -> list[Any]:
    """Flatten ``Annotated`` wrappers, union members and ``RootModel`` wrappers
    into concrete branches.

    ``Optional[Annotated[float, Gt(0)]]`` becomes ``[float, NoneType]`` and
    ``RootModel[Foo]`` becomes ``[Foo]`` — a root model is a wrapper around the
    payload, never the payload's shape, so peeling it here makes it transparent
    to every caller at once (see the module docstring). Only the outer layers are
    peeled: ``list[Foo]`` stays ``list[Foo]``, because the element type is looked
    up separately.
    """
    out: list[Any] = []
    #: Root models already peeled on this walk, so a mutually recursive pair
    #: (``A(RootModel[B])``, ``B(RootModel[A])``) terminates instead of looping.
    peeled: set[int] = set()

    def flatten(node: Any) -> None:
        if hasattr(node, "__metadata__"):  # Annotated[T, ...]
            flatten(typing.get_args(node)[0])
            return
        if typing.get_origin(node) in _UNION_ORIGINS:
            for arg in typing.get_args(node):
                flatten(arg)
            return
        root = _root_annotation(node)
        if root is not _MISSING and id(node) not in peeled:
            peeled.add(id(node))
            flatten(root)
            return
        out.append(node)

    flatten(annotation)
    return out


def _models(annotation: Any) -> list[type[BaseModel]]:
    """The ``BaseModel`` branches of an annotation, in declaration order."""
    return [alt for alt in _alternatives(annotation) if isinstance(alt, type) and issubclass(alt, BaseModel)]


def _element_annotation(annotation: Any) -> Any:
    """The annotation of a list/tuple/set element, or ``None`` if there is none."""
    for alt in _alternatives(annotation):
        if typing.get_origin(alt) in (list, tuple, set, frozenset):
            args = typing.get_args(alt)
            if args:
                return args[0]
    return None


def _value_annotation(annotation: Any) -> Any:
    """The annotation of a ``dict``/``Mapping`` value, or ``None`` if there is none."""
    for alt in _alternatives(annotation):
        if typing.get_origin(alt) in (dict, Mapping):
            args = typing.get_args(alt)
            if len(args) == 2:
                return args[1]
    return None


#: Where a model's memoized tables live: on the model class itself, under a
#: dunder-spelled key that cannot collide with a pydantic field name.
_FIELD_INDEX_ATTR = "__composio_aliasing_field_index__"
_DISCRIMINATORS_ATTR = "__composio_aliasing_discriminators__"


def _memoized(model: type[BaseModel], attr: str, build: Callable[[type[BaseModel]], _T]) -> _T:
    """``build(model)``, computed once per class and stored *on* that class.

    These tables are pure functions of ``model.model_fields``, and both are on
    the hot path of every dict request body, so they have to be memoized. The
    memo may not outlive its key, though: a ``functools.cache`` keyed on the
    class — what this used to be — holds a strong reference to every class it
    ever saw, which pins any dynamically created model
    (``pydantic.create_model``, a model declared inside a function or a test)
    and everything its ``__mro__`` and closure reach, for the life of the
    process. The generated models are module-level and immortal anyway; nothing
    else should be.

    Storing the table on the class ties the memo's lifetime to the class's
    exactly: when the class becomes garbage, so does its memo, with no bound to
    tune and no eviction to make the hot path cold. A ``WeakKeyDictionary``
    would look equivalent but is not — its *values* are held strongly, and
    ``_field_index``'s values contain field annotations, which for a
    self-referential model contain the model. That reference cycle runs through
    a module-level root, so the entry — and the class — could never be collected.

    Thread-safety: a read is one ``dict.get`` on the class ``__dict__`` and a
    write is one ``setattr``, both atomic. Two threads racing on a cold class
    may both build the table and one write may overwrite the other, which is
    harmless because the two results are equal by construction. That is exactly
    the guarantee ``functools.cache`` gave (it, too, does not hold a lock across
    the wrapped call), so the sync and async clients are no worse off.

    ``__dict__`` rather than ``getattr`` so a subclass never reads its base's
    table as its own.
    """
    cached = model.__dict__.get(attr)
    if cached is not None:
        return cast("_T", cached)
    value = build(model)
    try:
        setattr(model, attr, value)
    except (AttributeError, TypeError):
        # A metaclass that forbids class attribute assignment. Recomputing every
        # time is pure and correct; this rename is not allowed to fail.
        pass
    return value


def _field_index(model: type[BaseModel]) -> dict[str, tuple[str, Any]]:
    """``accepted key -> (wire name, annotation)`` for one model.

    Both spellings are accepted on input — the pythonic field name and the wire
    alias — mirroring the ``populate_by_name=True`` every generated model
    carries. Aliases are registered first so that a field's own *name* wins if
    some other field's alias happens to collide with it.
    """
    return _memoized(model, _FIELD_INDEX_ATTR, _build_field_index)


def _build_field_index(model: type[BaseModel]) -> dict[str, tuple[str, Any]]:
    index: dict[str, tuple[str, Any]] = {}
    for field in model.model_fields.values():
        if field.alias is not None:
            index[field.alias] = (field.alias, field.annotation)
    for name, field in model.model_fields.items():
        index[name] = (field.alias or name, field.annotation)
    return index


def _discriminators(model: type[BaseModel]) -> tuple[tuple[tuple[str, ...], Any], ...]:
    """The model's constant-valued fields, as ``(accepted keys, value)`` pairs.

    A field qualifies when its annotation is exactly one branch and that branch
    is a single-member ``Enum`` or a one-argument ``Literal`` — the shape
    hey-api emits for a ``oneOf`` member's discriminator. Anything optional or
    genuinely multi-valued is not a discriminator and is skipped.
    """
    return _memoized(model, _DISCRIMINATORS_ATTR, _build_discriminators)


def _build_discriminators(model: type[BaseModel]) -> tuple[tuple[tuple[str, ...], Any], ...]:
    out: list[tuple[tuple[str, ...], Any]] = []
    for name, field in model.model_fields.items():
        alternatives = _alternatives(field.annotation)
        if len(alternatives) != 1:
            continue
        constant = _constant(alternatives[0])
        if constant is _MISSING:
            continue
        keys = (name,) if field.alias is None else (name, field.alias)
        out.append((keys, constant))
    return tuple(out)


def _constant(annotation: Any) -> Any:
    """The single value ``annotation`` admits, or ``_MISSING``."""
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        members = list(annotation)
        return members[0].value if len(members) == 1 else _MISSING
    if typing.get_origin(annotation) is typing.Literal:
        args = typing.get_args(annotation)
        return args[0] if len(args) == 1 else _MISSING
    return _MISSING


def _matches_discriminators(mapping: Mapping[str, Any], model: type[BaseModel]) -> bool:
    discriminators = _discriminators(model)
    if not discriminators:
        return False
    for keys, expected in discriminators:
        present: Any = _MISSING
        for key in keys:
            if key in mapping:
                present = mapping[key]
                break
        if present is _MISSING or present != expected:
            return False
    return True


def _select_variant(mapping: Mapping[str, Any], models: list[type[BaseModel]]) -> type[BaseModel] | None:
    """Pick the union member ``mapping`` is written against — see the module docstring."""
    if not models:
        return None
    if len(models) == 1:
        return models[0]
    matched = [model for model in models if _matches_discriminators(mapping, model)]
    if len(matched) == 1:
        return matched[0]
    for model in models:
        try:
            model.model_validate(mapping)
        except ValidationError:
            continue
        return model
    return None


def _rename(value: Any, annotation: Any) -> Any:
    """One value, renamed in place against ``annotation`` (which may be ``None``).

    Scalars — every leaf that is not a mapping, a sequence or a model — are
    returned as the caller wrote them. That is the whole point of this pass.
    """
    # A model handed in *inside* a dict body still has to be serialized: it is
    # already the typed contract, so dumping it is the caller's stated intent.
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", by_alias=True, exclude_unset=True)
    if isinstance(value, Mapping):
        return _rename_mapping(value, annotation)
    # Public array parameters accept iterables. Materialize those containers
    # without validating or coercing their elements; opaque values stay opaque.
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray)):
        element = _element_annotation(annotation)
        if isinstance(value, (list, tuple)) or element is not None:
            return [_rename(item, element) for item in value]
    return value


def _rename_mapping(mapping: Mapping[str, Any], annotation: Any) -> dict[str, Any]:
    """One mapping, renamed against whatever ``annotation`` turns out to be.

    The single entry point for "a dict meets an annotation", so the top-level
    body and every nested mapping resolve their model — including through a
    ``RootModel`` wrapper, which :func:`_alternatives` peels — the same way.
    """
    model = _select_variant(mapping, _models(annotation))
    if model is not None:
        return _rename_fields(mapping, model)
    # No model to rename against: keep every key, and keep walking so a
    # nested model instance or list still gets its own treatment.
    nested = _value_annotation(annotation)
    return {key: _rename(value, nested) for key, value in mapping.items()}


def _rename_fields(mapping: Mapping[str, Any], model: type[BaseModel]) -> dict[str, Any]:
    index = _field_index(model)
    out: dict[str, Any] = {}
    for key, value in mapping.items():
        entry = index.get(key)
        if entry is None:
            # A key the model does not declare — a field the spec snapshot has
            # not caught up with — is forwarded verbatim, at any depth.
            out[key] = _rename(value, None)
            continue
        wire_name, annotation = entry
        out[wire_name] = _rename(value, annotation)
    return out


def rename_to_wire_names(model: type[BaseModel], mapping: Mapping[str, Any]) -> dict[str, Any]:
    """``mapping`` with every key the spec renames spelled the way the API reads it.

    Scalar values are copied through unchanged; keys the model does not declare are
    kept as written. This function cannot fail on a caller's body.
    """
    return _rename_mapping(mapping, model)
