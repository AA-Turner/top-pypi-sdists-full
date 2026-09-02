"""Unit tests for the kind-registry authoring toolsets (kind_* / kindcomp_*).

Pure-logic coverage: schema inference, slug normalization, validation
plumbing, arg-contract enforcement, and the in-code authorization mirror.
The live DB lifecycle (create kind -> component -> patch -> version snapshot
-> incident -> resolve -> soft-delete) is exercised by
``tests_trials/run_kind_tools_e2e.py`` (repo root) against the real database.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.tools.implementations.kind_shared import (
    KIND_ENTITY_TOKEN,
    can_access_kind,
    component_source_lint,
    ensure_root_marker,
    fields_from_json_schema,
    infer_schema_from_sample,
    json_schema_from_fields,
    normalize_kind_slug,
    validate_against_schema,
)
from matrx_ai.tools.models import ToolContext


def make_ctx() -> ToolContext:
    return ToolContext(call_id=str(uuid4()), tool_name="test")


@pytest.mark.asyncio
async def test_content_block_category_uses_manifest_model_key(monkeypatch) -> None:
    """The host injects platform.categories as ``SklCategories``.

    Using the concrete aidream class name (``Categories``) worked only when a
    caller accidentally supplied an undeclared alias and crashed the live
    kind_create_content_block path in the normal generated host wiring.
    """
    from matrx_ai.tools.implementations import kind_authoring

    requested: list[str] = []
    category = SimpleNamespace(
        id=uuid4(),
        name="Agent Skills",
        deleted_at=None,
    )

    class Query:
        def limit(self, _value: int) -> Query:
            return self

        async def all(self) -> list[SimpleNamespace]:
            return [category]

    class Categories:
        @classmethod
        def filter(cls, **filters: Any) -> Query:
            assert filters == {"placement_type": "content-block"}
            return Query()

    def fake_get_db_model(key: str) -> type[Categories]:
        requested.append(key)
        return Categories

    monkeypatch.setattr(kind_authoring, "get_db_model", fake_get_db_model)

    assert await kind_authoring._content_block_category_id() == str(category.id)
    assert requested == ["SklCategories"]


# ---------------------------------------------------------------------------
# Slug normalization — must match the contract publisher's normalization
# ---------------------------------------------------------------------------


def test_normalize_kind_slug_matches_publisher_normalization() -> None:
    assert normalize_kind_slug("Invoice Summary") == "invoice_summary"
    assert normalize_kind_slug("  Q3 -- Sales!! Report ") == "q3_sales_report"
    assert normalize_kind_slug("already_snake") == "already_snake"
    assert normalize_kind_slug("***") == "unnamed"


def test_normalize_kind_slug_agrees_with_contract_kinds() -> None:
    import re

    for name in ("My Fancy Kind", "a-b-c", "UPPER lower 42"):
        expected = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        assert normalize_kind_slug(name) == expected


# ---------------------------------------------------------------------------
# Schema inference
# ---------------------------------------------------------------------------


def test_infer_schema_scalars_and_required() -> None:
    schema = infer_schema_from_sample(
        {"name": "Acme", "count": 3, "ratio": 0.5, "active": True, "note": None}
    )
    props = schema["properties"]
    assert props["name"] == {"type": "string"}
    assert props["count"] == {"type": "integer"}
    assert props["ratio"] == {"type": "number"}
    assert props["active"] == {"type": "boolean"}
    # Null observed -> permissive union including null.
    assert "null" in props["note"]["type"]
    # Optional-by-default (the schema-evolution rule): no required list unless
    # the caller names required_fields.
    assert "required" not in schema
    assert schema["additionalProperties"] is False


def test_infer_schema_required_fields() -> None:
    schema = infer_schema_from_sample(
        {"name": "Acme", "count": 3}, required_fields=["name"]
    )
    assert schema["required"] == ["name"]
    with pytest.raises(ValueError):
        infer_schema_from_sample({"name": "Acme"}, required_fields=["missing"])


def test_infer_schema_nested_objects_and_arrays() -> None:
    schema = infer_schema_from_sample(
        {"items": [{"sku": "A1", "qty": 2}], "meta": {"source": "csv"}, "tags": []}
    )
    items = schema["properties"]["items"]
    assert items["type"] == "array"
    assert items["items"]["properties"]["sku"] == {"type": "string"}
    assert schema["properties"]["meta"]["properties"]["source"] == {"type": "string"}
    # Empty array -> unconstrained items.
    assert schema["properties"]["tags"] == {"type": "array", "items": {}}


def test_infer_schema_excludes_kind_key() -> None:
    schema = infer_schema_from_sample({"__kind": "invoice", "total": 10})
    assert "__kind" not in schema["properties"]
    assert list(schema["properties"]) == ["total"]


def test_infer_schema_rejects_non_object_sample() -> None:
    with pytest.raises(ValueError):
        infer_schema_from_sample([1, 2, 3])


def test_inferred_schema_validates_its_own_sample() -> None:
    sample = {
        "title": "Report",
        "sections": [{"heading": "Intro", "bullets": ["a", "b"]}],
        "score": 4.2,
    }
    schema = infer_schema_from_sample(sample, required_fields=["score"])
    assert validate_against_schema(sample, schema) == []
    # An extra key violates additionalProperties: false.
    assert validate_against_schema({**sample, "extra": 1}, schema) != []
    # A missing required key fails.
    bad = dict(sample)
    bad.pop("score")
    assert validate_against_schema(bad, schema) != []


def test_validate_against_schema_tolerates_the_root_marker() -> None:
    """VALIDATION TOLERANCE, NOT STRIPPING (KINDS_EVERYWHERE_PLAN §4.2).

    The wire schema does not declare `__kind`, so the checker reduces a LOCAL
    copy to run the check — and passes. The caller's value is never touched:
    that is the whole difference between a validator and a stripper.
    """
    schema = infer_schema_from_sample({"total": 10})
    value = {"__kind": "x", "total": 10}
    assert validate_against_schema(value, schema) == []
    assert value == {"__kind": "x", "total": 10}, "the validator MUTATED its input"


def test_ensure_root_marker_stamps_and_corrects_identity() -> None:
    assert ensure_root_marker({"a": 1}, "set") == {"__kind": "set", "a": 1}
    assert ensure_root_marker({"__kind": "wrong", "a": 1}, "set") == {
        "__kind": "set",
        "a": 1,
    }


def test_ensure_root_marker_preserves_nested_markers() -> None:
    value = {"options": [{"__kind": "item", "title": "A"}]}
    assert ensure_root_marker(value, "set") == {"__kind": "set", **value}


# ---------------------------------------------------------------------------
# Props-contract lint — the silent-empty-render hard gate
# ---------------------------------------------------------------------------


def test_component_source_lint_accepts_data_readers() -> None:
    assert (
        component_source_lint("function Card({ data }) { return <div>{data.title}</div>; }") is None
    )
    assert component_source_lint("const C = (props) => <p>{props.data.total}</p>;") is None
    assert (
        component_source_lint("export default function V({ data: wine }) { return null; }") is None
    )


def test_component_source_lint_refuses_flat_props_components() -> None:
    refusal = component_source_lint(
        "function Card(props) { return <div>{props.wine_name} {props.vintage}</div>; }"
    )
    assert refusal is not None
    assert "props.data" in refusal  # the refusal teaches the contract
    assert component_source_lint("") is not None


def test_component_source_lint_refuses_lucide_constructor_shadowing() -> None:
    source = """
        import { Map, MapPin } from "lucide-react";
        export default function Sources({ data }) {
            const byDomain = new Map(data.sources.map((source) => [source.domain, source]));
            return <Map />;
        }
    """
    refusal = component_source_lint(source)
    assert refusal is not None
    assert "Map as MapIcon" in refusal


def test_component_source_lint_accepts_aliased_lucide_constructor_name() -> None:
    source = """
        import { Map as MapIcon, MapPin } from "lucide-react";
        export default function Sources({ data }) {
            const byDomain = new Map(data.sources.map((source) => [source.domain, source]));
            return <MapIcon />;
        }
    """
    assert component_source_lint(source) is None


@pytest.mark.asyncio
async def test_kindcomp_create_component_refuses_flat_props_source() -> None:
    from matrx_ai.tools.implementations.kind_component import kindcomp_create_component

    result = await kindcomp_create_component(
        {
            "kind": "anything",
            "component_key": "card",
            "component_source": "const C = (props) => <div>{props.title}</div>;",
        },
        make_ctx(),
    )
    assert result.success is False
    assert result.error is not None and result.error.error_type == "validation"
    assert "props.data" in result.error.message


@pytest.mark.asyncio
async def test_kindcomp_create_component_replaces_existing_default(monkeypatch) -> None:
    from matrx_ai.tools.implementations import kind_component

    kind_id = uuid4()
    kind = SimpleNamespace(
        id=kind_id,
        kind="recipient_shortlist_result",
        organization_id=uuid4(),
    )
    updates: list[tuple[dict[str, Any], dict[str, Any]]] = []

    async def fake_resolve(_ref: str, _ctx: ToolContext):
        return kind, None

    async def fake_allow(_kind: Any, _ctx: ToolContext):
        return None

    async def fake_source(_source: str):
        return None, True

    class Query:
        async def all(self):
            return []

    class FakeKindComponent:
        @classmethod
        def filter(cls, **_filters):
            return Query()

        @classmethod
        async def update_where(cls, filters, **values):
            updates.append((filters, values))
            return []

        @classmethod
        async def create_item(cls, **payload):
            assert updates == [
                (
                    {
                        "kind_definition_id": str(kind_id),
                        "platform": "web",
                        "role": "output",
                        "is_default": True,
                        "deleted_at": None,
                    },
                    {"is_default": False, "updated_by": "user-1"},
                )
            ]
            return SimpleNamespace(id=uuid4(), semver="1.0.0")

    monkeypatch.setattr(kind_component, "resolve_kind", fake_resolve)
    monkeypatch.setattr(kind_component, "ensure_can_edit_kind", fake_allow)
    monkeypatch.setattr(kind_component, "_refuse_broken_source", fake_source)
    monkeypatch.setattr(kind_component, "get_db_model", lambda _name: FakeKindComponent)
    monkeypatch.setattr(kind_component, "ctx_user_id", lambda _ctx: "user-1")

    result = await kind_component.kindcomp_create_component(
        {
            "kind": kind.kind,
            "component_key": "recipient_shortlist_board",
            "component_source": "export default function C({ data }) { return <p>{data.title}</p>; }",
        },
        make_ctx(),
    )

    assert result.success is True


@pytest.mark.asyncio
async def test_kindcomp_create_component_captures_unexpected_failure(monkeypatch) -> None:
    from matrx_connect.streaming import error_capture

    from matrx_ai.tools.implementations import kind_component

    captured: list[tuple[BaseException, dict[str, object]]] = []
    kind = SimpleNamespace(id=uuid4(), kind="broken_kind", organization_id=uuid4())

    async def fake_sink(exc: BaseException, **fields: object) -> None:
        captured.append((exc, fields))

    async def fake_resolve(_ref: str, _ctx: ToolContext):
        return kind, None

    async def fake_allow(_kind: Any, _ctx: ToolContext):
        return None

    async def fake_source(_source: str):
        return None, True

    class Query:
        async def all(self):
            return []

    class FakeKindComponent:
        @classmethod
        def filter(cls, **_filters):
            return Query()

        @classmethod
        async def update_where(cls, _filters, **_values):
            return []

        @classmethod
        async def create_item(cls, **_payload):
            raise RuntimeError("forced create failure")

    monkeypatch.setattr(error_capture, "_capture_fn", fake_sink)
    monkeypatch.setattr(error_capture, "_allow_in_tests", True)
    monkeypatch.setattr(kind_component, "resolve_kind", fake_resolve)
    monkeypatch.setattr(kind_component, "ensure_can_edit_kind", fake_allow)
    monkeypatch.setattr(kind_component, "_refuse_broken_source", fake_source)
    monkeypatch.setattr(kind_component, "get_db_model", lambda _name: FakeKindComponent)
    monkeypatch.setattr(kind_component, "ctx_user_id", lambda _ctx: "user-1")

    result = await kind_component.kindcomp_create_component(
        {
            "kind": kind.kind,
            "component_key": "board",
            "component_source": "export default function C({ data }) { return <p>{data.title}</p>; }",
        },
        make_ctx(),
    )

    assert result.success is False
    assert len(captured) == 1
    _exc, fields = captured[0]
    assert fields["kind"] == kind_component.KIND_COMPONENT_CREATE_FAILED_KIND
    assert fields["route"] == "kindcomp_create_component"
    assert fields["context"] == {
        "kind": "broken_kind",
        "platform": "web",
        "role": "output",
    }


@pytest.mark.asyncio
async def test_kindcomp_update_code_refuses_flat_props_source() -> None:
    from matrx_ai.tools.implementations.kind_component import kindcomp_update_code

    result = await kindcomp_update_code(
        {
            "component_id": str(uuid4()),
            "updates": {"component_source": "const C = () => <div>static</div>;"},
        },
        make_ctx(),
    )
    assert result.success is False
    assert result.error is not None and result.error.error_type == "validation"
    assert "props.data" in result.error.message


# ---------------------------------------------------------------------------
# Flat schema -> fielded-form conversion (kind_definition.data)
# ---------------------------------------------------------------------------


def test_fields_from_json_schema_flat_conversion() -> None:
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Wine name"},
            "vintage": {"type": "integer"},
            "rating": {"type": "number"},
            "organic": {"type": "boolean", "default": False},
            "style": {"type": "string", "enum": ["red", "white", "rose"]},
            "notes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["name", "vintage"],
        "additionalProperties": False,
    }
    fields = fields_from_json_schema(schema)
    assert fields is not None
    by_name = {f["name"]: f for f in fields}
    assert by_name["name"] == {
        "name": "name",
        "required": True,
        "description": "Wine name",
        "type": "string",
    }
    assert by_name["vintage"]["type"] == "number" and by_name["vintage"]["required"] is True
    assert by_name["rating"]["type"] == "number" and "required" not in by_name["rating"]
    assert by_name["organic"]["type"] == "boolean" and by_name["organic"]["default"] is False
    assert by_name["style"] == {"name": "style", "type": "enum", "values": ["red", "white", "rose"]}
    assert by_name["notes"]["type"] == "string[]"


def test_fields_from_json_schema_declines_nested_shapes_entirely() -> None:
    # Any inexpressible property declines the WHOLE conversion — a partial
    # form would produce schema-invalid payloads.
    nested = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "line_items": {"type": "array", "items": {"type": "object", "properties": {}}},
        },
        "required": ["name", "line_items"],
    }
    assert fields_from_json_schema(nested) is None
    # null-union (nullable) fields also decline
    nullable = {
        "type": "object",
        "properties": {"note": {"type": ["string", "null"]}},
        "required": ["note"],
    }
    assert fields_from_json_schema(nullable) is None
    # non-object roots decline
    assert fields_from_json_schema({"type": "array", "items": {"type": "string"}}) is None


def test_fields_round_trip_validates_same_instances() -> None:
    """The stored fields must describe the same instances as the inferred
    schema: the sample validates under BOTH, required sets match, and a
    payload the inferred schema rejects is also rejected by the
    field-reconstructed schema."""
    sample = {
        "wine_name": "Chateau Test",
        "vintage": 2019,
        "rating": 4.5,
        "organic": True,
        "notes": ["cherry", "oak"],
    }
    inferred = infer_schema_from_sample(sample, required_fields=["wine_name"])
    fields = fields_from_json_schema(inferred)
    assert fields is not None
    reconstructed = json_schema_from_fields(fields)

    assert validate_against_schema(sample, inferred) == []
    assert validate_against_schema(sample, reconstructed) == []
    assert set(reconstructed["required"]) == set(inferred["required"])

    missing_required = {k: v for k, v in sample.items() if k != "wine_name"}
    assert validate_against_schema(missing_required, inferred) != []
    assert validate_against_schema(missing_required, reconstructed) != []


# ---------------------------------------------------------------------------
# Authorization — delegation to the live iam.has_access_for
#
# The gate's design guarantee is: OWNER passes without a DB call; EVERYONE
# ELSE resolves through iam.has_access_for(user, 'content_ir_kind', id, level)
# — the exact SECURITY DEFINER body behind the RLS policies (public / creator
# / internal+org-member / explicit grant / reachability). We therefore pin
# (a) the owner fast-path, (b) verbatim delegation args, (c) that the code
# NEVER short-circuits on org membership (the historical private-kind
# over-grant), and (d) fail-closed on checker errors. The visibility/grant
# matrix itself lives in ONE place — the DB function — by construction.
# ---------------------------------------------------------------------------


def _kind_row(created_by: str | None, organization_id: str) -> Any:
    return SimpleNamespace(
        id=uuid4(),
        kind="secret_private_slug",
        created_by=created_by,
        organization_id=organization_id,
    )


class _AccessRecorder:
    """Monkeypatch stand-in for kind_access_allowed that records delegations
    and answers from a scripted (kind_id, user_id, level) -> bool table."""

    def __init__(self, table: dict[tuple[str, str, str], bool]):
        self.table = table
        self.calls: list[tuple[str, str, str]] = []

    async def __call__(self, kind_id: str, user_id: str, level: str) -> bool:
        self.calls.append((kind_id, user_id, level))
        return self.table.get((kind_id, user_id, level), False)


@pytest.mark.asyncio
async def test_owner_passes_without_db_call(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.tools.implementations import kind_shared

    user = str(uuid4())
    monkeypatch.setattr(kind_shared, "ctx_user_id", lambda _ctx: user)
    recorder = _AccessRecorder({})
    monkeypatch.setattr(kind_shared, "kind_access_allowed", recorder)
    row = _kind_row(user, str(uuid4()))
    assert await can_access_kind(row, make_ctx(), "editor") is True
    assert await can_access_kind(row, make_ctx(), "viewer") is True
    assert recorder.calls == []  # owner never round-trips


@pytest.mark.asyncio
async def test_non_owner_delegates_verbatim_and_org_never_short_circuits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A co-member of the kind's org gets EXACTLY what iam.has_access_for
    says — private kind: denied at editor AND viewer; internal kind (which
    the live function grants to org members): allowed. The code contributes
    no org logic of its own."""
    from matrx_ai.tools.implementations import kind_shared

    user = str(uuid4())
    org = str(uuid4())
    monkeypatch.setattr(kind_shared, "ctx_user_id", lambda _ctx: user)

    private_kind = _kind_row(str(uuid4()), org)  # same org as the caller
    internal_kind = _kind_row(str(uuid4()), org)
    cross_org_kind = _kind_row(str(uuid4()), str(uuid4()))
    recorder = _AccessRecorder(
        {
            # scripted live-function answers: private denies co-members,
            # internal grants viewer+editor to org members, cross-org denies.
            (str(internal_kind.id), user, "viewer"): True,
            (str(internal_kind.id), user, "editor"): True,
        }
    )
    monkeypatch.setattr(kind_shared, "kind_access_allowed", recorder)

    ctx = make_ctx()
    # co-member, private kind: DENIED both levels (the refuted over-grant).
    assert await can_access_kind(private_kind, ctx, "viewer") is False
    assert await can_access_kind(private_kind, ctx, "editor") is False
    # co-member, internal kind: allowed per the live function.
    assert await can_access_kind(internal_kind, ctx, "viewer") is True
    assert await can_access_kind(internal_kind, ctx, "editor") is True
    # cross-org stranger: denied both levels.
    assert await can_access_kind(cross_org_kind, ctx, "viewer") is False
    assert await can_access_kind(cross_org_kind, ctx, "editor") is False
    # every non-owner decision delegated with verbatim args.
    assert (str(private_kind.id), user, "viewer") in recorder.calls
    assert (str(private_kind.id), user, "editor") in recorder.calls
    assert (str(cross_org_kind.id), user, "editor") in recorder.calls


