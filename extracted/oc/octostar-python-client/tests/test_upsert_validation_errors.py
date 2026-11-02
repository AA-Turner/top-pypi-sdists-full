"""Tests for ApiValidationError and upsert_entities._validate_response.

These verify the structured-error contract callers depend on: when the
server returns per-entity rejections, the SDK raises an
ApiValidationError whose attributes (entity_errors, missing_entity_ids,
mismatched_keys) and parsed conveniences (invalid_fields,
reserved_keyword_entity_types) match what the caller needs to recover
without regex-parsing str(exc).
"""

import pytest

from octostar.utils.exceptions import ApiConnectionError, ApiValidationError
from octostar.utils.workspace.upsert_entities import _validate_response


# ---------------------------------------------------------------------------
# ApiValidationError — class-level contract
# ---------------------------------------------------------------------------


def test_subclass_of_api_connection_error():
    # Legacy callers catch ApiConnectionError; the new exception must still
    # be caught by them, otherwise we silently break every existing handler.
    exc = ApiValidationError("upsert_entities", None, None)
    assert isinstance(exc, ApiConnectionError)
    assert isinstance(exc, ConnectionError)


def test_default_structured_attrs_are_empty_collections():
    exc = ApiValidationError("upsert_entities", None, None)
    assert exc.entity_errors == []
    assert exc.missing_entity_ids == set()
    assert exc.mismatched_keys == []
    assert exc.invalid_fields == {}
    assert exc.reserved_keyword_entity_types == set()


def test_invalid_fields_parses_per_entity_field_failures():
    exc = ApiValidationError(
        "upsert_entities",
        None,
        None,
        entity_errors=[
            {
                "entity_id": "abc-123",
                "error": "Invalid datetime value for field 'created_at': 'foo'",
            },
            {
                "entity_id": "abc-456",
                "error": "Invalid number value for field 'age'",
            },
            {
                "entity_id": "abc-456",
                "error": "Invalid date value for field 'dob': '2020-13-99'",
            },
        ],
    )
    assert exc.invalid_fields == {
        "abc-123": ["created_at"],
        "abc-456": ["age", "dob"],
    }


def test_invalid_fields_ignores_unparseable_errors():
    # Errors that don't match the "Invalid <type> value for field" pattern
    # should not appear in invalid_fields — they're still in entity_errors.
    exc = ApiValidationError(
        "upsert_entities",
        None,
        None,
        entity_errors=[
            {"entity_id": "abc-789", "error": "Something else went wrong"},
            {
                "entity_id": "abc-000",
                "error": "reserved keyword 'call' near position 17",
            },
        ],
    )
    assert exc.invalid_fields == {}


def test_invalid_fields_deduplicates_within_an_entity():
    # If the server somehow reports the same field twice for one entity, we
    # don't want the caller's "drop field" retry to see duplicates.
    exc = ApiValidationError(
        "upsert_entities",
        None,
        None,
        entity_errors=[
            {
                "entity_id": "x",
                "error": "Invalid datetime value for field 'created_at'",
            },
            {
                "entity_id": "x",
                "error": "Invalid datetime value for field 'created_at'",
            },
        ],
    )
    assert exc.invalid_fields == {"x": ["created_at"]}


def test_reserved_keyword_entity_types_extracts_quoted_tokens():
    exc = ApiValidationError(
        "upsert_entities",
        None,
        None,
        entity_errors=[
            {"entity_id": "a", "error": "reserved keyword 'call' near position 17"},
            {"entity_id": "b", "error": 'reserved keyword "match" at line 3'},
            {"entity_id": "c", "error": "no reserved keywords here"},
        ],
    )
    assert exc.reserved_keyword_entity_types == {"call", "match"}


def test_exception_message_still_human_readable():
    # The string form is what `print(exc)` and log statements show. Keep it
    # informative for the case where someone is reading logs, not handling
    # the exception programmatically.
    exc = ApiValidationError(
        "upsert_entities",
        type(
            "FakeResponse",
            (),
            {"status_code": 200, "content": "2 entities failed to upsert:\n  a: bad"},
        )(),
        None,
        entity_errors=[{"entity_id": "a", "error": "bad"}],
    )
    text = str(exc)
    assert "upsert_entities" in text
    assert "status code 200" in text
    assert "2 entities failed to upsert" in text


# ---------------------------------------------------------------------------
# _validate_response — end-to-end behaviour
# ---------------------------------------------------------------------------


def _body(entries):
    return [
        {
            "entity_id": e["os_entity_uid"],
            "entity_type": e.get("entity_type", "Person"),
            "os_workspace": e.get("os_workspace", "ws-1"),
        }
        for e in entries
    ]


def test_success_returns_returned_entities():
    entities = [{"os_entity_uid": "u1"}, {"os_entity_uid": "u2"}]
    body = _body(entities)
    data = {
        "entities": [
            {"entity_id": "u1", "os_workspace": "ws-1", "label": "Alice"},
            {"entity_id": "u2", "os_workspace": "ws-1", "label": "Bob"},
        ],
        "errors": [],
    }
    result = _validate_response(body, entities, data, response=None, client=None)
    assert {e["entity_id"] for e in result} == {"u1", "u2"}


