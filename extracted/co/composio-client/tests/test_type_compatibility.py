"""The generated ``types`` tree retains the frozen Stainless surface."""

from __future__ import annotations

import copy
import importlib
import inspect
import json
import pkgutil
from pathlib import Path
from typing import Any, cast, get_type_hints

from check_stainless_compatibility import (
    canonical_annotation,
    canonical_type,
    declares_no_annotation,
    expected_annotation,
    expected_request_annotation,
)
from typing_extensions import is_typeddict

import composio_client
from composio_client import BaseModel
from composio_client.types.auth_config_create_params import AuthConfigCreateParams
from composio_client.types.auth_config_create_response import AuthConfig, AuthConfigCreateResponse, Toolkit

FIXTURE = Path(__file__).parent / "fixtures" / "stainless_surface.json"


def _manifest() -> dict[str, Any]:
    fixture = cast(dict[str, Any], json.loads(FIXTURE.read_text(encoding="utf-8")))
    return cast(dict[str, Any], fixture["type_modules"])


def test_frozen_manifest_retains_its_documentation_contract() -> None:
    symbols = [symbol for module in _manifest().values() for symbol in module["symbols"].values()]
    documented_classes = sum(symbol.get("description") is not None for symbol in symbols)
    documented_fields = sum(
        len(symbol.get("descriptions", {}))
        + sum(field.get("description") is not None for field in symbol.get("fields", {}).values())
        for symbol in symbols
    )

    # The oracle source has six shadowed duplicate declarations; the frozen
    # public surface contains the 1,420 distinct fields callers can reach.
    assert (documented_classes, documented_fields) == (148, 1420)


def _annotation_report(manifest: dict[str, Any]) -> tuple[list[str], int]:
    """Every model field whose emitted annotation differs from the oracle's.

    Both sides go through ``canonical_annotation`` so the comparison measures
    fidelity to the frozen 1.43.0 contract rather than the renderer's own
    spelling of it.
    """
    problems: list[str] = []
    checked = 0
    for module_name, expected in manifest.items():
        module = importlib.import_module(module_name)
        for name, symbol in expected["symbols"].items():
            if symbol["kind"] != "model":
                continue
            emitted = {
                field_name: canonical_annotation(inspect.formatannotation(field.annotation))
                for field_name, field in getattr(module, name).model_fields.items()
            }
            for field_name, field in symbol["fields"].items():
                # A null expectation is a problem, not a match -- the same guard
                # `compare_snapshot` carries, for the same reason: the renderer
                # emits `Any` when the capture holds nothing, so folding a
                # missing expectation to `Any` would confirm a flattened tree.
                if declares_no_annotation(field.get("annotation")):
                    problems.append(f"{module_name}.{name}.{field_name}: fixture declares no annotation")
                    continue
                declared = canonical_annotation(
                    expected_annotation(module_name, name, field_name, field["annotation"])
                )
                found = emitted.get(field_name)
                if found is None or canonical_type(found) != canonical_type(declared):
                    problems.append(f"{module_name}.{name}.{field_name}: expected {declared}, found {found}")
            checked += 1
    return problems, checked


def test_every_stainless_type_module_and_export_is_present() -> None:
    for module_name, expected in _manifest().items():
        module = importlib.import_module(module_name)
        assert set(expected["exports"]) <= set(module.__all__)
        for name in expected["exports"]:
            assert hasattr(module, name), f"{module_name}.{name}"


def test_every_generated_type_module_imports() -> None:
    """Declaration order must leave every module importable.

    A model field naming a class declared later in the file resolves against
    the enclosing scope at class-creation time, so a class named ``Warning``
    binds to the builtin and pydantic rejects the module outright.
    """

    def reraise(name: str) -> None:
        raise AssertionError(f"walking composio_client.types could not import {name}")

    package = importlib.import_module("composio_client.types")
    # `walk_packages` swallows a subpackage `__init__` failure by default, which
    # would drop that whole subtree from `discovered` and quietly shrink what
    # this test walks.
    discovered = sorted(
        name for _, name, _ in pkgutil.walk_packages(package.__path__, "composio_client.types.", reraise)
    )
    for module_name in discovered:
        importlib.import_module(module_name)

    assert set(_manifest()) <= set(discovered)


def test_request_aliases_remain_constructible_typed_dicts() -> None:
    checked = 0
    for module_name, expected in _manifest().items():
        module = importlib.import_module(module_name)
        for name, symbol in expected["symbols"].items():
            if symbol["kind"] != "typed_dict":
                continue
            value = getattr(module, name)
            assert is_typeddict(value), f"{module_name}.{name}"
            assert value() == {}
            checked += 1
    assert checked == 375


