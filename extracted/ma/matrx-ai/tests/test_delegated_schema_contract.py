"""Guards for the 2026-09-13 delegated-tool schema class.

A browser-executed ``user`` question was suspended, then rejected by the
client's zod schema (``header`` > 12 chars) — a full suspend→reject→resume
cycle for a constraint the model was never shown. Three fixes, each proven:

  1. ``minLength``/``maxLength`` are forwarded to the provider schema;
  2. delegated args are validated against that same schema BEFORE suspending;
  3. every shell result names its ``backend`` (sandbox / durable_vfs / host).
"""

from __future__ import annotations

from matrx_ai.tools.executor import _validate_against_declared_schema
from matrx_ai.tools.kinds.execution import ShellExecution
from matrx_ai.tools.models import ToolDefinition, ToolType

USER_TOOL_PARAMS = {
    "type": {"type": "string", "enum": ["confirm", "choice", "text"]},
    "question": {"type": "string"},
    "header": {"type": "string", "maxLength": 12, "description": "chip label"},
    "questions": {
        "type": "array",
        "minItems": 1,
        "maxItems": 4,
        "items": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["confirm", "choice", "text"]},
                "question": {"type": "string"},
                "header": {"type": "string", "maxLength": 12},
            },
        },
    },
}


def _user_tool() -> ToolDefinition:
    return ToolDefinition(name="user", tool_type=ToolType.LOCAL, parameters=USER_TOOL_PARAMS)


def test_string_length_constraints_reach_the_provider_schema() -> None:
    schema = _user_tool()._build_json_schema()
    assert schema["properties"]["header"]["maxLength"] == 12
    assert schema["properties"]["questions"]["items"]["properties"]["header"]["maxLength"] == 12


def test_openai_strict_mode_still_strips_length_constraints() -> None:
    schema = _user_tool()._build_json_schema(strip_openai_unsupported=True)
    assert "maxLength" not in schema["properties"]["header"]


def test_delegated_precheck_rejects_the_incident_args() -> None:
    err = _validate_against_declared_schema(
        _user_tool(),
        {
            "questions": [
                {"type": "choice", "header": "aidream", "question": "Which?"},
                {"type": "text", "header": "common-docs repo", "question": "Name?"},
            ]
        },
    )
    assert err is not None
    assert "questions.1.header" in err and "16" in err or "too long" in err


def test_delegated_precheck_accepts_valid_args_and_tolerates_extra_keys() -> None:
    assert (
        _validate_against_declared_schema(
            _user_tool(), {"type": "text", "header": "docs repo", "question": "?", "extra": 1}
        )
        is None
    )


def test_delegated_precheck_never_blocks_on_a_broken_row() -> None:
    broken = ToolDefinition(
        name="odd", tool_type=ToolType.LOCAL, parameters={"x": {"type": "string", "pattern": "("}}
    )
    assert _validate_against_declared_schema(broken, {"x": "a"}) is None


def test_shell_execution_names_its_backend() -> None:
    assert ShellExecution(backend="durable_vfs").model_dump(mode="json")["backend"] == "durable_vfs"
    assert "backend" in ShellExecution.model_json_schema()["properties"]
