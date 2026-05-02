"""Cases for testing ``validate_credentials`` capability."""

import typing as t

from connector.generated import (
    ErrorResponse,
    StandardCapabilityName,
    ValidateCredentials,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.tests.type_definitions import ResponseBodyMap

from tests.common_mock_data import SETTINGS, VALID_AUTH

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    ValidateCredentialsRequest,
    ResponseBodyMap,
    ValidateCredentialsResponse | ErrorResponse,
]


def case_validate_credentials_200() -> Case:
    """Successful request."""
    args = ValidateCredentialsRequest(
        request=ValidateCredentials(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map: ResponseBodyMap = {{}}
    expected_response = ValidateCredentialsResponse(
        response=ValidatedCredentials(valid=True, unique_tenant_id="REPLACE_WITH_UNIQUE_TENANT_ID"),
    )
    return StandardCapabilityName.VALIDATE_CREDENTIALS, args, response_body_map, expected_response
