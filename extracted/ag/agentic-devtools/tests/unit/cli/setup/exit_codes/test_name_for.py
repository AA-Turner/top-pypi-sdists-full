"""Tests for name_for helper."""

from agentic_devtools.cli.setup.exit_codes import ExitCode, code_for, name_for


class TestNameForValidCodes:
    """name_for returns the correct member name for all valid codes."""

    def test_ok(self) -> None:
        assert name_for(0) == "OK"

    def test_warnings(self) -> None:
        assert name_for(1) == "WARNINGS"

    def test_missing_required_dep(self) -> None:
        assert name_for(2) == "MISSING_REQUIRED_DEP"

    def test_version_blocked(self) -> None:
        assert name_for(3) == "VERSION_BLOCKED"

    def test_upgraded_rerun_needed(self) -> None:
        assert name_for(4) == "UPGRADED_RERUN_NEEDED"

    def test_repo_mutation_failed(self) -> None:
        assert name_for(5) == "REPO_MUTATION_FAILED"

    def test_autorun_failed(self) -> None:
        assert name_for(6) == "AUTORUN_FAILED"


class TestNameForUnknownCodes:
    """name_for returns UNKNOWN_{code} for unrecognized codes."""

    def test_unknown_positive(self) -> None:
        assert name_for(99) == "UNKNOWN_99"

    def test_unknown_negative(self) -> None:
        assert name_for(-1) == "UNKNOWN_-1"

    def test_unknown_large(self) -> None:
        assert name_for(999) == "UNKNOWN_999"

    def test_unknown_gap(self) -> None:
        assert name_for(7) == "UNKNOWN_7"


class TestNameForRoundTrip:
    """name_for(code_for(name)) == name for every member."""

    def test_round_trip_all_members(self) -> None:
        for member in ExitCode:
            assert name_for(code_for(member.name)) == member.name
