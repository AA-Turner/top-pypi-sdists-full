from typing import Optional

from spotlight.api.alert.model import AlertRequest


def _get_alert_request_info(id: str) -> dict:
    return {"endpoint": f"data/alert/{id}"}


def _get_alerts_request_info(dataset_id: Optional[str] = None) -> dict:
    endpoint = "data/alert"
    params = {"dataset_id": dataset_id}

    filtered_params = {k: v for k, v in params.items() if v is not None}

    return {"endpoint": endpoint, "params": filtered_params}


def _get_alert_signal_request_info(start: int, end: int) -> dict:
    endpoint = "data/alert/signal"
    params = {"start": start, "end": end}

    return {"endpoint": endpoint, "params": params}


def _create_alert_request_info(request: AlertRequest) -> dict:
    return {"endpoint": f"data/alert", "json": request.request_dict()}


def _update_alert_request_info(id: str, request: AlertRequest) -> dict:
    return {"endpoint": f"data/alert/{id}", "json": request.request_dict()}


def _delete_alert_request_info(id: str) -> dict:
    return {"endpoint": f"data/alert/{id}"}
