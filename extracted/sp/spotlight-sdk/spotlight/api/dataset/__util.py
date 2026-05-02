from spotlight.api.dataset.model import DatasetRequest
from spotlight.api.dataset.model import SearchRequest


def _get_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"config/dataset/{id}"}


def _get_datasets_request_info() -> dict:
    return {"endpoint": f"config/dataset"}


def _search_datasets_request_info(request: SearchRequest) -> dict:
    return {
        "endpoint": f"config/dataset/search",
        "json": request.request_dict(),
    }


def _create_dataset_request_info(request: DatasetRequest) -> dict:
    return {"endpoint": f"config/dataset", "json": request.request_dict()}


def _update_dataset_request_info(id: str, request: DatasetRequest) -> dict:
    return {"endpoint": f"config/dataset/{id}", "json": request.request_dict()}


def _delete_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"config/dataset/{id}"}