@pytest.mark.asyncio
async def test_no_user_or_checker_error_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations import kind_shared

    monkeypatch.setattr(kind_shared, "ctx_user_id", lambda _ctx: None)
    assert (
        await can_access_kind(_kind_row(str(uuid4()), str(uuid4())), make_ctx(), "viewer") is False
    )

    # checker raising -> kind_access_allowed itself fails closed
    user = str(uuid4())

    async def _boom(*_args: Any, **_kwargs: Any):  # noqa: ANN202
        raise RuntimeError("db down")

    monkeypatch.setattr(kind_shared, "ctx_user_id", lambda _ctx: user)
    monkeypatch.setattr("matrx_orm.call_function", _boom, raising=False)
    assert await kind_shared.kind_access_allowed(str(uuid4()), user, "viewer") is False


def test_kind_entity_token_is_the_registered_token() -> None:
    assert KIND_ENTITY_TOKEN == "content_ir_kind"


# ---------------------------------------------------------------------------
# Read tools are gated: viewer on the bundle, editor on incident payloads
# ---------------------------------------------------------------------------


def _patch_resolve(monkeypatch: pytest.MonkeyPatch, module: Any, row: Any) -> None:
    async def _resolve(_ref: str, _ctx: ToolContext):  # noqa: ANN202
        return row, None

    monkeypatch.setattr(module, "resolve_kind", _resolve)


