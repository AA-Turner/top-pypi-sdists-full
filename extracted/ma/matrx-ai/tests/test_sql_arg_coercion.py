"""Regression guard for the 2026-05-25 SQL-tool loop-to-death incident.

A model passed `sql action=update` with `data` as a JSON *string* instead of a
JSON object. The wire model required a dict, so Pydantic rejected it with the
cryptic "Input should be a valid dictionary"; the model misread that, retried
the same broken shape 8x, and the loop guard killed the run.

A JSON-string object/array and the object/array itself resolve to the same
thing, so the wire models now coerce the string form. Anything genuinely not an
object/array raises an explicit, instructive error (never the bare Pydantic
message). These tests pin both behaviours.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.tools.arg_models.db_args import SqlArgs


def _root(payload: dict):
    return SqlArgs.model_validate(payload).root


def test_update_json_string_data_is_coerced_to_dict() -> None:
    m = _root({"action": "update", "table": "ai_model",
               "data": '{"name": "x", "priority": 3}', "match": '{"id": "1"}'})
    assert m.data == {"name": "x", "priority": 3}
    assert m.match == {"id": "1"}


def test_update_real_dict_passthrough() -> None:
    m = _root({"action": "update", "table": "t",
               "data": {"a": 1}, "match": {"id": 2}})
    assert m.data == {"a": 1} and m.match == {"id": 2}


def test_insert_json_string_array_is_coerced() -> None:
    m = _root({"action": "insert", "table": "t", "data": '[{"a": 1}, {"a": 2}]'})
    assert m.data == [{"a": 1}, {"a": 2}]


def test_insert_json_string_object_is_coerced() -> None:
    m = _root({"action": "insert", "table": "t", "data": '{"a": 1}'})
    assert m.data == {"a": 1}


def test_delete_json_string_match_is_coerced() -> None:
    m = _root({"action": "delete", "table": "t", "match": '{"id": 9}'})
    assert m.match == {"id": 9}


def test_upsert_json_string_data_is_coerced() -> None:
    m = _root({"action": "upsert", "table": "t", "data": '{"id": 1, "v": 2}'})
    assert m.data == {"id": 1, "v": 2}


def test_uncoercible_data_raises_clear_instructive_error() -> None:
    with pytest.raises(ValidationError) as ei:
        _root({"action": "update", "table": "t", "data": "not json", "match": {"id": 1}})
    msg = "; ".join(e["msg"] for e in ei.value.errors())
    # The message must teach the model the exact fix, not say "valid dictionary".
    assert "JSON object" in msg
    assert "do NOT" in msg.lower() or "do not" in msg.lower()
    assert "valid dictionary" not in msg  # the old cryptic message is gone


def test_uncoercible_match_raises_clear_error() -> None:
    with pytest.raises(ValidationError) as ei:
        _root({"action": "update", "table": "t", "data": {"a": 1}, "match": "42"})
    msg = "; ".join(e["msg"] for e in ei.value.errors())
    assert "JSON object" in msg and "match" in msg


# ── The same coercion is shared across the dispatcher tools (note/seo/picklist/
# cloud_file/ctx_patch/dataset) via matrx_ai.tools.arg_models._coercion ─────────

def test_dispatcher_list_field_coerces_json_string_array() -> None:
    from matrx_ai.tools.arg_models.dispatcher_args import PicklistArgs, SeoArgs

    m = PicklistArgs.model_validate(
        {"action": "create", "picklist_name": "p", "items": '[{"label": "A"}]'}
    ).root
    assert m.items == [{"label": "A"}]

    s = SeoArgs.model_validate(
        {"action": "check_titles", "titles": '["t1", "t2"]'}
    ).root
    assert s.titles == ["t1", "t2"]


def test_dispatcher_object_field_coerces_json_string_object() -> None:
    from matrx_ai.tools.arg_models.dispatcher_args import CtxPatchArgs

    m = CtxPatchArgs.model_validate(
        {"command": "json_merge", "key": "k", "patch": '{"a": 1}'}
    ).root
    assert m.patch == {"a": 1}


def test_dispatcher_optional_list_field_passes_none_through() -> None:
    from matrx_ai.tools.arg_models.dispatcher_args import NoteArgs

    m = NoteArgs.model_validate({"action": "create", "label": "L"}).root
    assert m.tags is None  # None is not coerced/rejected on an Optional field


def test_dispatcher_list_field_rejects_non_array_with_clear_error() -> None:
    from matrx_ai.tools.arg_models.dispatcher_args import SeoArgs

    with pytest.raises(ValidationError) as ei:
        SeoArgs.model_validate({"action": "check_titles", "titles": "just a string"})
    msg = "; ".join(e["msg"] for e in ei.value.errors())
    assert "JSON array" in msg and "valid list" not in msg
