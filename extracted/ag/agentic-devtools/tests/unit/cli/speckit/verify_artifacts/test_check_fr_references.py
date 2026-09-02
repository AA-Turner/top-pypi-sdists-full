"""Tests for ``check_fr_references()``."""

from pathlib import Path

from agentic_devtools.cli.speckit.verify_artifacts import CHECK_FR_REFERENCE, check_fr_references

_SPEC = "# Feature\n\n- **FR-001**: Do a thing.\n- **FR-002**: Do another thing.\n"


class TestCheckFrReferences:
    """Every downstream FR-NNN must be defined in ``spec.md``."""

    def test_no_violation_when_every_fr_is_defined(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "tasks.md").write_text("T001 covers FR-001 and FR-002.\n", encoding="utf-8")

        assert check_fr_references(tmp_path) == []

    def test_flags_undefined_fr_in_tasks(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "tasks.md").write_text("T001 covers FR-009.\n", encoding="utf-8")

        violations = check_fr_references(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_FR_REFERENCE
        assert violations[0].artifact == "tasks.md"
        assert "FR-009" in violations[0].detail

    def test_flags_undefined_fr_in_test_coverage_report(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "test-coverage.json").write_text('{"fr": "FR-042"}', encoding="utf-8")

        violations = check_fr_references(tmp_path)

        assert [v.artifact for v in violations] == ["test-coverage.json"]

    def test_flags_undefined_fr_in_generated_test_coverage_report(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        generated = tmp_path / "generated"
        generated.mkdir()
        (generated / "test-coverage.json").write_text('{"fr": "FR-042"}', encoding="utf-8")

        violations = check_fr_references(tmp_path)

        assert [v.artifact for v in violations] == ["test-coverage.json"]

    def test_reports_undefined_frs_in_numeric_order(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "tasks.md").write_text("FR-010 then FR-003.\n", encoding="utf-8")

        details = [v.detail for v in check_fr_references(tmp_path)]

        assert "FR-003" in details[0]
        assert "FR-010" in details[1]

    def test_matches_fr_ids_case_insensitively(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")
        (tmp_path / "tasks.md").write_text("fr-001 is covered.\n", encoding="utf-8")

        assert check_fr_references(tmp_path) == []

    def test_returns_empty_when_spec_is_absent(self, tmp_path: Path) -> None:
        (tmp_path / "tasks.md").write_text("FR-009.\n", encoding="utf-8")

        assert check_fr_references(tmp_path) == []

    def test_returns_empty_when_downstream_artifacts_are_absent(self, tmp_path: Path) -> None:
        (tmp_path / "spec.md").write_text(_SPEC, encoding="utf-8")

        assert check_fr_references(tmp_path) == []

    def test_uses_spec_context_when_no_local_spec_md(self, tmp_path: Path) -> None:
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        spec_dir = tmp_path / "task-spec"
        spec_dir.mkdir()
        (spec_dir / "tasks.md").write_text("T001 covers FR-001.\n", encoding="utf-8")

        assert check_fr_references(spec_dir, spec_context=spec_context) == []

    def test_spec_context_flags_undefined_fr_when_no_local_spec_md(self, tmp_path: Path) -> None:
        spec_context = tmp_path / "parent-spec.md"
        spec_context.write_text(_SPEC, encoding="utf-8")
        spec_dir = tmp_path / "task-spec"
        spec_dir.mkdir()
        (spec_dir / "tasks.md").write_text("T001 covers FR-099.\n", encoding="utf-8")

        violations = check_fr_references(spec_dir, spec_context=spec_context)

        assert len(violations) == 1
        assert violations[0].check == CHECK_FR_REFERENCE
        assert "FR-099" in violations[0].detail