@pytest.mark.asyncio
async def test_kind_get_denies_non_viewer_content_free(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations import kind_authoring, kind_shared

    user = str(uuid4())
    monkeypatch.setattr(kind_shared, "ctx_user_id", lambda _ctx: user)
    monkeypatch.setattr(kind_shared, "kind_access_allowed", _AccessRecorder({}))
    row = _kind_row(str(uuid4()), str(uuid4()))
    _patch_resolve(monkeypatch, kind_authoring, row)

    result = await kind_authoring.kind_get({"kind": str(row.id)}, make_ctx())
    assert result.success is False
    assert result.error is not None and result.error.error_type == "not_found"
    # content-free: no row attribute (slug or id) is echoed back to a prober.
    assert row.kind not in result.error.message
    assert str(row.id) not in result.error.message


@pytest.mark.asyncio
async def test_kindcomp_get_context_viewer_sees_no_incidents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """viewer-not-editor gets the bundle with the incident section omitted."""
    from matrx_ai.tools.implementations import kind_component, kind_shared

    user = str(uuid4())
    monkeypatch.setattr(kind_shared, "ctx_user_id", lambda _ctx: user)
    row = SimpleNamespace(
        id=uuid4(),
        kind="viewer_kind",
        label="V",
        authoring_owner="python",
        version=1,
        is_active=False,
        visibility="internal",
        organization_id=uuid4(),
        created_by=uuid4(),
        emitted_fingerprint=None,
        emitted_json_schema={"type": "object"},
        metadata={},
        deleted_at=None,
    )
    recorder = _AccessRecorder({(str(row.id), user, "viewer"): True})  # editor: False
    monkeypatch.setattr(kind_shared, "kind_access_allowed", recorder)
    _patch_resolve(monkeypatch, kind_component, row)

    class _EmptyModel:
        @staticmethod
        def filter(**_kw: Any) -> Any:
            class _Q:
                def order_by(self, *_a: Any) -> _Q:
                    return self

                def limit(self, _n: int) -> _Q:
                    return self

                async def all(self) -> list[Any]:
                    return []

            return _Q()

    monkeypatch.setattr(kind_component, "get_db_model", lambda _n: _EmptyModel)

    result = await kind_component.kindcomp_get_context({"kind": str(row.id)}, make_ctx())
    assert result.success is True
    assert result.output.incidents_visible is False
    assert result.output.open_incidents == []
    assert result.output.summary.open_incident_types is None
    # the editor probe actually happened (delegated, not assumed)
    assert (str(row.id), user, "editor") in recorder.calls


# ---------------------------------------------------------------------------
# Arg-contract enforcement + validation-shaped failures (no DB needed)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_kind_create_requires_schema_or_sample() -> None:
    from matrx_ai.tools.implementations.kind_authoring import kind_create

    result = await kind_create({"name": "x", "label": "X"}, make_ctx())
    assert result.success is False
    assert result.error is not None and result.error.error_type == "validation"


@pytest.mark.asyncio
async def test_kind_create_refuses_title_key_missing_from_schema() -> None:
    """title_key (the per-kind instance-title override) must name a schema
    property — a typo would silently produce 'Untitled' instances forever."""
    from matrx_ai.tools.implementations.kind_authoring import kind_create

    result = await kind_create(
        {
            "name": "wine_tasting_t",
            "label": "Wine Tasting",
            "sample_data": {"wine_name": "Opus One", "rating": 95},
            "title_key": "winename",  # typo — not a schema property
        },
        make_ctx(),
    )
    assert result.success is False
    assert result.error is not None and result.error.error_type == "validation"
    assert "title_key" in result.error.message


@pytest.mark.asyncio
async def test_kind_create_rejects_unknown_args() -> None:
    from pydantic import ValidationError

    from matrx_ai.tools.implementations.kind_authoring import kind_create

    with pytest.raises(ValidationError):
        await kind_create({"name": "x", "label": "X", "bogus": 1}, make_ctx())


def test_kind_create_large_echo_is_structurally_omitted() -> None:
    from matrx_ai.tools.implementations.kind_authoring import _bounded_create_echo

    canonical = {"__kind": "large", "body": "x" * 12_000}
    schema = {"type": "object", "description": "y" * 12_000}

    receipt_example, receipt_schema, instruction = _bounded_create_echo(canonical, schema)

    assert receipt_example is None
    assert receipt_schema is None
    assert instruction is not None and "kind_get" in instruction


def test_kind_create_small_echo_remains_structured() -> None:
    from matrx_ai.tools.implementations.kind_authoring import _bounded_create_echo

    canonical = {"__kind": "small", "name": "Example"}
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}

    receipt_example, receipt_schema, instruction = _bounded_create_echo(canonical, schema)

    assert receipt_example == canonical
    assert receipt_schema == schema
    assert instruction is None


