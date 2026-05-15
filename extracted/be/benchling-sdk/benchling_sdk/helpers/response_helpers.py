from typing import Iterable, Mapping, Optional, Type

from benchling_api_client.v2.types import Response

from benchling_sdk.errors import ExtendedBenchlingErrorBase, raise_for_status

RATE_LIMIT_LIMIT_HEADER = "X-Rate-Limit-Limit"
RATE_LIMIT_REMAINING_HEADER = "X-Rate-Limit-Remaining"
RATE_LIMIT_RESET_HEADER = "X-Rate-Limit-Reset"

LEGACY_RATE_LIMIT_LIMIT_HEADER = "X-RateLimit-Limit"
LEGACY_RATE_LIMIT_REMAINING_HEADER = "X-RateLimit-Remaining"
LEGACY_RATE_LIMIT_RESET_HEADER = "X-RateLimit-Reset"


def read_header_value(headers: Mapping[str, str], *expected_headers: str) -> Optional[str]:
    """
    Get a header value by name, with case-insensitive lookup and fallback support.

    Tries each expected header name in order, first with an exact match, then with a
    case-insensitive match. Returns the first found value or None.
    """
    for expected_header in expected_headers:
        value = headers.get(expected_header)
        if value is not None:
            return value
        lower_name = expected_header.lower()
        for header_name, header_value in headers.items():
            if header_name.lower() == lower_name:
                return header_value
    return None


def model_from_detailed(
    response: Response, error_types: Optional[Iterable[Type[ExtendedBenchlingErrorBase]]] = None
):
    """
    Deserialize a response into a model.

    May optionally take error_types which can produce an error_matcher() for more specific error cases.
    """
    matchers = [e.error_matcher() for e in error_types] if error_types else None
    raise_for_status(response, matchers)
    return response.parsed
