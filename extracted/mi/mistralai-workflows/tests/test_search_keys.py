"""Unit tests for search-key validation and extraction (RFC-402, V1 input path)."""

from __future__ import annotations

from enum import Enum
from typing import AbstractSet, Annotated, Any, Literal, Mapping, Sequence
from unittest import mock

import pytest
from pydantic import BaseModel, Field

from mistralai.workflows.core._registration import search_keys as search_keys_module
from mistralai.workflows.core._registration.search_keys import (
    extract_search_key_metadata,
    validate_search_key_paths,
)
from mistralai.workflows.core.config.config import MAX_SEARCH_KEY_CHARS, MAX_SEARCH_KEY_VALUE_CHARS
from mistralai.workflows.exceptions import WorkflowsException


class Customer(BaseModel):
    name: str
    tier: int


class ReportPayload(BaseModel):
    id: str
    customer: Customer
    note: str | None = None
    priority: int | str = 0
    tags: list[str] = []
    meta: dict[str, str] = {}


class MultiParamInput(BaseModel):
    """Simulates the wrapper model built for a multi-parameter entrypoint."""

    payload: ReportPayload
    tenant_name: str


class Address(BaseModel):
    city: str


class UnionLeaves(BaseModel):
    two_models: Customer | Address
    model_or_scalar: Customer | str
    container_or_scalar: list[str] | str
    scalar_union: int | str
    scalar_union_opt: int | str | None = None


class Priority(str, Enum):
    low = "low"
    high = "high"


class Color(Enum):
    red = "red"
    green = "green"


class AbstractCollections(BaseModel):
    """Abstract collection ABCs must be rejected like their concrete counterparts."""

    seq: Sequence[str] = []
    mapping: Mapping[str, str] = {}
    abstract_set: AbstractSet[str] = set()


class ScalarLeaves(BaseModel):
    status: Literal["active", "paused"]
    priority: Priority


class TestValidateSearchKeyPaths:
    @pytest.mark.parametrize(
        "paths",
        [
            ["id"],
            ["customer.name", "customer.tier"],
            ["note"],  # Optional[str] leaf is a scalar
            ["priority"],  # scalar union leaf (int | str)
            ["id", "customer.name", "customer.tier", "note"],
        ],
    )
    def test_accepts_valid_paths(self, paths: list[str]) -> None:
        validate_search_key_paths(ReportPayload, paths)

    def test_accepts_multi_param_paths_rooted_at_param_name(self) -> None:
        validate_search_key_paths(MultiParamInput, ["payload.id", "payload.customer.name", "tenant_name"])

    def test_rejects_colon(self) -> None:
        with pytest.raises(WorkflowsException, match="must not contain ':'"):
            validate_search_key_paths(ReportPayload, ["customer:name"])

    def test_rejects_unknown_field(self) -> None:
        with pytest.raises(WorkflowsException, match="not a field of"):
            validate_search_key_paths(ReportPayload, ["does_not_exist"])

    def test_rejects_unknown_nested_field(self) -> None:
        with pytest.raises(WorkflowsException, match="not a field of Customer"):
            validate_search_key_paths(ReportPayload, ["customer.missing"])

    def test_rejects_traversing_into_scalar(self) -> None:
        with pytest.raises(WorkflowsException, match="must be a nested model"):
            validate_search_key_paths(ReportPayload, ["id.nope"])

    def test_rejects_model_leaf(self) -> None:
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(ReportPayload, ["customer"])

    def test_rejects_list_leaf(self) -> None:
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(ReportPayload, ["tags"])

    def test_rejects_dict_leaf(self) -> None:
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(ReportPayload, ["meta"])

    @pytest.mark.parametrize("path", ["seq", "mapping", "abstract_set"])
    def test_rejects_abstract_collection_leaf(self, path: str) -> None:
        # Abstract ABCs (Sequence/Mapping/Set) must be rejected like concrete containers,
        # otherwise they pass validation but yield no metadata at runtime.
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(AbstractCollections, [path])

    def test_rejects_empty_path(self) -> None:
        with pytest.raises(WorkflowsException, match="must not be empty"):
            validate_search_key_paths(ReportPayload, [""])

    def test_rejects_whitespace_padded_path(self) -> None:
        with pytest.raises(WorkflowsException, match="must not be empty or padded"):
            validate_search_key_paths(ReportPayload, [" id"])

    def test_rejects_empty_segment(self) -> None:
        with pytest.raises(WorkflowsException, match="empty path segment"):
            validate_search_key_paths(ReportPayload, ["customer."])

    def test_allows_up_to_max_search_keys(self) -> None:
        with mock.patch.object(search_keys_module, "MAX_SEARCH_KEYS", 3):
            validate_search_key_paths(ReportPayload, ["id", "customer.name", "customer.tier"])

    def test_rejects_more_than_max_search_keys(self) -> None:
        with mock.patch.object(search_keys_module, "MAX_SEARCH_KEYS", 2):
            with pytest.raises(WorkflowsException, match="at most 2 search_keys"):
                validate_search_key_paths(ReportPayload, ["id", "customer.name", "customer.tier"])

    def test_rejects_duplicate_paths(self) -> None:
        with pytest.raises(WorkflowsException, match="duplicate search key"):
            validate_search_key_paths(ReportPayload, ["id", "id"])

    def test_rejects_over_long_key(self) -> None:
        with pytest.raises(WorkflowsException, match="at most 256 characters"):
            validate_search_key_paths(ReportPayload, ["a" * 257])

    def test_rejects_union_of_models_leaf(self) -> None:
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(UnionLeaves, ["two_models"])

    def test_rejects_model_or_scalar_union_leaf(self) -> None:
        # Runtime would emit for the scalar branch and skip the model branch, so reject at define time.
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(UnionLeaves, ["model_or_scalar"])

    def test_rejects_container_in_union_leaf(self) -> None:
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(UnionLeaves, ["container_or_scalar"])

    def test_accepts_scalar_only_union_leaves(self) -> None:
        validate_search_key_paths(UnionLeaves, ["scalar_union", "scalar_union_opt"])

    def test_accepts_literal_and_enum_leaves(self) -> None:
        # Blacklist semantics: Literal and Enum are scalars, not containers.
        validate_search_key_paths(ScalarLeaves, ["status", "priority"])

    def test_accumulates_errors_within_a_path(self) -> None:
        path = "a..b" + "c" * MAX_SEARCH_KEY_CHARS
        with pytest.raises(WorkflowsException) as exc_info:
            validate_search_key_paths(ReportPayload, [path], workflow_name="my-wf")
        message = exc_info.value.message
        assert "at most 256 characters" in message
        assert "has an empty path segment" in message
        assert "`my-wf`" in message

    def test_accumulates_errors_across_paths(self) -> None:
        with pytest.raises(WorkflowsException) as exc_info:
            validate_search_key_paths(
                ReportPayload,
                ["customer:", "does_not_exist", "tags", "customer.missing"],
                workflow_name="my-wf",
            )
        message = exc_info.value.message
        assert "At least one invalid search key in definition of workflow `my-wf`" in message
        for path in ("customer:", "does_not_exist", "tags", "customer.missing"):
            assert f"- `{path}`:" in message
        assert "must not contain ':'" in message
        assert "is not a field of ReportPayload" in message
        assert "is not a field of Customer" in message
        assert "leaf must be a scalar" in message