@pytest.mark.asyncio
async def test_kindcomp_create_component_validates_enums() -> None:
    from matrx_ai.tools.implementations.kind_component import kindcomp_create_component

    result = await kindcomp_create_component(
        {
            "kind": "whatever",
            "component_key": "k",
            "component_source": "export default () => null",
            "platform": "web",
            "role": "output",
        },
        make_ctx(),
    )
    # Fails at kind resolution (no DB in unit tests) or earlier — never at
    # the enum gate for valid values.
    assert result.success is False

    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        await kindcomp_create_component(
            {
                "kind": "whatever",
                "component_key": "k",
                "component_source": "x",
                "platform": "not-a-platform",
            },
            make_ctx(),
        )


@pytest.mark.asyncio
async def test_kindcomp_patch_code_requires_patch_shape() -> None:
    from matrx_ai.tools.implementations.kind_component import kindcomp_patch_code

    result = await kindcomp_patch_code(
        {"component_id": str(uuid4()), "patches": [{"old_string": "a"}]}, make_ctx()
    )
    assert result.success is False
    assert result.error is not None and result.error.error_type == "validation"
    assert "new_string" in result.error.message


@pytest.mark.asyncio
async def test_kindcomp_patch_code_accepts_find_replace_aliases(monkeypatch) -> None:
    from matrx_ai.tools.implementations import kind_component

    observed = {}

    async def fake_load(component_id, ctx):
        return SimpleNamespace(component_source="before", semver="1.0.0"), object(), None

    def fake_apply(code, old_string, new_string):
        observed.update(old=old_string, new=new_string)
        return code.replace(old_string, new_string), "exact"

    async def fake_refuse(source):
        return None, True

    class FakeKindComponent:
        @classmethod
        async def update_where(cls, filters, **payload):
            return [payload]

        @classmethod
        async def get_or_none(cls, **kwargs):
            return SimpleNamespace(semver="1.0.0", version=2)

    monkeypatch.setattr(kind_component, "_load_editable_component", fake_load)
    monkeypatch.setattr(kind_component, "_apply_patch", fake_apply)
    monkeypatch.setattr(kind_component, "_refuse_broken_source", fake_refuse)
    monkeypatch.setattr(kind_component, "get_db_model", lambda name: FakeKindComponent)
    monkeypatch.setattr(kind_component, "ctx_user_id", lambda ctx: "user-1")

    result = await kind_component.kindcomp_patch_code(
        {
            "component_id": str(uuid4()),
            "patches": [{"find": "before", "replace": "data after"}],
        },
        make_ctx(),
    )

    assert result.success is True
    assert observed == {"old": "before", "new": "data after"}


