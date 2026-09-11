import inspect

import pytest

from seltz import (
    ContentOptions,
    Document,
    Fields,
    FieldsMessage,
    Snippet,
    SnippetOptions,
)
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
    request = _request(fields={"snippets": True})

    assert request.HasField("fields")
    assert request.fields.snippets_enabled
    assert request.fields.WhichOneof("content") is None


def test_both_members_travel_when_both_are_named() -> None:
    request = _request(fields={"content": True, "snippets": True})

    assert request.fields.content_enabled
    assert request.fields.snippets_enabled


def test_an_empty_selection_is_sent_rather_than_dropped() -> None:
    request = _request(fields={})

    assert request.HasField("fields")
    assert request.fields.WhichOneof("content") is None
    assert request.fields.WhichOneof("snippets") is None


def test_a_bag_selects_the_member_and_carries_its_ceilings() -> None:
    request = _request(
        fields={"content": ContentOptions(max_characters_per_result=500)}
    )

    assert request.fields.WhichOneof("content") == "content_options"
    assert request.fields.content_options.max_characters_per_result == 500


def test_a_bag_is_taken_as_a_mapping_too() -> None:
    """A bag reaches the same arm whether it is a mapping or the generated message."""
    from_mapping = _request(fields={"content": {"max_characters_per_result": 500}})
    from_message = _request(
        fields={"content": ContentOptions(max_characters_per_result=500)}
    )

    assert from_mapping.fields == from_message.fields


def test_false_switches_a_member_off_explicitly() -> None:
    request = _request(fields={"content": False})

    assert request.fields.WhichOneof("content") == "content_enabled"
    assert not request.fields.content_enabled


def test_the_member_is_recoverable_from_the_value_alone() -> None:
    """What makes the projection total: a boolean and a message cannot be confused."""
    boolean = _request(fields={"content": True}).fields
    bag = _request(fields={"content": ContentOptions()}).fields

    assert boolean.WhichOneof("content") == "content_enabled"
    assert bag.WhichOneof("content") == "content_options"


@pytest.mark.parametrize(
    "member",
    ["cont" + "nt", "Content", "snippet", "content_enabled"],  # codespell:ignore
)
def test_a_key_the_json_body_lacks_is_refused(member: str) -> None:
    """The silent failure this exists to stop: a typo that reaches the service as an
    empty selection returns documents nobody asked for, and says nothing about why.

    `content_enabled` is in this list on purpose. It is a real protobuf field, so the
    message constructor would take it, but the JSON body has no such key and discards
    it. Accepting it here would make one selection mean two things.
    """
    with pytest.raises(TypeError, match=r"fields has no member"):
        _request(fields={member: True})


@pytest.mark.parametrize("value", ["true", 5, [], None])
def test_a_value_that_is_neither_is_refused_by_name(value: object) -> None:
    with pytest.raises(TypeError, match=r"fields\['content'\]"):
        _request(fields={"content": value})


@pytest.mark.parametrize(
    "selection",
    [
        FieldsMessage(),
        FieldsMessage(content_enabled=True),
        FieldsMessage(snippets_enabled=True),
        FieldsMessage(content_options=ContentOptions(max_characters_per_result=500)),
        FieldsMessage(snippet_options=SnippetOptions(max_snippets_per_result=5)),
    ],
)
def test_a_message_built_by_hand_is_transmitted_unchanged(
    selection: FieldsMessage,
) -> None:
    """The faithful form stays available beside the shorthand."""
    assert _request(fields=selection).fields == selection


@pytest.mark.parametrize(
    ("selection", "expected_arm"),
    [
        (Fields(content=True), "content_enabled"),
        (Fields(content=False), "content_enabled"),
        (Fields(content={"max_characters_per_result": 500}), "content_options"),
        (
            Fields(content=ContentOptions(max_characters_per_result=500)),
            "content_options",
        ),
    ],
)
def test_the_convenience_form_picks_the_arm(
    selection: Fields, expected_arm: str
) -> None:
    """`Fields` is the shape a caller writes; the arm names stay out of the surface."""
    assert _request(fields=selection).fields.WhichOneof("content") == expected_arm


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
