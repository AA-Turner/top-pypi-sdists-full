# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Data Worker allocation API client."""

import pytest
import requests
from requests import Response

from airbyte_ops_mcp.cloud_admin import data_worker_allocation as dwa

ROOT = "https://example.test/api/v1"
ORG = "11111111-1111-4111-8111-111111111111"


def _response(status_code: int, body: bytes) -> Response:
    response = Response()
    response.status_code = status_code
    response._content = body
    return response


@pytest.fixture(autouse=True)
def _token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dwa, "_get_access_token", lambda *_a, **_k: "token")


def test_list_dataplane_groups_returns_named_regions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = b'{"dataplaneGroups":[{"dataplane_group_id":"abc","name":"US"}]}'
    monkeypatch.setattr(dwa.requests, "post", lambda *a, **k: _response(200, body))

    groups = dwa.list_dataplane_groups(ORG, config_api_root=ROOT, bearer_token="t")

    assert groups.dataplane_groups[0].name == "US"


@pytest.mark.parametrize(
    "failure",
    [
        pytest.param(requests.ConnectionError("no route"), id="transport"),
        pytest.param(requests.Timeout("too slow"), id="timeout"),
    ],
)
def test_list_dataplane_groups_wraps_transport_failures(
    monkeypatch: pytest.MonkeyPatch, failure: Exception
) -> None:
    """Names are fetched after a change commits, so nothing else may escape."""

    def boom(*_a, **_k):
        raise failure

    monkeypatch.setattr(dwa.requests, "post", boom)

    with pytest.raises(dwa.DataWorkerAllocationAPIError):
        dwa.list_dataplane_groups(ORG, config_api_root=ROOT, bearer_token="t")


@pytest.mark.parametrize(
    "body",
    [
        pytest.param(b"not json at all", id="malformed_json"),
        pytest.param(b'{"dataplaneGroups":[{"name":123}]}', id="schema_mismatch"),
    ],
)
def test_list_dataplane_groups_wraps_bad_responses(
    monkeypatch: pytest.MonkeyPatch, body: bytes
) -> None:
    """A 200 with an unreadable body is still that same error."""
    monkeypatch.setattr(dwa.requests, "post", lambda *a, **k: _response(200, body))

    with pytest.raises(dwa.DataWorkerAllocationAPIError):
        dwa.list_dataplane_groups(ORG, config_api_root=ROOT, bearer_token="t")


def test_list_dataplane_groups_reports_non_200(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        dwa.requests, "post", lambda *a, **k: _response(403, b"forbidden")
    )

    with pytest.raises(dwa.DataWorkerAllocationAPIError, match="403"):
        dwa.list_dataplane_groups(ORG, config_api_root=ROOT, bearer_token="t")


@pytest.mark.parametrize(
    "body",
    [
        pytest.param(b"<html>gateway</html>", id="malformed_json"),
        pytest.param(b'{"organization_id":"x"}', id="missing_fields"),
    ],
)
def test_mutation_with_unreadable_200_is_not_a_failed_call(
    monkeypatch: pytest.MonkeyPatch, body: bytes
) -> None:
    """A 200 means the change committed, so this is not DataWorkerAllocationAPIError alone."""
    monkeypatch.setattr(dwa.requests, "post", lambda *a, **k: _response(200, body))

    with pytest.raises(dwa.DataWorkerAllocationResponseError):
        dwa.add_data_worker_capacity(ORG, 1.0, config_api_root=ROOT, bearer_token="t")


def test_mutation_transport_failure_is_a_plain_api_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A transport failure leaves the outcome unknown, so it stays a failure."""

    def boom(*_a, **_k):
        raise requests.ConnectionError("reset")

    monkeypatch.setattr(dwa.requests, "post", boom)

    with pytest.raises(dwa.DataWorkerAllocationAPIError) as caught:
        dwa.add_data_worker_capacity(ORG, 1.0, config_api_root=ROOT, bearer_token="t")
    assert not isinstance(caught.value, dwa.DataWorkerAllocationResponseError)


def test_remove_capacity_sends_region_and_amount(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sent: dict[str, object] = {}
    body = (
        b'{"organization_id":"' + ORG.encode() + b'",'
        b'"total_allocated_capacity":2.0,"allocations":[]}'
    )

    def capture(url, json, **_k):
        sent["url"] = url
        sent["json"] = json
        return _response(200, body)

    monkeypatch.setattr(dwa.requests, "post", capture)

    dwa.remove_data_worker_capacity(
        ORG, "region-1", 1.5, config_api_root=ROOT, bearer_token="t"
    )

    assert sent["url"] == f"{ROOT}/data_worker_allocation/remove_capacity"
    assert sent["json"] == {
        "organization_id": ORG,
        "dataplane_group_id": "region-1",
        "amount": 1.5,
    }
