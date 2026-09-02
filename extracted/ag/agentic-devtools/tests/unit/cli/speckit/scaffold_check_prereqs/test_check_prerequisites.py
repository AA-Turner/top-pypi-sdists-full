"""Tests for ``check_prerequisites``."""

from pathlib import Path

import pytest

from agentic_devtools.cli.speckit.scaffold_check_prereqs import check_prerequisites


class TestCheckPrerequisites:
    """check_prerequisites validates required docs and reports available ones."""

    def test_raises_when_feature_dir_missing(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="Run agdt-speckit-specify first"):
            check_prerequisites(tmp_path / "specs" / "042-x", require_tasks=False, include_tasks=False)

    def test_raises_when_plan_md_missing(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)

        with pytest.raises(FileNotFoundError, match="Run agdt-speckit-plan first"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

    def test_raises_when_tasks_required_but_missing(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        with pytest.raises(FileNotFoundError, match="Run agdt-speckit-tasks first"):
            check_prerequisites(feature_dir, require_tasks=True, include_tasks=False)

    def test_reports_available_optional_docs(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (feature_dir / "spec.md").write_text("spec", encoding="utf-8")
        (feature_dir / "research.md").write_text("research", encoding="utf-8")

        result = check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

        assert result.feature_dir == feature_dir
        assert result.available_docs == ["spec.md", "research.md"]

    def test_reports_contracts_dir_when_non_empty(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        contracts_dir = feature_dir / "contracts"
        contracts_dir.mkdir()
        (contracts_dir / "api.yaml").write_text("openapi: 3.0.0", encoding="utf-8")

        result = check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

        assert "contracts/" in result.available_docs

    def test_omits_tasks_md_when_include_tasks_false(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (feature_dir / "tasks.md").write_text("tasks", encoding="utf-8")

        result = check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

        assert "tasks.md" not in result.available_docs

    def test_includes_tasks_md_when_include_tasks_true(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (feature_dir / "tasks.md").write_text("tasks", encoding="utf-8")

        result = check_prerequisites(feature_dir, require_tasks=False, include_tasks=True)

        assert "tasks.md" in result.available_docs

    def test_include_tasks_true_but_tasks_missing_is_omitted(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")

        result = check_prerequisites(feature_dir, require_tasks=False, include_tasks=True)

        assert "tasks.md" not in result.available_docs

    def test_raises_when_plan_md_is_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        external_plan = tmp_path / "external-plan.md"
        external_plan.write_text("plan", encoding="utf-8")
        (feature_dir / "plan.md").symlink_to(external_plan)

        with pytest.raises(ValueError, match="Refusing symlinked plan.md"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

    def test_raises_when_plan_md_is_broken_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").symlink_to(tmp_path / "missing-plan.md")

        with pytest.raises(ValueError, match="Refusing symlinked plan.md"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

    def test_raises_when_tasks_md_is_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        external_tasks = tmp_path / "external-tasks.md"
        external_tasks.write_text("tasks", encoding="utf-8")
        (feature_dir / "tasks.md").symlink_to(external_tasks)

        with pytest.raises(ValueError, match="Refusing symlinked tasks.md"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=True)

    def test_raises_when_tasks_md_is_broken_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (feature_dir / "tasks.md").symlink_to(tmp_path / "missing-tasks.md")

        with pytest.raises(ValueError, match="Refusing symlinked tasks.md"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=True)

    def test_raises_when_optional_doc_is_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        external_spec = tmp_path / "external-spec.md"
        external_spec.write_text("spec", encoding="utf-8")
        (feature_dir / "spec.md").symlink_to(external_spec)

        with pytest.raises(ValueError, match="Refusing symlinked spec.md"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

    def test_raises_when_optional_doc_is_broken_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        (feature_dir / "spec.md").symlink_to(tmp_path / "does-not-exist.md")

        with pytest.raises(ValueError, match="Refusing symlinked spec.md"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

    def test_raises_when_contracts_entry_is_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        contracts_dir = feature_dir / "contracts"
        contracts_dir.mkdir()
        external_contract = tmp_path / "external-contract.yaml"
        external_contract.write_text("openapi: 3.0.0", encoding="utf-8")
        (contracts_dir / "api.yaml").symlink_to(external_contract)

        with pytest.raises(ValueError, match="Refusing symlinked contracts/ entry"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)

    def test_raises_when_contracts_dir_is_symlink(self, tmp_path: Path) -> None:
        feature_dir = tmp_path / "specs" / "042-x"
        feature_dir.mkdir(parents=True)
        (feature_dir / "plan.md").write_text("plan", encoding="utf-8")
        external_contracts = tmp_path / "external-contracts"
        external_contracts.mkdir()
        (feature_dir / "contracts").symlink_to(external_contracts, target_is_directory=True)

        with pytest.raises(ValueError, match="Refusing symlinked contracts/"):
            check_prerequisites(feature_dir, require_tasks=False, include_tasks=False)