class TestExtractSearchKeyMetadata:
    def test_extracts_flat_and_nested(self) -> None:
        params = {"id": "pr-402", "customer": {"name": "acme", "tier": 2}}
        result = extract_search_key_metadata(params, ["id", "customer.name", "customer.tier"])
        assert result == {"id": "pr-402", "customer.name": "acme", "customer.tier": "2"}

    def test_coerces_scalars_to_str(self) -> None:
        # Bools lowercase so JSON-style searches for "true"/"false" match.
        params = {"flag": True, "count": 0}
        assert extract_search_key_metadata(params, ["flag", "count"]) == {"flag": "true", "count": "0"}

    def test_coerces_float_to_str(self) -> None:
        params = {"ratio": 1.5}
        assert extract_search_key_metadata(params, ["ratio"]) == {"ratio": "1.5"}

    def test_coerces_literal_to_str(self) -> None:
        assert extract_search_key_metadata({"status": "active"}, ["status"]) == {"status": "active"}

    def test_coerces_enum_to_value_not_repr(self) -> None:
        # A plain (non-str) Enum member serializes to its .value, not the "Color.red" repr.
        assert extract_search_key_metadata({"color": Color.red}, ["color"]) == {"color": "red"}

    def test_skips_missing_key(self) -> None:
        params = {"id": "x", "customer": {"name": "acme"}}
        assert extract_search_key_metadata(params, ["customer.tier"]) == {}

    def test_skips_none_value(self) -> None:
        assert extract_search_key_metadata({"note": None}, ["note"]) == {}

    def test_returns_empty_for_no_search_keys(self) -> None:
        assert extract_search_key_metadata({"id": "x"}, []) == {}

    def test_returns_empty_for_non_dict_params(self) -> None:
        assert extract_search_key_metadata(None, ["id"]) == {}
        assert extract_search_key_metadata("not-a-dict", ["id"]) == {}

    def test_accepts_basemodel_params(self) -> None:
        params = ReportPayload(id="pr-1", customer=Customer(name="acme", tier=3))
        result = extract_search_key_metadata(params, ["id", "customer.tier"])
        assert result == {"id": "pr-1", "customer.tier": "3"}

    def test_does_not_stringify_container_leaf(self) -> None:
        params = {"tags": ["a", "b"], "meta": {"k": "v"}}
        assert extract_search_key_metadata(params, ["tags", "meta"]) == {}

    def test_does_not_traverse_through_scalar(self) -> None:
        params = {"id": "x"}
        assert extract_search_key_metadata(params, ["id.deeper"]) == {}

    def test_extracts_multi_param_wrapper_shape(self) -> None:
        # Multi-param entrypoints serialize to a dict keyed by parameter name.
        params = {"order": {"id": "ord-2"}, "customer": {"name": "acme", "tier": 3}}
        result = extract_search_key_metadata(params, ["order.id", "customer.name", "customer.tier"])
        assert result == {"order.id": "ord-2", "customer.name": "acme", "customer.tier": "3"}

    def test_keeps_value_within_char_cap_unchanged(self) -> None:
        exact = "a" * MAX_SEARCH_KEY_VALUE_CHARS
        assert extract_search_key_metadata({"id": exact}, ["id"]) == {"id": exact}

    def test_truncates_value_exceeding_char_cap(self) -> None:
        big = "a" * (MAX_SEARCH_KEY_VALUE_CHARS + 500)
        result = extract_search_key_metadata({"id": big}, ["id"])
        assert len(result["id"]) == MAX_SEARCH_KEY_VALUE_CHARS
        assert big.startswith(result["id"])

    def test_truncation_counts_characters_and_never_splits_a_char(self) -> None:
        # Multibyte chars each count as one; slicing a str can't split a code point.
        value = "€" * (MAX_SEARCH_KEY_VALUE_CHARS + 10)
        truncated = extract_search_key_metadata({"id": value}, ["id"])["id"]
        assert len(truncated) == MAX_SEARCH_KEY_VALUE_CHARS
        assert value.startswith(truncated)

    def test_swallows_exception_and_returns_empty(self) -> None:
        # The contract: metadata must never fail the workflow. A raising accessor
        # (malformed value, hostile .get, etc.) is swallowed and the offending key
        # contributes nothing rather than propagating.
        class _ExplodingDict(dict):
            def get(self, key: str, default: Any = None) -> Any:  # type: ignore[override]
                raise RuntimeError("boom")

        # A raising .get on the root dict trips the try/except in the loop.
        params: Any = _ExplodingDict()
        assert extract_search_key_metadata(params, ["id"]) == {}

    def test_swallows_exception_partway_through_traversal(self) -> None:
        # Exception raised mid-traversal: a still-usable key on a sibling branch
        # is unaffected, and the failing key simply yields no entry.
        class _ExplodingDict(dict):
            def get(self, key: str, default: Any = None) -> Any:  # type: ignore[override]
                raise RuntimeError("boom")

        params = {"ok": "value", "bad": _ExplodingDict()}
        result = extract_search_key_metadata(params, ["ok", "bad.missing"])
        assert result == {"ok": "value"}


