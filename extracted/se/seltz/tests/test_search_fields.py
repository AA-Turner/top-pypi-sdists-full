import inspect

import pytest

from seltz import Document, Fields, Snippet
from seltz._types import OMIT
from seltz.services.search_service import (
    AsyncSearchService,
    SearchService,
    _build_search_request,
)


def _request(**overrides):
    args = dict(
        query="q",
        api_key="k",
        max_results=10,
        scope=OMIT,
        include_domains=OMIT,
        exclude_domains=OMIT,
        from_date=OMIT,
        to_date=OMIT,
        tier=OMIT,
        fields=OMIT,
    )
    args.update(overrides)
    return _build_search_request(**args)


def test_an_omitted_selection_is_absent_from_the_request() -> None:
    assert not _request().HasField("fields")


def test_naming_one_member_leaves_the_others_off() -> None:
    request = _request(fields=Fields(snippets=True))

    assert request.HasField("fields")
    assert request.fields.snippets
    assert not request.fields.content


def test_both_members_travel_when_both_are_named() -> None:
    request = _request(fields=Fields(content=True, snippets=True))

    assert request.fields.content
    assert request.fields.snippets


def test_an_empty_selection_is_sent_rather_than_dropped() -> None:
    request = _request(fields=Fields())

    assert request.HasField("fields")
    assert not request.fields.content
    assert not request.fields.snippets


@pytest.mark.parametrize(
    "selection",
    [Fields(), Fields(content=True), Fields(snippets=True)],
)
def test_the_selection_is_transmitted_unchanged(selection: Fields) -> None:
    assert _request(fields=selection).fields == selection


def test_a_document_carries_its_snippets_as_messages() -> None:
    document = Document(
        url="http://example.com/a",
        snippets=[Snippet(text="The second passage.")],
    )

    assert [snippet.text for snippet in document.snippets] == ["The second passage."]


def test_a_document_without_snippets_has_an_empty_repeated_field() -> None:
    document = Document(url="http://example.com/a")

    assert list(document.snippets) == []
    assert not document.content


def test_the_two_services_take_the_same_arguments() -> None:
    assert list(inspect.signature(AsyncSearchService.search).parameters) == list(
        inspect.signature(SearchService.search).parameters
    )


def test_fields_is_a_monitor_search_request_field() -> None:
    from seltz.services.monitor_service import _SEARCH_REQUEST_FIELDS

    assert "fields" in _SEARCH_REQUEST_FIELDS
