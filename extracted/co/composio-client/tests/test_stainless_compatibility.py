"""The offline Stainless compatibility gate and its failure directions."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest


def load_checker() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "scripts" / "check_stainless_compatibility.py"
    spec = importlib.util.spec_from_file_location("_stainless_compatibility", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_checker()


@pytest.fixture(scope="module")
def fixture() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(checker.FIXTURE_PATH.read_text(encoding="utf-8")))


@pytest.fixture(scope="module")
def snapshot(fixture: dict[str, Any]) -> dict[str, Any]:
    return cast(dict[str, Any], checker.capture_importable(fixture))


def test_source_tree_preserves_the_frozen_contract(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    assert checker.compare_snapshot(fixture, snapshot) == []


def test_missing_root_export_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    broken["root_exports"].remove("RequestOptions")

    assert "missing root export RequestOptions" in checker.compare_snapshot(fixture, broken)


def test_missing_resource_parameter_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    del broken["clients"]["sync"]["resources"]["auth_configs"]["methods"]["create"]["parameters"]["toolkit"]

    assert any(
        "sync.auth_configs.create: missing parameter toolkit" in problem
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_readded_removed_parameter_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    expected = next(
        parameter
        for parameter in fixture["clients"]["sync"]["resources"]["connected_accounts"]["methods"]["create"][
            "parameters"
        ]
        if parameter["name"] == "validate_credentials"
    )
    broken["clients"]["sync"]["resources"]["connected_accounts"]["methods"]["create"]["parameters"][
        "validate_credentials"
    ] = {key: expected[key] for key in ("kind", "default", "annotation")}

    assert any(
        problem.startswith(
            "sync.connected_accounts.create: parameter validate_credentials "
            "is declared removed (removed upstream"
        )
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_removed_client_api_key_is_carved_out_and_readding_it_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    # rc.18 replaced `api_key` with `auth`; the carve-out is the declared
    # removal, and it must stop matching the moment the keyword comes back.
    assert "api_key" not in snapshot["clients"]["sync"]["methods"]["__init__"]["parameters"]
    assert not any(
        "client.__init__: missing parameter api_key" in problem
        for problem in checker.compare_snapshot(fixture, snapshot)
    )

    broken = copy.deepcopy(snapshot)
    expected = next(
        parameter
        for parameter in fixture["clients"]["sync"]["methods"]["__init__"]["parameters"]
        if parameter["name"] == "api_key"
    )
    broken["clients"]["sync"]["methods"]["__init__"]["parameters"]["api_key"] = {
        key: expected[key] for key in ("kind", "default", "annotation")
    }
    assert any(
        problem.startswith("sync.client.__init__: parameter api_key is declared removed (2.0.0-rc.18")
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_missing_wrapper_group_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    del broken["clients"]["async"]["resources"]["tools"]["streaming_methods"]

    assert "async.tools: missing streaming_methods" in checker.compare_snapshot(fixture, broken)


def test_missing_downstream_import_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    broken["compatibility_imports"]["composio_client._types"].remove("SequenceNotStr")

    assert "composio_client._types: missing compatibility import SequenceNotStr" in checker.compare_snapshot(
        fixture, broken
    )


def test_missing_type_module_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.tool_router.session_create_params"
    del broken["type_modules"][module]

    assert f"missing type module {module}" in checker.compare_snapshot(fixture, broken)


def test_unconstructible_parameter_alias_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.tool_router.session_create_params"
    broken["type_modules"][module]["symbols"]["SessionCreateParams"]["constructs_mapping"] = False

    assert any(
        "SessionCreateParams: parameter alias is not constructible" in problem
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_changed_request_annotation_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.auth_config_create_params"
    annotations = broken["type_modules"][module]["symbols"]["AuthConfigCreateParams"]["annotations"]
    annotations["toolkit"] = "Required[str]"

    assert any(
        f"{module}.AuthConfigCreateParams.toolkit: expected annotation Required[{module}.Toolkit], "
        "found Required[str]" == problem
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_missing_request_field_docstring_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.mcp.custom_create_params"
    del broken["type_modules"][module]["symbols"]["CustomCreateParams"]["descriptions"]["name"]

    assert f"{module}.CustomCreateParams.name: field docstring changed" in checker.compare_snapshot(
        fixture, broken
    )


def test_missing_response_field_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.tool_router.session_create_response"
    del broken["type_modules"][module]["symbols"]["SessionCreateResponse"]["fields"]["session_id"]

    assert any(
        "SessionCreateResponse: missing response field session_id" in problem
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_changed_response_annotation_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.mcp.custom_create_response"
    fields = broken["type_modules"][module]["symbols"]["CustomCreateResponse"]["fields"]
    fields["commands"]["annotation"] = "Any"

    assert any(
        f"{module}.CustomCreateResponse.commands: expected annotation {module}.Commands, found Any" == problem
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_missing_response_class_docstring_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.mcp.custom_create_response"
    del broken["type_modules"][module]["symbols"]["Commands"]["description"]

    assert f"{module}.Commands: class docstring changed" in checker.compare_snapshot(fixture, broken)


def test_missing_response_field_docstring_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.mcp.custom_create_response"
    del broken["type_modules"][module]["symbols"]["Commands"]["fields"]["claude"]["description"]

    assert f"{module}.Commands.claude: field docstring changed" in checker.compare_snapshot(fixture, broken)


def test_incomplete_response_model_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.tool_router.session_create_response"
    broken["type_modules"][module]["symbols"]["SessionCreateResponse"]["complete"] = False

    assert f"{module}.SessionCreateResponse: model annotations did not resolve" in checker.compare_snapshot(
        fixture, broken
    )


def test_missing_response_serialization_helpers_are_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    module = "composio_client.types.tool_router.session_create_response"
    broken["type_modules"][module]["symbols"]["SessionCreateResponse"]["serialization_helpers"] = False

    assert (
        f"{module}.SessionCreateResponse: missing response serialization helpers"
        in checker.compare_snapshot(fixture, broken)
    )


def test_wheel_inspection_refreshes_an_overwritten_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    command: list[str] = []

    def run(args: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        command.extend(args)
        return subprocess.CompletedProcess(args, 0, stdout="{}", stderr="")

    monkeypatch.setattr(checker.subprocess, "run", run)
    checker.snapshot_from_wheel(tmp_path / "composio_client-2.0.0-py3-none-any.whl")

    refresh = command.index("--refresh-package")
    assert command[refresh : refresh + 2] == ["--refresh-package", "composio-client"]


def _resource_parameter(snapshot: dict[str, Any], path: str, method: str, name: str) -> dict[str, Any]:
    return cast(
        dict[str, Any], snapshot["clients"]["sync"]["resources"][path]["methods"][method]["parameters"][name]
    )


def test_a_loosened_parameter_type_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    _resource_parameter(broken, "link", "create", "auth_config_id")["annotation"] = "object"

    assert "sync.link.create.auth_config_id: expected type str, found object" in checker.compare_snapshot(
        fixture, broken
    )


def test_a_required_parameter_made_optional_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    _resource_parameter(broken, "link", "create", "user_id")["default"] = {
        "kind": "sentinel",
        "value": "OMIT",
    }

    assert any(
        problem.startswith("sync.link.create.user_id: expected a required parameter")
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_a_declared_literal_addition_that_is_absent_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    captured = next(
        parameter["annotation"]
        for parameter in fixture["clients"]["sync"]["resources"]["tool_router.session"]["methods"][
            "execute_meta"
        ]["parameters"]
        if parameter["name"] == "slug"
    )
    _resource_parameter(broken, "tool_router.session", "execute_meta", "slug")["annotation"] = captured

    assert any(
        problem.startswith("sync.tool_router.session.execute_meta.slug: declared Literal addition")
        for problem in checker.compare_snapshot(fixture, broken)
    )


def _resource_method(snapshot: dict[str, Any], lane: str, path: str, method: str) -> dict[str, Any]:
    return cast(dict[str, Any], snapshot["clients"][lane]["resources"][path]["methods"][method])


def test_a_changed_return_annotation_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    broken = copy.deepcopy(snapshot)
    _resource_method(broken, "async", "link", "create")["return"] = "object"

    assert "async.link.create: expected return LinkCreateResponse, found object" in checker.compare_snapshot(
        fixture, broken
    )


@pytest.mark.parametrize(("resource", "method"), sorted(checker.UPSTREAM_RETURN_DEPARTURES))
def test_a_declared_return_departure_that_is_absent_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any], resource: str, method: str
) -> None:
    """Every entry is live, and returning the captured annotation again reports it."""
    path = next(path for path in snapshot["clients"]["sync"]["resources"] if path.split(".")[-1] == resource)
    declared, _reason = checker.UPSTREAM_RETURN_DEPARTURES[(resource, method)]
    assert _resource_method(snapshot, "sync", path, method)["return"] == declared

    broken = copy.deepcopy(snapshot)
    _resource_method(broken, "sync", path, method)["return"] = fixture["clients"]["sync"]["resources"][path][
        "methods"
    ][method]["return"]

    assert any(
        problem.startswith(f"sync.{path}.{method}: declared return departure {declared}")
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_a_declared_return_departure_returns_only_the_declared_name(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    broken = copy.deepcopy(snapshot)
    _resource_method(broken, "sync", "tool_router.session", "execute")["return"] = (
        "SessionExecuteInputRequiredResponse"
    )

    assert (
        "sync.tool_router.session.execute: expected return SessionExecuteResult, "
        "found SessionExecuteInputRequiredResponse"
    ) in checker.compare_snapshot(fixture, broken)


def test_the_execute_response_names_are_classes_under_the_frozen_checks(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    """The three `...Response` names carry no exemption: a lost field is reported."""
    module = "composio_client.types.tool_router.session_execute_response"
    assert snapshot["type_modules"][module]["symbols"]["SessionExecuteResponse"]["kind"] == "model"
    broken = copy.deepcopy(snapshot)
    del broken["type_modules"][module]["symbols"]["SessionExecuteResponse"]["fields"]["log_id"]

    assert f"{module}.SessionExecuteResponse: missing response field log_id" in checker.compare_snapshot(
        fixture, broken
    )


def _declared_annotation(symbol: dict[str, Any], field: str) -> str:
    """A field's annotation, from a model symbol or a ``TypedDict`` one."""
    model_field = symbol.get("fields", {}).get(field, {}).get("annotation")
    return cast(str, model_field or symbol.get("annotations", {}).get(field))


