from spotlight.api.dataset.abstract.model import AbstractDatasetRequest
from spotlight.api.dataset.model import SearchRequest


def _get_abstract_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"config/dataset/abstract/{id}"}


def _get_abstract_datasets_request_info() -> dict:
    return {"endpoint": f"config/dataset/abstract"}


def _search_abstract_datasets_request_info(request: SearchRequest) -> dict:
    return {
        "endpoint": f"config/dataset/abstract/search",
        "json": request.request_dict(),
    }


def _create_abstract_dataset_request_info(request: AbstractDatasetRequest) -> dict:
    return {"endpoint": f"config/dataset/abstract", "json": request.request_dict()}


def _update_abstract_dataset_request_info(
    id: str, request: AbstractDatasetRequest
) -> dict:
    return {
        "endpoint": f"config/dataset/abstract/{id}",
        "json": request.request_dict(),
    }


def _delete_abstract_dataset_request_info(id: str) -> dict:
    return {"endpoint": f"config/dataset/abstract/{id}"}
