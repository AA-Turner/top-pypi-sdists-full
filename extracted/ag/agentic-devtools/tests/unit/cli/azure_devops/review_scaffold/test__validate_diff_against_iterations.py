"""Tests for _validate_diff_against_iterations helper function."""

from agentic_devtools.cli.azure_devops.review_scaffold import (
    FileChangeResult,
    _validate_diff_against_iterations,
)


class TestValidateDiffAgainstIterations:
    """Tests for _validate_diff_against_iterations."""

    def test_no_discrepancies_print_nothing(self, capsys):
        """Matching git and iteration files produce no warnings."""
        result = FileChangeResult()

        _validate_diff_against_iterations(
            result,
            iteration_changed_files={"/src/a.ts"},
            git_changed={"/src/a.ts"},
            current_file_set={"/src/a.ts"},
        )

        assert result.validation_warnings == []
        assert capsys.readouterr().err == ""

    def test_at_most_five_discrepancies_print_individual_warnings(self, capsys):
        """At most five discrepancies in each direction print sorted file warnings."""
        result = FileChangeResult()
        git_only = {f"/src/git-{index}.ts" for index in range(5)}
        iterations_only = {f"/src/iteration-{index}.ts" for index in range(5)}

        _validate_diff_against_iterations(
            result,
            iteration_changed_files=iterations_only,
            git_changed=git_only,
            current_file_set=git_only | iterations_only,
        )

        assert capsys.readouterr().err.splitlines() == [
            *(f"Warning: File {path} changed in git diff but not in iterations API" for path in sorted(git_only)),
            *(
                f"Warning: File {path} changed in iterations API but not in git diff"
                for path in sorted(iterations_only)
            ),
        ]
        assert result.validation_warnings == [
            *(f"File {path} changed in git diff but not in iterations API" for path in sorted(git_only)),
            *(f"File {path} changed in iterations API but not in git diff" for path in sorted(iterations_only)),
        ]

    def test_more_than_five_git_discrepancies_print_summary(self, capsys):
        """More than five git-only discrepancies print one summary warning."""
        result = FileChangeResult()
        git_only = {f"/src/file-{index}.ts" for index in range(6)}

        _validate_diff_against_iterations(
            result,
            iteration_changed_files=set(),
            git_changed=git_only,
            current_file_set=git_only,
        )

        assert capsys.readouterr().err == "Warning: 6 files changed in git diff but not in iterations API\n"
        assert result.validation_warnings == [
            f"File {path} changed in git diff but not in iterations API" for path in sorted(git_only)
        ]

    def test_more_than_five_iteration_discrepancies_print_summary(self, capsys):
        """More than five iterations-only discrepancies print one summary warning."""
        result = FileChangeResult()
        iterations_only = {f"/src/file-{index}.ts" for index in range(6)}

        _validate_diff_against_iterations(
            result,
            iteration_changed_files=iterations_only,
            git_changed=set(),
            current_file_set=iterations_only,
        )

        assert capsys.readouterr().err == "Warning: 6 files changed in iterations API but not in git diff\n"
        assert result.validation_warnings == [
            f"File {path} changed in iterations API but not in git diff" for path in sorted(iterations_only)
        ]