class _Inner(BaseModel):
    x: str


class AnnotatedInput(BaseModel):
    nested: Annotated[_Inner, Field(description="d")]
    leaf_list: Annotated[list[str], Field(description="d")]
    leaf_scalar: Annotated[str, Field(description="d")]


class TestAnnotatedFields:
    def test_annotated_nested_model_traversal_is_accepted(self) -> None:
        validate_search_key_paths(AnnotatedInput, ["nested.x"])

    def test_annotated_container_leaf_is_rejected(self) -> None:
        with pytest.raises(WorkflowsException, match="leaf must be a scalar"):
            validate_search_key_paths(AnnotatedInput, ["leaf_list"])

    def test_annotated_scalar_leaf_is_accepted(self) -> None:
        validate_search_key_paths(AnnotatedInput, ["leaf_scalar"])

    def test_runtime_extracts_annotated_nested_model(self) -> None:
        params = {"nested": {"x": "hello"}, "leaf_scalar": "s"}
        result = extract_search_key_metadata(params, ["nested.x", "leaf_scalar"])
        assert result == {"nested.x": "hello", "leaf_scalar": "s"}


class AliasedInput(BaseModel):
    customer_id: str = Field(alias="customerId")
    name: str = Field(alias="customerName")
    plain: str = "default"


class TestAliasedFields:
    def test_define_time_rejects_aliased_leaf(self) -> None:
        with pytest.raises(WorkflowsException, match="uses a Pydantic alias"):
            validate_search_key_paths(AliasedInput, ["customer_id"])

    def test_define_time_rejects_aliased_segment_when_traversing(self) -> None:
        class Outer(BaseModel):
            inner: AliasedInput

        with pytest.raises(WorkflowsException, match="uses a Pydantic alias"):
            validate_search_key_paths(Outer, ["inner.customer_id"])

    def test_define_time_rejects_alias_path_string(self) -> None:
        with pytest.raises(WorkflowsException, match="not a field of AliasedInput"):
            validate_search_key_paths(AliasedInput, ["customerId"])

    def test_define_time_accepts_plain_field_alongside_aliased(self) -> None:
        validate_search_key_paths(AliasedInput, ["plain"])

    def test_extraction_cannot_resolve_aliased_leaf(self) -> None:
        # Extraction is a plain field-name walk; aliased keys are invisible.
        wire = {"customerId": "c-123", "customerName": "acme"}
        assert extract_search_key_metadata(wire, ["customer_id", "name"]) == {}
        assert extract_search_key_metadata(wire, ["plain"]) == {}
