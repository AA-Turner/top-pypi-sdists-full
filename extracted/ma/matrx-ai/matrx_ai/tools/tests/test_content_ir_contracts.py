from types import SimpleNamespace

import pytest

from matrx_ai.tools.executor import (
    TOOL_EXECUTION_FAILED_KIND,
    TOOL_INPUT_CONTRACT_DRIFT_KIND,
    TOOL_OUTPUT_CONTRACT_DRIFT_KIND,
    _capture_tool_execution_failed,
    _capture_tool_input_contract_drift,
    _capture_tool_output_contract_drift,
    _capture_tool_result_kind_missing,
    _capture_tool_result_size_unmanaged,
    _is_expected_domain_failure,
)
from matrx_ai.tools.implementations.shell import shell_python
from matrx_ai.tools.models import ToolDefinition


def test_tool_contract_uses_normalized_provider_input_schema() -> None:
    tool = ToolDefinition(
        name="files:read",
        tool_id="7d2960ec-605a-4f18-bb9c-2add9d29ac77",
        parameters={
            "path": {"type": "string", "required": True},
            "$variants": {"internal": True},
        },
        output_schema={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
        version=3,
    )

    input_contract, output_contract = tool.content_ir_contracts()

    assert "$variants" not in input_contract.json_schema["properties"]
    assert input_contract.json_schema["required"] == ["path"]
    assert input_contract.kind.startswith("tool_io_files_read_")
    assert input_contract.source_id == "7d2960ec-605a-4f18-bb9c-2add9d29ac77"
    assert input_contract.version == 3
    assert output_contract is not None
    assert output_contract.json_schema == tool.output_schema


def test_tool_without_output_schema_stays_explicitly_opaque() -> None:
    tool = ToolDefinition(name="opaque", parameters={})
    _input_contract, output_contract = tool.content_ir_contracts()
    assert output_contract is None


def test_request_local_tool_contract_identity_includes_schema() -> None:
    """One reused client tool name must not merge unrelated surface contracts."""
    sql_surface = ToolDefinition(
        name="apply_surface_write",
        parameters={
            "target": {"type": "string", "enum": ["sql_query"], "required": True}
        },
    )
    task_surface = ToolDefinition(
        name="apply_surface_write",
        parameters={
            "target": {"type": "string", "enum": ["task_title"], "required": True}
        },
    )
    same_sql_surface = ToolDefinition(
        name="apply_surface_write",
        parameters={
            "target": {"required": True, "enum": ["sql_query"], "type": "string"}
        },
    )

    sql_kind = sql_surface.content_ir_contracts()[0].kind
    task_kind = task_surface.content_ir_contracts()[0].kind
    same_sql_kind = same_sql_surface.content_ir_contracts()[0].kind

    assert sql_kind != task_kind
    assert sql_kind == same_sql_kind


def test_tool_contract_exposes_uuid_for_a3_reference_backfill() -> None:
    tool = ToolDefinition(
        name="tool_name",
        tool_id="7d2960ec-605a-4f18-bb9c-2add9d29ac77",
        parameters={},
    )
    contract = tool.content_ir_contracts()[0]
    assert contract.metadata()["source_id"] == tool.tool_id


def test_dispatcher_contract_flattens_generated_variant_properties() -> None:
    tool = ToolDefinition(
        name="cloud_browser",
        parameters={
            "action": {
                "type": "string",
                "enum": ["click", "navigate"],
                "required": True,
            },
            "session_id": {"type": "string"},
            "url": {"type": "string"},
            "$variants": {
                "click": {
                    "type": "object",
                    "required": ["session_id"],
                    "properties": {"session_id": {"type": "string"}},
                },
                "navigate": {
                    "type": "object",
                    "required": ["url"],
                    "properties": {
                        "session_id": {"type": "string", "default": ""},
                        "url": {"type": "string"},
                    },
                },
            },
        },
    )

    schema = tool.content_ir_contracts()[0].json_schema

    assert set(schema["properties"]) == {"action", "session_id", "url"}
    assert schema["properties"]["session_id"]["type"] == "string"
    assert schema["required"] == ["action"]


def test_typeless_dispatcher_property_accepts_object_in_content_ir_contract() -> None:
    """A JSON-Schema property without ``type`` is unconstrained, never text-only.

    Generated dispatcher rows use this shape for fields shared by variants with
    incompatible value shapes. Credential login's ``submit`` is the production
    forcing case: an attempt submits an object even though another action may use
    a different public shape.
    """
    tool = ToolDefinition(
        name="credential_login",
        parameters={
            "action": {
                "type": "string",
                "enum": ["attempt", "propose_recipe"],
                "required": True,
            },
            "submit": {"description": "Variant-owned submit shape."},
            "$variants": {
                "attempt": {
                    "type": "object",
                    "properties": {
                        "submit": {"description": "A login submit command."},
                    },
                    "required": ["submit"],
                },
                "propose_recipe": {
                    "type": "object",
                    "properties": {
                        "submit": {"type": "string"},
                    },
                    "required": [],
                },
            },
        },
    )

    contract = tool.content_ir_contracts()[0].json_schema

    assert "type" not in contract["properties"]["submit"]
    from matrx_graph.contract_kinds import check_schema

    verdict = check_schema(
        {
            "action": "attempt",
            "submit": {"kind": "click", "selector": "#totpNext"},
        },
        contract,
    )
    assert verdict.errors == []


def test_typeless_dispatcher_root_is_not_narrowed_by_first_variant() -> None:
    """The generated union root wins over one action's narrower field shape."""
    tool = ToolDefinition(
        name="dataset",
        parameters={
            "action": {
                "type": "string",
                "enum": ["create", "update_row"],
                "required": True,
            },
            "data": {"description": "Rows or one row patch, depending on action."},
            "$variants": {
                "create": {
                    "type": "object",
                    "properties": {"data": {"type": "array"}},
                    "required": [],
                },
                "update_row": {
                    "type": "object",
                    "properties": {"data": {"type": "object"}},
                    "required": [],
                },
            },
        },
    )

    contract = tool.content_ir_contracts()[0].json_schema

    assert "type" not in contract["properties"]["data"]
    from matrx_graph.contract_kinds import check_schema

    verdict = check_schema(
        {"action": "update_row", "data": {"name": "orcho"}},
        contract,
    )
    assert verdict.errors == []


def test_dispatcher_ignores_stale_root_type_when_variants_disagree() -> None:
    """Variant execution contracts outrank a stale scalar dispatcher root."""
    tool = ToolDefinition(
        name="apply_surface_write",
        parameters={
            "action": {
                "type": "string",
                "enum": ["set_text", "set_record"],
                "required": True,
            },
            "value": {
                "type": "string",
                "description": "Value written to the mounted surface.",
            },
            "$variants": {
                "set_text": {
                    "type": "object",
                    "properties": {"value": {"type": "string"}},
                    "required": ["value"],
                },
                "set_record": {
                    "type": "object",
                    "properties": {"value": {"type": "object"}},
                    "required": ["value"],
                },
            },
        },
    )

    schema = tool.content_ir_contracts()[0].json_schema

    assert schema["properties"]["value"] == {
        "description": "Value written to the mounted surface."
    }


def test_inline_multi_type_union_is_not_narrowed_to_first_member() -> None:
    """A client-authored JSON-Schema union remains open at dispatch."""
    tool = ToolDefinition(
        name="apply_surface_write",
        parameters={
            "target": {"type": "string", "required": True},
            "value": {
                "type": ["string", "number", "boolean", "array", "object", "null"],
                "description": "Value shaped for the selected surface target.",
                "required": True,
            },
        },
    )

    contract = tool.content_ir_contracts()[0].json_schema

    assert contract["properties"]["value"] == {
        "description": "Value shaped for the selected surface target."
    }
    from matrx_graph.contract_kinds import check_schema

    verdict = check_schema(
        {
            "target": "reputation_case_triage",
            "value": {"case_id": "case-1", "status": "monitoring"},
        },
        contract,
    )
    assert verdict.errors == []


def test_nullable_single_type_keeps_its_concrete_contract() -> None:
    tool = ToolDefinition(
        name="nullable_text",
        parameters={"value": {"type": ["string", "null"], "required": True}},
    )

    contract = tool.content_ir_contracts()[0].json_schema

    assert contract["properties"]["value"]["type"] == "string"


@pytest.mark.asyncio
async def test_input_drift_creates_bounded_structured_capture(monkeypatch) -> None:
    captured = {}

    async def fake_capture_error(exc, **kwargs):
        captured["exc"] = exc
        captured.update(kwargs)

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        fake_capture_error,
    )

    await _capture_tool_input_contract_drift(
        ctx=SimpleNamespace(
            request_id="req-1",
            user_id="user-1",
            conversation_id="conv-1",
        ),
        tool_name="cloud_browser",
        input_kind="tool_io_cloud_browser_input",
        error_count=1,
    )

    assert captured["kind"] == TOOL_INPUT_CONTRACT_DRIFT_KIND
    assert captured["error_type"] == "ToolInputContractDrift"
    assert captured["request_id"] == "req-1"
    assert captured["context"] == {
        "tool_name": "cloud_browser",
        "input_kind": "tool_io_cloud_browser_input",
        "error_count": 1,
    }
    assert "arguments" not in captured["context"]


