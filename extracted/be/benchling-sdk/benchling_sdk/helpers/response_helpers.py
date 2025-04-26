from typing import Iterable, Optional, Type

from benchling_api_client.v2.types import Response

from benchling_sdk.errors import ExtendedBenchlingErrorBase, raise_for_status


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
