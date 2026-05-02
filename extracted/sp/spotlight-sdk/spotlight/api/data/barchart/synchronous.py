from pandas import DataFrame

from spotlight.api.data.barchart.__util import _get_history_info, _transform_results
from spotlight.api.data.barchart.model import BarchartQuery
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import __get_request


@data_request(transformers=[_transform_results])
def get_series(query: BarchartQuery) -> DataFrame:
    """
    Get barchart history.

    Args:
        query (BarchartQuery): Barchart query

    Returns:
        DataFrame: DataFrame
    """
    request_info = _get_history_info(query)
    return __get_request(**request_info)