@pytest.mark.parametrize(("module", "name", "field"), sorted(checker.UPSTREAM_UNION_ADDITIONS))
def test_every_declared_union_addition_is_live_and_reported_when_absent(
    fixture: dict[str, Any], snapshot: dict[str, Any], module: str, name: str, field: str
) -> None:
    emitted = _declared_annotation(snapshot["type_modules"][module]["symbols"][name], field)
    frozen = _declared_annotation(fixture["type_modules"][module]["symbols"][name], field)
    _after, added, _reason = checker.UPSTREAM_UNION_ADDITIONS[(module, name, field)]

    assert f"{module}.{added}" in emitted
    assert checker.absent_union_addition(module, name, field, frozen, emitted) is None
    assert (
        checker.absent_union_addition(module, name, field, frozen, checker.canonical_annotation(frozen))
        == f"{module}.{name}.{field}: declared union addition {added} ({_reason}) is absent"
    )


def test_a_union_back_at_its_captured_members_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    module = "composio_client.types.tool_router.session_create_response"
    frozen = fixture["type_modules"][module]["symbols"]["Config"]["fields"]["toolkits"]["annotation"]
    broken = copy.deepcopy(snapshot)
    broken["type_modules"][module]["symbols"]["Config"]["fields"]["toolkits"]["annotation"] = (
        checker.canonical_annotation(frozen)
    )

    problems = checker.compare_snapshot(fixture, broken)
    assert (
        f"{module}.Config.toolkits: declared union addition ConfigToolkitsRequireApproval "
        "(approval-only variant added upstream in the 2026-10 spec refresh) is absent"
    ) in problems


