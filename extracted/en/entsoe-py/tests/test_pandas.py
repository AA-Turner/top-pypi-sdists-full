from itertools import product
import os

import numpy as np
from dotenv import load_dotenv
from entsoe import EntsoePandasClient
from entsoe.decorators import year_limited
import pandas as pd
import pytest

load_dotenv()

API_KEY = os.getenv("API_KEY")


@pytest.fixture
def client():
    yield EntsoePandasClient(api_key=API_KEY)


# this on purpose more than a month since entsoe has now a lot of "30 days" limits
STARTS = [pd.Timestamp("20260301", tz="Europe/Amsterdam")]
ENDS = [pd.Timestamp("20260402 23:59", tz="Europe/Amsterdam")]

# much shorter interval for 4 seconds-resolution data, otherwise requests will take forever
STARTS_4S = [pd.Timestamp("20260301", tz="Europe/Amsterdam")]
ENDS_4S = [pd.Timestamp("20260301 23:59", tz="Europe/Amsterdam")]

COUNTRY_CODES = ["NL", "BE", "DE_LU", "FR"]
COUNTRY_CODES_FROM = ["NL"]
COUNTRY_CODES_TO = ["DE_LU", 'NO_2', 'BE']
AREA_CODES_AFRR = ["DE_TRANSNET"]

BASIC_QUERIES_TIMESERIES = [
    "query_day_ahead_prices",
    "query_net_position",
    "query_load",
    "query_load_forecast",
    "query_wind_and_solar_forecast",
    "query_generation_forecast",
    "query_generation",
    "query_generation_per_plant",
    "query_installed_generation_capacity",
    "query_current_balancing_state"
]

BASIC_QUERIES = [
    "query_installed_generation_capacity_per_unit",
]

BASIC_QUERIES_TIMESERIES_ZIP = [
    "query_imbalance_prices",
    "query_imbalance_volumes",
]

CROSSBORDER_QUERIES = [
    "query_crossborder_flows",
    "query_scheduled_exchanges",
    "query_net_transfer_capacity_dayahead",
    "query_net_transfer_capacity_weekahead",
    "query_net_transfer_capacity_monthahead",
    # "query_net_transfer_capacity_yearahead",
]


def basic_checks(result, timeseries=True):
    assert isinstance(result, pd.Series) or isinstance(result, pd.DataFrame)
    assert not result.empty
    if timeseries:
        assert result.index.is_monotonic_increasing and result.index.is_unique

    if isinstance(result, pd.Series):
        assert not result.isna().all()
    elif isinstance(result, pd.DataFrame):
        assert not result.isna().all().all()


@pytest.mark.parametrize(
    "country_code, start, end, query",
    list(product(COUNTRY_CODES, STARTS, ENDS, BASIC_QUERIES_TIMESERIES)),
)
def test_basic_queries_timeseries(client, query, country_code, start, end):
    if query == 'query_current_balancing_state' and country_code == 'DE_LU':
        country_code = 'DE_AMPRION'
    if query == 'query_generation_per_plant' and country_code == 'DE_LU':
        # this is bugged, ticket raised at entsoe
        return
    result = getattr(client, query)(country_code, start=start, end=end)
    basic_checks(result)


@pytest.mark.parametrize(
    "country_code, start, end, query",
    list(product(COUNTRY_CODES, STARTS, ENDS, BASIC_QUERIES)),
)
def test_basic_queries(client, query, country_code, start, end):
    result = getattr(client, query)(country_code, start=start, end=end)
    basic_checks(result, timeseries=False)


@pytest.mark.parametrize(
    "country_code, start, end, query",
    list(product(['BE', 'FR'], STARTS, ENDS, BASIC_QUERIES_TIMESERIES_ZIP)),
)
def test_basic_queries_zip(client, query, country_code, start, end):
    result = getattr(client, query)(country_code, start=start, end=end)
    basic_checks(result)


@pytest.mark.parametrize(
    "country_code_from, country_code_to, start, end, query",
    list(product(COUNTRY_CODES_FROM, COUNTRY_CODES_TO, STARTS, ENDS, CROSSBORDER_QUERIES)),
)
def test_crossborder_queries(
        client, query, country_code_from, country_code_to, start, end
):
    result = getattr(client, query)(country_code_from, country_code_to, start=start, end=end)
    basic_checks(result)


