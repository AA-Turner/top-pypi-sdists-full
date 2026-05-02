from spotlight.api.dataset.model import SearchRequest


def _get_dataset_view_request_info(id: str) -> dict:
    return {"endpoint": f"config/dataset/view/{id}"}


def _get_dataset_views_request_info() -> dict:
    return {"endpoint": f"config/dataset/view"}


def _search_dataset_views_request_info(request: SearchRequest) -> dict:
    return {
        "endpoint": f"config/dataset/view/search",
        "json": request.request_dict(),
    }
