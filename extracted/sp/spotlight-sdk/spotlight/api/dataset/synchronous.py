from typing import Dict, Any, List

from spotlight.api.dataset.__util import (
    _get_dataset_request_info,
    _get_datasets_request_info,
    _search_datasets_request_info,
    _create_dataset_request_info,
    _update_dataset_request_info,
    _delete_dataset_request_info,
)
from spotlight.api.dataset.model import DatasetRequest
from spotlight.api.dataset.model import SearchRequest
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request()
def get_dataset(id: str) -> Dict[str, Any]:
    """
    Get dataset by ID.

    Args:
        id (str): Dataset ID

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _get_dataset_request_info(id)
    return __get_request(**request_info)


@data_request()
def get_datasets() -> List[Dict[str, Any]]:
    """
    Get all dataset.

    Returns:
        List[Dict[str, Any]]: List of dataset response
    """
    request_info = _get_datasets_request_info()
    return __get_request(**request_info)


@data_request()
def search_datasets(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Search all dataset.

    Args:
        request (SearchRequest): Dataset search request

    Returns:
        List[Dict[str, Any]]: List of dataset response
    """
    request_info = _search_datasets_request_info(request)
    return __post_request(**request_info)


@data_request()
def create_dataset(request: DatasetRequest) -> Dict[str, Any]:
    """
    Create dataset.

    Args:
        request (DatasetRequest): Dataset request

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _create_dataset_request_info(request)
    return __put_request(**request_info)


@data_request()
def update_dataset(id: str, request: DatasetRequest) -> Dict[str, Any]:
    """
    Update dataset.

    Args:
        id (str): Dataset ID
        request (DatasetRequest): Dataset request

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _update_dataset_request_info(id, request)
    return __post_request(**request_info)


@data_request(processor=lambda response: None)
def delete_dataset(id: str) -> None:
    """
    Delete dataset by ID.

    Args:
        id (str): Dataset ID

    Returns:
        None
    """
    request_info = _delete_dataset_request_info(id)
    return __delete_request(**request_info)