def _request_annotation_report(manifest: dict[str, Any]) -> tuple[list[str], int]:
    problems: list[str] = []
    checked = 0
    for module_name, expected in manifest.items():
        module = importlib.import_module(module_name)
        for name, symbol in expected["symbols"].items():
            if symbol["kind"] != "typed_dict":
                continue
            emitted = {
                field_name: canonical_annotation(inspect.formatannotation(annotation))
                for field_name, annotation in get_type_hints(
                    getattr(module, name), include_extras=True
                ).items()
            }
            for field_name, annotation in symbol["annotations"].items():
                if declares_no_annotation(annotation):
                    problems.append(f"{module_name}.{name}.{field_name}: fixture declares no annotation")
                    continue
                declared = canonical_annotation(
                    expected_request_annotation(module_name, name, field_name, annotation)
                )
                found = emitted.get(field_name)
                if found is None or canonical_type(found) != canonical_type(declared):
                    problems.append(f"{module_name}.{name}.{field_name}: expected {declared}, found {found}")
            checked += 1
    return problems, checked


def test_request_typed_dicts_retain_their_declared_annotations() -> None:
    problems, checked = _request_annotation_report(_manifest())

    assert problems == []
    assert checked == 375


def test_request_annotation_comparison_reports_a_mutated_expectation() -> None:
    mutated = copy.deepcopy(_manifest())
    module = "composio_client.types.auth_config_create_params"
    mutated[module]["symbols"]["AuthConfigCreateParams"]["annotations"]["toolkit"] = "Required[str]"
    problems, _ = _request_annotation_report(mutated)

    assert any(
        f"{module}.AuthConfigCreateParams.toolkit: expected Required[str]" in problem for problem in problems
    )


def test_response_models_retain_fields_aliases_and_requiredness() -> None:
    checked = 0
    for module_name, expected in _manifest().items():
        module = importlib.import_module(module_name)
        for name, symbol in expected["symbols"].items():
            if symbol["kind"] != "model":
                continue
            value = getattr(module, name)
            assert inspect.isclass(value) and issubclass(value, BaseModel)
            assert value.__pydantic_root_model__ is symbol["root_model"]
            assert {
                field_name: {
                    "alias": field.alias,
                    "required": field.is_required(),
                }
                for field_name, field in value.model_fields.items()
                if field_name in symbol["fields"]
            } == {
                field_name: {
                    "alias": field["alias"],
                    "required": field["required"],
                }
                for field_name, field in symbol["fields"].items()
            }
            checked += 1
    assert checked == 544


def test_response_models_report_resolved_annotations() -> None:
    """An incomplete model would hand the annotation gate a ``ForwardRef``.

    ``__pydantic_complete__`` is self-healing -- pydantic rebuilds a model on
    first validation -- so this reads "resolved by the time the gates run", not
    "resolved at class creation". `test_every_generated_type_module_imports` is
    what pins the creation-time property, because a class that resolves its own
    name to a builtin fails there before anything can heal it.
    """
    checked = 0
    for module_name, expected in _manifest().items():
        module = importlib.import_module(module_name)
        for name, symbol in expected["symbols"].items():
            if symbol["kind"] != "model":
                continue
            assert getattr(module, name).__pydantic_complete__, f"{module_name}.{name}"
            checked += 1
    assert checked == 544


def test_response_models_retain_their_declared_annotations() -> None:
    problems, checked = _annotation_report(_manifest())

    assert problems == []
    assert checked == 544


def test_annotation_comparison_reports_a_mutated_expectation() -> None:
    """The total comparison is load-bearing, not vacuously equal."""
    mutated = copy.deepcopy(_manifest())
    module = "composio_client.types.mcp.custom_create_response"
    mutated[module]["symbols"]["CustomCreateResponse"]["fields"]["commands"]["annotation"] = "str"
    problems, _ = _annotation_report(mutated)

    assert any(f"{module}.CustomCreateResponse.commands: expected str" in problem for problem in problems)


def test_annotation_comparison_reports_an_expectation_that_went_missing() -> None:
    """A fixture that lost an annotation must fail, not agree with `Any`.

    This is the shape the original regression had: the renderer emits `Any`
    when the capture carries nothing, so a comparison that read a missing
    expectation the same way would confirm the flattened tree as correct.
    """
    mutated = copy.deepcopy(_manifest())
    module = "composio_client.types.mcp.custom_create_response"
    mutated[module]["symbols"]["CustomCreateResponse"]["fields"]["commands"]["annotation"] = None
    problems, _ = _annotation_report(mutated)

    assert f"{module}.CustomCreateResponse.commands: fixture declares no annotation" in problems


