"""Tests for the per-action (dispatcher) tool-drift validation path.

Covers GAP 1 of common-docs/systems/agents/agent-tools/STATE.md: multi-action tools register a
discriminated ``RootModel`` union (so the executor validates the real per-action
contract) and the DB row carries a ``$variants`` map, and the engine diffs the
two per action. Also locks the registration shape (RootModel.model_validate
dispatches and errors cleanly) and the back-compat of the flat path.
"""

from __future__ import annotations

from typing import Annotated, Literal

import pytest
from pydantic import Field, RootModel

from matrx_ai.tools.declared import DeclaredFamily, DeclaredTool, NoArgs, ToolArgs
from matrx_ai.tools.models import ToolDefinition
from matrx_ai.tools.validation.engine import validate
from matrx_ai.tools.validation.runner import find_unverified_tools
from matrx_ai.tools.validation.schema import (
    canon_db_params,
    canon_db_variants,
    db_discriminator_enum,
    discriminated_union_members,
)


# ── sample per-action wire models + union (mirrors the real `web` shape) ─────
class _SearchWire(ToolArgs):
    action: Literal["search"]
    queries: list[str]
    freshness: str | None = None
    max_results_per_query: int = 5


class _ReadWire(ToolArgs):
    action: Literal["read"]
    url: str
    summarize: bool = False
    max_content_length: int = 50000


class _WebArgs(RootModel[Annotated[_SearchWire | _ReadWire, Field(discriminator="action")]]):
    pass


class _FlatArgs(ToolArgs):
    path: str
    limit: int = 10


def _decl(name, model, func=None, *, source_kind="native", executor=None):
    def _default(args, ctx):  # pragma: no cover - placeholder body
        return None

    return DeclaredTool(
        name=name,
        source_kind=source_kind,
        args_model=model,
        func=func or _default,
        module="tests.fake",
        qualname=name,
        executor=executor,
        validate=True,
        deprecated=False,
    )


def _web_db_row(variants=None, action_enum=("search", "read")):
    if variants is None:
        variants = {
            "search": {
                "queries": {"type": "array", "required": True},
                "freshness": {"type": "string"},
                "max_results_per_query": {"type": "integer", "default": 5},
            },
            "read": {
                "url": {"type": "string", "required": True},
                "summarize": {"type": "boolean", "default": False},
                "max_content_length": {"type": "integer", "default": 50000},
            },
        }
    return {
        "name": "web",
        "source_kind": "native",
        "function_path": "tests.fake.web",
        "description": "",
        "is_active": True,
        "validation_exempt": False,
        "executors": [],
        "parameters": {
            "action": {"type": "string", "enum": list(action_enum), "required": True},
            # Legacy flat union — present in prod, ignored by the dispatcher path.
            "queries": {"type": "array"},
            "url": {"type": "string"},
            "freshness": {"type": "string"},
            "summarize": {"type": "boolean", "default": False},
            "max_results_per_query": {"type": "integer", "default": 5},
            "max_content_length": {"type": "integer", "default": 50000},
            "$variants": variants,
        },
    }


# ── schema helpers ──────────────────────────────────────────────────────────
def test_union_member_introspection():
    res = discriminated_union_members(_WebArgs)
    assert res is not None
    disc, members = res
    assert disc == "action"
    assert set(members) == {"search", "read"}
    assert members["search"] is _SearchWire


def test_plain_and_noargs_not_union():
    assert discriminated_union_members(_FlatArgs) is None
    assert discriminated_union_members(NoArgs) is None
    assert discriminated_union_members(int) is None


def test_canon_db_params_skips_dollar_keys():
    canon = canon_db_params(_web_db_row()["parameters"])
    assert "$variants" not in canon
    assert "action" in canon and "queries" in canon


def test_canon_db_variants_and_enum():
    params = _web_db_row()["parameters"]
    variants = canon_db_variants(params)
    assert set(variants) == {"search", "read"}
    assert variants["search"]["queries"].required is True
    assert variants["read"]["summarize"].has_default is True
    assert db_discriminator_enum(params, "action") == {"search", "read"}


def test_canon_db_variants_none_without_key():
    assert canon_db_variants({"path": {"type": "string"}}) is None


# ── engine: per-action diffing ──────────────────────────────────────────────
def test_dispatcher_match_no_drift():
    report = validate(
        {"web": _decl("web", _WebArgs)}, [_web_db_row()], owner_executors={"matrx-ai-core"}
    )
    assert report.ok, [f.message for f in report.findings]


