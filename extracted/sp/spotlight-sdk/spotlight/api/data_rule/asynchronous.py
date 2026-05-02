from typing import Dict, Any, List, Optional

from spotlight.api.data_rule.__util import (
    _get_data_rule_request_info,
    _get_data_rules_request_info,
    _create_data_rule_request_info,
    _update_data_rule_request_info,
    _delete_data_rule_request_info,
)
from spotlight.api.data_rule.model import DataRuleRequest
from spotlight.core.common.decorators import async_data_request
from spotlight.core.common.requests import (
    __async_get_request,
    __async_post_request,
    __async_put_request,
    __async_delete_request,
)


@async_data_request()
async def async_get_data_rule(id: str) -> Dict[str, Any]:
    """
    Asynchronously get data rule by ID.

    Args:
        id (str): Data rule ID

    Returns:
        Dict[str, Any]: Data rule response
    """
    request_info = _get_data_rule_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request()
async def async_get_data_rules(
    override_find_all: Optional[bool] = False,
) -> List[Dict[str, Any]]:
    """
    Asynchronously get all data rules.

    Args:
        override_find_all (Optional[bool]): If True, overrides the default limitation to fetch all results. This parameter is restricted to admin use only. Non-admin users will receive a 'Forbidden' exception if they attempt to use it. Defaults to False.

    Returns:
        List[Dict[str, Any]]: List of data rule responses
    """
    request_info = _get_data_rules_request_info(override_find_all)
    return await __async_get_request(**request_info)


@async_data_request()
async def async_create_data_rule(request: DataRuleRequest) -> Dict[str, Any]:
    """
    Asynchronously create data rule.

    Args:
        request (DataRuleRequest): Data rule request

    Returns:
        Dict[str, Any]: Data rule response
    """
    request_info = _create_data_rule_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request()
async def async_update_data_rule(id: str, request: DataRuleRequest) -> Dict[str, Any]:
    """
    Asynchronously update data rule.

    Args:
        id (str): Data rule ID
        request (DataRuleRequest): Data rule request

    Returns:
        Dict[str, Any]: Data rule response
    """
    request_info = _update_data_rule_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request(processor=lambda response: None)
async def async_delete_data_rule(id: str) -> None:
    """
    Asynchronously delete data rule by ID.

    Args:
        id (str): Data rule ID

    Returns:
        None
    """
    request_info = _delete_data_rule_request_info(id)
    return await __async_delete_request(**request_info)