def test_annotation_comparison_rejects_an_expectation_of_any() -> None:
    """`Any` is the flattened spelling, so it can never be the expectation.

    A refresh that captured `Any` instead of losing the key entirely would
    otherwise agree with the tree the renderer built from it, which is one step
    around the guard above rather than a different failure.
    """
    mutated = copy.deepcopy(_manifest())
    module = "composio_client.types.mcp.custom_create_response"
    problems: list[str] = []
    for spelling in ("Any", "typing.Any"):
        mutated[module]["symbols"]["CustomCreateResponse"]["fields"]["commands"]["annotation"] = spelling
        problems.extend(_annotation_report(mutated)[0])

    expected = f"{module}.CustomCreateResponse.commands: fixture declares no annotation"
    assert problems.count(expected) == 2


def test_only_a_whole_annotation_of_any_counts_as_declaring_nothing() -> None:
    """`Dict[str, Any]` is a real annotation; a bare `Any` is the flattening."""
    assert declares_no_annotation("Any")
    assert declares_no_annotation("typing.Any")
    assert declares_no_annotation(None)
    assert not declares_no_annotation("Dict[str, Any]")
    assert not declares_no_annotation("Optional[Any]")
    assert not declares_no_annotation("str")


def test_canonicalization_folds_only_the_renderer_list_spelling() -> None:
    assert canonical_annotation("List[str]") == canonical_annotation("list[str]")
    assert canonical_annotation("Optional[List[Commands]]") == "Optional[list[Commands]]"
    assert canonical_annotation("list[typing.Union[str, Item]]") == "list[Union[str, Item]]"
    assert canonical_annotation("Dict[str, str]") == "Dict[str, str]"
    # A Literal member is an accepted *value*; folding it would make two
    # different accepted values compare equal.
    assert canonical_annotation("Literal['List[str]']") == "Literal['List[str]']"
    assert canonical_annotation("Literal['typing.Warning']") == "Literal['typing.Warning']"
    # An escaped quote must not end the literal early and expose the rest.
    assert canonical_annotation(r"""Literal['a\'b" List[str]']""") == r"""Literal['a\'b" List[str]']"""
    assert canonical_annotation("Optional[Union[Literal['List[str]'], List[str]]]") == (
        "Optional[Union[Literal['List[str]'], list[str]]]"
    )
    assert canonical_annotation("ListingItem") == "ListingItem"
    assert canonical_annotation("composio_client.types.mcp.custom_create_response.Commands") == (
        "composio_client.types.mcp.custom_create_response.Commands"
    )


def test_representative_request_and_response_values_keep_their_shape() -> None:
    params = AuthConfigCreateParams(toolkit={"slug": "gmail"})
    response = AuthConfigCreateResponse(
        auth_config={"id": "ac_1", "auth_scheme": "OAUTH2", "is_composio_managed": True},
        toolkit={"slug": "gmail"},
    )

    assert params == {"toolkit": {"slug": "gmail"}}
    assert isinstance(response.auth_config, AuthConfig)
    assert response.auth_config.id == "ac_1"
    assert response.auth_config.auth_scheme == "OAUTH2"
    assert isinstance(response.toolkit, Toolkit)
    assert response.toolkit.slug == "gmail"
    assert response.to_dict() == {
        "auth_config": {
            "auth_scheme": "OAUTH2",
            "id": "ac_1",
            "is_composio_managed": True,
        },
        "toolkit": {"slug": "gmail"},
    }
    assert response.auth_config.to_dict() == {
        "auth_scheme": "OAUTH2",
        "id": "ac_1",
        "is_composio_managed": True,
    }
    assert response.model_dump() == {
        "auth_config": {
            "auth_scheme": "OAUTH2",
            "id": "ac_1",
            "is_composio_managed": True,
            "restrict_to_following_tools": None,
        },
        "toolkit": {"slug": "gmail"},
    }


def test_root_types_export_and_owned_only_modules_are_additive() -> None:
    assert composio_client.types is importlib.import_module("composio_client.types")
    assert "AuthConfigCreateParams" in composio_client.types.__all__
    assert "ApiKeyRevocationCreateParams" in composio_client.types.__all__
    importlib.import_module("composio_client.types.api_key_revocation_create_params")
