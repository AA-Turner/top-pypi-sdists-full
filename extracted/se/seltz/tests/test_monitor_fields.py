"""Every request field the proto carries is reachable, and nothing else is set.

A field the wrapper cannot set is invisible: the request still serializes, the
server applies its own default, and the caller sees a plausible answer to a
question they did not ask. `run_records` shipped without `include_content` and
silently returned records with no content for as long as it existed.

The mirror of that is a client-side default. `limit` and `include_content` are
`optional` in the proto precisely so the server can fill them in, so an omitted
argument must leave the field unset rather than freeze a number the server
never specified.
"""

import pytest

from seltz import MonitorStatus, SearchRequest, SortOrder
from seltz._types import OMIT
from seltz.services.monitor_service import (
    _create_request,
    _list_request,
    _list_records_request,
    _list_run_records_request,
    _list_runs_request,
    _search_requests,
    _update_request,
)


def test_create_carries_the_status_verbatim() -> None:
    request = _create_request(
        "k", "n", "1h", [], OMIT, MonitorStatus.MONITOR_STATUS_DISABLED
    )
    assert request.status == MonitorStatus.MONITOR_STATUS_DISABLED


def test_create_omits_the_status() -> None:
    """Unset is create-as-active. Sending ACTIVE unconditionally would
    reactivate a monitor the server had disabled."""
    assert not _create_request("k", "n", "1h", [], OMIT, OMIT).HasField("status")


def test_update_carries_the_status_verbatim() -> None:
    request = _update_request(
        "k", "m", OMIT, MonitorStatus.MONITOR_STATUS_PAUSED, OMIT, OMIT, OMIT
    )
    assert request.status == MonitorStatus.MONITOR_STATUS_PAUSED


def test_list_filters_by_status() -> None:
    request = _list_request(
        "k", OMIT, MonitorStatus.MONITOR_STATUS_ACTIVE, OMIT, OMIT, OMIT
    )
    assert request.status == MonitorStatus.MONITOR_STATUS_ACTIVE


def test_records_takes_the_before_bound() -> None:
    assert _list_records_request("k", "m", OMIT, 7, OMIT, OMIT).before == 7


def test_run_records_takes_include_content() -> None:
    assert (
        _list_run_records_request("k", "m", 1, OMIT, OMIT, OMIT, False).include_content
        is False
    )


def test_runs_carries_the_sort_order() -> None:
    request = _list_runs_request("k", "m", OMIT, OMIT, OMIT, SortOrder.SORT_ORDER_ASC)
    assert request.sort == SortOrder.SORT_ORDER_ASC


@pytest.mark.parametrize(
    ("request_", "field"),
    [
        (_list_request("k", OMIT, OMIT, OMIT, OMIT, OMIT), "limit"),
        (_list_runs_request("k", "m", OMIT, OMIT, OMIT, OMIT), "limit"),
        (_list_records_request("k", "m", OMIT, OMIT, OMIT, OMIT), "limit"),
        (_list_records_request("k", "m", OMIT, OMIT, OMIT, OMIT), "include_content"),
        (_list_run_records_request("k", "m", 1, OMIT, OMIT, OMIT, OMIT), "limit"),
        (_list_run_records_request("k", "m", 1, OMIT, OMIT, OMIT, OMIT), "before"),
        (
            _list_run_records_request("k", "m", 1, OMIT, OMIT, OMIT, OMIT),
            "include_content",
        ),
    ],
)
def test_an_omitted_paging_field_is_left_to_the_server(request_, field: str) -> None:
    assert not request_.HasField(field)


def test_search_requests_accept_three_forms() -> None:
    built = _search_requests(
        [
            "bare",
            {"query": "mapped", "max_results": 3, "include_domains": ["example.com"]},
            SearchRequest(query="prebuilt"),
        ]
    )
    assert [request.query for request in built] == ["bare", "mapped", "prebuilt"]
    assert built[1].max_results == 3
    assert list(built[1].include_domains) == ["example.com"]


def test_a_search_request_mapping_refuses_an_api_key() -> None:
    """The server rejects a monitor's search request that carries one."""
    with pytest.raises(TypeError):
        _search_requests([{"query": "q", "api_key": "k"}])


def test_run_records_carries_before() -> None:
    assert _list_run_records_request("k", "m", 1, OMIT, 42, OMIT, OMIT).before == 42