@pytest.mark.asyncio
async def test_output_drift_creates_bounded_structured_capture(monkeypatch) -> None:
    captured = {}

    async def fake_capture_error(exc, **kwargs):
        captured["exc"] = exc
        captured.update(kwargs)

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        fake_capture_error,
    )

    await _capture_tool_output_contract_drift(
        ctx=SimpleNamespace(
            request_id="req-1",
            user_id="user-1",
            conversation_id="conv-1",
        ),
        tool_name="kindcomp_get_code",
        output_kind="tool_io_kindcomp_get_code_output",
        error_count=1,
    )

    assert captured["kind"] == TOOL_OUTPUT_CONTRACT_DRIFT_KIND
    assert captured["error_type"] == "ToolOutputContractDrift"
    assert captured["context"] == {
        "tool_name": "kindcomp_get_code",
        "output_kind": "tool_io_kindcomp_get_code_output",
        "error_count": 1,
    }
    assert "output" not in captured["context"]


@pytest.mark.asyncio
async def test_execution_failure_creates_bounded_structured_capture(monkeypatch) -> None:
    captured = {}

    async def fake_capture_error(exc, **kwargs):
        captured["exc"] = exc
        captured.update(kwargs)

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        fake_capture_error,
    )

    await _capture_tool_execution_failed(
        ctx=SimpleNamespace(
            request_id="req-1",
            user_id="user-1",
            conversation_id="conv-1",
            call_id="call-1",
        ),
        tool_name="fs_write",
        error_type="execution",
    )

    assert captured["kind"] == TOOL_EXECUTION_FAILED_KIND
    assert captured["route"] == "tool_executor.execution"
    assert captured["error_type"] == "execution"
    assert captured["context"] == {"tool_name": "fs_write", "call_id": "call-1"}
    assert "arguments" not in captured["context"]


