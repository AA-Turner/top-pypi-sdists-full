"""Agent-facing arg-error hints: stringified-JSON coercion + format_args_error.

Covers the two upgrades born from trace-log evidence (8x "Input should be a
valid dictionary" retries in one conversation on sql update.data, plus workbook
`ops`):

* ``coerce_stringified_containers`` — the executor's pre-dispatch recovery for
  a JSON STRING sent where a dict/list is required (exact-container, top-level,
  one pass; caller re-validates).
* ``format_args_error`` — appends explicit "you sent a JSON-encoded string"
  advice and enum/Literal did-you-mean lines.
"""
from __future__ import annotations

from typing import Any, Literal, Union

import pytest
from pydantic import BaseModel, ConfigDict, Field, RootModel, ValidationError

from matrx_ai.tools._dispatch_util import (
    coerce_stringified_containers,
    format_args_error,
    remove_flattened_variant_extras,
)


class _UpdateArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["update"]
    table: str
    data: dict[str, Any]
    match: dict[str, Any]


class _InsertArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["insert"]
    table: str
    data: Union[dict[str, Any], list[dict[str, Any]]]


class _SqlLikeArgs(RootModel):
    """Mimics the sql tool's discriminated-union RootModel — loc carries the
    union tag ('update', 'data'), the value lives at top-level 'data'."""

    root: Union[_UpdateArgs, _InsertArgs] = Field(discriminator="action")


class _OpsArgs(BaseModel):
    """Mimics the workbook tool shape — a top-level list field."""

    model_config = ConfigDict(extra="forbid")
    action: str
    ops: list[dict[str, Any]]


class _ModeArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["read", "write", "append"]


def _fail(model: type[BaseModel], payload: dict) -> ValidationError:
    with pytest.raises(ValidationError) as ei:
        model.model_validate(payload)
    return ei.value


# ---------------------------------------------------------------------------
# coerce_stringified_containers — happy paths
# ---------------------------------------------------------------------------


class TestCoercionHappyPaths:
    def test_dict_field_json_string_is_coerced(self) -> None:
        args = {"action": "update", "table": "t", "data": '{"a": 1}', "match": {"id": 2}}
        exc = _fail(_SqlLikeArgs, args)
        out = coerce_stringified_containers(args, exc)
        assert out is not None
        merged, fields = out
        assert merged["data"] == {"a": 1}
        assert fields == ["data"]
        _SqlLikeArgs.model_validate(merged)  # the executor's re-validate step

    def test_list_field_json_string_is_coerced(self) -> None:
        args = {"action": "edit", "ops": '[{"op": "set"}]'}
        exc = _fail(_OpsArgs, args)
        out = coerce_stringified_containers(args, exc)
        assert out is not None
        merged, fields = out
        assert merged["ops"] == [{"op": "set"}]
        assert fields == ["ops"]
        _OpsArgs.model_validate(merged)

    def test_union_dict_or_list_matches_either_branch(self) -> None:
        args = {"action": "insert", "table": "t", "data": '[{"a": 1}, {"a": 2}]'}
        exc = _fail(_SqlLikeArgs, args)
        out = coerce_stringified_containers(args, exc)
        assert out is not None
        merged, fields = out
        assert merged["data"] == [{"a": 1}, {"a": 2}]
        assert fields == ["data"]
        _SqlLikeArgs.model_validate(merged)

    def test_multiple_fields_coerced_in_one_pass(self) -> None:
        args = {"action": "update", "table": "t", "data": '{"a": 1}', "match": '{"id": 9}'}
        exc = _fail(_SqlLikeArgs, args)
        out = coerce_stringified_containers(args, exc)
        assert out is not None
        merged, fields = out
        assert merged["data"] == {"a": 1} and merged["match"] == {"id": 9}
        assert fields == ["data", "match"]

    def test_original_arguments_not_mutated(self) -> None:
        args = {"action": "update", "table": "t", "data": '{"a": 1}', "match": {"id": 2}}
        exc = _fail(_SqlLikeArgs, args)
        coerce_stringified_containers(args, exc)
        assert args["data"] == '{"a": 1}'


# ---------------------------------------------------------------------------
# coerce_stringified_containers — refuse paths
# ---------------------------------------------------------------------------


