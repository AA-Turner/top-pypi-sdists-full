"""Tests for ``check_referenced_paths()``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.verify_artifacts import CHECK_REFERENCED_PATH, check_referenced_paths


class TestCheckReferencedPaths:
    """Verifying that referenced repository paths exist."""

    def test_no_violation_when_reference_exists(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        (repo_root / "pkg").mkdir(parents=True)
        (repo_root / "pkg" / "mod.py").write_text("", encoding="utf-8")
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text("Update `pkg/mod.py` now.\n", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_flags_missing_reference(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text("Update `pkg/absent.py` now.\n", encoding="utf-8")

        violations = check_referenced_paths(spec_dir, repo_root, ("plan.md",))

        assert len(violations) == 1
        assert violations[0].check == CHECK_REFERENCED_PATH
        assert violations[0].artifact == "plan.md"
        assert "pkg/absent.py" in violations[0].detail

    def test_skips_reference_the_plan_intends_to_create(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text("Create `pkg/new_module.py` for this.\n", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_skips_shell_variable_interpolation(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text('SPEC_FILE="$OUT_DIR/notes.md"\n', encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_skips_spec_directory_artifacts(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text("See `spec.md` and `checklists/x.md`.\n", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_reports_a_repeated_missing_path_once(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text(
            "Update `pkg/absent.py` here.\nAlso touch `pkg/absent.py` there.\n",
            encoding="utf-8",
        )

        assert len(check_referenced_paths(spec_dir, repo_root, ("plan.md",))) == 1

    def test_scans_every_requested_artifact(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text("Update `pkg/a.py` now.\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("Update `pkg/b.py` now.\n", encoding="utf-8")

        violations = check_referenced_paths(spec_dir, repo_root, ("plan.md", "tasks.md"))

        assert {v.artifact for v in violations} == {"plan.md", "tasks.md"}

    def test_ignores_absent_artifact(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_only_skips_the_reference_marked_for_creation(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text(
            "Create `pkg/new.py` and update `pkg/missing.py`.\n",
            encoding="utf-8",
        )

        violations = check_referenced_paths(spec_dir, repo_root, ("plan.md",))

        assert len(violations) == 1
        assert "pkg/missing.py" in violations[0].detail

    def test_skips_created_reference_when_path_contains_a_clause_keyword(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text(
            "Create docs/and/file.py and update `pkg/existing.py`.\n",
            encoding="utf-8",
        )
        (repo_root / "pkg").mkdir(parents=True)
        (repo_root / "pkg" / "existing.py").write_text("", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_accepts_existing_reference_with_anchor_suffix(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        (repo_root / "pkg").mkdir(parents=True)
        (repo_root / "pkg" / "mod.py").write_text("", encoding="utf-8")
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text("Update `pkg/mod.py#L12` now.\n", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_tasks_md_flags_missing_spec_artifact_reference(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text("Review `contracts/api.md` for consistency.\n", encoding="utf-8")

        violations = check_referenced_paths(spec_dir, repo_root, ("tasks.md",))

        assert len(violations) == 1
        assert violations[0].check == CHECK_REFERENCED_PATH
        assert violations[0].artifact == "tasks.md"
        assert "contracts/api.md" in violations[0].detail

    def test_tasks_md_accepts_existing_spec_artifact_reference(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        (spec_dir / "contracts").mkdir(parents=True)
        (spec_dir / "contracts" / "api.md").write_text("# API\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("Review `contracts/api.md` for consistency.\n", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("tasks.md",)) == []

    def test_tasks_md_accepts_existing_non_markdown_spec_artifact_reference(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        (spec_dir / "contracts").mkdir(parents=True)
        (spec_dir / "contracts" / "openapi.yaml").write_text("openapi: 3.1.0\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("Review `contracts/openapi.yaml` for consistency.\n", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("tasks.md",)) == []

    def test_tasks_md_flags_gitignored_spec_artifact_reference(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "research.md").write_text("# Research\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("Review `research.md` for consistency.\n", encoding="utf-8")

        with patch("agentic_devtools.cli.speckit.verify_artifacts.is_gitignored", return_value=True):
            violations = check_referenced_paths(spec_dir, repo_root, ("tasks.md",))

        assert len(violations) == 1
        assert violations[0].check == CHECK_REFERENCED_PATH
        assert violations[0].artifact == "tasks.md"
        assert "research.md" in violations[0].detail

    def test_skips_non_checkable_reference_tokens(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text("See `https://example.com/spec.md`.\n", encoding="utf-8")

        assert check_referenced_paths(spec_dir, repo_root, ("tasks.md",)) == []

    def test_ignores_shadowed_basenames_from_existing_full_paths(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        (repo_root / ".github" / "workflows").mkdir(parents=True)
        (repo_root / ".github" / "workflows" / "ai-pr-loop.yml").write_text("", encoding="utf-8")
        (repo_root / "docs").mkdir(parents=True)
        (repo_root / "docs" / "agdt-cli-reference.md").write_text("", encoding="utf-8")
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "plan.md").write_text(
            "Update `.github/workflows/ai-pr-loop.yml` and `docs/agdt-cli-reference.md`.\n",
            encoding="utf-8",
        )

        assert check_referenced_paths(spec_dir, repo_root, ("plan.md",)) == []

    def test_skips_illustrative_example_references(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text(
            "Create `tests/unit/a/` with per-symbol files (e.g. `test_a.py`, `test_b.py`).\n",
            encoding="utf-8",
        )

        assert check_referenced_paths(spec_dir, repo_root, ("tasks.md",)) == []

    def test_reports_repeated_path_when_only_one_occurrence_is_illustrative(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text(
            "For example, inspect `missing.py`; then update `missing.py`.\n",
            encoding="utf-8",
        )

        violations = check_referenced_paths(spec_dir, repo_root, ("tasks.md",))

        assert len(violations) == 1
        assert "missing.py" in violations[0].detail

    def test_reports_repeated_markdown_link_path_when_only_one_occurrence_is_illustrative(
        self,
        tmp_path: Path,
    ) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text(
            "For example, inspect [sample](missing.py); then update [required](missing.py).\n",
            encoding="utf-8",
        )

        violations = check_referenced_paths(spec_dir, repo_root, ("tasks.md",))

        assert len(violations) == 1
        assert "missing.py" in violations[0].detail

    def test_reports_repeated_unquoted_path_when_only_one_occurrence_is_illustrative(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text(
            "For example, inspect missing.py; then update missing.py.\n",
            encoding="utf-8",
        )

        violations = check_referenced_paths(spec_dir, repo_root, ("tasks.md",))

        assert len(violations) == 1
        assert "missing.py" in violations[0].detail

    def test_reports_repeated_created_then_updated_path_when_only_later_occurrence_is_required(
        self,
        tmp_path: Path,
    ) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text(
            "For example, create `missing.py` and update `missing.py`.\n",
            encoding="utf-8",
        )

        violations = check_referenced_paths(spec_dir, repo_root, ("tasks.md",))

        assert len(violations) == 1
        assert "missing.py" in violations[0].detail

    def test_ignores_plain_illustrative_reference(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text(
            "Create files (e.g. test_a.py) in the package.\n",
            encoding="utf-8",
        )

        assert check_referenced_paths(spec_dir, repo_root, ("tasks.md",)) == []

    def test_ignores_second_plain_illustrative_reference_in_parenthetical_list(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        spec_dir = repo_root / "specs" / "001-x"
        spec_dir.mkdir(parents=True)
        (spec_dir / "tasks.md").write_text(
            "Create files (e.g. test_a.py and test_b.py) in the package.\n",
            encoding="utf-8",
        )

        assert check_referenced_paths(spec_dir, repo_root, ("tasks.md",)) == []