def test_dispatcher_action_set_mismatch():
    one_variant = {
        "search": {
            "queries": {"type": "array", "required": True},
            "freshness": {"type": "string"},
            "max_results_per_query": {"type": "integer", "default": 5},
        }
    }
    report = validate(
        {"web": _decl("web", _WebArgs)},
        [_web_db_row(variants=one_variant, action_enum=("search",))],
        owner_executors={"matrx-ai-core"},
    )
    assert not report.ok
    assert "action set differs" in " ".join(f.message for f in report.findings)


def test_dispatcher_per_variant_param_drift():
    # search.queries optional in DB, required in code -> per-variant drift.
    variants = {
        "search": {
            "queries": {"type": "array"},
            "freshness": {"type": "string"},
            "max_results_per_query": {"type": "integer", "default": 5},
        },
        "read": {
            "url": {"type": "string", "required": True},
            "summarize": {"type": "boolean", "default": False},
            "max_content_length": {"type": "integer", "default": 50000},
        },
    }
    report = validate(
        {"web": _decl("web", _WebArgs)},
        [_web_db_row(variants=variants)],
        owner_executors={"matrx-ai-core"},
    )
    msgs = " ".join(f.message for f in report.findings)
    assert not report.ok
    assert "[search]" in msgs and "queries" in msgs


def test_dispatcher_discriminator_enum_mismatch():
    # $variants match (search, read) but the top-level action.enum has an extra.
    report = validate(
        {"web": _decl("web", _WebArgs)},
        [_web_db_row(action_enum=("search", "read", "crawl"))],
        owner_executors={"matrx-ai-core"},
    )
    msgs = " ".join(f.message for f in report.findings)
    assert "discriminator 'action' enum differs" in msgs


def test_union_without_variants_is_drift():
    row = _web_db_row()
    del row["parameters"]["$variants"]
    report = validate({"web": _decl("web", _WebArgs)}, [row], owner_executors={"matrx-ai-core"})
    assert "no $variants" in " ".join(f.message for f in report.findings)


def test_variants_without_union_is_drift():
    report = validate(
        {"web": _decl("web", _FlatArgs)}, [_web_db_row()], owner_executors={"matrx-ai-core"}
    )
    assert "not a discriminated RootModel union" in " ".join(f.message for f in report.findings)


def test_flat_tool_backcompat():
    row = {
        "name": "fs_read",
        "source_kind": "native",
        "function_path": "tests.fake.fs_read",
        "description": "",
        "is_active": True,
        "validation_exempt": False,
        "executors": [],
        "parameters": {
            "path": {"type": "string", "required": True},
            "limit": {"type": "integer", "default": 10},
        },
    }
    report = validate(
        {"fs_read": _decl("fs_read", _FlatArgs)}, [row], owner_executors={"matrx-ai-core"}
    )
    assert report.ok, [f.message for f in report.findings]


def test_provider_schema_is_derived_from_dispatcher_variants():
    tool = ToolDefinition(
        name="sql",
        parameters={
            "action": {
                "type": "string",
                "enum": ["query", "insert", "schema"],
                "required": True,
            },
            "query": {
                "type": "string",
                "description": "Stale free-form SQL field that must never reach a provider.",
            },
            "table": {"type": "string"},
            "$variants": {
                "query": {
                    "table": {"type": "string", "required": True},
                    "match": {"type": "object", "default": {}},
                    "fields": {"type": "array", "default": ["*"]},
                    "order_by": {"type": "array", "default": []},
                    "limit": {"type": "integer", "default": 100},
                    "offset": {"type": "integer", "default": 0},
                },
                "insert": {
                    "table": {"type": "string", "required": True},
                    "data": {"type": "object", "required": True},
                },
                "schema": {
                    "table": {"type": "string", "default": ""},
                },
            },
        },
    )

    schema = tool._build_json_schema()

    assert "query" not in schema["properties"]
    assert {
        "action",
        "table",
        "match",
        "fields",
        "order_by",
        "limit",
        "offset",
        "data",
    } == set(schema["properties"])
    assert schema["required"] == ["action"]


