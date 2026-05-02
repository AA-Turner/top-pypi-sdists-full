from spotlight.api.data.barchart.model import BarchartQuery


def _transform_results(data: dict) -> dict:
    return data["results"]


def _get_history_info(query: BarchartQuery) -> dict:
    return {
        "endpoint": "/getHistory.json",
        "url_key": "barchart",
        "params": query.request_dict(),
    }
