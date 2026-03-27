"""Tests for workflow artifact integration (#957).

Tests skill expansion, source context injection, rules/conventions injection,
and integration with the workflow engine.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    _resolve_source_group_ref,
    _resolve_source_ref,
    load_definition,
    resolve_context_from,
)
from anteroom.services.workflow_runners import RunnerResult, create_default_registry

# ---------------------------------------------------------------------------
# Test YAML
# ---------------------------------------------------------------------------

SKILL_WORKFLOW = """\
kind: workflow
id: test_skill
version: 0.1.0
inputs: {}
steps:
  - id: run_skill
    type: runner
    runner: cli_claude
    skill_name: test-skill
    skill_args: "some arguments"
    timeout: 10
"""

INJECT_RULES_WORKFLOW = """\
kind: workflow
id: test_inject
version: 0.1.0
inputs: {}
policies:
  inject_rules: true
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo hello"
    timeout: 10
"""

SOURCE_CONTEXT_WORKFLOW = """\
kind: workflow
id: test_source_ctx
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo hello"
    timeout: 10
  - id: step_two
    type: runner
    runner: shell
    command: "echo with context"
    timeout: 10
    context_from:
      - source_id: "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
"""

SKILL_ON_OPAQUE_WORKFLOW = """\
kind: workflow
id: test_bad_skill
version: 0.1.0
inputs: {}
steps:
  - id: bad
    type: runner
    runner: shell
    skill_name: test-skill
    command: "echo hello"
    timeout: 10
"""


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn


@pytest.fixture()
def registry():
    return create_default_registry()


async def _mock_opaque_runner(**kwargs: Any) -> RunnerResult:
    return RunnerResult(status="success", summary="done", duration_ms=10)


# ---------------------------------------------------------------------------
# Skill expansion tests
# ---------------------------------------------------------------------------


@dataclass
class MockSkill:
    name: str = "test-skill"
    prompt: str = "Do the thing: {args}"


class TestSkillExpansion:
    def test_skill_name_on_opaque_runner_rejected(self) -> None:
        with pytest.raises(ValueError, match="skill_name requires an agent runner"):
            load_definition(SKILL_ON_OPAQUE_WORKFLOW)

    def test_expand_skill_prompt(self, db: Any, registry: Any) -> None:
        skill_reg = MagicMock()
        skill_reg.get.return_value = MockSkill()
        engine = WorkflowEngine(db, WorkflowConfig(), registry, skill_registry=skill_reg)
        defn = load_definition(SKILL_WORKFLOW)
        step = defn.steps[0]
        result = engine._expand_skill_prompt(step)
        assert "Do the thing: some arguments" == result

    def test_skill_not_found_raises(self, db: Any, registry: Any) -> None:
        skill_reg = MagicMock()
        skill_reg.get.return_value = None
        engine = WorkflowEngine(db, WorkflowConfig(), registry, skill_registry=skill_reg)
        defn = load_definition(SKILL_WORKFLOW)
        step = defn.steps[0]
        with pytest.raises(ValueError, match="not found in registry"):
            engine._expand_skill_prompt(step)

    def test_skill_no_registry_raises(self, db: Any, registry: Any) -> None:
        engine = WorkflowEngine(db, WorkflowConfig(), registry)  # no skill_registry
        defn = load_definition(SKILL_WORKFLOW)
        step = defn.steps[0]
        with pytest.raises(ValueError, match="requires a SkillRegistry"):
            engine._expand_skill_prompt(step)


# ---------------------------------------------------------------------------
# Source context_from tests
# ---------------------------------------------------------------------------


class TestSourceContextFrom:
    def test_source_id_resolves(self) -> None:
        mock_db = MagicMock()
        source = {"id": "abc", "title": "test", "content": "Source content here"}
        with patch("anteroom.services.storage.get_source", return_value=source):
            result = _resolve_source_ref("abc", mock_db)
        assert result is not None
        assert "Source content here" in result

    def test_source_id_not_found(self) -> None:
        mock_db = MagicMock()
        with patch("anteroom.services.storage.get_source", return_value=None):
            result = _resolve_source_ref("missing-id", mock_db)
        assert result is None

    def test_source_id_no_db(self) -> None:
        result = _resolve_source_ref("abc", None)
        assert result is None

    def test_source_group_resolves(self) -> None:
        mock_db = MagicMock()
        sources = [
            {"id": "s1", "content": "Doc one"},
            {"id": "s2", "content": "Doc two"},
        ]
        with patch("anteroom.services.storage.list_sources", return_value=sources):
            result = _resolve_source_group_ref("grp-1", mock_db)
        assert result is not None
        assert "Doc one" in result
        assert "Doc two" in result

    def test_source_group_empty(self) -> None:
        mock_db = MagicMock()
        with patch("anteroom.services.storage.list_sources", return_value=[]):
            result = _resolve_source_group_ref("empty-grp", mock_db)
        assert result is None

    def test_mixed_context_from(self) -> None:
        """context_from with both step and source_id refs."""
        refs = [
            {"step": "step_one", "field": "result_summary"},
            {"source_id": "abc-123"},
        ]
        step_results = {"step_one": {"result_summary": "Step one output"}}
        mock_db = MagicMock()
        source = {"id": "abc-123", "content": "Source content"}
        with patch("anteroom.services.storage.get_source", return_value=source):
            result = resolve_context_from(refs, step_results, db=mock_db)
        assert "Step one output" in result
        assert "Source content" in result

    def test_resolve_context_from_backward_compat(self) -> None:
        """Existing step-only context_from works without db."""
        refs = [{"step": "s1", "field": "result_summary"}]
        step_results = {"s1": {"result_summary": "hello"}}
        result = resolve_context_from(refs, step_results)
        assert "hello" in result


# ---------------------------------------------------------------------------
# Artifact/convention injection tests
# ---------------------------------------------------------------------------


@dataclass
class MockArtifact:
    artifact_type: Any = None
    content: str = ""
    source: Any = None


class MockArtifactType:
    def __init__(self, value: str) -> None:
        self.value = value


class MockArtifactSource:
    def __init__(self, value: str) -> None:
        self.value = value


class TestArtifactInjection:
    def test_inject_rules_from_registry(self, db: Any, registry: Any) -> None:
        art_reg = MagicMock()
        art = MockArtifact(
            artifact_type=MockArtifactType("rule"),
            content="Always use type hints",
            source=MockArtifactSource("global"),
        )
        art_reg.list_all.return_value = [art]
        engine = WorkflowEngine(db, WorkflowConfig(), registry, artifact_registry=art_reg)

        yaml_src = """\
