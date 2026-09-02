"""Tests for the ``FeatureResolutionError`` exception."""

from agentic_devtools.cli.speckit.scaffold_common import FeatureResolutionError


class TestFeatureResolutionError:
    """FeatureResolutionError is a plain RuntimeError subclass with a message."""

    def test_is_a_runtime_error(self) -> None:
        assert issubclass(FeatureResolutionError, RuntimeError)

    def test_preserves_message(self) -> None:
        error = FeatureResolutionError("multiple matches")
        assert str(error) == "multiple matches"
