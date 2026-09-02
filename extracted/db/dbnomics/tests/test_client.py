from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from werkzeug import Response

from dbnomics import fetch_series

if TYPE_CHECKING:
    from pytest_httpserver import HTTPServer


def test_fetch_series_with_filter_on_one_series_with_filter_parameter_error(caplog) -> None:
    filters = [
        {
            "code": "interpolate",
            "parameters": {"foo": "bar"},
        }
    ]
    with caplog.at_level(logging.INFO):
        df = fetch_series(
            "AMECO",
            "ZUTN",
            "DEU.1.0.0.0.ZUTN",
            filters=filters,
        )
    assert all(df.filtered == False)  # : == is a Pandas operator  # noqa: E712
    dbnomics_log_records = [record for record in caplog.records if record.name == "dbnomics"]
    assert len(dbnomics_log_records) == 1
    assert dbnomics_log_records[0].levelname == "ERROR"
    assert "Error with filter parameters" in dbnomics_log_records[0].message


def test_fetch_series_with_filter_on_one_series_with_wrong_frequency(caplog) -> None:
    filters = [
        {
            "code": "aggregate",
            "parameters": {"frequency": "annual"},
        }
    ]
    with caplog.at_level(logging.INFO):
        df = fetch_series(
            "AMECO",
            "ZUTN",
            "DEU.1.0.0.0.ZUTN",
            filters=filters,
        )
    assert all(df.filtered == False)  # : == is a Pandas operator  # noqa: E712
    dbnomics_log_records = [record for record in caplog.records if record.name == "dbnomics"]
    assert len(dbnomics_log_records) == 1
    assert dbnomics_log_records[0].levelname == "ERROR"
    assert "Annual is already the lowest frequency" in dbnomics_log_records[0].message


def test_fetch_series_with_filter_on_one_series_with_filter_error(caplog) -> None:
    filters = [
        {
            "code": "foo",
            "parameters": {},
        }
    ]
    with caplog.at_level(logging.INFO):
        df = fetch_series(
            "AMECO",
            "ZUTN",
            "DEU.1.0.0.0.ZUTN",
            filters=filters,
        )
    assert all(df.filtered == False)  # : == is a Pandas operator  # noqa: E712
    dbnomics_log_records = [record for record in caplog.records if record.name == "dbnomics"]
    assert len(dbnomics_log_records) == 1
    assert dbnomics_log_records[0].levelname == "ERROR"
    assert "Filter not found" in dbnomics_log_records[0].message


def test_fetch_series_should_follow_redirects(httpserver: HTTPServer) -> None:
    httpserver.expect_request(
        "/series",
        query_string={
            "observations": "1",
            "offset": "0",
            "series_ids": "IMF/WEO:latest/NZL.LP.persons",
        },
    ).respond_with_response(
        Response(
            status=302,
            headers={
                "Location": "/series?"
                + urlencode({
                    "observations": "1",
                    "offset": "0",
                    "series_ids": "IMF/WEO:2023-04/NZL.LP.persons",
                })
            },
        )
    )
    httpserver.expect_request(
        "/series",
        query_string={
            "observations": "1",
            "offset": "0",
            "series_ids": "IMF/WEO:2023-04/NZL.LP.persons",
        },
    ).respond_with_json({
        "datasets": {
            "IMF/WEO:2023-04": {
                "code": "WEO:2023-04",
                "dimensions_codes_order": [],
                "name": "WEO by countries (2023-04 release)",
                "nb_series": 8624,
                "provider_code": "IMF",
                "provider_name": "International Monetary Fund",
            }
        },
        "providers": {
            "IMF": {
                "code": "IMF",
                "name": "International Monetary Fund",
                "region": "World",
                "slug": "imf",
                "terms_of_use": "http://datahelp.imf.org/tos",
                "website": "https://www.imf.org/",
            }
        },
        "series": {
            "docs": [
                {
                    "@frequency": "annual",
                    "dataset_code": "WEO:2023-04",
                    "dataset_name": "WEO by countries (2023-04 release)",
                    "dimensions": {"unit": "persons", "weo-country": "NZL", "weo-subject": "LP"},
                    "indexed_at": "2023-04-22T03:15:05.736Z",
                    "period": ["1980"],
                    "period_start_day": ["1980-01-01"],
                    "provider_code": "IMF",
                    "series_code": "NZL.LP.persons",
                    "series_name": "New Zealand \u2013 Population \u2013 Persons",
                    "value": [3.108],
                }
            ],
            "limit": 1000,
            "num_found": 1,
            "offset": 0,
        },
    })
    df = fetch_series("IMF/WEO:latest/NZL.LP.persons", api_base_url=httpserver.url_for("/"))
    assert df.value[0] == 3.108
