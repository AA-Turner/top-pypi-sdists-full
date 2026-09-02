"""`omit` decides whether a field is sent. `None` is an ordinary value.

The sentinel means "the caller left this argument out". `None` means "no
value": on a filter that reads the same as leaving it out, and on a field the
server lets you clear, it clears.

Collapsing the two is the trap this suite exists to prevent. It costs nothing
while every field is a filter, and turns into a typed surface that cannot
express a documented operation the moment one field is clearable.
"""

import pytest

from seltz import Webhook
from seltz._types import OMIT
from seltz.services.answer_service import _build_answer_request
from seltz.services.monitor_service import _create_request, _update_request
from seltz.services.search_service import _build_search_request

SEARCH = dict(query="q", max_results=10, api_key="k")


def _search(**overrides):
    args = dict(
        scope=OMIT,
        include_domains=OMIT,
        exclude_domains=OMIT,
        from_date=OMIT,
        to_date=OMIT,
    )
    args.update(overrides)
    return _build_search_request(**SEARCH, **args)


@pytest.mark.parametrize(
    "field", ["scope", "include_domains", "exclude_domains", "from_date", "to_date"]
)
def test_search_treats_none_and_omit_alike(field: str) -> None:
    """Nothing on search is clearable, so the two must agree byte for byte."""
    assert _search(**{field: None}).SerializeToString() == _search().SerializeToString()


def test_answer_treats_none_and_omit_alike() -> None:
    omitted = _build_answer_request(
        api_key="k",
        query="q",
        include_content=True,
        scope=OMIT,
        model=OMIT,
        response_format=OMIT,
        system_prompt=OMIT,
    )
    nulled = _build_answer_request(
        api_key="k",
        query="q",
        include_content=True,
        scope=None,
        model=None,
        response_format=None,
        system_prompt=None,
    )
    assert omitted.SerializeToString() == nulled.SerializeToString()


def test_monitor_filters_accept_none() -> None:
    """The documented paging idiom seeds the cursor with None."""
    from seltz.services.monitor_service import _list_records_request

    assert not _list_records_request("k", "m", None, None, OMIT, OMIT).HasField("since")


def test_update_omits_keeps_the_webhook() -> None:
    request = _update_request("k", "m", OMIT, OMIT, OMIT, OMIT, OMIT)
    assert not request.HasField("webhook")


def test_update_none_clears_the_webhook() -> None:
    """Present but empty is the clear. Passing None straight to protobuf would
    produce the same bytes as omitting it, which keeps the webhook instead."""
    request = _update_request("k", "m", OMIT, OMIT, OMIT, OMIT, None)
    assert request.HasField("webhook")
    assert request.webhook.url == ""
    assert list(request.webhook.events) == []


def test_update_sets_the_webhook() -> None:
    request = _update_request(
        "k",
        "m",
        OMIT,
        OMIT,
        OMIT,
        OMIT,
        Webhook(url="https://e.com/h", events=["run.failed"]),
    )
    assert request.webhook.url == "https://e.com/h"
    assert list(request.webhook.events) == ["run.failed"]


def test_update_takes_a_webhook_mapping() -> None:
    request = _update_request(
        "k",
        "m",
        OMIT,
        OMIT,
        OMIT,
        OMIT,
        {"url": "https://e.com/h", "events": ["run.failed"]},
    )
    assert request.webhook.url == "https://e.com/h"
    assert list(request.webhook.events) == ["run.failed"]


def test_a_webhook_without_events_is_sent_as_given() -> None:
    """The server rejects a subscription to nothing; the SDK states no such
    rule and substitutes no event list of its own."""
    request = _create_request("k", "n", "1h", [], {"url": "https://e.com/h"}, OMIT)
    assert request.webhook.url == "https://e.com/h"
    assert list(request.webhook.events) == []


def test_create_none_means_no_webhook() -> None:
    request = _create_request("k", "n", "1h", [], None, OMIT)
    assert not request.HasField("webhook")
