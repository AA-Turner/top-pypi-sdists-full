"""Tests for PHASES tuple."""

from agentic_devtools.cli.setup.phases import PHASES


class TestPhases:
    """PHASES tuple is well-formed."""

    def test_is_tuple(self) -> None:
        assert isinstance(PHASES, tuple)

    def test_non_empty(self) -> None:
        assert len(PHASES) > 0

    def test_no_duplicates(self) -> None:
        assert len(PHASES) == len(set(PHASES))

    def test_all_strings(self) -> None:
        for phase in PHASES:
            assert isinstance(phase, str)
            assert len(phase) > 0

    def test_expected_phases_present(self) -> None:
        assert "version_check" in PHASES
        assert "certificate_prefetch" in PHASES
        assert "cli_installation" in PHASES
        assert "dependency_check" in PHASES
        assert "environment_persistence" in PHASES
        assert "file_modifications" in PHASES
