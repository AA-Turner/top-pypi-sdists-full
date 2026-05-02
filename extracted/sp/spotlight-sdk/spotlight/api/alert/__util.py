from typing import Optional

from spotlight.api.alert.model import AlertRequest


def _get_alert_request_info(id: str) -> dict:
    return {"endpoint": f"config/alert/{id}"}


def _get_alerts_request_info(override_find_all: Optional[bool] = False) -> dict:
    endpoint = "config/alert"
    params = {"override_find_all": override_find_all}

    filtered_params = {k: v for k, v in params.items() if v is not None}

    return {"endpoint": endpoint, "params": filtered_params}


def _get_alert_signal_request_info(start: int, end: int) -> dict:
    endpoint = "config/alert/signal"
    params = {"start": start, "end": end}

    return {"endpoint": endpoint, "params": params}


def _create_alert_request_info(request: AlertRequest) -> dict:
    return {"endpoint": f"config/alert", "json": request.request_dict()}


def _update_alert_request_info(id: str, request: AlertRequest) -> dict:
    return {"endpoint": f"config/alert/{id}", "json": request.request_dict()}


def _delete_alert_request_info(id: str) -> dict:
    return {"endpoint": f"config/alert/{id}"}
