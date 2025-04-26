import json
import typing as t

import pytest_cases
from connector.generated import StandardCapabilityName
from connector.oai.integration import Integration


@pytest_cases.parametrize_with_cases(
    ["integration", "capability_name", "request_data", "expected_response"],
    cases=[
        "tests.oai.test_exception_handler_handled_cases",
    ],
)
async def test_handled_exception(
    integration: Integration,
    capability_name: StandardCapabilityName,
    request_data: str,
    expected_response: dict[str, t.Any],
) -> None:
    """Test various exception handlers."""
    response = await integration.dispatch(capability_name, request_data)
    assert json.loads(response) == expected_response
