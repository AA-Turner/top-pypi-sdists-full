"""Tests for code_for helper."""

import pytest

from agentic_devtools.cli.setup.exit_codes import ExitCode, code_for


class TestCodeForValidNames:
    """code_for returns the correct integer for all valid member names."""

    def test_ok(self) -> None:
        assert code_for("OK") == 0

    def test_warnings(self) -> None:
        assert code_for("WARNINGS") == 1

    def test_missing_required_dep(self) -> None:
        assert code_for("MISSING_REQUIRED_DEP") == 2

    def test_version_blocked(self) -> None:
        assert code_for("VERSION_BLOCKED") == 3

    def test_upgraded_rerun_needed(self) -> None:
        assert code_for("UPGRADED_RERUN_NEEDED") == 4

    def test_repo_mutation_failed(self) -> None:
        assert code_for("REPO_MUTATION_FAILED") == 5

    def test_autorun_failed(self) -> None:
        assert code_for("AUTORUN_FAILED") == 6


class TestCodeForInvalidNames:
    """code_for raises KeyError for unrecognized names."""

    def test_unknown_name_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            code_for("NONEXISTENT")

    def test_empty_string_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            code_for("")

    def test_lowercase_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            code_for("ok")

    def test_all_members_accessible(self) -> None:
        for member in ExitCode:
            assert code_for(member.name) == member.value
