import importlib
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any, cast

import git
import pydantic
import pytest
import tomlkit
from connector.oai.capability import StandardCapabilityName
from connector.oai.integration import Integration
from connector_sdk_types import OAS
from connector_sdk_types.generated import (
    AppInfoRequest,
    AppInfoRequestPayload,
    OpenAPISpecificationInfo,
)
from openapi_schema_validator import OAS30Validator

from .schema_linter_checks import SCHEMA_CHECK_LIST

"""
Test utilities
"""


def _get_project_root() -> Path:
    path = Path(__file__).resolve()
    git_repo = git.Repo(path, search_parent_directories=True)
    return Path(git_repo.git.rev_parse("--show-toplevel"))


def _iter_all_integrations() -> Iterable[tuple[str, Integration]]:
    integrations: list[tuple[str, Integration]] = []

    root = _get_project_root()
    connectors_dir = root / "projects" / "connectors" / "python"

    for connector_dir in connectors_dir.iterdir():
        if not connector_dir.is_dir() or connector_dir.name.startswith("_"):
            continue

        pyproject = connector_dir / "pyproject.toml"
        if not pyproject.exists():
            continue

        with pyproject.open("r") as f:
            config = tomlkit.load(f)

        package_name = config.get("project", {}).get("name", "")
        if not package_name.startswith("connector-"):
            continue

        for potential_module in connector_dir.iterdir():
            if potential_module.is_dir() and (potential_module / "integration.py").exists():
                import_name = potential_module.name
                try:
                    module = importlib.import_module(f"{import_name}.integration")
                    integration = cast(Integration, module.integration)
                    integrations.append((import_name, integration))
                    break
                except (ImportError, AttributeError):
                    continue

    return integrations


async def _get_app_schema(
    integration: Integration,
) -> tuple[OAS.OpenAPI, OpenAPISpecificationInfo]:
    # Construct request and retrieve the dispatch
    request = AppInfoRequest(
        request=AppInfoRequestPayload(),
        credentials=None,
        settings=None,
    )
    request_json = request.model_dump_json()
    response = await integration.dispatch(StandardCapabilityName.APP_INFO, request_json)

    # Parse the response
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError as e:
        raise AssertionError(f"{integration.app_id} app_info returned invalid JSON: {e}") from e

    # Parse common fields
    connector_response = response_json.get("response")
    app_schema = connector_response.get("app_schema") if connector_response else None
    is_error = response_json.get("is_error", False)

    # Fail on errors/exceptions
    if is_error:
        error = response_json.get("error")
        if error:
            raise AssertionError(
                f"{integration.app_id} app_info errored with: {error.get('message')}"
            )
        else:
            raise AssertionError(f"{integration.app_id} app_info errored with no error message")

    # Fail on missing app_schema
    if app_schema is None:
        raise AssertionError(f"{integration.app_id} returned app_schema as None")

    # Validate the app_schema as OpenAPI (standard)
    try:
        spec = OAS.OpenAPI.model_validate(app_schema)
    except pydantic.ValidationError as e:
        raise AssertionError(f"{integration.app_id} returned invalid app_schema: {e}") from e

    # Validate the app_schema.info as OpenAPISpecificationInfo (custom model)
    try:
        info = OpenAPISpecificationInfo.model_validate(spec.info.model_dump(by_alias=True))
    except pydantic.ValidationError as e:
        raise AssertionError(f"{integration.app_id} returned invalid app_schema.info: {e}") from e

    return spec, info


def _validate_oas_with_warnings(spec_dict: dict[str, Any], connector_name: str):
    """Validate OAS and return (errors, warnings)."""
    validator = OAS30Validator(spec_dict)
    errors = list(validator.iter_errors(spec_dict))
    warnings = []

    for error in errors:
        if hasattr(error, "level") and error.level == "warning":
            warnings.append(error)
            errors.remove(error)

    return sorted(errors, key=lambda e: str(e.path)), sorted(warnings, key=lambda e: str(e.path))


"""
Connector tests
"""

ALL_INTEGRATIONS = _iter_all_integrations()


@pytest.mark.appinfo_all_connectors
@pytest.mark.parametrize("import_name, integration", ALL_INTEGRATIONS)
async def test_appinfo_all_connectors(import_name: str, integration: Integration):
    app_schema, info_schema = await _get_app_schema(integration)

    # OAS 3.0 compliance and validity check
    errors, warnings = _validate_oas_with_warnings(
        app_schema.model_dump(by_alias=True), import_name
    )
    assert not errors, f"OAS validation errors for {import_name}: {errors}"

    if warnings:
        pytest.warns(UserWarning, lambda: f"OAS validation warnings for {import_name}: {warnings}")

    # Various schema checks
    for check in SCHEMA_CHECK_LIST:
        try:
            check.check(app_schema, info_schema, integration, import_name)
        except AssertionError as e:
            if check.severity == "error":
                raise AssertionError(f"Linter error for {import_name}: {e}") from e
            else:
                pytest.warns(UserWarning, match=f"Linter warning for {import_name}: {e}")