# ── registration shape (locks the executor contract) ────────────────────────
def test_rootmodel_validate_dispatches_and_errors():
    ok = _WebArgs.model_validate({"action": "search", "queries": ["x"]})
    assert isinstance(ok.root, _SearchWire)

    with pytest.raises(Exception) as bad_tag:
        _WebArgs.model_validate({"action": "crawl", "queries": ["x"]})
    assert "action" in str(bad_tag.value).lower()

    with pytest.raises(Exception):  # extra key rejected inside the variant
        _WebArgs.model_validate({"action": "search", "queries": ["x"], "bogus": 1})


# ── generic tool families (one handler, N data-driven rows) ─────────────────
def _bundle_family():
    def _list(args, ctx):  # pragma: no cover - placeholder body
        return None

    return DeclaredFamily(
        name_prefix="bundle:list_",
        source_kind="native",
        args_model=NoArgs,
        func=_list,
        module="tests.fake",
        qualname="list_bundle_tools",
        executor="matrx-ai-core",
        validate=True,
        deprecated=False,
    )


def _bundle_db_row(name, parameters=None):
    return {
        "name": name,
        "source_kind": "native",
        "description": "",
        "is_active": True,
        "validation_exempt": False,
        "executors": ["matrx-ai-core"],
        "parameters": parameters or {},
    }


def test_family_covers_data_only_member():
    # An owned tool_def row that exists ONLY as data (no per-member @tool) is
    # covered by the family — NOT flagged missing_in_code. This is the whole point:
    # a DB row must work without a hand-written code declaration.
    report = validate(
        {},
        [_bundle_db_row("bundle:list_agent-core")],
        owner_executors={"matrx-ai-core"},
        families=[_bundle_family()],
    )
    assert report.ok, [f.message for f in report.findings]
    assert "bundle:list_agent-core" in report.checked


def test_without_family_member_is_missing_in_code():
    # Remove the family → the same row is correctly flagged. Proves the family
    # is what provides coverage, not a blanket name-prefix exemption.
    report = validate(
        {},
        [_bundle_db_row("bundle:list_agent-core")],
        owner_executors={"matrx-ai-core"},
    )
    assert not report.ok
    assert any(
        f.kind.value == "missing_in_code" and f.tool_name == "bundle:list_agent-core"
        for f in report.findings
    )


def test_family_member_args_are_actually_checked():
    # A family member is verified against the family's contract (NoArgs), not
    # blindly silenced — a DB row that carries parameters is real arg drift.
    report = validate(
        {},
        [_bundle_db_row("bundle:list_x", parameters={"foo": {"type": "string"}})],
        owner_executors={"matrx-ai-core"},
        families=[_bundle_family()],
    )
    assert not report.ok
    assert any(f.kind.value == "arg_drift" for f in report.findings)


# ── unverified detection is union-aware ─────────────────────────────────────
def test_find_unverified_union_aware():
    def web_bound(args, ctx):
        return _WebArgs.model_validate(args).root  # references the RootModel

    def web_unbound(args, ctx):
        return args.get("action")

    # Ownership is filtered by executor binding (not source_kind), so the
    # declared tool must carry an executor that THIS repo owns to be checked.
    assert (
        find_unverified_tools(
            {"web": _decl("web", _WebArgs, func=web_bound, executor="matrx-ai-core")},
            {"matrx-ai-core"},
        )
        == []
    )
    flagged = find_unverified_tools(
        {"web": _decl("web", _WebArgs, func=web_unbound, executor="matrx-ai-core")},
        {"matrx-ai-core"},
    )
    assert [f["tool_name"] for f in flagged] == ["web"]


class _WrappedArgs(ToolArgs):
    value: str


def _wrapped_impl(args, ctx):
    return _WrappedArgs.model_validate(args).value


def _wrapped_tool(args, ctx):
    return _wrapped_impl(args, ctx)


def _still_unbound_wrapper(args, ctx):
    return args.get("value")


def test_find_unverified_follows_only_executed_local_helpers():
    assert (
        find_unverified_tools(
            {
                "wrapped": _decl(
                    "wrapped", _WrappedArgs, func=_wrapped_tool, executor="matrx-ai-core"
                )
            },
            {"matrx-ai-core"},
        )
        == []
    )

    flagged = find_unverified_tools(
        {
            "unbound": _decl(
                "unbound", _WrappedArgs, func=_still_unbound_wrapper, executor="matrx-ai-core"
            )
        },
        {"matrx-ai-core"},
    )
    assert [finding["tool_name"] for finding in flagged] == ["unbound"]
