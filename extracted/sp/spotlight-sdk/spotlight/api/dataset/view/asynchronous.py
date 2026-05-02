from typing import Dict, Any, List

from spotlight.api.dataset.model import SearchRequest
from spotlight.api.dataset.view.__util import (
    _get_dataset_view_request_info,
    _get_dataset_views_request_info,
    _search_dataset_views_request_info,
)
from spotlight.core.common.decorators import async_data_request
from spotlight.core.common.requests import (
    __async_get_request,
    __async_post_request,
)


@async_data_request()
async def async_get_dataset_view(id: str) -> Dict[str, Any]:
    """
    Asynchronously get dataset view by ID.

    Args:
        id (str): Dataset ID

    Returns:
        Dict[str, Any]: Dataset view response
    """
    request_info = _get_dataset_view_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request()
async def async_get_dataset_views() -> List[Dict[str, Any]]:
    """
    Asynchronously get all dataset views.

    Returns:
        List[Dict[str, Any]]: List of dataset view response
    """
    request_info = _get_dataset_views_request_info()
    return await __async_get_request(**request_info)


@async_data_request()
async def async_search_dataset_views(
    request: SearchRequest,
) -> List[Dict[str, Any]]:
    """
    Asynchronously search all dataset views.

    Args:
        request (SearchRequest): Dataset view search request

    Returns:
        List[Dict[str, Any]]: List of dataset view response
    """
    request_info = _search_dataset_views_request_info(request)
    return await __async_post_request(**request_info)