class TestCoercionRefusePaths:
    def test_non_json_string_refused(self) -> None:
        args = {"action": "update", "table": "t", "data": "not json", "match": {"id": 1}}
        exc = _fail(_SqlLikeArgs, args)
        assert coerce_stringified_containers(args, exc) is None

    def test_json_scalar_refused_not_exact_container(self) -> None:
        args = {"action": "update", "table": "t", "data": "42", "match": {"id": 1}}
        exc = _fail(_SqlLikeArgs, args)
        assert coerce_stringified_containers(args, exc) is None

    def test_json_list_where_only_dict_required_refused(self) -> None:
        args = {"action": "update", "table": "t", "data": '[{"a": 1}]', "match": {"id": 1}}
        exc = _fail(_SqlLikeArgs, args)
        # _UpdateArgs.data requires a dict; a list is not an exact match.
        assert coerce_stringified_containers(args, exc) is None

    def test_non_string_value_refused(self) -> None:
        args = {"action": "update", "table": "t", "data": 42, "match": {"id": 1}}
        exc = _fail(_SqlLikeArgs, args)
        assert coerce_stringified_containers(args, exc) is None

    def test_nested_field_not_coerced(self) -> None:
        class _Nested(BaseModel):
            config: dict[str, Any]

        class _Outer(BaseModel):
            inner: _Nested

        args = {"inner": {"config": '{"a": 1}'}}
        exc = _fail(_Outer, args)
        # loc is ('inner', 'config'); 'config' is not a top-level key.
        assert coerce_stringified_containers(args, exc) is None

    def test_unrelated_error_types_ignored(self) -> None:
        args = {"mode": "raed"}
        exc = _fail(_ModeArgs, args)
        assert coerce_stringified_containers(args, exc) is None

    def test_non_pydantic_exception_returns_none(self) -> None:
        assert coerce_stringified_containers({"a": "{}"}, ValueError("boom")) is None


# ---------------------------------------------------------------------------
# format_args_error — message upgrades
# ---------------------------------------------------------------------------


class TestFormatArgsError:
    def test_stringified_container_advice_appended(self) -> None:
        args = {"action": "update", "table": "t", "data": '{"a": 1}', "match": {"id": 1}}
        msg = format_args_error(_fail(_SqlLikeArgs, args))
        assert "Input should be a valid dictionary" in msg
        assert "JSON-encoded string" in msg
        assert "raw JSON object/array" in msg

    def test_list_field_string_gets_same_advice(self) -> None:
        msg = format_args_error(_fail(_OpsArgs, {"action": "edit", "ops": '[{"a":1}]'}))
        assert "JSON-encoded string" in msg

    def test_no_advice_when_shape_is_unrelated(self) -> None:
        msg = format_args_error(_fail(_OpsArgs, {"action": "edit", "ops": 42}))
        assert "JSON-encoded string" not in msg

    def test_literal_mismatch_gets_did_you_mean(self) -> None:
        msg = format_args_error(_fail(_ModeArgs, {"mode": "raed"}))
        # Best match first; phrasing is single or multi depending on how many
        # permitted values clear the cutoff.
        assert "Did you mean" in msg
        assert "read" in msg.split("Did you mean", 1)[1]

    def test_literal_far_miss_no_did_you_mean(self) -> None:
        msg = format_args_error(_fail(_ModeArgs, {"mode": "zzzzzz"}))
        assert "Did you mean" not in msg
        # Pydantic's own permitted-values line still present.
        assert "read" in msg

    def test_plain_exception_falls_back_to_str(self) -> None:
        assert format_args_error(ValueError("plain boom")) == "plain boom"

    def test_missing_field_shape_unchanged(self) -> None:
        msg = format_args_error(_fail(_OpsArgs, {"action": "edit"}))
        assert "ops" in msg and "required" in msg.lower()


class TestFlattenedVariantExtras:
    def test_field_owned_by_another_action_is_removed(self) -> None:
        from matrx_ai.tools.arg_models.db_args import SqlArgs

        args = {
            "action": "query",
            "table": "ai.provider",
            "data": {"name": "ignored"},
        }
        exc = _fail(SqlArgs, args)

        recovered = remove_flattened_variant_extras(args, SqlArgs, exc)

        assert recovered == (
            {"action": "query", "table": "ai.provider"},
            ["data"],
        )
        SqlArgs.model_validate(recovered[0])

    def test_unknown_field_is_not_silently_removed(self) -> None:
        from matrx_ai.tools.arg_models.db_args import SqlArgs

        args = {
            "action": "query",
            "table": "ai.provider",
            "typo_field": "must remain an error",
        }
        exc = _fail(SqlArgs, args)

        assert remove_flattened_variant_extras(args, SqlArgs, exc) is None
