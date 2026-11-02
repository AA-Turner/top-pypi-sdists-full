"""Tests for ``check_advertised_artifacts()``."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.verify_artifacts import (
    CHECK_ADVERTISED_ARTIFACT,
    check_advertised_artifacts,
)


class TestCheckAdvertisedArtifacts:
    """Every spec artifact named by ``plan.md`` must have been produced."""

    def test_no_violation_when_advertised_artifact_exists(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `research.md` for detail.\n", encoding="utf-8")
        (tmp_path / "research.md").write_text("# Research\n", encoding="utf-8")

        assert check_advertised_artifacts(tmp_path) == []

    def test_flags_advertised_artifact_that_was_not_produced(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `research.md` for detail.\n", encoding="utf-8")

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_ADVERTISED_ARTIFACT
        assert violations[0].artifact == "plan.md"
        assert "research.md" in violations[0].detail

    def test_accepts_generated_diagnostic_written_under_generated(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `analysis-report.md`.\n", encoding="utf-8")
        generated = tmp_path / "generated"
        generated.mkdir()
        (generated / "analysis-report.md").write_text("# Analysis\n", encoding="utf-8")

        assert check_advertised_artifacts(tmp_path) == []

    def test_generated_fallback_does_not_satisfy_non_relocated_artifact(self, tmp_path: Path) -> None:
        """A file under generated/ must not satisfy a missing non-generated artifact like spec.md."""
        (tmp_path / "plan.md").write_text("See `spec.md` for the specification.\n", encoding="utf-8")
        generated = tmp_path / "generated"
        generated.mkdir()
        (generated / "spec.md").write_text("# Spec\n", encoding="utf-8")

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert "spec.md" in violations[0].detail

    def test_flags_relocated_diagnostic_missing_from_both_root_and_generated(self, tmp_path: Path) -> None:
        """A relocated artifact that exists in neither root nor generated/ still raises a violation."""
        (tmp_path / "plan.md").write_text("See `analysis-report.md` for details.\n", encoding="utf-8")
        # Neither root nor generated/ contains the file.

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert "analysis-report.md" in violations[0].detail

    def test_flags_missing_artifact_in_a_subdirectory(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `contracts/api.md`.\n", encoding="utf-8")

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert "contracts/api.md" in violations[0].detail

    def test_accepts_artifact_present_in_a_subdirectory(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `contracts/api.md`.\n", encoding="utf-8")
        (tmp_path / "contracts").mkdir()
        (tmp_path / "contracts" / "api.md").write_text("# API\n", encoding="utf-8")

        assert check_advertised_artifacts(tmp_path) == []

    def test_accepts_non_markdown_contract_artifact_present_in_a_subdirectory(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `contracts/openapi.yaml`.\n", encoding="utf-8")
        (tmp_path / "contracts").mkdir()
        (tmp_path / "contracts" / "openapi.yaml").write_text("openapi: 3.1.0\n", encoding="utf-8")

        assert check_advertised_artifacts(tmp_path) == []

    def test_reports_a_repeated_missing_artifact_once(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `research.md`.\nAgain see `research.md`.\n", encoding="utf-8")

        assert len(check_advertised_artifacts(tmp_path)) == 1

    def test_ignores_repository_paths(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("Update `agentic_devtools/x.py`.\n", encoding="utf-8")

        assert check_advertised_artifacts(tmp_path) == []

    def test_returns_empty_when_plan_is_absent(self, tmp_path: Path) -> None:
        assert check_advertised_artifacts(tmp_path) == []

    def test_flags_missing_artifact_advertised_via_markdown_link(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text(
            "Deliver [research.md](research.md) as the analysis artifact.\n",
            encoding="utf-8",
        )

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_ADVERTISED_ARTIFACT
        assert "research.md" in violations[0].detail

    def test_accepts_existing_artifact_when_link_contains_anchor(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text(
            "See [research](research.md#findings).\n",
            encoding="utf-8",
        )
        (tmp_path / "research.md").write_text("# Findings\n", encoding="utf-8")

        assert check_advertised_artifacts(tmp_path) == []

    def test_flags_artifact_reference_that_escapes_spec_directory(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text("See `contracts/../../README.md`.\n", encoding="utf-8")
        (tmp_path.parent / "README.md").write_text("outside spec dir\n", encoding="utf-8")

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_ADVERTISED_ARTIFACT
        assert "contracts/../../README.md" in violations[0].detail

    def test_ignores_negated_named_artifact_reference(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text(
            "No separate `research.md` artifact is committed for this plan.\n",
            encoding="utf-8",
        )

        assert check_advertised_artifacts(tmp_path) == []

    def test_ignores_negated_artifact_list(self, tmp_path: Path) -> None:
        (tmp_path / "plan.md").write_text(
            "No separate `research.md` or `quickstart.md` artifact is committed for this plan.\n",
            encoding="utf-8",
        )

        assert check_advertised_artifacts(tmp_path) == []

    def test_flags_artifact_that_exists_but_is_gitignored(self, tmp_path: Path) -> None:
        """A file that exists on disk but is gitignored will not be committed.

        The gate must report a violation so the PR does not advertise an
        artifact that ``git add`` will silently omit (e.g. ``research.md``,
        ``data-model.md``, ``contracts/*`` are excluded by ``.gitignore``).
        """
        (tmp_path / "plan.md").write_text("See `research.md` for detail.\n", encoding="utf-8")
        (tmp_path / "research.md").write_text("# Research\n", encoding="utf-8")

        gitignored = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=gitignored,
        ):
            violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_ADVERTISED_ARTIFACT
        assert "research.md" in violations[0].detail

    def test_accepts_artifact_that_exists_and_is_not_gitignored(self, tmp_path: Path) -> None:
        """A file that exists and is not gitignored is committable — no violation."""
        (tmp_path / "plan.md").write_text("See `spec.md` for detail.\n", encoding="utf-8")
        (tmp_path / "spec.md").write_text("# Spec\n", encoding="utf-8")

        not_ignored = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
        with patch(
            "agentic_devtools.cli.speckit.verify_artifacts.subprocess.run",
            return_value=not_ignored,
        ):
            assert check_advertised_artifacts(tmp_path) == []

    def test_accepts_optional_artifact_annotated_in_tree_block(self, tmp_path: Path) -> None:
        """Artifacts annotated as 'Optional — only when …' in a tree block must not raise a violation.

        The plan-template emits a directory-tree section where optional artifacts carry an
        '# Optional — only when …' inline comment.  Agents that faithfully copy that tree
        into their plan.md must not be penalised for files that are legitimately absent.
        """
        tree = (
            "```text\n"
            "specs/001-feature/\n"
            "├── plan.md              # This file (always)\n"
            "├── spec.md              # Phase 1 (always)\n"
            "├── research.md          # Optional — only when there are unresolved technical unknowns\n"
            "├── data-model.md        # Optional — only when the feature introduces data entities\n"
            "├── quickstart.md        # Optional — only when a developer-facing walkthrough adds value\n"
            "├── contracts/           # Optional — only when the feature defines API contracts\n"
            "└── tasks.md             # Phase 4\n"
            "```\n"
        )
        (tmp_path / "plan.md").write_text(tree, encoding="utf-8")
        # spec.md and tasks.md are always-present; the optional ones are absent — no violation expected.
        (tmp_path / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (tmp_path / "tasks.md").write_text("# Tasks\n", encoding="utf-8")

        assert check_advertised_artifacts(tmp_path) == []

    def test_still_flags_non_optional_missing_artifact_alongside_optional_ones(self, tmp_path: Path) -> None:
        """A required artifact that is absent must still be reported even when optional ones are present."""
        (tmp_path / "plan.md").write_text(
            "See `spec.md` for the full specification.\n"
            "```text\n"
            "├── research.md          # Optional — only when there are unresolved technical unknowns\n"
            "```\n",
            encoding="utf-8",
        )
        # spec.md is absent; research.md is optional — only spec.md should be reported
        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert "spec.md" in violations[0].detail

    def test_flags_artifact_that_appears_optional_first_then_unconditionally(self, tmp_path: Path) -> None:
        """An artifact appearing first as optional and later as an unconditional promise must be flagged.

        When the same filename occurs first in the optional tree (conditional) and then again
        in the plan body as an unconditional reference, the conditional first occurrence must
        not permanently suppress the check.  The unconditional later occurrence is a promise.
        """
        content = (
            "```text\n"
            "├── research.md          # Optional — only when there are unresolved technical unknowns\n"
            "```\n"
            "\n"
            "See `research.md` for the Research Summary.\n"  # unconditional promise
        )
        (tmp_path / "plan.md").write_text(content, encoding="utf-8")
        # research.md is absent

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert "research.md" in violations[0].detail

    def test_flags_artifact_when_optional_backtick_mention_precedes_unconditional_backtick(
        self, tmp_path: Path
    ) -> None:
        """An unconditional promise must be flagged even when a backtick-quoted optional mention comes first.

        When a code-fence tree uses backtick-quoted filenames (e.g. ``├── `research.md`  # Optional …``)
        and a later prose line also uses a backtick-quoted reference unconditionally, the
        deduplication inside extract_references must not discard the later unconditional occurrence.
        """
        content = (
            "```text\n"
            "├── `research.md`          # Optional — only when there are unresolved technical unknowns\n"
            "```\n"
            "\n"
            "See `research.md` for the Research Summary.\n"  # unconditional promise
        )
        (tmp_path / "plan.md").write_text(content, encoding="utf-8")
        # research.md is absent

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert "research.md" in violations[0].detail

    def test_flags_artifact_when_negation_precedes_unconditional_promise(self, tmp_path: Path) -> None:
        """An unconditional promise must be flagged even when a negation precedes it.

        A plan that first says "No research.md is produced" and later
        unconditionally promises "See research.md" must still trigger a
        violation — the unconditional occurrence overrides the negation.
        """
        content = (
            "No separate `research.md` artifact is committed for this plan.\n"
            "\n"
            "See `research.md` for the Research Summary.\n"
        )
        (tmp_path / "plan.md").write_text(content, encoding="utf-8")
        # research.md is absent

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert "research.md" in violations[0].detail

    def test_flags_canonical_generated_path_when_file_absent(self, tmp_path: Path) -> None:
        """A canonical ``generated/analysis-report.md`` reference is a spec artifact.

        When ``plan.md`` references the canonical generated path and neither the
        canonical file nor the legacy root copy exists, a violation must be raised.
        """
        (tmp_path / "plan.md").write_text(
            "See `generated/analysis-report.md` for the analysis.\n",
            encoding="utf-8",
        )
        # Neither generated/analysis-report.md nor root analysis-report.md exists.

        violations = check_advertised_artifacts(tmp_path)

        assert len(violations) == 1
        assert violations[0].check == CHECK_ADVERTISED_ARTIFACT
        assert "generated/analysis-report.md" in violations[0].detail

    def test_accepts_canonical_generated_path_when_file_exists(self, tmp_path: Path) -> None:
        """A canonical ``generated/analysis-report.md`` reference is satisfied when the file exists."""
        generated_dir = tmp_path / "generated"
        generated_dir.mkdir()
        (generated_dir / "analysis-report.md").write_text("# Analysis\n", encoding="utf-8")
        (tmp_path / "plan.md").write_text(
            "See `generated/analysis-report.md` for the analysis.\n",
            encoding="utf-8",
        )

        assert check_advertised_artifacts(tmp_path) == []

    def test_phase_filter_suppresses_canonical_generated_analysis_report(self, tmp_path: Path) -> None:
        """The phase-3 filter must suppress ``generated/analysis-report.md`` just like the bare name.

        ``analysis-report.md`` is excluded from the phase-3 allowed set because it is
        produced in phase 5.  The same exclusion must apply to the canonical
        ``generated/analysis-report.md`` path so phase-3 checks don't raise a false violation.
        """
        from agentic_devtools.cli.speckit.verify_artifacts import (
            _PHASE3_ADVERTISED_ARTIFACT_FILENAMES,
            _PHASE3_ADVERTISED_GENERATED_ARTIFACT_FILENAMES,
        )

        (tmp_path / "plan.md").write_text(
            "See `generated/analysis-report.md` for the analysis.\n",
            encoding="utf-8",
        )
        # The file is absent — but the phase-3 filter should suppress the check.

        violations = check_advertised_artifacts(
            tmp_path,
            _PHASE3_ADVERTISED_ARTIFACT_FILENAMES,
            _PHASE3_ADVERTISED_GENERATED_ARTIFACT_FILENAMES,
        )

        assert violations == []

    def test_phase_filter_suppresses_phase4_generated_diagnostics(self, tmp_path: Path) -> None:
        """Phase 3 must not require phase-4 generated diagnostics."""
        from agentic_devtools.cli.speckit.verify_artifacts import (
            _PHASE3_ADVERTISED_ARTIFACT_FILENAMES,
            _PHASE3_ADVERTISED_GENERATED_ARTIFACT_FILENAMES,
        )

        (tmp_path / "plan.md").write_text(
            "Phase 4 diagnostics live at `generated/fr-coverage.json` and `generated/test-coverage.json`.\n",
            encoding="utf-8",
        )

        violations = check_advertised_artifacts(
            tmp_path,
            _PHASE3_ADVERTISED_ARTIFACT_FILENAMES,
            _PHASE3_ADVERTISED_GENERATED_ARTIFACT_FILENAMES,
        )

        assert violations == []
