"""Tests for ``_merge_stranded_value`` (field-by-field nested-dict merge)."""

from agentic_devtools.adapters.pull_request_create import _merge_stranded_value


def test_merges_nested_dict_field_by_field_when_destination_has_partial_mapping() -> None:
    new_state: dict = {"github": {"pull_request_url": "https://example.com/pr/1"}}

    _merge_stranded_value(new_state, "github", {"pull_request_number": 42})

    assert new_state == {
        "github": {
            "pull_request_url": "https://example.com/pr/1",
            "pull_request_number": 42,
        }
    }


def test_destination_nested_value_wins_on_conflict() -> None:
    new_state: dict = {"github": {"pull_request_number": 99}}

    _merge_stranded_value(new_state, "github", {"pull_request_number": 42})

    assert new_state == {"github": {"pull_request_number": 99}}


def test_recursively_merges_nested_dict_fields() -> None:
    new_state: dict = {"workflow": {"context": {"nested": {"destination_only": "kept", "conflict": "destination"}}}}

    _merge_stranded_value(
        new_state,
        "workflow",
        {"context": {"nested": {"source_only": "preserved", "conflict": "source"}}},
    )

    assert new_state == {
        "workflow": {
            "context": {
                "nested": {
                    "destination_only": "kept",
                    "source_only": "preserved",
                    "conflict": "destination",
                }
            }
        }
    }


def test_creates_nested_dict_when_destination_key_is_missing() -> None:
    new_state: dict = {}

    _merge_stranded_value(new_state, "github", {"pull_request_number": 42})

    assert new_state == {"github": {"pull_request_number": 42}}


def test_non_dict_value_uses_plain_setdefault() -> None:
    new_state: dict = {"pull_request_id": 99}

    _merge_stranded_value(new_state, "pull_request_id", 42)

    assert new_state == {"pull_request_id": 99}


def test_non_dict_destination_key_missing_sets_value() -> None:
    new_state: dict = {}

    _merge_stranded_value(new_state, "pull_request_id", 42)

    assert new_state == {"pull_request_id": 42}


def test_non_dict_destination_wins_when_stranded_value_is_dict() -> None:
    new_state: dict = {"github": "concurrent-value"}

    _merge_stranded_value(new_state, "github", {"pull_request_number": 42})

    assert new_state == {"github": "concurrent-value"}
