from pandas import DataFrame

from spotlight.api.data.barchart.__util import _get_history_info, _transform_results
from spotlight.api.data.barchart.model import BarchartQuery
from spotlight.core.common.decorators import async_data_request
from spotlight.core.common.requests import __async_get_request


@async_data_request(transformers=[_transform_results])
async def async_get_history(query: BarchartQuery):
    """
    Asynchronously get barchart history.

    Args:
        query (BarchartQuery): Barchart query

    Returns:
        DataFrame: DataFrame
    """
    request_info = _get_history_info(query)
    return await __async_get_request(**request_info)
