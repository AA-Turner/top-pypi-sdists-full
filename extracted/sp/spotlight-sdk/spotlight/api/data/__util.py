import json
from typing import Optional

from spotlight.api.data.model import (
    DistinctQueryRequest,
    MarketShareQuery,
    MarketShareSummaryQuery,
    QueryRequest,
    TimeseriesQueryRequest,
    TradeCountByTenorQuery,
)


def _query_timeseries_request_info(
    request: TimeseriesQueryRequest, one: Optional[bool] = False
) -> dict:
    return {
        "endpoint": f"data/v1.1/timeseries",
        "json": request.request_dict(),
        "params": {"one": True} if one else {},
    }


def _query_timeseries_csv_request_info(
    id: str, request: TimeseriesQueryRequest
) -> dict:
    return {"endpoint": f"data/v1.1/{id}.csv", "json": request.request_dict()}


def _query_distinct_fields_request_info(
    request: DistinctQueryRequest, use_cache: Optional[bool] = None
) -> dict:
    return {
        "endpoint": f"data/v1.1/distinct",
        "json": request.request_dict(),
        "params": {"cache": str(use_cache)},
    }


def _query_request_info(request: QueryRequest, one: Optional[bool] = False) -> dict:
    return {
        "endpoint": f"data/v1.1/query",
        "json": request.request_dict(),
        "params": {"one": "true"} if one else {},
    }


def _query_csv_request_info(id: str, request: QueryRequest) -> dict:
    json_str = json.dumps(request.request_dict(), separators=(",", ":"))

    return {
        "endpoint": f"data/v1.1/query/{id}.csv",
        "params": {"query": json_str},
    }


def _query_market_share_asset_request_info(request: MarketShareQuery) -> dict:
    return {
        "endpoint": "data/v1/market-share/asset",
        "json": request.request_dict(),
    }


def _query_market_share_totals_request_info(request: MarketShareQuery) -> dict:
    return {
        "endpoint": "data/v1/market-share/total",
        "json": request.request_dict(),
    }


def _query_market_share_summary_request_info(request: MarketShareSummaryQuery) -> dict:
    return {
        "endpoint": "data/v1/market-share/summary",
        "json": request.request_dict(),
    }


def _query_trade_count_by_tenor_request_info(request: TradeCountByTenorQuery) -> dict:
    return {
        "endpoint": "data/v1/trade-count/tenor",
        "json": request.request_dict(),
    }


def _query_trade_count_by_currency_request_info(
    request: TradeCountByTenorQuery,
) -> dict:
    return {
        "endpoint": "data/v1/trade-count/currency",
        "json": request.request_dict(),
    }
