"""Phase 0 regression tests for the silent-failure / embedded-error-envelope
bug class. See /Users/armanisadeghi/.claude/plans/yes-i-think-it-s-elegant-meadow.md.

The bug pattern these tests pin down:
  - A tool catches a DB exception and returns ``{"success": False, "error": ...}``
    instead of raising.
  - A caller wraps that as ``ToolResult(success=True, output={"table_id":
    str(error_dict), ...})``.
  - The orchestrator, trace log, and cx_tool_call row all record OK.

Two defenses landed in Phase 0:
  - ``ToolResult.output`` Pydantic validator rejects string fields that look
    like ``str()``-serialised dicts/lists or JSON objects.
  - ``ToolExecutor.execute`` (separate, not unit-tested here) flips the
    outer ``ToolResult.success`` to False when ``output`` is a dict with
    ``success: False`` inside.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.tools.models import ToolError, ToolOutputContractError, ToolResult


# The gate raises ``ToolOutputContractError`` (a ``ValueError`` subclass).
# Pydantic v2 wraps validator-raised ``ValueError``s in ``ValidationError``,
# so ``ValidationError`` is the type that actually escapes ``ToolResult(...)``
# and the type production code catches at the tool-executor boundary. It then
# unwraps the original gate exception via ``.errors()[].ctx.error`` — see
# ``tools/implementations/ctx.py::_extract_gate_message``. These tests pin
# that exact contract: catch the wrapped ``ValidationError``, recover the
# inner ``ToolOutputContractError``, and assert its clean message is surfaced.


class TestToolOutputValidatorRejectsStringifiedStructures:
    def test_python_repr_of_error_envelope_is_rejected(self):
        """The exact bug from the 2026-05-16 usertable_create incident."""
        error_dict = {
            "error": "column \"authenticated_read\" does not exist",
            "success": False,
            "table_name": "x",
        }
        with pytest.raises(ValidationError) as exc_info:
            ToolResult(
                success=True,
                output={
                    "table_id": str(error_dict),
                    "table_name": "x",
                    "row_count": 15,
                },
            )
        # Recover the gate's own exception the way production does, so this
        # test breaks loudly if Pydantic ever stops surfacing it here.
        gate_err = exc_info.value.errors()[0]["ctx"]["error"]
        assert isinstance(gate_err, ToolOutputContractError)
        msg = str(gate_err)
        assert "table_id" in msg  # the offending field is named
        assert "stringified" in msg  # the antipattern is identified

    def test_json_encoded_dict_string_is_rejected(self):
        import json

        with pytest.raises(ValidationError):
            ToolResult(
                success=True,
                output={"payload": json.dumps({"k": "v"})},
            )

    def test_stringified_list_is_rejected(self):
        with pytest.raises(ValidationError):
            ToolResult(
                success=True,
                output={"items": str([1, 2, 3])},
            )


class TestToolOutputValidatorAcceptsLegitimateShapes:
    def test_scalar_string_output_is_accepted(self):
        ToolResult(success=True, output={"table_id": "abc-123-uuid"})

    def test_nested_dict_output_is_accepted(self):
        ToolResult(
            success=True,
            output={
                "tables": [{"id": "x", "name": "y"}],
                "count": 1,
            },
        )

    def test_top_level_string_output_is_accepted(self):
        # Plain string output (not a dict) bypasses the validator.
        ToolResult(success=True, output="hello world")

    def test_shell_execution_accepts_json_stdout_as_opaque_process_text(self):
        """A successful shell command may intentionally print JSON."""
        result = ToolResult(
            success=True,
            output={
                "__kind": "shell_execution",
                "stdout": '{"answer": 42}',
                "stderr": "[]",
                "exit_code": 0,
            },
        )
        assert result.output["stdout"] == '{"answer": 42}'
        assert result.output["stderr"] == "[]"

    def test_shell_execution_exemption_does_not_cover_other_fields(self):
        with pytest.raises(ValidationError):
            ToolResult(
                success=True,
                output={
                    "__kind": "shell_execution",
                    "stdout": "ok",
                    "metadata": '{"silently": "stringified"}',
                    "exit_code": 0,
                },
            )

    def test_file_read_result_accepts_json_as_opaque_file_text(self):
        result = ToolResult(
            success=True,
            output={
                "__kind": "file_read_result",
                "path": "data.json",
                "content": '{"answer": 42}',
                "size": 14,
                "truncated": False,
            },
        )
        assert result.output["content"] == '{"answer": 42}'

    def test_file_read_result_exemption_does_not_cover_other_fields(self):
        with pytest.raises(ValidationError):
            ToolResult(
                success=True,
                output={
                    "__kind": "file_read_result",
                    "path": '{"silently": "stringified"}',
                    "content": "ordinary text",
                    "size": 13,
                    "truncated": False,
                },
            )

    def test_image_ref_output_shape_is_accepted(self):
        # The canonical image_ref output shape from matrx_ai.tools.image_outputs.
        ToolResult(
            success=True,
            output={
                "kind": "image_ref",
                "media_ref": {"file_id": "abc", "vision_class": "v1"},
                "media_type": "image/png",
                "source_width": 1024,
                "source_height": 768,
            },
        )

    def test_string_with_leading_brace_but_not_parseable_is_accepted(self):
        # Mustache template, code snippet, etc. — starts with { but isn't
        # a dict literal or JSON.
        ToolResult(
            success=True,
            output={"template": "{not a dict, just text}"},
        )

    def test_empty_output_is_accepted(self):
        ToolResult(success=True, output=None)
        ToolResult(success=True, output={})

    def test_failure_result_with_error_envelope_in_output_is_accepted(self):
        # Legitimate use: a tool that genuinely failed and surfaces a
        # structured payload alongside ``error``. Validator only checks
        # string fields, so a nested-dict payload is fine.
        ToolResult(
            success=False,
            error=ToolError(error_type="execution", message="oops"),
            output={"partial_rows": [{"id": 1}], "stderr": "..."},
        )


class TestToolOutputContractError:
    def test_is_value_error_subclass(self):
        assert issubclass(ToolOutputContractError, ValueError)


class TestDatasetCreationErrorImportable:
    """Phase 0.1 — the exception class exists and is a plain Exception
    subclass. Tools that catch it can rely on the type."""

    def test_importable_and_is_exception(self):
        # ``user_data`` is an aidream host module, not part of matrx-ai. When the
        # package is tested standalone (CI runs matrx-ai in isolation) the repo
        # root is not on sys.path, so this contract test skips rather than
        # erroring — it only asserts the host's exception shape when the host is
        # present. Keeps the package-independence boundary intact.
        pytest.importorskip("user_data.dataset_creator")
        from user_data.dataset_creator import DatasetCreationError

        assert issubclass(DatasetCreationError, Exception)

        with pytest.raises(DatasetCreationError):
            raise DatasetCreationError("test")
