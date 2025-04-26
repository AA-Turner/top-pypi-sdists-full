import json

import pydantic
from connector.generated import (
    ErrorResponse,
)
from connector.oai.capability import StandardCapabilityName
from connector.tests.gather_cases import gather_cases
from connector.tests.mock_httpx import mock_requests
from connector.tests.type_definitions import ResponseBodyMap
from {name}.constants import BASE_URL
from {name}.integration import integration
from pytest_cases import parametrize_with_cases
from pytest_httpx import HTTPXMock

# If you want to test specific capability than replace gather_cases with list of cases.
INTEGRATION_CASES = gather_cases(integration)


@parametrize_with_cases(
    ["capability_name", "args", "response_body_map", "expected_response"],
    cases=INTEGRATION_CASES,
)
async def test_all_capabilities(
    capability_name: StandardCapabilityName,
    args: pydantic.BaseModel,
    response_body_map: ResponseBodyMap,
    expected_response: pydantic.BaseModel | ErrorResponse,
    httpx_mock: HTTPXMock,
) -> None:
    """Test all registered capabilities.
    Cases MUST:
        - be within any directory in <connector_name>/tests or tests themselves
        - file name in this format: "test_{{capability_name}}_cases.py"
    Good example of file location:
        - {name}/tests/read_capabilities/test_list_accounts_cases.py
    """
    mock_requests(response_body_map, httpx_mock, host=BASE_URL)
    response = await integration.dispatch(capability_name, args.model_dump_json())

    assert json.loads(response) == expected_response.model_dump()