def test_a_request_union_back_at_its_captured_members_is_reported(
    fixture: dict[str, Any], snapshot: dict[str, Any]
) -> None:
    module = "composio_client.types.tool_router.session_patch_params"
    frozen = fixture["type_modules"][module]["symbols"]["SessionPatchParams"]["annotations"]["tools"]
    broken = copy.deepcopy(snapshot)
    broken["type_modules"][module]["symbols"]["SessionPatchParams"]["annotations"]["tools"] = (
        checker.canonical_annotation(frozen)
    )

    assert any(
        problem.startswith(f"{module}.SessionPatchParams.tools: declared union addition ToolsRequireApproval")
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_a_union_addition_whose_captured_sibling_is_gone_is_reported() -> None:
    """An entry naming a member the capture does not hold widens nothing, and says so."""
    module = "composio_client.types.tool_router.session_create_response"
    captured = f"Union[{module}.ConfigToolkitsEnabled, NoneType]"

    assert checker.expected_annotation(module, "Config", "toolkits", captured) == captured
    assert checker.absent_union_addition(
        module, "Config", "toolkits", captured, "ConfigToolkitsEnabled | ConfigToolkitsRequireApproval | None"
    ) == (
        f"{module}.Config.toolkits: declared union addition ConfigToolkitsRequireApproval "
        "(approval-only variant added upstream in the 2026-10 spec refresh) is absent"
    )


def test_an_undeclared_union_member_is_reported(fixture: dict[str, Any], snapshot: dict[str, Any]) -> None:
    """The ledger licenses the one declared class, not any widening of that union."""
    module = "composio_client.types.tool_router.session_create_response"
    broken = copy.deepcopy(snapshot)
    field = broken["type_modules"][module]["symbols"]["Config"]["fields"]["toolkits"]
    field["annotation"] = field["annotation"].replace("ConfigToolkitsRequireApproval", "ConfigTags")

    assert any(
        problem.startswith(f"{module}.Config.toolkits: expected annotation")
        for problem in checker.compare_snapshot(fixture, broken)
    )


def test_annotations_compare_by_meaning_not_by_spelling() -> None:
    assert checker.canonical_type("Optional[List[Literal['a', 'b']]] | Omit") == checker.canonical_type(
        'list[Literal["b", "a"]] | None | Omit'
    )
    assert checker.canonical_type("Dict[str, Optional[object]]") == checker.canonical_type(
        "dict[str, object | None]"
    )
    assert checker.canonical_type("Dict[str, str]") != checker.canonical_type("dict[str, object]")
    assert checker.canonical_type("Literal['a'] | Literal['b']") == checker.canonical_type(
        'Literal["a", "b"]'
    )


@pytest.mark.parametrize(("module", "name", "field"), sorted(checker.UPSTREAM_FIELD_LITERAL_ADDITIONS))
def test_every_declared_tag_addition_preserves_captured_values(
    fixture: dict[str, Any], snapshot: dict[str, Any], module: str, name: str, field: str
) -> None:
    frozen = _declared_annotation(fixture["type_modules"][module]["symbols"][name], field)
    emitted = _declared_annotation(snapshot["type_modules"][module]["symbols"][name], field)
    expected = checker.expected_annotation(module, name, field, frozen)

    assert checker.canonical_type(expected) != checker.canonical_type(frozen)
    assert checker.canonical_type(emitted) == checker.canonical_type(expected)
