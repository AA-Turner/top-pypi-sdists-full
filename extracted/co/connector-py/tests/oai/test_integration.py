"""Tests for ``connector.oai.integration`` module."""

import json
import typing as t

import pytest
import pytest_cases
from connector.oai.capability import (
    CapabilityCallableProto,
    CustomRequest,
    CustomResponse,
    StandardCapabilityName,
)
from connector.oai.integration import CapabilityMetadata, DescriptionData, Integration
from connector_sdk_types.generated import BasicCredential, Info
from pydantic import BaseModel


@pytest_cases.parametrize_with_cases(
    ["integration", "capability_name", "request_", "expected_response"],
    cases=[
        "tests.oai.test_dispatch_cases",
        "tests.oai.test_dispatch_settings_cases",
    ],
)
async def test_dispatch_settings(
    integration: Integration,
    capability_name: StandardCapabilityName,
    request_: str,
    expected_response: t.Any,
) -> None:
    actual_response = await integration.dispatch(capability_name, request_)
    assert json.loads(actual_response) == expected_response.model_dump()


@pytest_cases.parametrize_with_cases(
    ["integration", "expected_info"],
    cases=[
        "tests.oai.test_info_cases",
    ],
)
async def test_info(
    integration: Integration,
    expected_info: Info,
) -> None:
    actual_info = integration.info()
    assert actual_info.model_dump() == expected_info.model_dump()


@pytest_cases.parametrize_with_cases(
    ["capability_name", "integration_capabilities"],
    cases=[
        "tests.oai.test_register_capability_cases",
    ],
)
async def test_registration(
    capability_name: StandardCapabilityName | str,
    integration_capabilities: dict[StandardCapabilityName, CapabilityCallableProto[t.Any]],
) -> None:
    if isinstance(capability_name, StandardCapabilityName):
        assert capability_name in integration_capabilities


class CustomRequestModel(BaseModel):
    input: str


class CustomResponseModel(BaseModel):
    output: str


@pytest.mark.asyncio
async def test_register_custom_capabilities_without_metadata() -> None:
    """Test registering custom capabilities without metadata."""
    integration = Integration(
        app_id="test",
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="testing thing",
            categories=[],
        ),
    )

    async def custom_capability_one(
        args: CustomRequest[CustomRequestModel],
    ) -> CustomResponse[CustomResponseModel]:
        return CustomResponse(response=CustomResponseModel(output="success"))

    async def custom_capability_two(
        args: CustomRequest[CustomRequestModel],
    ) -> CustomResponse[CustomResponseModel]:
        return CustomResponse(response=CustomResponseModel(output="ok"))

    integration.register_custom_capabilities(
        {
            "custom_capability_one": custom_capability_one,
            "custom_capability_two": custom_capability_two,
        }
    )

    assert "custom_capability_one" in integration.capabilities
    assert "custom_capability_two" in integration.capabilities
    assert integration.capabilities["custom_capability_one"] == custom_capability_one
    assert integration.capabilities["custom_capability_two"] == custom_capability_two


@pytest.mark.asyncio
async def test_register_custom_capabilities_with_metadata() -> None:
    """Test registering custom capabilities with metadata."""
    integration = Integration(
        app_id="test",
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="testing thing",
            categories=[],
        ),
    )

    async def custom_capability_one(
        args: CustomRequest[CustomRequestModel],
    ) -> CustomResponse[CustomResponseModel]:
        return CustomResponse(response=CustomResponseModel(output="success"))

    async def custom_capability_two(
        args: CustomRequest[CustomRequestModel],
    ) -> CustomResponse[CustomResponseModel]:
        return CustomResponse(response=CustomResponseModel(output="ok"))

    metadata_one = CapabilityMetadata(
        display_name="Custom One",
        description="First custom capability",
    )
    metadata_two = CapabilityMetadata(
        display_name="Custom Two",
        description="Second custom capability",
    )

    integration.register_custom_capabilities(
        {
            "custom_capability_one": (custom_capability_one, metadata_one),
            "custom_capability_two": (custom_capability_two, metadata_two),
        }
    )

    assert "custom_capability_one" in integration.capabilities
    assert "custom_capability_two" in integration.capabilities
    assert integration.capabilities["custom_capability_one"] == custom_capability_one
    assert integration.capabilities["custom_capability_two"] == custom_capability_two
    assert integration.capability_metadata["custom_capability_one"].display_name == "Custom One"
    assert (
        integration.capability_metadata["custom_capability_one"].description
        == "First custom capability"
    )
    assert integration.capability_metadata["custom_capability_two"].display_name == "Custom Two"
    assert (
        integration.capability_metadata["custom_capability_two"].description
        == "Second custom capability"
    )
