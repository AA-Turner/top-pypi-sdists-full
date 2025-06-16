# Copyright (C) Cardiff University (2018-2021)
# SPDX-License-Identifier: MIT

"""Tests for :mod:`gwosc.api.v2`"""

from unittest.mock import patch

import pytest

from ..api import v2 as apiv2

__author__ = "Martin Beroiz <martin.beroiz@ligo.org>"


def test_cache():
    apiv2.JSON_CACHE["something"] = "cached_value"
    assert apiv2.fetch_json("something") == "cached_value"


@patch("gwosc.api.v2.fetch_json")
def test_produce_fetched_objects_pagination(mock_fetch):
    mock_fetch.side_effect = [
        {
            "next": "http://dummy_url.com?page=2",
            "results": [1, 2, 3],
            "num_pages": 10,
        },
        {
            "next": None,
            "results": [4, 5, 6],
            "num_pages": 10,
        },
    ]
    result = list(apiv2.produce_fetched_objects("mock_url"))
    assert result == [1, 2, 3, 4, 5, 6]


@patch("gwosc.api.v2.fetch_json")
def test_produce_fetched_objects_toomanypages(mock_fetch):
    mock_fetch.side_effect = [
        {
            "next": "http://dummy_url.com?page=2",
            "results": [1, 2, 3],
            "num_pages": 1000,
        },
        {
            "next": None,
            "results": [4, 5, 6],
            "num_pages": 1000,
        },
    ]
    with pytest.warns(UserWarning, match="1000 pages"):
        result = list(apiv2.produce_fetched_objects("mock_url"))
        assert result == [1, 2, 3, 4, 5, 6]


@pytest.mark.remote
def test_fetch_run_strain_files():
    s5_files = list(
        apiv2.fetch_run_strain_files(
            detector="H1", run="S5", start=826175488, end=826200064
        )
    )
    assert len(s5_files) == 4
    o1_files = list(
        apiv2.fetch_run_strain_files(
            detector="L1", run="O1", start=1127407616, end=1127420000
        )
    )
    assert len(o1_files) == 4


@pytest.mark.remote
def test_fetch_event_strain_data():
    gw_files = list(
        apiv2.fetch_event_strain_data(
            "GW150914", version=3, sample_rate=4096, format="txt"
        )
    )
    assert len(gw_files) == 4
    for afile in gw_files:
        assert afile["sample_rate_kHz"] == 4
        assert afile["file_format"].lower() == "txt"


@pytest.mark.remote
def test_fetch_segments():
    segs = list(apiv2.fetch_segments("H1_DATA", start=932540000, end=932560000))
    assert len(segs) == 2


@pytest.mark.remote
def test_fetch_runs():
    assert "S6" in set(run["name"] for run in apiv2.fetch_runs())


@pytest.mark.remote
def test_fetch_catalogs():
    catalogs = set(cat["name"] for cat in apiv2.fetch_catalogs())
    assert "GWTC" in catalogs
    assert "GWTC-1-confident" in catalogs


@pytest.mark.remote
def test_fetch_event_versions():
    event = list(apiv2.fetch_event_versions(name="GW150914"))[0]
    assert event["name"] == "GW150914"

    events = list(apiv2.fetch_event_versions(catalogs="GWTC-1-confident"))
    assert len(events) == 11

    event = list(apiv2.fetch_event_versions(segment=(1126259450, 1126259470)))[0]
    assert event["name"] == "GW150914"

    events = list(
        apiv2.fetch_event_versions(
            select={
                "max-mass-1-source": 5,
                "min-p-astro": 0.5,
            }
        )
    )[0]
    assert len(events) > 0


def test_fetch_run():
    run = apiv2.fetch_run("S5")
    assert run["name"] == "S5"


def test_fetch_event_version():
    event = apiv2.fetch_event_version("GW150914", version=3)
    assert "150914" in event["name"]
    assert event["version"] == 3

    event = apiv2.fetch_event_version("GW150914", catalog="GWTC")
    assert "150914" in event["name"]
    assert "GWTC" in event["catalog"]
    assert event["catalog"] == "GWTC-1-confident"


def test_fetch_allowed_params():
    params = apiv2.fetch_allowed_params()
    assert len(params) > 0