@pytest.mark.parametrize("include_currency", [False, True])
def test_query_day_ahead_prices_currency(client, include_currency):
    start = pd.Timestamp("2026-03-01", tz="Europe/Brussels")
    end = start + pd.Timedelta(hours=1)
    result = client.query_day_ahead_prices(
        "BE", start=start, end=end, include_currency=include_currency
    )
    basic_checks(result)
    if include_currency:
        assert set(result.columns) == {'Price', 'Currency'}
        assert result["Currency"].eq("EUR").all()
        assert pd.api.types.is_numeric_dtype(result["Price"])
    else:
        assert isinstance(result, pd.Series)


def test_query_day_ahead_prices_year_boundary(client):
    start = pd.Timestamp("2024-01-01", tz="Europe/Brussels")
    end = pd.Timestamp("2025-01-31 23:00", tz="Europe/Brussels")
    result = client.query_day_ahead_prices("BE", start=start, end=end)

    # Include both endpoints: all 8,784 hours of 2024.
    expected = pd.date_range(start, end, freq="h", inclusive="both")
    assert set(result.index) == set(expected)


def test_query_aggregate_water_reservoirs_and_hydro_storage(client):
    result = client.query_aggregate_water_reservoirs_and_hydro_storage('NO_2',
                                                                       start=STARTS[0], end=ENDS[0])
    basic_checks(result)


@pytest.mark.parametrize(
    "country_code_from, country_code_to, start, end, id_type",
    [x for x in product(["BE", "NL"], ["BE", "NL"], STARTS, ENDS, ['IDCT', 'IDA1', 'IDA2', 'IDA3']) if x[0] != x[1]],
)
def test_query_intraday_offered_capacity(client, country_code_from, country_code_to, start, end, id_type):
    result = client.query_intraday_offered_capacity(
        country_code_from, country_code_to, start=start, end=end, implicit=True, id_type=id_type
    )
    basic_checks(result)


# @pytest.mark.parametrize(
#     "country_code, process_type, start, end",
#     product([x if x != 'DE_LU' else 'DE_AMPRION' for x in COUNTRY_CODES], ['A51', 'A52', 'A47'], STARTS, ENDS),
# )
# def test_query_contracted_reserve_prices_procured_capacity(client, country_code, process_type, start, end):
#     # [O] A51 = Automatic frequency restoration reserve; A52 = Frequency containment reserve; A47 = Manual frequency restoration reserve; A46 = Replacement reserve
#     result = client.query_contracted_reserve_prices_procured_capacity(
#         country_code, start=start, end=end, process_type=process_type, type_marketagreement_type='A01'
#     )
#     basic_checks(result)


def test_query_procured_balancing_capacity_keeps_all_offset_pages(client):
    # 126 bids on this day: 100 at offset 0 and 26 at offset 100, both pages numbering mRIDs from 1
    result = client.query_procured_balancing_capacity(
        'NL', start=pd.Timestamp("20260526", tz="Europe/Amsterdam"), end=pd.Timestamp("20260527", tz="Europe/Amsterdam"),
        process_type='A47', type_marketagreement_type='A01'
    )
    basic_checks(result)
    assert result.columns.droplevel('unit').nunique() == 126


@pytest.mark.parametrize(
    "country_code, start, end",
    list(product(COUNTRY_CODES, STARTS, ENDS)),
)
def test_query_unavailability_of_generation_units(client, country_code, start, end):
    result = client.query_unavailability_of_generation_units(country_code, start=start, end=end, docstatus=None, periodstartupdate=None, periodendupdate=None)
    basic_checks(result, timeseries=False)


@pytest.mark.parametrize(
    "country_code, start, end",
    list(product([x for x in COUNTRY_CODES if x != 'BE'], STARTS, ENDS)),
)
def test_query_unavailability_of_production_units(client, country_code, start, end):
    result = client.query_unavailability_of_production_units(country_code, start=start, end=end, docstatus=None, periodstartupdate=None, periodendupdate=None)
    basic_checks(result, timeseries=False)


@pytest.mark.parametrize(
    "country_code_from, country_code_to, start, end",
    list(product(COUNTRY_CODES_FROM, [x for x in COUNTRY_CODES_TO if x != 'DE_LU'], STARTS, ENDS)),
)
def test_query_unavailability_transmission(
        client, country_code_from, country_code_to, start, end
):
    result = client.query_unavailability_transmission(
        country_code_from, country_code_to, start=start, end=end, docstatus=None, periodstartupdate=None, periodendupdate=None
    )
    basic_checks(result, timeseries=False)


@pytest.mark.parametrize(
    "country_code, start, end",
    list(product(COUNTRY_CODES, STARTS, ENDS)),
)
def test_query_withdrawn_unavailability_of_generation_units(
        client, country_code, start, end
):
    result = client.query_withdrawn_unavailability_of_generation_units(
        country_code, start, end,
    )
    basic_checks(result, timeseries=False)
