from typing import Any, Dict, List, Optional
from requests import Response

from spotlight.api.data.__util import (
    _query_csv_request_info,
    _query_distinct_fields_request_info,
    _query_market_share_asset_request_info,
    _query_market_share_summary_request_info,
    _query_market_share_totals_request_info,
    _query_request_info,
    _query_timeseries_csv_request_info,
    _query_timeseries_request_info,
    _query_trade_count_by_currency_request_info,
    _query_trade_count_by_tenor_request_info,
)
from spotlight.api.data.model import (
    DistinctQueryRequest,
    MarketShareQuery,
    MarketShareSummaryQuery,
    QueryRequest,
    TimeseriesQueryRequest,
    TradeCountByTenorQuery,
)
from spotlight.core.common.decorators import async_data_request
from spotlight.core.common.requests import __async_get_request, __async_post_request


@async_data_request
async def async_query_timeseries(
    request: TimeseriesQueryRequest, one: Optional[bool] = False
) -> List[Dict[str, Any]]:
    """
    Asynchronously get timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request
        one (Optional[bool]): Flag to determine whether to return only one record

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_timeseries_request_info(request, one)
    return await __async_post_request(**request_info)


async def async_query_timeseries_csv(
    id: str, request: TimeseriesQueryRequest
) -> Response:
    """
    Asynchronously query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        Response: HTTP response object
    """
    request_info = _query_timeseries_csv_request_info(id, request)
    return await __async_get_request(**request_info)


@async_data_request
async def async_query_distinct_fields(
    request: DistinctQueryRequest, use_cache: Optional[bool] = None
) -> List[str]:
    """
    Asynchronously query dataset for distinct values of a specified field.

    Args:
        request (DistinctQueryRequest): Distinct query request
        use_cache (Optional[bool]): Flag to determine whether data cache should be used in fetching unique values

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_distinct_fields_request_info(request, use_cache)
    return await __async_post_request(**request_info)


@async_data_request
def async_query(
    request: QueryRequest, one: Optional[bool] = False
) -> List[Dict[str, Any]]:
    """
    Asynchronously query dataset by query request.

    Args:
        request (QueryRequest): Query request
        one (Union[bool, str]): Flag to determine whether to return only one record

    Returns:
        List[Dict[str, Any]]: List of records
    """
    request_info = _query_request_info(request, one)
    return __async_post_request(**request_info)


async def async_query_csv(id: str, request: QueryRequest) -> Response:
    """
    Asynchronously query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        request (QueryRequest): Query request

    Returns:
        Response: HTTP response object
    """
    request_info = _query_csv_request_info(id, request)
    return await __async_get_request(**request_info)


@async_data_request
async def async_query_market_share_asset(
    request: MarketShareQuery,
) -> List[Dict[str, Any]]:
    """
    Asynchronously query market share grouped by asset category.

    Args:
        request (MarketShareQuery): Market share query request

    Returns:
        List[Dict[str, Any]]: List of market share asset rows
    """
    request_info = _query_market_share_asset_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_query_market_share_totals(
    request: MarketShareQuery,
) -> List[Dict[str, Any]]:
    """
    Asynchronously query market share totals.

    Args:
        request (MarketShareQuery): Market share query request

    Returns:
        List[Dict[str, Any]]: List of market share total rows
    """
    request_info = _query_market_share_totals_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_query_market_share_summary(
    request: MarketShareSummaryQuery,
) -> Optional[Dict[str, Any]]:
    """
    Asynchronously query market share summary.

    Args:
        request (MarketShareSummaryQuery): Market share summary query request

    Returns:
        Optional[Dict[str, Any]]: Summary object or null
    """
    request_info = _query_market_share_summary_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_query_trade_count_by_tenor(
    request: TradeCountByTenorQuery,
) -> List[Dict[str, Any]]:
    """
    Asynchronously query trade counts by tenor bucket.

    Args:
        request (TradeCountByTenorQuery): Trade count query request

    Returns:
        List[Dict[str, Any]]: List of tenor count rows
    """
    request_info = _query_trade_count_by_tenor_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request
async def async_query_trade_count_by_currency(
    request: TradeCountByTenorQuery,
) -> List[Dict[str, Any]]:
    """
    Asynchronously query trade counts by currency.

    Args:
        request (TradeCountByTenorQuery): Trade count query request

    Returns:
        List[Dict[str, Any]]: List of currency count rows
    """
    request_info = _query_trade_count_by_currency_request_info(request)
    return await __async_post_request(**request_info)