# ---------------------------------------------------------------------------
# One-shape doctrine + composition (2026-08-22)
# ---------------------------------------------------------------------------


def test_ensure_root_marker_sets_and_corrects_first_key() -> None:
    from matrx_ai.tools.implementations.kind_shared import ensure_root_marker

    out = ensure_root_marker({"a": 1}, "invoice")
    assert list(out) == ["__kind", "a"] and out["__kind"] == "invoice"
    # A wrong existing marker is corrected, nested markers kept verbatim.
    out = ensure_root_marker(
        {"__kind": "wrong", "items": [{"__kind": "line_item", "sku": "A"}]}, "invoice"
    )
    assert out["__kind"] == "invoice"
    assert out["items"][0]["__kind"] == "line_item"


def test_collect_child_kind_fields_objects_lists_and_mixed_refusal() -> None:
    from matrx_ai.tools.implementations.kind_shared import collect_child_kind_fields

    sample = {
        "__kind": "research",
        "primary": "x",
        "summary": {"__kind": "summary_card", "text": "t"},
        "lists": [{"__kind": "keyword_list", "label": "A", "keywords": ["k"]}],
        "plain": [{"no_marker": True}],
    }
    children = collect_child_kind_fields(sample, "research")
    assert children["summary"]["slug"] == "summary_card"
    assert children["summary"]["is_list"] is False
    assert children["lists"]["slug"] == "keyword_list"
    assert children["lists"]["is_list"] is True
    assert "plain" not in children

    with pytest.raises(ValueError):
        collect_child_kind_fields(
            {"items": [{"__kind": "a"}, {"__kind": "b"}]}, "research"
        )


