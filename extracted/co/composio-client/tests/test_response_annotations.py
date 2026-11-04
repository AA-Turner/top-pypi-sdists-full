"""No resource method returns a type that reaches `Any`.

`Any` switches type checking off for everything read through it, so a response
field typed `dict[str, Any]` lets `log.metadata["k"].anything()` pass mypy. An
open value is spelled `object` instead — the Stainless oracle's spelling, which
makes a caller narrow first.

The walk covers every operation in the generated table, on both clients and all
three calling conventions, and descends through every nested model, container,
union and `RootModel` payload. It works on resolved runtime annotations rather
than source text, so it sees the same thing whichever module a response type
comes from: the Stainless-shaped `types/` classes or the hey-api models the
additive operations alias.
"""

from __future__ import annotations

import functools
import typing
from collections.abc import Iterator
from typing import Any, Literal, get_args, get_origin, get_type_hints

import pydantic
import pytest
from typing_extensions import is_typeddict

from composio_client import AsyncComposio, Composio, ProjectAuth
from composio_client._operations import OPERATIONS, OPERATIONS_BY_CHAIN

from .conftest import API_KEY, BASE_URL

_CONVENTIONS = ("", "with_raw_response", "with_streaming_response")
_CASES = [
    pytest.param(
        kind,
        chain,
        convention,
        id=".".join((kind, *chain[:-1], convention, chain[-1]) if convention else (kind, *chain)),
    )
    for kind in ("sync", "async")
    for chain in OPERATIONS_BY_CHAIN
    for convention in _CONVENTIONS
]


def _any_paths(annotation: object, path: str, seen: frozenset[type] = frozenset()) -> list[str]:
    """Every location under `annotation` typed `Any`, or left unresolved.

    An unresolved annotation is reported rather than skipped: a walk that could
    not see a field must not read as one that found nothing there.
    """
    if annotation is Any:
        return [path]
    if isinstance(annotation, (str, typing.ForwardRef)):
        return [f"{path} (unresolved {annotation!r})"]
    if get_origin(annotation) is Literal:
        return []
    if is_typeddict(annotation):
        if annotation in seen:
            return []
        return [
            found
            for name, hint in get_type_hints(annotation).items()
            for found in _any_paths(hint, f"{path}.{name}", seen | {annotation})
        ]
    if isinstance(annotation, type) and issubclass(annotation, pydantic.BaseModel):
        if annotation in seen:
            return []
        return [
            found
            for name, field in annotation.model_fields.items()
            for found in _any_paths(field.annotation, f"{path}.{name}", seen | {annotation})
        ]
    return [
        found
        for index, arg in enumerate(get_args(annotation))
        if arg is not Ellipsis
        for found in _any_paths(arg, f"{path}[{index}]", seen)
    ]


@pytest.fixture(scope="module")
def clients() -> Iterator[dict[str, object]]:
    sync = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    yield {"sync": sync, "async": AsyncComposio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)}
    sync.close()


def _method(root: object, chain: tuple[str, ...], convention: str) -> Any:
    resource = functools.reduce(getattr, chain[:-1], root)
    holder = getattr(resource, convention) if convention else resource
    return getattr(holder, chain[-1])


def test_the_walk_covers_every_operation_on_both_clients_and_all_conventions() -> None:
    assert len(_CASES) == 2 * len(_CONVENTIONS) * len(OPERATIONS)
    assert len(OPERATIONS_BY_CHAIN) == len(OPERATIONS)


@pytest.mark.parametrize(("kind", "chain", "convention"), _CASES)
def test_no_response_type_reaches_any(
    clients: dict[str, object], kind: str, chain: tuple[str, ...], convention: str
) -> None:
    returned = get_type_hints(_method(clients[kind], chain, convention))["return"]

    assert _any_paths(returned, "<return>") == []


class _Nested(pydantic.BaseModel):
    value: dict[str, Any]


class _Outer(pydantic.BaseModel):
    items: list[_Nested | None]
    open: dict[str, object]
    kind: Literal["Any"]


class _Root(pydantic.RootModel[_Nested | dict[str, Any]]):
    pass


def test_the_walk_finds_any_through_nested_models_containers_and_root_models() -> None:
    assert _any_paths(_Outer, "<return>") == ["<return>.items[0][0].value[1]"]
    assert _any_paths(_Root, "<return>") == ["<return>.root[0].value[1]", "<return>.root[1][1]"]


def test_the_walk_accepts_object_and_reports_what_it_cannot_resolve() -> None:
    assert _any_paths(dict[str, object], "<return>") == []
    unresolved = list[typing.ForwardRef("Missing")]

    assert _any_paths(unresolved, "<return>") == ["<return>[0] (unresolved ForwardRef('Missing'))"]
