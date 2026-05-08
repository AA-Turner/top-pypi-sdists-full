"""Unit tests for flowtask.parsers.syntax.schema.ROOT_TASK_SCHEMA."""
import inspect

import jsonschema
import pytest

from flowtask.parsers.syntax.schema import ROOT_TASK_SCHEMA


def test_root_task_schema_is_a_draft07_schema():
    """The constant must identify as a JSON Schema Draft-07 object schema."""
    assert ROOT_TASK_SCHEMA["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert ROOT_TASK_SCHEMA["type"] == "object"
    assert "name" in ROOT_TASK_SCHEMA["required"]
    assert "steps" in ROOT_TASK_SCHEMA["required"]
    assert ROOT_TASK_SCHEMA["additionalProperties"] is False


def test_root_task_schema_accepts_minimal_valid_task():
    """A task with only name and steps must pass validation."""
    task = {"name": "demo", "steps": [{"AddDataset": {"dataset": "x"}}]}
    jsonschema.validate(instance=task, schema=ROOT_TASK_SCHEMA)  # no raise


def test_root_task_schema_rejects_missing_name():
    """A task without 'name' must fail validation."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            instance={"steps": [{"AddDataset": {}}]},
            schema=ROOT_TASK_SCHEMA,
        )


def test_root_task_schema_rejects_missing_steps():
    """A task without 'steps' must fail validation."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            instance={"name": "demo"},
            schema=ROOT_TASK_SCHEMA,
        )


def test_root_task_schema_rejects_step_with_two_keys():
    """Each step must be a single-key object whose key is the component name."""
    bad = {"name": "x", "steps": [{"AddDataset": {}, "Other": {}}]}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad, schema=ROOT_TASK_SCHEMA)


def test_root_task_schema_rejects_unknown_top_level_key():
    """additionalProperties=False means extra top-level keys must fail."""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            instance={"name": "x", "steps": [], "unknown_field": True},
            schema=ROOT_TASK_SCHEMA,
        )


def test_abstract_check_syntax_uses_the_constant_not_a_local_literal():
    """The refactor must keep the constant as the only source of truth.

    We assert by source inspection: AbstractTask.check_syntax does NOT
    contain '$schema' as a string literal anymore.

    Uses file-based inspection to avoid loading the full AbstractTask module
    (which requires compiled Cython extensions).
    """
    from pathlib import Path
    abstract_py = (
        Path(__file__).parent.parent.parent.parent.parent
        / "flowtask" / "tasks" / "abstract.py"
    )
    source = abstract_py.read_text()
    # Find only the check_syntax method body (from "def check_syntax" to "async def close")
    start = source.find("def check_syntax(")
    end = source.find("\n    async def close(", start)
    method_source = source[start:end]
    assert "$schema" not in method_source, (
        "AbstractTask.check_syntax still inlines the JSON Schema literal; "
        "it must import ROOT_TASK_SCHEMA from flowtask.parsers.syntax.schema."
    )
