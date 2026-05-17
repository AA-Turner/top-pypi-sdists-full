from spotlight.api.dataset.model import DatasetRequest
from spotlight.api.dataset.model import DatasetUpdateRequest


def _get_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"data/dataset/{id}"}


def _get_datasets_request_info() -> dict:
    return {"endpoint": f"data/dataset"}


def _get_default_dataset_request_info() -> dict:
    return {"endpoint": "data/dataset/default"}


def _create_dataset_request_info(request: DatasetRequest) -> dict:
    return {"endpoint": f"data/dataset", "json": request.request_dict()}


def _update_dataset_request_info(id: str, request: DatasetUpdateRequest) -> dict:
    return {"endpoint": f"data/dataset/{id}", "json": request.request_dict()}


def _delete_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"data/dataset/{id}"}
