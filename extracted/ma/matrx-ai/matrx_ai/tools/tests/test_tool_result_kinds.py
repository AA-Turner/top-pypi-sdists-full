"""A tool's RESULT kind is the one its payload declares.

The tools family sweep (KINDS_EVERYWHERE_PLAN §10d-C, OWNER_BRIEF rollout R8)
turns on one seam in ``executor.execute``, and these tests pin its selection
rule — the part that has to be right for all 279 tools:

* the CURATED kind is the payload's own ``__kind``, exactly as everywhere else
  in the platform (discriminator-as-data);
* the GENERATED contract (``tool_io_<name>_<digest>_output``, derived from the
  row's hand-written ``output_schema``) is an ABI fingerprint for drift, and it
  must NOT win the identity when the payload declared one;
* ``json`` is a format word and is never adopted as an identity — the same
  refusal the workflow scheduler makes when propagating a payload's kind;
* a payload that declares nothing changes nothing.

These run the REAL dispatch path against the real executor. They deliberately
do NOT assert ``output_kind_checked``: validation resolves the live kind
catalog, and a test that stubbed the catalog would be asserting its own
fixture. Whether the check RAN is catalog truth; which slug is the result's
IDENTITY is this seam's truth, and that is what is pinned here.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.lifecycle import ToolLifecycleManager
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry

_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {"bundle": {"type": "string"}},
}


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


#: What the tool under test returns; each test sets this before dispatch.
_PAYLOAD: Any = {}


async def _fixture_tool(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    output = dict(_PAYLOAD) if isinstance(_PAYLOAD, dict) else _PAYLOAD
    return ToolResult(success=True, output=output, tool_name="kindful", call_id=ctx.call_id)


async def _failed_fixture_tool(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error={"error_type": "validation", "message": "expected refusal"},
        tool_name="kindful",
        call_id=ctx.call_id,
    )


@pytest.fixture
def isolated_registry():
    registry = ToolRegistry.get_instance()
    saved = dict(registry._tools)
    yield registry
    registry._tools = saved


@pytest.fixture
def executor(isolated_registry):
    return ToolExecutor(
        registry=isolated_registry,
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )


@pytest.fixture
def app_ctx_set():
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    ctx = AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True)
    token = set_app_context(ctx)
    yield ctx
    clear_app_context(token)


@pytest.fixture
def kindful_tool(isolated_registry):
    td = ToolDefinition(
        name="kindful",
        description="fixture tool for the result-kind seam",
        parameters={},
        output_schema=dict(_OUTPUT_SCHEMA),
        tool_type=ToolType.LOCAL,
        function_path=f"{__name__}._fixture_tool",
        source_kind="native",
    )
    td._callable = _fixture_tool
    isolated_registry._tools["kindful"] = td
    return td


async def _run(executor: ToolExecutor, payload: Any) -> ToolResult:
    global _PAYLOAD
    _PAYLOAD = payload
    ctx = ToolContext(call_id="call-kind-test", tool_name="kindful")
    _content, result = await executor.execute("kindful", {}, ctx)
    return result


class TestResultKindSelection:
    async def test_payload_kind_beats_the_generated_contract(
        self, executor, kindful_tool, app_ctx_set
    ) -> None:
        """The whole point of the sweep: identity comes from the data."""
        result = await _run(executor, {"__kind": "tool_bundle_listing", "bundle": "supabase"})

        assert result.success is True
        assert result.output_kind == "tool_bundle_listing"
        # The tool row HAS an output_schema, so a generated contract exists and
        # would have claimed output_kind before this seam. It must not now.
        assert not result.output_kind.startswith("tool_io_")

    async def test_json_is_never_adopted_as_an_identity(
        self, executor, kindful_tool, app_ctx_set
    ) -> None:
        """'json' is a format word. Adopting it would make every anonymous
        payload look declared — the exact lie the sweep exists to remove."""
        result = await _run(executor, {"__kind": "json", "bundle": "supabase"})

        assert result.output_kind is not None
        assert result.output_kind.startswith("tool_io_"), (
            "a payload calling itself 'json' must fall through to the generated "
            f"contract, not be adopted as a kind (got {result.output_kind!r})"
        )

    async def test_undeclared_payload_leaves_the_contract_in_charge(
        self, executor, kindful_tool, app_ctx_set
    ) -> None:
        """The untouched path: 208 tools still return anonymous dicts, and
        their behaviour must be exactly what it was."""
        result = await _run(executor, {"bundle": "supabase"})

        assert result.output_kind is not None
        assert result.output_kind.startswith("tool_io_")
        assert result.output_kind_checked is True
        assert result.output_kind_errors == []


class TestDeclarationEnforcement:
    """The RECONCILED measure (§10g GAP 3) has a runtime half that can rot.

    ``TOOL_RESULT_KINDS`` is what the coverage board reads and what
    ``scripts/backfill_tool_output_schemas.py`` derives the stored
    ``output_schema`` from. If a declared tool's implementation quietly stops
    returning its KindModel — a branch nobody converted, an error path building
    a plain dict — the stored schema becomes a promise nothing keeps, and the
    board would keep reporting the tool as covered. The executor screams.
    """

    async def test_a_declared_tool_that_stops_returning_its_kind_screams(
        self, executor, isolated_registry, app_ctx_set, caplog
    ) -> None:
        from matrx_ai.tools.kinds import TOOL_RESULT_KINDS
        from matrx_ai.tools.kinds.tooling import ToolBundleListing

        TOOL_RESULT_KINDS["kindful"] = ToolBundleListing
        try:
            td = ToolDefinition(
                name="kindful",
                description="fixture tool for the result-kind seam",
                parameters={},
                output_schema=ToolBundleListing.model_json_schema(),
                tool_type=ToolType.LOCAL,
                function_path=f"{__name__}._fixture_tool",
                source_kind="native",
            )
            td._callable = _fixture_tool
            isolated_registry._tools["kindful"] = td

            with caplog.at_level("ERROR"):
                result = await _run(executor, {"bundle": "supabase", "count": 1})
        finally:
            TOOL_RESULT_KINDS.pop("kindful", None)

        # Loud, not fatal — the same posture as every other kind check.
        assert result.success is True
        assert any(
            "DECLARED tool result kind missing" in rec.getMessage() for rec in caplog.records
        ), "a declared tool returning a bare dict must scream"
        assert any("not carried by the payload" in e for e in result.output_kind_errors)

    async def test_a_declared_tool_that_keeps_its_promise_is_silent(
        self, executor, isolated_registry, app_ctx_set, caplog
    ) -> None:
        from matrx_ai.tools.kinds import TOOL_RESULT_KINDS
        from matrx_ai.tools.kinds.tooling import ToolBundleListing

        TOOL_RESULT_KINDS["kindful"] = ToolBundleListing
        try:
            td = ToolDefinition(
                name="kindful",
                description="fixture tool for the result-kind seam",
                parameters={},
                output_schema=ToolBundleListing.model_json_schema(),
                tool_type=ToolType.LOCAL,
                function_path=f"{__name__}._fixture_tool",
                source_kind="native",
            )
            td._callable = _fixture_tool
            isolated_registry._tools["kindful"] = td

            with caplog.at_level("ERROR"):
                result = await _run(
                    executor,
                    ToolBundleListing(bundle="supabase", count=1).model_dump(mode="json"),
                )
        finally:
            TOOL_RESULT_KINDS.pop("kindful", None)

        assert result.output_kind == "tool_bundle_listing"
        assert not any(
            "DECLARED tool result kind missing" in rec.getMessage() for rec in caplog.records
        )

    async def test_a_declared_tool_failure_does_not_validate_success_payload(
        self, executor, isolated_registry, app_ctx_set, caplog
    ) -> None:
        from matrx_ai.tools.kinds import TOOL_RESULT_KINDS
        from matrx_ai.tools.kinds.tooling import ToolBundleListing

        TOOL_RESULT_KINDS["kindful"] = ToolBundleListing
        try:
            td = ToolDefinition(
                name="kindful",
                description="fixture tool for a declared result failure",
                parameters={},
                output_schema=ToolBundleListing.model_json_schema(),
                tool_type=ToolType.LOCAL,
                function_path=f"{__name__}._failed_fixture_tool",
                source_kind="native",
            )
            td._callable = _failed_fixture_tool
            isolated_registry._tools["kindful"] = td
            with caplog.at_level("ERROR"):
                result = await _run(executor, {})
        finally:
            TOOL_RESULT_KINDS.pop("kindful", None)

        assert result.success is False
        assert not any(
            "DECLARED tool result kind missing" in rec.getMessage() for rec in caplog.records
        )

    async def test_pydantic_result_is_serialized_before_output_contract_check(
        self, executor, isolated_registry, app_ctx_set, monkeypatch
    ) -> None:
        """A stored output schema describes JSON, not the BaseModel object."""
        from matrx_ai.tools.kinds import TOOL_RESULT_KINDS
        from matrx_ai.tools.kinds.tooling import ToolBundleListing

        captures: list[dict[str, Any]] = []

        async def fake_capture(**kwargs: Any) -> None:
            captures.append(kwargs)

        monkeypatch.setattr(
            "matrx_ai.tools.executor._capture_tool_output_contract_drift",
            fake_capture,
        )
        TOOL_RESULT_KINDS["kindful"] = ToolBundleListing
        try:
            td = ToolDefinition(
                name="kindful",
                description="fixture tool for the result-kind seam",
                parameters={},
                output_schema=ToolBundleListing.model_json_schema(),
                tool_type=ToolType.LOCAL,
                function_path=f"{__name__}._fixture_tool",
                source_kind="native",
            )
            td._callable = _fixture_tool
            isolated_registry._tools["kindful"] = td
            result = await _run(executor, ToolBundleListing(bundle="supabase", count=1))
        finally:
            TOOL_RESULT_KINDS.pop("kindful", None)

        assert result.success is True
        assert result.output_kind == "tool_bundle_listing"
        assert result.output_kind_errors == []
        assert captures == []


class TestBothHalvesStayOneFact:
    """The stored schema is DERIVED, never hand-written — that is what makes the
    two instruments agree. Every declared model must therefore emit a ``__kind``
    ``const`` matching its own slug, or the backfill would write a schema the
    coverage board cannot read as a declaration."""

    def test_every_declared_model_emits_its_own_slug_as_a_const(self) -> None:
        from matrx_ai.tools.kinds import TOOL_RESULT_KIND_PREFIXES, TOOL_RESULT_KINDS

        models = list(TOOL_RESULT_KINDS.values()) + [m for _p, m in TOOL_RESULT_KIND_PREFIXES]
        assert models, "the declaration is empty — the runtime half measures nothing"
        for model in models:
            schema = model.model_json_schema()
            marker = schema.get("properties", {}).get("__kind")
            assert isinstance(marker, dict), f"{model.__name__} emits no __kind property"
            assert marker.get("const") == model.kind_slug, (
                f"{model.__name__} must pin __kind const to {model.kind_slug!r}"
            )
