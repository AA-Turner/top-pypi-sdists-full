from typing import Dict, Any, List

from spotlight.api.dataset.model import SearchRequest
from spotlight.api.dataset.view.__util import (
    _get_dataset_view_request_info,
    _get_dataset_views_request_info,
    _search_dataset_views_request_info,
)
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import (
    __get_request,
    __post_request,
)


@data_request()
def get_dataset_view(id: str) -> Dict[str, Any]:
    """
    Get dataset view by ID.

    Args:
        id (str): Dataset ID

    Returns:
        Dict[str, Any]: Dataset view response
    """
    request_info = _get_dataset_view_request_info(id)
    return __get_request(**request_info)


@data_request()
def get_dataset_views() -> List[Dict[str, Any]]:
    """
    Get all dataset views.

    Returns:
        List[Dict[str, Any]]: List of dataset view response
    """
    request_info = _get_dataset_views_request_info()
    return __get_request(**request_info)


@data_request()
def search_dataset_views(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Search all dataset views.

    Args:
        request (SearchRequest): Dataset view search request

    Returns:
        List[Dict[str, Any]]: List of dataset view response
    """
    request_info = _search_dataset_views_request_info(request)
    return __post_request(**request_info)
