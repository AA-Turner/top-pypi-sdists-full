"""
Data API query functions for timeseries data.
"""

from spotlight.api.data.asynchronous import (
    async_query,
    async_query_distinct_fields,
    async_query_market_share_asset,
    async_query_market_share_summary,
    async_query_market_share_totals,
    async_query_timeseries,
    async_query_timeseries_csv,
    async_query_trade_count_by_currency,
    async_query_trade_count_by_tenor,
)
from spotlight.api.data.synchronous import (
    query,
    query_distinct_fields,
    query_market_share_asset,
    query_market_share_summary,
    query_market_share_totals,
    query_timeseries,
    query_timeseries_csv,
    query_trade_count_by_currency,
    query_trade_count_by_tenor,
)
