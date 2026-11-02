"""Tests for ``check_unmapped_test_tasks()``."""

from pathlib import Path

from agentic_devtools.cli.speckit.verify_artifacts import (
    CHECK_UNMAPPED_TEST_TASK,
    check_unmapped_test_tasks,
)

_SPEC = """# Feature

## Requirements

- **FR-001**: The system MUST do the thing.
"""


class TestCheckUnmappedTestTasks:
    """Tracing test tasks back to a requirement."""

    def test_no_violation_when_test_task_references_an_fr(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "tasks.md").write_text(
            "- [ ] T001 Add unit test for FR-001 in tests/unit/x/test_a.py\n",
            encoding="utf-8",
        )

        assert check_unmapped_test_tasks(tmp_path) == []

    def test_flags_test_task_without_a_requirement(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "tasks.md").write_text(
            "- [ ] T001 Add unit test coverage for the new helper\n",
            encoding="utf-8",
        )

        violations = check_unmapped_test_tasks(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_UNMAPPED_TEST_TASK
        assert violations[0].artifact == "tasks.md"
        assert "T001" in violations[0].detail

    def test_returns_empty_when_spec_is_absent(self, tmp_path: Path) -> None:
        (tmp_path / "tasks.md").write_text("- [ ] T001 Add unit test\n", encoding="utf-8")

        assert check_unmapped_test_tasks(tmp_path) == []

    def test_returns_empty_when_tasks_are_absent(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")

        assert check_unmapped_test_tasks(tmp_path) == []

    def test_flags_test_tasks_when_spec_defines_no_requirements(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text("# Feature\n", encoding="utf-8")
        (tmp_path / "tasks.md").write_text(
            "- [ ] T001 Add unit test coverage for the new helper\n",
            encoding="utf-8",
        )

        violations = check_unmapped_test_tasks(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_UNMAPPED_TEST_TASK
        assert "T001" in violations[0].detail
        assert "defines no FR-NNN entries" in violations[0].detail

    def test_ignores_non_test_tasks_when_spec_defines_no_requirements(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text("# Feature\n", encoding="utf-8")
        (tmp_path / "tasks.md").write_text(
            "- [ ] T001 Implement the helper in agentic_devtools/helper.py\n",
            encoding="utf-8",
        )

        assert check_unmapped_test_tasks(tmp_path) == []

    def test_ignores_implementation_tasks(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "tasks.md").write_text(
            "- [ ] T001 Implement the helper in agentic_devtools/helper.py\n",
            encoding="utf-8",
        )

        assert check_unmapped_test_tasks(tmp_path) == []

    def test_uses_spec_context_when_no_local_spec_md(self, tmp_path: Path) -> None:
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        spec_dir = tmp_path / "task-spec"
        spec_dir.mkdir()
        (spec_dir / "tasks.md").write_text(
            "- [ ] T001 Add unit test for FR-001 in tests/unit/x/test_a.py\n",
            encoding="utf-8",
        )

        assert check_unmapped_test_tasks(spec_dir, spec_context=spec_context) == []

    def test_spec_context_detects_unmapped_task_when_no_local_spec_md(self, tmp_path: Path) -> None:
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        spec_dir = tmp_path / "task-spec"
        spec_dir.mkdir()
        (spec_dir / "tasks.md").write_text(
            "- [ ] T001 Add unit test coverage for the new helper\n",
            encoding="utf-8",
        )

        violations = check_unmapped_test_tasks(spec_dir, spec_context=spec_context)

        assert len(violations) == 1
        assert violations[0].check == CHECK_UNMAPPED_TEST_TASK

    def test_spec_context_takes_precedence_over_local_spec_md(self, tmp_path: Path) -> None:
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        # Local spec.md deliberately absent so spec_context is the sole source
        (tmp_path / "tasks.md").write_text(
            "- [ ] T001 Add unit test for FR-001 in tests/unit/x/test_a.py\n",
            encoding="utf-8",
        )

        assert check_unmapped_test_tasks(tmp_path, spec_context=spec_context) == []