def test_block_schema_injection_validates_marked_example() -> None:
    """The BLOCK schema declares __kind at the root and at every nested marked
    position, so the marked canonical example validates as stored — the
    one-shape doctrine's round trip."""
    from matrx_ai.tools.implementations.kind_shared import (
        ensure_root_marker,
        infer_schema_from_sample,
        inject_kind_markers_into_schema,
    )

    marked = ensure_root_marker(
        {
            "primary_keyword": "x",
            "keyword_lists": [
                {"__kind": "keyword_list", "label": "Parents", "keywords": ["a"]}
            ],
        },
        "keyword_relationship_research",
    )
    wire = infer_schema_from_sample(marked)
    assert "__kind" not in wire["properties"]
    block = inject_kind_markers_into_schema(wire, marked, "keyword_relationship_research")
    assert block["properties"]["__kind"] == {"const": "keyword_relationship_research"}
    nested = block["properties"]["keyword_lists"]["items"]["properties"]["__kind"]
    assert nested == {"const": "keyword_list"}
    # Marked example validates against the block schema…
    assert validate_against_schema(marked, block) == []
    # …and the same marked value validates against the marker-tolerant wire
    # schema; callers never create a second stripped artifact.
    assert validate_against_schema(marked, wire) == []


def test_component_import_lint_allows_and_refuses() -> None:
    from matrx_ai.tools.implementations.kind_shared import component_import_lint

    good = (
        'import { useState } from "react";\n'
        'import { Star } from "lucide-react";\n'
        'import { Card } from "@/components/ui/card";\n'
        'import { CopyButtons } from "@/components/agent-copy/CopyButtons";\n'
        "export default function C({ data }) { return null; }"
    )
    assert component_import_lint(good) is None
    bad = 'import axios from "axios";\nexport default function C({ data }) { return null; }'
    refusal = component_import_lint(bad)
    assert refusal is not None and "axios" in refusal


@pytest.mark.asyncio
async def test_tsx_compile_check_flags_syntax_errors_when_esbuild_present() -> None:
    import shutil as _shutil

    from matrx_ai.tools.implementations.kind_shared import tsx_compile_check

    if not _shutil.which("esbuild"):
        errors, checked = await tsx_compile_check("const x = <div>ok</div>;")
        assert checked is False and errors == []
        pytest.skip("esbuild not installed on this host")
    ok_errors, ok_checked = await tsx_compile_check(
        "export default function C({ data }: any) { return <div>{data?.x}</div>; }"
    )
    assert ok_checked is True and ok_errors == []
    bad_errors, bad_checked = await tsx_compile_check(
        "export default function C({ data }) { return <div>{data.x</div>; }"
    )
    assert bad_checked is True and bad_errors


def test_infer_schema_merges_heterogeneous_list_items() -> None:
    """Real samples carry nullable and optional fields across list items; a
    first-element-only inference rejected the kind's own example."""
    sample = {
        "books": [
            {"title": "A", "rating": 5},
            {"title": "B", "rating": None, "note": "optional key"},
        ]
    }
    schema = infer_schema_from_sample(sample)
    items = schema["properties"]["books"]["items"]
    assert set(items["properties"]) == {"title", "rating", "note"}
    assert set(items["properties"]["rating"]["type"]) == {"integer", "null"}
    assert validate_against_schema(sample, schema) == []
    # A key that was only ever null stays permissive.
    only_null = infer_schema_from_sample({"x": None})
    assert "null" in only_null["properties"]["x"]["type"] and "string" in only_null["properties"]["x"]["type"]


# ---------------------------------------------------------------------------
# B6 — the platform_kind mint path (admin → system-org/public on EVERY row;
# default keeps caller-org/internal; non-admin + true refuses loudly)
# ---------------------------------------------------------------------------

CALLER_ORG = str(uuid4())
CALLER_USER = str(uuid4())


class _FakeQuery:
    def __init__(self, rows: list[Any]):
        self._rows = rows

    def limit(self, _n: int) -> "_FakeQuery":
        return self

    async def all(self) -> list[Any]:
        return self._rows


