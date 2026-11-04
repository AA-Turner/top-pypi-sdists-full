"""Resource method parameters are typed, and typed the way the runtime enforces them.

Three checks, each making one the others cannot:

* Every parameter annotation, on every signature a type checker resolves a
  call against -- the ``@overload`` stubs and the implementation -- resolves at
  runtime and reaches no ``Any``, TypedDict fields included.
* The Stainless-shaped signature requires exactly the fields the runtime
  refuses a call without, for every operation. An annotation must not call a
  field optional that ``require_fields`` rejects, nor required when it is not.
* mypy, run over ``typecheck/resource_calls.py``, accepts the calls it should
  and rejects the ones it should, with the error code it should.

The frozen Stainless comparison of the 64 released methods lives in
``scripts/check_stainless_compatibility.py``; these cover all 111.
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any, get_type_hints

import httpx
import pytest
import respx
from mypy import api as mypy_api
from typing_extensions import get_overloads

from composio_client import AsyncComposio, Composio, ProjectAuth
from composio_client._operations import OPERATIONS_BY_CHAIN

from .conftest import API_KEY, BASE_URL
from .test_response_annotations import _any_paths

_PYTHON_ROOT = Path(__file__).resolve().parents[1]
_CONVENTIONS = ("", "with_raw_response", "with_streaming_response")
#: The two refusals a missing argument can produce: Python's own for a
#: parameter without a default, and ``require_fields`` /
#: ``normalize_path_arguments`` for one an aggregate could have carried.
_MISSING = re.compile(r"(?i)missing (?:\d+ )?required")


def _holder(root: object, chain: tuple[str, ...], convention: str) -> object:
    resource = functools.reduce(getattr, chain[:-1], root)
    return getattr(resource, convention) if convention else resource


def _label(kind: str, chain: tuple[str, ...], convention: str) -> str:
    return ".".join((kind, *chain[:-1], convention, chain[-1]) if convention else (kind, *chain))


def _functions() -> dict[str, Callable[..., object]]:
    """Every generated method, sync and async, in every calling convention."""
    sync = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    async_client = AsyncComposio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        return {
            _label(kind, chain, convention): getattr(type(_holder(root, chain, convention)), chain[-1])
            for kind, root in (("sync", sync), ("async", async_client))
            for chain in OPERATIONS_BY_CHAIN
            for convention in _CONVENTIONS
        }
    finally:
        sync.close()
        asyncio.run(async_client.close())


_FUNCTIONS = _functions()


def _stainless_required(function: Callable[..., object]) -> list[inspect.Parameter]:
    """What the Stainless-shaped signature requires: the first stub, or the only signature."""
    overloads = get_overloads(function)
    signature = inspect.signature(overloads[0] if overloads else function)
    return [
        parameter
        for parameter in list(signature.parameters.values())[1:]
        if parameter.default is inspect.Parameter.empty
        and parameter.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
    ]


_REQUIRED = {
    chain: _stainless_required(_FUNCTIONS[_label("sync", chain, "")]) for chain in OPERATIONS_BY_CHAIN
}
_DROPPED = [
    pytest.param(chain, parameter.name, id=f"{'.'.join(chain)}-{parameter.name}")
    for chain, required in _REQUIRED.items()
    for parameter in required
]


def _call(client: Composio, chain: tuple[str, ...], supplied: list[inspect.Parameter]) -> str:
    """The message of the ``TypeError`` a call raises, or ``""`` for any other outcome."""
    method: Any = getattr(_holder(client, chain, ""), chain[-1])
    positional = [
        "value" for parameter in supplied if parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    ]
    keywords = {
        parameter.name: "value" for parameter in supplied if parameter.kind is inspect.Parameter.KEYWORD_ONLY
    }
    try:
        method(*positional, **keywords)
    except TypeError as exc:
        return str(exc)
    except Exception:  # noqa: BLE001 - past the argument check, the outcome is not under test
        return ""
    return ""


@pytest.mark.parametrize("label", sorted(_FUNCTIONS))
def test_every_parameter_annotation_resolves_without_any(label: str) -> None:
    function = _FUNCTIONS[label]
    found = [
        location
        for signature in [*get_overloads(function), function]
        for name, hint in get_type_hints(signature).items()
        for location in _any_paths(hint, f"{signature.__qualname__}({name})")
    ]

    assert found == []


def test_the_walks_cover_every_operation_in_every_convention() -> None:
    assert len(_FUNCTIONS) == 2 * len(_CONVENTIONS) * len(OPERATIONS_BY_CHAIN)
    assert any(get_overloads(function) for function in _FUNCTIONS.values())


@respx.mock
@pytest.mark.parametrize("chain", list(OPERATIONS_BY_CHAIN), ids=".".join)
def test_the_stainless_signature_supplies_every_field_the_runtime_requires(
    client: Composio, chain: tuple[str, ...]
) -> None:
    respx.route().mock(return_value=httpx.Response(200, json={}))

    assert not _MISSING.search(_call(client, chain, _REQUIRED[chain]))


@respx.mock
@pytest.mark.parametrize(("chain", "dropped"), _DROPPED)
def test_every_field_the_stainless_signature_requires_is_required_at_runtime(
    client: Composio, chain: tuple[str, ...], dropped: str
) -> None:
    respx.route().mock(return_value=httpx.Response(200, json={}))
    supplied = [parameter for parameter in _REQUIRED[chain] if parameter.name != dropped]

    assert _MISSING.search(_call(client, chain, supplied))


def test_mypy_accepts_and_rejects_the_calls_it_should() -> None:
    """Each ``# type: ignore[code]`` in the file is an expected error, held by ``--warn-unused-ignores``."""
    stdout, stderr, status = mypy_api.run(
        [
            str(Path(__file__).parent / "typecheck" / "resource_calls.py"),
            "--config-file",
            str(_PYTHON_ROOT / "pyproject.toml"),
            "--warn-unused-ignores",
        ]
    )

    assert (status, stdout.strip()) == (0, "Success: no issues found in 1 source file"), stdout + stderr
