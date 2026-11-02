"""``pg_emitter`` reads a function's result keys from ``pg_proc``, never guesses them.

The bodies below are the real shapes the topical-map door uses: a literal object,
an object composed onto another function's result (``replace_map_section`` over
``upsert_map_topics``), and the two shapes pg_proc cannot state.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.pg_emitter import (
    PgFunction,
    UngradeableEmitter,
    emitter_model,
    json_return_keys,
)
from matrx_graph.content_ir.sample import contract_drift

UPSERT = PgFunction(
    "seo.upsert_map_topics",
    "jsonb",
    """DECLARE v_errors jsonb := '[]';
BEGIN
  -- RETURN jsonb_build_object('commented_out', 1);
  v_errors := v_errors || jsonb_build_object('slug', 'x', 'message', 'it''s invalid');
  IF p_tree IS NULL THEN RETURN NULL; END IF;
  RETURN jsonb_build_object('created', to_jsonb(v_created), 'updated', to_jsonb(v_updated),
                            'kept_retired', v_kept_retired);
END""",
)

REPLACE = PgFunction(
    "seo.replace_map_section",
    "jsonb",
    """BEGIN
  v_up := seo.upsert_map_topics(p_map_id, v_tree);
  RETURN v_up || jsonb_build_object('moved_in', '[]'::jsonb, 'removed', v_rep);
END""",
)

FACET = PgFunction(
    "seo.set_map_topic_facet",
    "jsonb",
    """BEGIN
  IF p_value IS NULL THEN RETURN jsonb_build_object('ok', true, 'cleared', p_facet); END IF;
  RETURN jsonb_build_object('ok', true, 'value', p_value);
END""",
)


def _resolve(name: str) -> PgFunction | None:
    return {"seo.upsert_map_topics": UPSERT}.get(name)


def test_literal_keys_are_read_and_comments_and_nested_objects_ignored():
    assert json_return_keys(UPSERT) == {"created": True, "kept_retired": True, "updated": True}


def test_a_key_in_only_some_returns_is_optional():
    assert json_return_keys(FACET) == {"cleared": False, "ok": True, "value": False}


def test_composition_follows_the_other_function_through_its_own_row():
    keys = json_return_keys(REPLACE, resolve=_resolve)
    assert keys == {
        "created": True, "kept_retired": True, "moved_in": True, "removed": True, "updated": True,
    }


def test_composition_without_the_callee_is_ungradeable_never_empty():
    with pytest.raises(UngradeableEmitter, match="upsert_map_topics"):
        json_return_keys(REPLACE, resolve=lambda _name: None)


@pytest.mark.parametrize(
    "body",
    [
        "BEGIN v_out := '{}'; v_out := v_out || jsonb_build_object('a', 1); RETURN v_out; END",
        "BEGIN RETURN jsonb_build_object(v_key, 1); END",
        "BEGIN RETURN to_jsonb(v_row); END",
    ],
)
def test_what_pg_proc_does_not_state_is_ungradeable(body: str):
    with pytest.raises(UngradeableEmitter):
        json_return_keys(PgFunction("seo.f", "jsonb", body), resolve=_resolve)


def test_the_check_catches_a_key_the_kind_never_declared():
    class Result(BaseModel):
        model_config = ConfigDict(extra="forbid")
        action: str
        created: list[str] | None = None
        updated: list[str] | None = None

    model = emitter_model(UPSERT, name="upsert_emits", envelope={"action": (str, ...)})
    assert contract_drift(model, Result) == [("kept_retired", "extra_forbidden")]

    class Caught(Result):
        kept_retired: list[dict] | None = None

    assert contract_drift(model, Caught) == []


def test_a_keyed_result_contributes_exactly_its_key():
    outline = PgFunction("seo.map_outline", "text", "BEGIN RETURN 'x'; END")
    model = emitter_model(outline, name="outline", under_key="outline")
    assert set(model.model_fields) == {"outline"}