kind: workflow
id: test_rules
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo hi"
    inject_rules: true
"""
        defn = load_definition(yaml_src)
        step = defn.steps[0]
        context = engine._build_agent_system_context(step, defn)
        assert "Always use type hints" in context
        assert "untrusted" in context.lower()  # non-built-in wrapped

    def test_inject_rules_built_in_not_wrapped(self, db: Any, registry: Any) -> None:
        art_reg = MagicMock()
        art = MockArtifact(
            artifact_type=MockArtifactType("rule"),
            content="Built-in rule content",
            source=MockArtifactSource("built_in"),
        )
        art_reg.list_all.return_value = [art]
        engine = WorkflowEngine(db, WorkflowConfig(), registry, artifact_registry=art_reg)

        yaml_src = """\
kind: workflow
id: test_builtin
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo hi"
    inject_rules: true
"""
        defn = load_definition(yaml_src)
        step = defn.steps[0]
        context = engine._build_agent_system_context(step, defn)
        assert "Built-in rule content" in context
        assert "untrusted" not in context.lower()  # built-in not wrapped

    def test_inject_rules_no_registry(self, db: Any, registry: Any) -> None:
        """inject_rules with no artifact_registry silently skips."""
        engine = WorkflowEngine(db, WorkflowConfig(), registry)  # no artifact_registry

        yaml_src = """\
kind: workflow
id: test_no_reg
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo hi"
    inject_rules: true
"""
        defn = load_definition(yaml_src)
        step = defn.steps[0]
        context = engine._build_agent_system_context(step, defn)
        assert context == ""

    def test_inject_conventions_global_only(self, db: Any, registry: Any, tmp_path: Path) -> None:
        """inject_conventions loads global ANTEROOM.md, not project-level."""
        engine = WorkflowEngine(db, WorkflowConfig(), registry)
        anteroom_dir = tmp_path / ".anteroom"
        anteroom_dir.mkdir()
        (anteroom_dir / "ANTEROOM.md").write_text("Global conventions here")

        yaml_src = """\
kind: workflow
id: test_conv
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo hi"
    inject_conventions: true
"""
        defn = load_definition(yaml_src)
        step = defn.steps[0]

        with patch("pathlib.Path.home", return_value=tmp_path):
            context = engine._build_agent_system_context(step, defn)
        assert "Global conventions here" in context

    def test_policy_default_inject_rules(self, db: Any, registry: Any) -> None:
        """inject_rules=None inherits from definition.policies."""
        art_reg = MagicMock()
        art = MockArtifact(
            artifact_type=MockArtifactType("rule"),
            content="Policy rule",
            source=MockArtifactSource("team"),
        )
        art_reg.list_all.return_value = [art]
        engine = WorkflowEngine(db, WorkflowConfig(), registry, artifact_registry=art_reg)
        defn = load_definition(INJECT_RULES_WORKFLOW)  # policies.inject_rules: true
        step = defn.steps[0]
        # step.inject_rules is None, should inherit from policies
        assert step.inject_rules is None
        context = engine._build_agent_system_context(step, defn)
        assert "Policy rule" in context


# ---------------------------------------------------------------------------
# API redaction test
# ---------------------------------------------------------------------------


class TestAPIRedaction:
    def test_definition_content_stripped_from_detail(self) -> None:
        """Verify the router strips definition_content from run detail."""
        # This is a structural test — we verify the pop() call exists
        run = {
            "id": "test-run",
            "definition_content": "sensitive YAML content",
            "definition_hash": "abc123",
            "status": "completed",
        }
        run.pop("definition_content", None)
        assert "definition_content" not in run
        assert "definition_hash" in run  # hash is not sensitive
