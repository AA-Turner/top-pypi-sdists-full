"""Tests for ``connector.oai.integration`` module."""

import io
import sys

import pytest_cases
from connector.generated import StandardCapabilityName
from connector.oai.integration import Integration
from connector.oai.modules.base_module import BaseIntegrationModule

from tests.oai.test_modules_cases import (
    case_add_module,
    case_register_module_capabilities,
)


@pytest_cases.parametrize_with_cases(
    ["integration", "module"],
    cases=[
        case_add_module,
    ],
)
async def test_add_module(
    integration: Integration,
    module: BaseIntegrationModule,
) -> None:
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        integration.add_module(module)

        assert captured_output.getvalue().strip() == "registered module"
        assert module in integration.modules
    finally:
        sys.stdout = sys.__stdout__


@pytest_cases.parametrize_with_cases(
    ["integration", "module"],
    cases=[
        case_register_module_capabilities,
    ],
)
async def test_register_module_capabilities(
    integration: Integration,
    module: BaseIntegrationModule,
) -> None:
    integration.add_module(module)

    assert integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIALS] is not None
    assert integration.info().response.capabilities == [
        StandardCapabilityName.APP_INFO,
        StandardCapabilityName.VALIDATE_CREDENTIALS,
    ]
    assert module.capabilities == [StandardCapabilityName.VALIDATE_CREDENTIALS]