def _install_fake_kind_db(monkeypatch: pytest.MonkeyPatch) -> dict[str, list[dict[str, Any]]]:
    """Fake the four models kind_create's composed write touches, recording
    every create_item payload by table so tests can assert org/visibility on
    EVERY row type the tool writes."""
    created: dict[str, list[dict[str, Any]]] = {
        "kind_definition": [],
        "kind_example": [],
        "kind_component": [],
        "kind_edge": [],
    }
    examples_by_id: dict[str, Any] = {}

    class KindDefinition:
        _database = object()

        @classmethod
        def filter(cls, **_kw: Any) -> _FakeQuery:
            return _FakeQuery([])  # no collisions, no duplicates in this harness

        @classmethod
        async def create_item(cls, **payload: Any) -> Any:
            created["kind_definition"].append(payload)
            return SimpleNamespace(id=uuid4(), version=1, deleted_at=None, **payload)

    class KindExample:
        @classmethod
        async def create_item(cls, **payload: Any) -> Any:
            created["kind_example"].append(payload)
            row = SimpleNamespace(id=uuid4(), validation_status="passed", **payload)
            examples_by_id[str(row.id)] = row
            return row

        @classmethod
        async def get_or_none(cls, **kw: Any) -> Any:
            return examples_by_id.get(str(kw.get("id")))

    class KindComponent:
        @classmethod
        async def create_item(cls, **payload: Any) -> Any:
            created["kind_component"].append(payload)
            return SimpleNamespace(id=uuid4(), **payload)

    class KindEdge:
        @classmethod
        async def create_item(cls, **payload: Any) -> Any:
            created["kind_edge"].append(payload)
            return SimpleNamespace(id=uuid4(), **payload)

    models = {
        "KindDefinition": KindDefinition,
        "KindExample": KindExample,
        "KindComponent": KindComponent,
        "KindEdge": KindEdge,
    }

    from matrx_ai.tools.implementations import kind_authoring, kind_shared

    def fake_get_db_model(key: str) -> Any:
        return models[key]

    monkeypatch.setattr(kind_authoring, "get_db_model", fake_get_db_model)
    monkeypatch.setattr(kind_shared, "get_db_model", fake_get_db_model)
    monkeypatch.setattr(kind_authoring, "ctx_user_id", lambda _ctx: CALLER_USER)
    monkeypatch.setattr(kind_authoring, "ctx_org_id", lambda _ctx: CALLER_ORG)
    return created


def _composed_args(**extra: Any) -> dict[str, Any]:
    """A root kind with one marked child list — exercises definition, child
    definition, examples, seeded input components, and the kind_edge row."""
    return {
        "name": "b6_platform_root",
        "label": "B6 Platform Root",
        "sample_data": {
            "title": "Deck",
            "cards": [{"__kind": "b6_platform_card", "front": "Q", "back": "A"}],
        },
        **extra,
    }


def _all_created_rows(created: dict[str, list[dict[str, Any]]]) -> list[tuple[str, dict[str, Any]]]:
    return [(table, row) for table, rows in created.items() for row in rows]