@pytest.mark.asyncio
async def test_missing_declared_result_kind_creates_bounded_capture(monkeypatch) -> None:
    captured = {}

    async def fake_capture_error(exc, **kwargs):
        captured["exc"] = exc
        captured.update(kwargs)

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture_error)
    await _capture_tool_result_kind_missing(
        ctx=SimpleNamespace(request_id="req-1", user_id="user-1", conversation_id="conv-1"),
        tool_name="fs_edit",
        output_kind="file_edit_result",
    )

    assert captured["kind"] == "tool_result_kind_missing"
    assert captured["error_type"] == "ToolResultKindMissing"
    assert captured["context"] == {
        "tool_name": "fs_edit",
        "output_kind": "file_edit_result",
    }
    assert "output" not in captured["context"]


@pytest.mark.asyncio
async def test_unmanaged_owned_tool_result_creates_bounded_capture(monkeypatch) -> None:
    captured = {}

    async def fake_capture_error(exc, **kwargs):
        captured["exc"] = exc
        captured.update(kwargs)

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture_error)
    await _capture_tool_result_size_unmanaged(
        ctx=SimpleNamespace(
            request_id="req-1",
            user_id="user-1",
            conversation_id="conv-1",
            call_id="call-1",
        ),
        tool_name="data",
    )

    assert captured["kind"] == "tool_result_size_unmanaged"
    assert captured["error_type"] == "ToolResultSizeUnmanaged"
    assert captured["context"] == {"tool_name": "data", "call_id": "call-1"}
    assert "output" not in captured["context"]


@pytest.mark.parametrize(
    "error_type",
    ["validation", "invalid_arguments", "auth_required", "missing_context"],
)
def test_expected_tool_refusals_do_not_enter_error_queue(error_type: str) -> None:
    assert _is_expected_domain_failure(tool_name="any_tool", error_type=error_type)


def test_database_failure_requires_structured_capture() -> None:
    assert not _is_expected_domain_failure(
        tool_name="knowledge_browse",
        error_type="UnknownDatabaseError",
    )


def test_shell_nonzero_exit_is_expected_tool_feedback() -> None:
    assert _is_expected_domain_failure(
        tool_name="shell_execute",
        error_type="exit_code",
    )
    assert not _is_expected_domain_failure(
        tool_name="shell_execute",
        error_type="timeout",
    )


@pytest.mark.asyncio
async def test_shell_python_nonzero_exit_is_expected_tool_feedback(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "matrx_ai.tools.implementations.shell.get_active_sandbox",
        lambda: None,
    )
    monkeypatch.setattr(
        "matrx_ai.tools.implementations.shell._workspace_dir",
        lambda _ctx: str(tmp_path),
    )

    result = await shell_python(
        {"code": "print('expected-exit')\nraise SystemExit(7)"},
        SimpleNamespace(call_id="call-1"),
    )

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "exit_code"
    assert result.output["exit_code"] == 7
    assert result.output["stdout"] == "expected-exit\n"
    assert _is_expected_domain_failure(
        tool_name="shell_python",
        error_type=result.error.error_type,
    )
    assert not _is_expected_domain_failure(
        tool_name="shell_python",
        error_type="execution",
    )


def test_cloud_browser_run_state_conflict_is_expected_tool_feedback() -> None:
    assert _is_expected_domain_failure(
        tool_name="cloud_browser",
        error_type="run_state_conflict",
    )
    assert not _is_expected_domain_failure(
        tool_name="cloud_browser",
        error_type="worker_unreachable",
    )
