###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import json
import os
import time
from typing import Optional

import pytest
import requests

from lb_telemetry import INFLUXDB_LEGAL_TYPES, Logger

TEST_TABLE = "testing_032"
TEST_DATA = {
    "test_field1": "test_value",
    "test_field2": False,
    "test_field3": 0,
    "test_field4": 3.5,
    "test_tag1": "some_tag",
}
TEST_TAGS = ["test_tag1"]
os.environ["LBTELEMETRY_ENABLED"] = "x"


class LogFetchError(Exception):
    pass


def test_build_payload_valid():
    logger = Logger()

    for include_host_info in [False, True]:
        payload: dict = logger.build_payload(
            table=TEST_TABLE,
            data=TEST_DATA,
            tags=TEST_TAGS,
            include_host_info=include_host_info,
        )

        # Ensure payload has mandatory fields
        mandatory_keys = ["producer", "type", "idb_tags"]
        assert all(key in payload for key in mandatory_keys)

        assert payload["producer"] == logger.producer
        assert payload["type"] == TEST_TABLE

        # Ensure that all tags we defined appear in the list of tags
        for tag in TEST_TAGS:
            assert tag in payload["idb_tags"]

        # Ensure that all tags declared appear in the payload
        for tag in payload["idb_tags"]:
            assert tag in payload

        # Ensure value types are compatible with InfluxDB
        tags_and_fields = {k: payload[k] for k in payload if k not in mandatory_keys}
        assert all([type(value) in INFLUXDB_LEGAL_TYPES for value in tags_and_fields])

        if include_host_info:
            payload_without_host_info: dict = logger.build_payload(
                table=TEST_TABLE,
                data=TEST_DATA,
                tags=TEST_TAGS,
                include_host_info=False,
            )

            assert len(payload) > len(payload_without_host_info)


def test_is_data_valid():
    invalid = [
        ({}, []),
        ({"some_field": ["arrays are", "not allowed"]}, []),
        ({"some_field": {"sets are", "not allowed"}}, []),
        ({"some_field": {"dicts are": "not allowed"}}, []),
        ({"some_field": 0}, ["illegal_unused_tag"]),
    ]
    assert not any([Logger.is_data_valid(data, tags) for data, tags in invalid])

    valid = [
        ({"some_field": 5}, []),
        ({"some_field": "some_value"}, []),
        ({"some_tag": "some_value"}, ["some_tag"]),
        ({"some_field": False, "some_tag": 3.5}, ["some_tag"]),
    ]
    assert all([Logger.is_data_valid(data, tags) for data, tags in valid])


@pytest.fixture
def token() -> str:
    token = os.environ.get("LB_TELEMETRY_TOKEN")
    if not token:
        pytest.skip("LB_TELEMETRY_TOKEN variable not set")

    return token


def fetch_test_log(logger: Logger, ts: int, token: str) -> Optional[dict]:
    base_url = "https://monit-grafana.cern.ch/api/datasources"
    path = f"proxy/{logger.datasource_id}/query?db={logger.database}"
    query = f"select * from {TEST_TABLE} where time = {ts}ms"

    try:
        response = requests.post(
            f"{base_url}/{path}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={"q": query.encode("utf-8")},
        )
    except requests.exceptions.RequestException as e:
        raise LogFetchError(
            f"An error occurred while verifying the test log: {e}"
        ) from e

    if response.status_code != 200:
        raise LogFetchError(
            f"Unexpected status code {response.status_code}: " f"{response.text}"
        )

    results: dict = json.loads(response.text)["results"][0]

    if "error" in results:
        raise LogFetchError(
            f"An error appeared in the results: {results}\n\n"
            f"Request path: {path}\n\n"
            f"Query: {query}"
        )
    elif "series" in results:
        return results["series"][0]

    return None


def test_log_to_monit(token):
    # Send valid log
    logger = Logger()
    ts = logger.log_to_monit(TEST_TABLE, TEST_DATA, TEST_TAGS, include_host_info=False)
    if ts is None:
        raise ValueError("Timestamp of log is None")

    # Check if the log can be fetched
    MAX_ATTEMPTS = 10
    for i in range(MAX_ATTEMPTS):
        fetch_result = fetch_test_log(logger, ts, token)

        is_final_attempt = i == MAX_ATTEMPTS - 1
        if is_final_attempt:
            raise AssertionError(
                "Could not find test measurement "
                "(there must've been an error posting it)"
            )

        if fetch_result is None:
            # Wait a bit
            # (The test log can take a few seconds to show up in the database)
            time.sleep(2)
            continue
        else:
            break

    assert fetch_result["name"] == TEST_TABLE
    assert all([field in fetch_result["columns"] for field in TEST_DATA.keys()])

    for i, field in enumerate(fetch_result["columns"]):
        if field == "time":
            continue

        assert TEST_DATA[field] == fetch_result["values"][0][i]


def test_log_to_monit_fail(token):
    # Ensure we cannot fetch a fake timestamp
    logger = Logger()
    fake_ts = 10000000
    assert fetch_test_log(logger, fake_ts, token) is None

    invalid_logger = Logger(send_url="invalid")
    ts = invalid_logger.log_to_monit(TEST_TABLE, TEST_DATA, TEST_TAGS)
    assert ts is None