@pytest.mark.asyncio
async def test_kind_create_default_stays_caller_org_internal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No platform_kind → exactly today's behavior, even for an admin: caller
    org on every row, visibility='internal' on the definitions."""
    from matrx_ai.tools.implementations import kind_authoring

    created = _install_fake_kind_db(monkeypatch)
    monkeypatch.setattr(kind_authoring, "ctx_is_admin", lambda _ctx: True)

    result = await kind_authoring.kind_create(_composed_args(), make_ctx())
    assert result.success, result.error
    assert result.output_self_capped is True
    assert result.output.platform_kind is False
    assert result.output.visibility == "internal"

    rows = _all_created_rows(created)
    assert {t for t, _ in rows} == {
        "kind_definition", "kind_example", "kind_component", "kind_edge",
    }
    assert len(created["kind_definition"]) == 2  # root + minted child
    for _table, row in rows:
        assert str(row["organization_id"]) == CALLER_ORG
    for defn in created["kind_definition"]:
        assert defn["visibility"] == "internal"
        assert defn["created_by"] == CALLER_USER


@pytest.mark.asyncio
async def test_kind_create_large_receipt_stays_below_result_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations import kind_authoring
    from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS

    _install_fake_kind_db(monkeypatch)
    monkeypatch.setattr(kind_authoring, "ctx_is_admin", lambda _ctx: True)

    result = await kind_authoring.kind_create(
        {
            "name": "large_receipt",
            "label": "Large Receipt",
            "sample_data": {"body": "x" * 40_000},
        },
        make_ctx(),
    )

    assert result.success, result.error
    assert result.output_self_capped is True
    assert result.output.canonical_example is None
    assert result.output.json_schema is None
    assert result.output.retrieval_instruction is not None
    assert len(result.output.model_dump_json()) < TOOL_RESULT_SOFT_CAP_CHARS


@pytest.mark.asyncio
async def test_kind_create_platform_kind_admin_stamps_system_org_public_everywhere(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations import kind_authoring
    from matrx_ai.tools.implementations.kind_shared import system_organization_id

    created = _install_fake_kind_db(monkeypatch)
    monkeypatch.setattr(kind_authoring, "ctx_is_admin", lambda _ctx: True)

    result = await kind_authoring.kind_create(
        _composed_args(platform_kind=True), make_ctx()
    )
    assert result.success, result.error
    system_org = system_organization_id()
    assert result.output.platform_kind is True
    assert result.output.visibility == "public"
    assert result.output.organization_id == system_org

    rows = _all_created_rows(created)
    # Every row type of the composed create: root + child definitions, both
    # canonical examples, both seeded input components, and the edge.
    assert len(created["kind_definition"]) == 2
    assert len(created["kind_example"]) == 2
    assert len(created["kind_component"]) == 2
    assert len(created["kind_edge"]) == 1
    for _table, row in rows:
        assert str(row["organization_id"]) == system_org
    for defn in created["kind_definition"]:
        assert defn["visibility"] == "public"
        # Attribution stays honest — the admin caller, never a fabricated user.
        assert defn["created_by"] == CALLER_USER


@pytest.mark.asyncio
async def test_kind_create_platform_kind_refused_for_non_admin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations import kind_authoring

    created = _install_fake_kind_db(monkeypatch)
    monkeypatch.setattr(kind_authoring, "ctx_is_admin", lambda _ctx: False)

    result = await kind_authoring.kind_create(
        _composed_args(platform_kind=True), make_ctx()
    )
    assert not result.success
    assert result.error.error_type == "forbidden"
    assert "admin-only" in result.error.message
    # Refusal is loud AND clean: nothing was written anywhere.
    assert _all_created_rows(created) == []


def test_ctx_is_admin_fails_closed_without_context() -> None:
    from matrx_ai.tools.implementations.kind_shared import ctx_is_admin

    assert ctx_is_admin(make_ctx()) is False


def test_kind_create_args_declare_platform_kind_default_false() -> None:
    """The declared arg contract carries the param with default false, so the
    registered tool schema (model_json_schema) and dispatch validation both
    know it."""
    from matrx_ai.tools._generated_declarations import KindCreateArgs

    field = KindCreateArgs.model_fields["platform_kind"]
    assert field.default is False
    assert KindCreateArgs.model_validate({"name": "x", "label": "X"}).platform_kind is False


# ---------------------------------------------------------------------------
# kind_create_content_block — visibility enum serialization (feedback 194575e6)
# ---------------------------------------------------------------------------
# KindDefinition.visibility hydrates as a (str, Enum) member of content_ir's
# Visibility class; RenderDefinition validates against skill's own Visibility
# class. Serializing with str(member) yields the repr 'Visibility.INTERNAL',
# which every wave-4 content-block write died on. The row must carry the plain
# value ('internal' / 'public').


def _install_fake_content_block_db(
    monkeypatch: pytest.MonkeyPatch, kd: Any
) -> dict[str, list[dict[str, Any]]]:
    from enum import Enum

    from matrx_ai.tools.implementations import kind_authoring

    created: dict[str, list[dict[str, Any]]] = {"render_definition": []}

    class SkillVisibility(str, Enum):
        PERSONAL = "personal"
        INTERNAL = "internal"
        LINK = "link"
        PUBLIC = "public"

    class KindExample:
        @classmethod
        def filter(cls, **_kw: Any) -> _FakeQuery:
            return _FakeQuery(
                [SimpleNamespace(deleted_at=None, is_canonical=True, data={"score": 1})]
            )

    class RenderDefinition:
        @classmethod
        def filter(cls, **_kw: Any) -> _FakeQuery:
            return _FakeQuery([])

        @classmethod
        async def create_item(cls, **payload: Any) -> Any:
            # Enforce the real model's contract: the visibility payload must be
            # a valid value of skill's OWN Visibility enum. The repr string
            # 'Visibility.INTERNAL' raises exactly like the live EnumField did.
            SkillVisibility(payload["visibility"])
            created["render_definition"].append(payload)
            return SimpleNamespace(id=uuid4(), **payload)

    class SklDefinition:
        @classmethod
        def filter(cls, **_kw: Any) -> _FakeQuery:
            return _FakeQuery([])

    models = {
        "KindExample": KindExample,
        "RenderDefinition": RenderDefinition,
        "SklDefinition": SklDefinition,
    }
    monkeypatch.setattr(kind_authoring, "get_db_model", lambda key: models[key])

    async def fake_resolve_kind(_ref: str, _ctx: Any) -> tuple[Any, None]:
        return kd, None

    async def fake_ensure_can_edit(_kd: Any, _ctx: Any) -> None:
        return None

    async def fake_category_id() -> str:
        return str(uuid4())

    monkeypatch.setattr(kind_authoring, "resolve_kind", fake_resolve_kind)
    monkeypatch.setattr(kind_authoring, "ensure_can_edit_kind", fake_ensure_can_edit)
    monkeypatch.setattr(kind_authoring, "_content_block_category_id", fake_category_id)
    monkeypatch.setattr(kind_authoring, "ctx_user_id", lambda _ctx: CALLER_USER)
    return created


def _kd_with_enum_visibility(visibility: Any) -> Any:
    return SimpleNamespace(
        id=uuid4(),
        kind="research_coverage_audit",
        label="Research Coverage Audit",
        organization_id=uuid4(),
        visibility=visibility,
    )


@pytest.mark.parametrize("value", ["internal", "public"])
@pytest.mark.asyncio
async def test_content_block_serializes_visibility_enum_by_value(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    from enum import Enum

    from matrx_ai.tools.implementations import kind_authoring

    class KdVisibility(str, Enum):  # content_ir's own class — NOT skill's
        INTERNAL = "internal"
        PUBLIC = "public"

    kd = _kd_with_enum_visibility(KdVisibility(value))
    created = _install_fake_content_block_db(monkeypatch, kd)

    result = await kind_authoring.kind_create_content_block(
        {"kind": "research_coverage_audit"}, make_ctx()
    )
    assert result.success, result.error and result.error.message
    [row] = created["render_definition"]
    assert row["visibility"] == value  # plain value, never 'Visibility.INTERNAL'


@pytest.mark.asyncio
async def test_content_block_visibility_defaults_internal_when_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations import kind_authoring

    kd = _kd_with_enum_visibility(None)
    created = _install_fake_content_block_db(monkeypatch, kd)

    result = await kind_authoring.kind_create_content_block(
        {"kind": "research_coverage_audit"}, make_ctx()
    )
    assert result.success, result.error and result.error.message
    [row] = created["render_definition"]
    assert row["visibility"] == "internal"
