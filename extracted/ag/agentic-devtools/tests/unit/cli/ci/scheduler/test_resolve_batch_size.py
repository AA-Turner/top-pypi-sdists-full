"""Tests for resolve_batch_size."""

from agentic_devtools.cli.ci.scheduler import resolve_batch_size


class TestResolveBatchSize:
    """Tests for the resolve_batch_size function."""

    def test_env_value_valid(self) -> None:
        assert resolve_batch_size("5", None) == 5

    def test_repo_value_valid(self) -> None:
        assert resolve_batch_size(None, "3") == 3

    def test_env_takes_priority_over_repo(self) -> None:
        assert resolve_batch_size("7", "3") == 7

    def test_default_when_both_none(self) -> None:
        assert resolve_batch_size(None, None) == 1

    def test_default_when_both_empty(self) -> None:
        assert resolve_batch_size("", "") == 1

    def test_custom_default(self) -> None:
        assert resolve_batch_size(None, None, default=5) == 5

    def test_invalid_env_falls_through_to_repo(self) -> None:
        assert resolve_batch_size("abc", "4") == 4

    def test_invalid_both_uses_default(self) -> None:
        assert resolve_batch_size("abc", "xyz") == 1

    def test_value_below_1_clamped(self) -> None:
        assert resolve_batch_size("0", None) == 1
        assert resolve_batch_size("-5", None) == 1

    def test_value_above_100_clamped(self) -> None:
        assert resolve_batch_size("150", None) == 100

    def test_whitespace_stripped(self) -> None:
        assert resolve_batch_size("  10  ", None) == 10
