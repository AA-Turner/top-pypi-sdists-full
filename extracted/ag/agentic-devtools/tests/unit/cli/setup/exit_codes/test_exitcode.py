"""Tests for ExitCode IntEnum class."""

import enum

import pytest

from agentic_devtools.cli.setup.exit_codes import ALL_EXIT_CODES, EXIT_CODE_DESCRIPTIONS, ExitCode


class TestExitCodeMembers:
    """ExitCode enum has exactly the expected members and values."""

    def test_member_count_is_seven(self) -> None:
        assert len(ExitCode) == 7

    def test_ok_is_zero(self) -> None:
        assert ExitCode.OK.value == 0

    def test_warnings_is_one(self) -> None:
        assert ExitCode.WARNINGS.value == 1

    def test_missing_required_dep_is_two(self) -> None:
        assert ExitCode.MISSING_REQUIRED_DEP.value == 2

    def test_version_blocked_is_three(self) -> None:
        assert ExitCode.VERSION_BLOCKED.value == 3

    def test_upgraded_rerun_needed_is_four(self) -> None:
        assert ExitCode.UPGRADED_RERUN_NEEDED.value == 4

    def test_repo_mutation_failed_is_five(self) -> None:
        assert ExitCode.REPO_MUTATION_FAILED.value == 5

    def test_autorun_failed_is_six(self) -> None:
        assert ExitCode.AUTORUN_FAILED.value == 6

    def test_int_cast_ok(self) -> None:
        assert int(ExitCode.OK) == 0

    def test_int_cast_autorun_failed(self) -> None:
        assert int(ExitCode.AUTORUN_FAILED) == 6

    def test_no_dry_run_member(self) -> None:
        member_names = [m.name for m in ExitCode]
        assert "DRY_RUN" not in member_names

    def test_no_aliases(self) -> None:
        values = [m.value for m in ExitCode]
        assert len(values) == len(set(values)), "Exit code values must be unique (no aliases)"

    def test_unique_decorator_enforced(self) -> None:
        """@enum.unique raises ValueError if an alias is introduced."""
        with pytest.raises(ValueError, match="duplicate"):

            @enum.unique
            class _BadExitCode(enum.IntEnum):
                OK = 0
                ALSO_OK = 0  # alias → should raise


class TestExitCodeSysExitCompat:
    """ExitCode members are usable with sys.exit()."""

    def test_sys_exit_with_exit_code(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            import sys

            sys.exit(ExitCode.WARNINGS)
        assert exc_info.value.code == 1


class TestStabilityGuarantee:
    """Stability regression: OK=0 and WARNINGS=1 must never change."""

    def test_ok_value_stable(self) -> None:
        assert ExitCode.OK.value == 0

    def test_warnings_value_stable(self) -> None:
        assert ExitCode.WARNINGS.value == 1


class TestDerivedDicts:
    """ALL_EXIT_CODES and EXIT_CODE_DESCRIPTIONS are enum-derived."""

    def test_all_exit_codes_matches_enum(self) -> None:
        assert ALL_EXIT_CODES == {m.name: m.value for m in ExitCode}

    def test_exit_code_descriptions_covers_all_members(self) -> None:
        for member in ExitCode:
            assert member.value in EXIT_CODE_DESCRIPTIONS

    def test_no_extra_descriptions(self) -> None:
        valid_codes = {m.value for m in ExitCode}
        for code in EXIT_CODE_DESCRIPTIONS:
            assert code in valid_codes

    def test_descriptions_are_non_empty_strings(self) -> None:
        for code, desc in EXIT_CODE_DESCRIPTIONS.items():
            assert isinstance(desc, str)
            assert len(desc) > 0
