"""Self-consistency checks for the frozen Stainless public-surface oracle."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from check_stainless_compatibility import declares_no_annotation

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "stainless_surface.json"


@pytest.fixture(scope="module")
def surface() -> dict[str, Any]:
    loaded: object = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return cast(dict[str, Any], loaded)


def test_fixture_is_pinned_to_the_takeover_oracle(surface: dict[str, Any]) -> None:
    assert surface["oracle"] == {
        "package": "composio-client",
        "version": "1.43.0",
        "regenerate": (
            "cd python && uv run --isolated --no-project --with composio-client==1.43.0 "
            "python scripts/capture_stainless_surface.py"
        ),
    }


def test_fixture_records_the_released_client_inventory(surface: dict[str, Any]) -> None:
    assert len(surface["root_exports"]) == 42
    assert len(surface["type_modules"]) == 120

    for flavor in ("sync", "async"):
        resources = surface["clients"][flavor]["resources"]
        assert sum(len(resource["methods"]) for resource in resources.values()) == 64
        assert sum(len(resource["raw_methods"]) for resource in resources.values()) == 64
        assert sum(len(resource["streaming_methods"]) for resource in resources.values()) == 64


def test_fixture_records_first_party_downstream_imports(surface: dict[str, Any]) -> None:
    assert surface["compatibility_imports"] == {
        "composio_client._base_client": ["DEFAULT_MAX_RETRIES"],
        "composio_client._types": ["SequenceNotStr"],
    }


def test_every_parameter_typed_dict_remains_constructible(surface: dict[str, Any]) -> None:
    typed_dicts = [
        symbol
        for name, module in surface["type_modules"].items()
        if name.endswith("_params")
        for symbol in module["symbols"].values()
        if symbol["kind"] == "typed_dict"
    ]

    assert len(typed_dicts) > 51
    assert all(symbol["constructs_mapping"] for symbol in typed_dicts)


def test_every_parameter_typed_dict_field_carries_a_resolved_annotation(surface: dict[str, Any]) -> None:
    annotations = [
        annotation
        for module in surface["type_modules"].values()
        for symbol in module["symbols"].values()
        if symbol["kind"] == "typed_dict"
        for annotation in symbol["annotations"].values()
    ]

    assert len(annotations) == 5259
    assert sum(annotation.startswith("Required[") for annotation in annotations) == 469
    assert [annotation for annotation in annotations if "ForwardRef" in annotation] == []


def test_parameter_alias_metadata_survives_resolution(surface: dict[str, Any]) -> None:
    annotations = surface["type_modules"]["composio_client.types.auth_config_create_params"]["symbols"]
    auth_scheme = annotations["AuthConfigUnionMember1"]["annotations"]["auth_scheme"]

    assert "Annotated[" in auth_scheme
    assert auth_scheme.endswith("PropertyInfo(alias='authScheme')]]")


def test_every_response_model_field_carries_a_captured_annotation(surface: dict[str, Any]) -> None:
    """The gates that compare annotations are only as good as this property.

    Both the renderer and the comparison fall back to ``Any`` for an absent
    annotation, so a refresh that dropped them would emit ``Any`` everywhere,
    expect ``Any`` everywhere, and agree -- reinstating the exact regression
    those gates exist to catch, with nothing left to notice. Assert the oracle's
    own contents here so the loss fails at the fixture instead.
    """
    fields = [
        field
        for module in surface["type_modules"].values()
        for symbol in module["symbols"].values()
        if symbol["kind"] == "model"
        for field in symbol["fields"].values()
    ]

    assert len(fields) == 6908
    # `Any` is forbidden as well as absent -- in any spelling, and via `.get`
    # so a lost key is reported rather than raising. The oracle declares none of
    # them, and each would make the renderer and the gate agree about nothing:
    # emit `Any`, expect `Any`, pass -- the regression, certified.
    assert [field for field in fields if declares_no_annotation(field.get("annotation"))] == []


def test_sync_and_async_resource_methods_are_symmetric(surface: dict[str, Any]) -> None:
    sync = surface["clients"]["sync"]["resources"]
    async_ = surface["clients"]["async"]["resources"]

    assert sync.keys() == async_.keys()
    for path in sync:
        assert sync[path]["methods"] == async_[path]["methods"]
        assert sync[path]["raw_methods"] == async_[path]["raw_methods"]
        assert sync[path]["streaming_methods"] == async_[path]["streaming_methods"]