def test_success_deduplicates_returned_entities_by_id():
    # The server may echo the same entity twice (rare but observed); the
    # SDK should hand back one row per entity_id.
    entities = [{"os_entity_uid": "u1"}]
    body = _body(entities)
    data = {
        "entities": [
            {"entity_id": "u1", "os_workspace": "ws-1", "label": "v1"},
            {"entity_id": "u1", "os_workspace": "ws-1", "label": "v2"},
        ],
        "errors": [],
    }
    result = _validate_response(body, entities, data, response=None, client=None)
    assert len(result) == 1


def test_per_entity_errors_raise_with_structured_payload():
    entities = [{"os_entity_uid": "abc-123"}, {"os_entity_uid": "abc-456"}]
    body = _body(entities)
    data = {
        "entities": [],
        "errors": [
            {
                "entity_id": "abc-123",
                "error": "Invalid datetime value for field 'created_at': 'foo'",
            },
            {
                "entity_id": "abc-456",
                "error": "Invalid number value for field 'age'",
            },
        ],
    }
    with pytest.raises(ApiValidationError) as excinfo:
        _validate_response(body, entities, data, response=None, client=None)

    exc = excinfo.value
    # Structured: caller can iterate entity_errors without regex.
    assert len(exc.entity_errors) == 2
    assert {e["entity_id"] for e in exc.entity_errors} == {"abc-123", "abc-456"}
    # invalid_fields shape exactly matches what the field-fallback retry
    # in app.entity-extract-and-graph reads from.
    assert exc.invalid_fields == {"abc-123": ["created_at"], "abc-456": ["age"]}
    # Other structured slots stay empty when the failure mode is per-entity.
    assert exc.missing_entity_ids == set()
    assert exc.mismatched_keys == []


def test_missing_entity_ids_raise_with_structured_payload():
    # If the server returns neither a success row nor an error row for an
    # entity we sent, the caller can't tell what happened — surface the
    # missing IDs explicitly.
    entities = [{"os_entity_uid": "u1"}, {"os_entity_uid": "u2"}]
    body = _body(entities)
    data = {"entities": [], "errors": []}
    with pytest.raises(ApiValidationError) as excinfo:
        _validate_response(body, entities, data, response=None, client=None)

    exc = excinfo.value
    assert exc.missing_entity_ids == {"u1", "u2"}
    assert exc.entity_errors == []


def test_mismatched_workspace_keys_raise_with_structured_payload():
    # Caller asks to write u1 in workspace ws-1, server returns it under
    # ws-stale. This is the "you got a stale record" path.
    entities = [{"os_entity_uid": "u1"}]
    body = _body(entities)
    data = {
        "entities": [{"entity_id": "u1", "os_workspace": "ws-stale"}],
        "errors": [],
    }
    with pytest.raises(ApiValidationError) as excinfo:
        _validate_response(body, entities, data, response=None, client=None)

    exc = excinfo.value
    assert exc.mismatched_keys == [("u1", "ws-stale")]
    assert exc.entity_errors == []


def test_truncates_per_entity_error_lines_in_message():
    # The message string caps at MAX_ERROR_DETAILS=10 lines so it stays
    # log-friendly; the structured entity_errors list is NOT truncated —
    # callers retrying via invalid_fields need all of them.
    entities = [{"os_entity_uid": f"u{i}"} for i in range(15)]
    body = _body(entities)
    errors = [
        {"entity_id": f"u{i}", "error": f"Invalid datetime value for field 'f{i}'"}
        for i in range(15)
    ]
    data = {"entities": [], "errors": errors}
    with pytest.raises(ApiValidationError) as excinfo:
        _validate_response(body, entities, data, response=None, client=None)

    exc = excinfo.value
    # Message is truncated for readability.
    assert "and 5 more" in str(exc)
    # Structured payload is complete — every rejected entity is recoverable.
    assert len(exc.entity_errors) == 15
    assert len(exc.invalid_fields) == 15


def test_legacy_except_api_connection_error_still_catches():
    # The whole point of subclassing: existing handlers in callers that
    # catch ApiConnectionError keep working without code changes.
    entities = [{"os_entity_uid": "u1"}]
    body = _body(entities)
    data = {
        "entities": [],
        "errors": [
            {"entity_id": "u1", "error": "Invalid datetime value for field 'x'"}
        ],
    }
    try:
        _validate_response(body, entities, data, response=None, client=None)
    except ApiConnectionError as exc:
        # We caught it via the parent type — proves backward compatibility.
        # And we can still inspect structured fields if we want.
        assert isinstance(exc, ApiValidationError)
        assert exc.invalid_fields == {"u1": ["x"]}
    else:
        pytest.fail("expected ApiValidationError")
