from typing import Dict, Any, List

from spotlight.api.dataset.abstract.__util import (
    _get_abstract_dataset_request_info,
    _get_abstract_datasets_request_info,
    _search_abstract_datasets_request_info,
    _create_abstract_dataset_request_info,
    _update_abstract_dataset_request_info,
    _delete_abstract_dataset_request_info,
)
from spotlight.api.dataset.abstract.model import AbstractDatasetRequest
from spotlight.api.dataset.model import SearchRequest
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request()
def get_abstract_dataset(id: str) -> Dict[str, Any]:
    """
    Get abstract dataset by ID.

    Args:
        id (str): Abstract dataset ID

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _get_abstract_dataset_request_info(id)
    return __get_request(**request_info)


@data_request()
def get_abstract_datasets() -> List[Dict[str, Any]]:
    """
    Get all abstract datasets.

    Returns:
        List[Dict[str, Any]]: List of abstract dataset response
    """
    request_info = _get_abstract_datasets_request_info()
    return __get_request(**request_info)


@data_request()
def search_abstract_datasets(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Search all abstract datasets.

    Args:
        request (SearchRequest): Abstract dataset search request

    Returns:
        List[Dict[str, Any]]: List of abstract dataset response
    """
    request_info = _search_abstract_datasets_request_info(request)
    return __post_request(**request_info)


@data_request()
def create_abstract_dataset(request: AbstractDatasetRequest) -> Dict[str, Any]:
    """
    Create abstract dataset.

    Args:
        request (DatasetRequest): Abstract dataset request

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _create_abstract_dataset_request_info(request)
    return __put_request(**request_info)


@data_request()
def update_abstract_dataset(id: str, request: AbstractDatasetRequest) -> Dict[str, Any]:
    """
    Update abstract dataset.

    Args:
        id (str): Abstract dataset ID
        request (DatasetRequest): Abstract dataset request

    Returns:
        Dict[str, Any]: Abstract dataset response
    """
    request_info = _update_abstract_dataset_request_info(id, request)
    return __post_request(**request_info)


@data_request(processor=lambda response: None)
def delete_abstract_dataset(id: str) -> None:
    """
    Delete abstract dataset by ID.

    Args:
        id (str): Abstract dataset ID

    Returns:
        None
    """
    request_info = _delete_abstract_dataset_request_info(id)
    return __delete_request(**request_info)
