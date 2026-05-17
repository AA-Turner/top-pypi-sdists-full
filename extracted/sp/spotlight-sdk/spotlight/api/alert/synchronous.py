from typing import Dict, Any, List, Optional

from spotlight.api.alert.__util import (
    _get_alert_request_info,
    _get_alerts_request_info,
    _create_alert_request_info,
    _update_alert_request_info,
    _delete_alert_request_info,
    _get_alert_signal_request_info,
)
from spotlight.api.alert.model import AlertRequest
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request()
def get_alert(id: str) -> Dict[str, Any]:
    """
    Get alert by ID.

    Args:
        id (str): Alert ID

    Returns:
        Dict[str, Any]: Alert response
    """
    request_info = _get_alert_request_info(id)
    return __get_request(**request_info)


@data_request()
def get_alerts(dataset_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all alerts.

    Args:
        dataset_id (Optional[str]): If provided, filter alerts by dataset id.

    Returns:
        List[Dict[str, Any]]: List of alert responses
    """
    request_info = _get_alerts_request_info(dataset_id)
    return __get_request(**request_info)


@data_request()
def get_alert_signal(start: int, end: int) -> List[Dict[str, Any]]:
    """
    Get signals for each alert in time window.

    Args:
        start (int): Unix timestamp for the start of the time window
        end (int): Unix timestamp for the end of the time window

    Returns:
        Dict[str, Any]: AlertSignal response
    """
    request_info = _get_alert_signal_request_info(start, end)
    return __get_request(**request_info)


@data_request()
def create_alert(request: AlertRequest) -> Dict[str, Any]:
    """
    Create alert.

    Args:
        request (AlertRequest): Alert request

    Returns:
        Dict[str, Any]: Alert response
    """
    request_info = _create_alert_request_info(request)
    return __post_request(**request_info)


@data_request()
def update_alert(id: str, request: AlertRequest) -> Dict[str, Any]:
    """
    Update alert.

    Args:
        id (str): Alert ID
        request (AlertRequest): Alert request

    Returns:
        Dict[str, Any]: Alert response
    """
    request_info = _update_alert_request_info(id, request)
    return __put_request(**request_info)


@data_request(processor=lambda response: None)
def delete_alert(id: str) -> None:
    """
    Delete alert by ID.

    Args:
        id (str): Alert ID

    Returns:
        None
    """
    request_info = _delete_alert_request_info(id)
    return __delete_request(**request_info)
