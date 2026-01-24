from typing import Any, Callable, Dict, List

from galileo_core.helpers.logger import logger
from galileo_core.schemas.core.pagination import PaginationDefaults, PaginationRequest, PaginationResponse


def paginated_request(
    request_partial: Callable[..., Dict],
    result_key: str,
    starting_token: int = PaginationDefaults.starting_token,
    limit: int = PaginationDefaults.limit,
) -> List[Any]:
    """
    Get results from a request that may be paginated.

    We make an API request (from a partial function) and get the results from the response. If the response is paginated,
    we make a follow-up request with the next starting token and append the results to the list.

    Parameters
    ----------
    request_partial : Callable[..., Dict]
        Partial function for making an API request.
    result_key : str
        Key in the response JSON to get the results from.
    starting_token : int, optional
        Starting token for the request, by default 0
    limit : int, optional
        Limit for the number of items to request, by default 25

    Returns
    -------
    List[Any]
        List of results from the API request.
    """
    logger.debug(f"Requesting {limit} items starting from {starting_token}...")
    response = request_partial(params=PaginationRequest(starting_token=starting_token, limit=limit).model_dump())
    results = response.get(result_key, list())
    # If the response is paginated, make a follow-up request with the next starting token.
    pagination_response = PaginationResponse.model_validate(response)
    if pagination_response.paginated and pagination_response.next_starting_token is not None:
        # Recursively get the results from the next page.
        results += paginated_request(
            request_partial, result_key, starting_token=pagination_response.next_starting_token, limit=limit
        )
    return results
