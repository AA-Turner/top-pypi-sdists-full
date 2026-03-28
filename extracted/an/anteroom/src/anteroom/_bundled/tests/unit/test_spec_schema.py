"""Unit tests for spec_schema — parsing, validation, serialization, phase metadata."""

from __future__ import annotations

import pytest

from anteroom.services.spec_schema import (
    CREATION_FLOW_FROM_ISSUE,
    CREATION_FLOW_MANUAL,
    CREATION_FLOW_PROMPT,
    SPEC_GENERATION_SCHEMA,
    SpecContent,
    SpecPhaseStatus,
    SpecTask,
    SpecValidationError,
    default_phase_metadata,
    get_phase_status,
    parse_spec_content,
    serialize_spec_content,
    set_phase_status,
    topological_sort_tasks,
)

# ---------------------------------------------------------------------------
# Valid spec YAML fixtures
# ---------------------------------------------------------------------------

VALID_SPEC = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
"""

MINIMAL_SPEC = """\
requirements: "req"
design: "des"
tasks:
  - id: t1
    summary: "do it"
"""


# ---------------------------------------------------------------------------
# Parsing — happy path
# ---------------------------------------------------------------------------


class TestParseSpecContent:
    def test_valid_spec(self) -> None:
        spec = parse_spec_content(VALID_SPEC)
        assert isinstance(spec, SpecContent)
        assert "widgets" in spec.requirements
        assert "widget parser" in spec.design
        assert len(spec.tasks) == 2
        assert spec.tasks[0].id == "t1"
        assert spec.tasks[1].depends_on == ["t1"]

    def test_minimal_spec(self) -> None:
        spec = parse_spec_content(MINIMAL_SPEC)
        assert spec.requirements == "req"
        assert spec.design == "des"
        assert len(spec.tasks) == 1

    def test_extra_fields_ignored(self) -> None:
        yaml_str = MINIMAL_SPEC + "extra_field: ignored\n"
        spec = parse_spec_content(yaml_str)
        assert len(spec.tasks) == 1

    def test_task_without_depends_on(self) -> None:
        spec = parse_spec_content(MINIMAL_SPEC)
        assert spec.tasks[0].depends_on == []


# ---------------------------------------------------------------------------
# Parsing — error cases
# ---------------------------------------------------------------------------


class TestParseSpecContentErrors:
    def test_invalid_yaml(self) -> None:
        with pytest.raises(SpecValidationError, match="Invalid YAML"):
            parse_spec_content("{ invalid yaml")

    def test_not_a_mapping(self) -> None:
        with pytest.raises(SpecValidationError, match="YAML mapping"):
            parse_spec_content("- list item")

    def test_missing_requirements(self) -> None:
        with pytest.raises(SpecValidationError, match="requirements"):
            parse_spec_content("design: x\ntasks:\n  - id: t1\n    summary: s\n")

    def test_empty_requirements(self) -> None:
        with pytest.raises(SpecValidationError, match="requirements"):
            parse_spec_content('requirements: ""\ndesign: x\ntasks:\n  - id: t1\n    summary: s\n')

    def test_missing_design(self) -> None:
        with pytest.raises(SpecValidationError, match="design"):
            parse_spec_content("requirements: x\ntasks:\n  - id: t1\n    summary: s\n")

    def test_empty_design(self) -> None:
        with pytest.raises(SpecValidationError, match="design"):
            parse_spec_content('requirements: x\ndesign: "  "\ntasks:\n  - id: t1\n    summary: s\n')

    def test_tasks_not_list(self) -> None:
        with pytest.raises(SpecValidationError, match="tasks.*list"):
            parse_spec_content("requirements: x\ndesign: y\ntasks: not-a-list\n")

    def test_task_not_mapping(self) -> None:
        with pytest.raises(SpecValidationError, match="Task at index 0.*mapping"):
            parse_spec_content("requirements: x\ndesign: y\ntasks:\n  - just a string\n")

    def test_task_missing_id(self) -> None:
        with pytest.raises(SpecValidationError, match="non-empty string 'id'"):
            parse_spec_content("requirements: x\ndesign: y\ntasks:\n  - summary: s\n")

    def test_task_empty_id(self) -> None:
        with pytest.raises(SpecValidationError, match="non-empty string 'id'"):
            parse_spec_content('requirements: x\ndesign: y\ntasks:\n  - id: ""\n    summary: s\n')

    def test_task_missing_summary(self) -> None:
        with pytest.raises(SpecValidationError, match="non-empty string 'summary'"):
            parse_spec_content("requirements: x\ndesign: y\ntasks:\n  - id: t1\n")

    def test_task_depends_on_not_list(self) -> None:
        with pytest.raises(SpecValidationError, match="depends_on.*list of strings"):
            parse_spec_content("requirements: x\ndesign: y\ntasks:\n  - id: t1\n    summary: s\n    depends_on: t2\n")

    def test_duplicate_task_ids(self) -> None:
        yaml_str = "requirements: x\ndesign: y\ntasks:\n  - id: t1\n    summary: a\n  - id: t1\n    summary: b\n"
        with pytest.raises(SpecValidationError, match="Duplicate task ID.*t1"):
            parse_spec_content(yaml_str)

    def test_unknown_dependency(self) -> None:
        yaml_str = "requirements: x\ndesign: y\ntasks:\n  - id: t1\n    summary: a\n    depends_on: [t99]\n"
        with pytest.raises(SpecValidationError, match="depends on unknown task.*t99"):
            parse_spec_content(yaml_str)

    def test_circular_dependency(self) -> None:
        yaml_str = (
            "requirements: x\ndesign: y\ntasks:\n"
            "  - id: t1\n    summary: a\n    depends_on: [t2]\n"
            "  - id: t2\n    summary: b\n    depends_on: [t1]\n"
        )
        with pytest.raises(SpecValidationError, match="Circular dependency"):
            parse_spec_content(yaml_str)

    def test_self_dependency(self) -> None:
        yaml_str = "requirements: x\ndesign: y\ntasks:\n  - id: t1\n    summary: a\n    depends_on: [t1]\n"
        with pytest.raises(SpecValidationError, match="Circular dependency"):
            parse_spec_content(yaml_str)


# ---------------------------------------------------------------------------
# Serialization round-trip
# ---------------------------------------------------------------------------


class TestSerialize:
    def test_round_trip(self) -> None:
        spec = parse_spec_content(VALID_SPEC)
        yaml_out = serialize_spec_content(spec)
        spec2 = parse_spec_content(yaml_out)
        assert spec.requirements == spec2.requirements
        assert spec.design == spec2.design
        assert len(spec.tasks) == len(spec2.tasks)
        for t1, t2 in zip(spec.tasks, spec2.tasks):
            assert t1.id == t2.id
            assert t1.summary == t2.summary
            assert t1.depends_on == t2.depends_on

    def test_depends_on_omitted_when_empty(self) -> None:
        spec = SpecContent(requirements="r", design="d", tasks=[SpecTask(id="t1", summary="s")])
        yaml_out = serialize_spec_content(spec)
        assert "depends_on" not in yaml_out


# ---------------------------------------------------------------------------
# Phase metadata helpers
# ---------------------------------------------------------------------------


class TestPhaseMetadata:
    def test_default_metadata(self) -> None:
        meta = default_phase_metadata()
        assert set(meta["phases"].keys()) == {"requirements", "design", "tasks"}
        for phase_data in meta["phases"].values():
            assert phase_data["status"] == "draft"
            assert phase_data["approved_at"] is None
            assert phase_data["approved_by"] is None

    def test_get_phase_status_draft(self) -> None:
        meta = default_phase_metadata()
        assert get_phase_status(meta, "requirements") == SpecPhaseStatus.DRAFT

    def test_get_phase_status_missing_phases_key(self) -> None:
        assert get_phase_status({}, "requirements") == SpecPhaseStatus.DRAFT

    def test_get_phase_status_invalid_phase(self) -> None:
        with pytest.raises(ValueError, match="Invalid phase name"):
            get_phase_status({}, "nonexistent")

    def test_set_phase_approved(self) -> None:
        meta = default_phase_metadata()
        updated = set_phase_status(meta, "design", SpecPhaseStatus.APPROVED, approved_by="troy")
        assert updated["phases"]["design"]["status"] == "approved"
        assert updated["phases"]["design"]["approved_by"] == "troy"
        assert updated["phases"]["design"]["approved_at"] is not None
        # Original unchanged
        assert meta["phases"]["design"]["status"] == "draft"

    def test_set_phase_draft_clears_approval(self) -> None:
        meta = default_phase_metadata()
        meta = set_phase_status(meta, "design", SpecPhaseStatus.APPROVED, approved_by="troy")
        meta = set_phase_status(meta, "design", SpecPhaseStatus.DRAFT)
        assert meta["phases"]["design"]["status"] == "draft"
        assert meta["phases"]["design"]["approved_at"] is None
        assert meta["phases"]["design"]["approved_by"] is None

    def test_set_phase_stale_preserves_approval_info(self) -> None:
        meta = default_phase_metadata()
        meta = set_phase_status(meta, "design", SpecPhaseStatus.APPROVED, approved_by="troy")
        approved_at = meta["phases"]["design"]["approved_at"]
        meta = set_phase_status(meta, "design", SpecPhaseStatus.STALE)
        assert meta["phases"]["design"]["status"] == "stale"
        assert meta["phases"]["design"]["approved_at"] == approved_at
        assert meta["phases"]["design"]["approved_by"] == "troy"

    def test_set_phase_invalid_name(self) -> None:
        with pytest.raises(ValueError, match="Invalid phase name"):
            set_phase_status({}, "invalid", SpecPhaseStatus.DRAFT)

    def test_set_phase_invalid_status(self) -> None:
        meta = default_phase_metadata()
        with pytest.raises(ValueError):
            set_phase_status(meta, "design", "invalid_status")

    def test_set_phase_with_string_status(self) -> None:
        meta = default_phase_metadata()
        updated = set_phase_status(meta, "requirements", "approved", approved_by="user")
        assert updated["phases"]["requirements"]["status"] == "approved"


# ---------------------------------------------------------------------------
# Constants (#1165)
# ---------------------------------------------------------------------------


class TestCreationFlowConstants:
    def test_creation_flow_prompt(self) -> None:
        assert CREATION_FLOW_PROMPT == "prompt"

    def test_creation_flow_from_issue(self) -> None:
        assert CREATION_FLOW_FROM_ISSUE == "from_issue"

    def test_creation_flow_manual(self) -> None:
        assert CREATION_FLOW_MANUAL == "manual"

    def test_spec_generation_schema_has_required_fields(self) -> None:
        assert "properties" in SPEC_GENERATION_SCHEMA
        props = SPEC_GENERATION_SCHEMA["properties"]
        assert "requirements" in props
        assert "design" in props
        assert "tasks" in props


# ---------------------------------------------------------------------------
# Topological sort (#1165)
# ---------------------------------------------------------------------------


class TestTopologicalSortTasks:
    def test_empty_list(self) -> None:
        assert topological_sort_tasks([]) == []

    def test_single_task(self) -> None:
        t = SpecTask(id="a", summary="A")
        result = topological_sort_tasks([t])
        assert result == [[t]]

    def test_all_independent(self) -> None:
        a = SpecTask(id="a", summary="A")
        b = SpecTask(id="b", summary="B")
        c = SpecTask(id="c", summary="C")
        result = topological_sort_tasks([a, b, c])
        assert len(result) == 1
        assert set(t.id for t in result[0]) == {"a", "b", "c"}

    def test_linear_chain(self) -> None:
        a = SpecTask(id="a", summary="A")
        b = SpecTask(id="b", summary="B", depends_on=["a"])
        c = SpecTask(id="c", summary="C", depends_on=["b"])
        result = topological_sort_tasks([a, b, c])
        assert len(result) == 3
        assert [t.id for t in result[0]] == ["a"]
        assert [t.id for t in result[1]] == ["b"]
        assert [t.id for t in result[2]] == ["c"]

    def test_diamond(self) -> None:
        a = SpecTask(id="a", summary="A")
        b = SpecTask(id="b", summary="B", depends_on=["a"])
        c = SpecTask(id="c", summary="C", depends_on=["a"])
        d = SpecTask(id="d", summary="D", depends_on=["b", "c"])
        result = topological_sort_tasks([a, b, c, d])
        assert len(result) == 3
        assert [t.id for t in result[0]] == ["a"]
        assert set(t.id for t in result[1]) == {"b", "c"}
        assert [t.id for t in result[2]] == ["d"]

    def test_complex_dag(self) -> None:
        a = SpecTask(id="a", summary="A")
        b = SpecTask(id="b", summary="B")
        c = SpecTask(id="c", summary="C", depends_on=["a"])
        d = SpecTask(id="d", summary="D", depends_on=["a", "b"])
        e = SpecTask(id="e", summary="E", depends_on=["c", "d"])
        result = topological_sort_tasks([a, b, c, d, e])
        assert len(result) == 3
        assert set(t.id for t in result[0]) == {"a", "b"}
        assert set(t.id for t in result[1]) == {"c", "d"}
        assert [t.id for t in result[2]] == ["e"]

    def test_preserves_task_objects(self) -> None:
        a = SpecTask(id="a", summary="A")
        b = SpecTask(id="b", summary="B", depends_on=["a"])
        result = topological_sort_tasks([a, b])
        assert result[0][0] is a
        assert result[1][0] is b

    def test_two_independent_chains(self) -> None:
        a = SpecTask(id="a", summary="A")
        b = SpecTask(id="b", summary="B", depends_on=["a"])
        c = SpecTask(id="c", summary="C")
        d = SpecTask(id="d", summary="D", depends_on=["c"])
        result = topological_sort_tasks([a, b, c, d])
        assert len(result) == 2
        assert set(t.id for t in result[0]) == {"a", "c"}
        assert set(t.id for t in result[1]) == {"b", "d"}

    def test_wide_fan_out(self) -> None:
        root = SpecTask(id="root", summary="Root")
        leaves = [SpecTask(id=f"l{i}", summary=f"Leaf {i}", depends_on=["root"]) for i in range(5)]
        result = topological_sort_tasks([root] + leaves)
        assert len(result) == 2
        assert result[0][0].id == "root"
        assert len(result[1]) == 5

    def test_fan_in(self) -> None:
        sources = [SpecTask(id=f"s{i}", summary=f"Source {i}") for i in range(3)]
        sink = SpecTask(id="sink", summary="Sink", depends_on=["s0", "s1", "s2"])
        result = topological_sort_tasks(sources + [sink])
        assert len(result) == 2
        assert len(result[0]) == 3
        assert result[1][0].id == "sink"
