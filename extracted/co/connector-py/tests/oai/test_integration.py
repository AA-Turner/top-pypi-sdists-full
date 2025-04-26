"""Tests for ``connector.oai.integration`` module."""

import json
import typing as t

import pytest_cases
from connector.generated import Info
from connector.oai.capability import CapabilityCallableProto, StandardCapabilityName
from connector.oai.integration import Integration


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
