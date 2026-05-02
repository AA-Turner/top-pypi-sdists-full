from typing import Dict, Any, List, Optional

from spotlight.api.data_rule.__util import (
    _get_data_rule_request_info,
    _get_data_rules_request_info,
    _create_data_rule_request_info,
    _update_data_rule_request_info,
    _delete_data_rule_request_info,
)
from spotlight.api.data_rule.model import DataRuleRequest
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request()
def get_data_rule(id: str) -> Dict[str, Any]:
    """
    Get data rule by ID.

    Args:
        id (str): Data rule ID

    Returns:
        Dict[str, Any]: Data rule response
    """
    request_info = _get_data_rule_request_info(id)
    return __get_request(**request_info)


@data_request()
def get_data_rules(override_find_all: Optional[bool] = False) -> List[Dict[str, Any]]:
    """
    Get all data rules.

    Args:
        override_find_all (Optional[bool]): If True, overrides the default limitation to fetch all results. This parameter is restricted to admin use only. Non-admin users will receive a 'Forbidden' exception if they attempt to use it. Defaults to False.

    Returns:
        List[Dict[str, Any]]: List of data rule responses
    """
    request_info = _get_data_rules_request_info(override_find_all)
    return __get_request(**request_info)


@data_request()
def create_data_rule(request: DataRuleRequest) -> Dict[str, Any]:
    """
    Create data rule.

    Args:
        request (DataRuleRequest): Data rule request

    Returns:
        Dict[str, Any]: Data rule response
    """
    request_info = _create_data_rule_request_info(request)
    return __put_request(**request_info)


@data_request()
def update_data_rule(id: str, request: DataRuleRequest) -> Dict[str, Any]:
    """
    Update data rule.

    Args:
        id (str): Data rule ID
        request (DataRuleRequest): Data rule request

    Returns:
        Dict[str, Any]: Data rule response
    """
    request_info = _update_data_rule_request_info(id, request)
    return __post_request(**request_info)


@data_request(processor=lambda response: None)
def delete_data_rule(id: str) -> None:
    """
    Delete data rule by ID.

    Args:
        id (str): Data rule ID

    Returns:
        None
    """
    request_info = _delete_data_rule_request_info(id)
    return __delete_request(**request_info)
