"""Tests for workflow simulation and validation (#968)."""

from __future__ import annotations

import textwrap
from pathlib import Path

from anteroom.services.workflow_engine import validate_workflow_definition


class TestValidateWorkflowDefinition:
    def test_valid_definition(self, tmp_path: Path) -> None:
        defn_path = tmp_path / "valid.yaml"
        defn_path.write_text(
            textwrap.dedent("""\
            kind: workflow
            id: test_workflow
            version: "0.1.0"
            steps:
              - id: build
                type: runner
                runner: shell
                command: echo hello
            """)
        )
        result = validate_workflow_definition(defn_path)
        assert result.is_valid
        assert result.definition is not None
        assert result.definition.id == "test_workflow"
        assert len(result.errors) == 0

    def test_missing_kind(self, tmp_path: Path) -> None:
        defn_path = tmp_path / "no_kind.yaml"
        defn_path.write_text(
            textwrap.dedent("""\
            id: test
            version: "0.1.0"
            steps:
              - id: s1
                type: runner
                runner: shell
                command: echo
            """)
        )
        result = validate_workflow_definition(defn_path)
        assert not result.is_valid
        assert any("kind" in e.lower() for e in result.errors)

    def test_missing_id(self, tmp_path: Path) -> None:
        defn_path = tmp_path / "no_id.yaml"
        defn_path.write_text(
            textwrap.dedent("""\
            kind: workflow
            version: "0.1.0"
            steps:
              - id: s1
                type: runner
                runner: shell
                command: echo
            """)
        )
        result = validate_workflow_definition(defn_path)
        assert not result.is_valid

    def test_no_steps(self, tmp_path: Path) -> None:
        defn_path = tmp_path / "no_steps.yaml"
        defn_path.write_text(
            textwrap.dedent("""\
            kind: workflow
            id: test
            version: "0.1.0"
            steps: []
            """)
        )
        result = validate_workflow_definition(defn_path)
        assert not result.is_valid
        assert any("step" in e.lower() for e in result.errors)

    def test_file_not_found(self, tmp_path: Path) -> None:
        result = validate_workflow_definition(tmp_path / "nonexistent.yaml")
        assert not result.is_valid
        assert any("not found" in e.lower() for e in result.errors)

    def test_invalid_yaml_string(self) -> None:
        result = validate_workflow_definition("not: valid: yaml: {{{}}")
        assert not result.is_valid

    def test_valid_multi_step(self, tmp_path: Path) -> None:
        defn_path = tmp_path / "multi.yaml"
        defn_path.write_text(
            textwrap.dedent("""\
            kind: workflow
            id: multi_step
            version: "0.1.0"
            steps:
              - id: lint
                type: runner
                runner: shell
                command: ruff check .
              - id: test
                type: runner
                runner: shell
                command: pytest
            """)
        )
        result = validate_workflow_definition(defn_path)
        assert result.is_valid
        assert len(result.definition.steps) == 2

    def test_runner_step_without_command(self, tmp_path: Path) -> None:
        defn_path = tmp_path / "no_cmd.yaml"
        defn_path.write_text(
            textwrap.dedent("""\
            kind: workflow
            id: test
            version: "0.1.0"
            steps:
              - id: s1
                type: runner
                runner: shell
            """)
        )
        result = validate_workflow_definition(defn_path)
        assert not result.is_valid

    def test_gate_step_without_condition(self, tmp_path: Path) -> None:
        defn_path = tmp_path / "no_cond.yaml"
        defn_path.write_text(
            textwrap.dedent("""\
            kind: workflow
            id: test
            version: "0.1.0"
            steps:
              - id: check
                type: gate
            """)
        )
        result = validate_workflow_definition(defn_path)
        assert not result.is_valid


class TestStubRunnerRegistry:
    def test_stub_registered(self) -> None:
        from anteroom.services.workflow_runners import create_stub_registry

        registry = create_stub_registry()
        assert registry.is_registered("stub")
        assert registry.is_opaque_runner("stub")

    def test_stub_in_opaque_types(self) -> None:
        from anteroom.services.workflow_runners import OPAQUE_RUNNER_TYPES

        assert "stub" in OPAQUE_RUNNER_TYPES

    def test_default_registry_no_stub(self) -> None:
        from anteroom.services.workflow_runners import create_default_registry

        registry = create_default_registry()
        assert not registry.is_registered("stub")
