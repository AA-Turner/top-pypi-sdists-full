"""Tests for ArtifactCleanupResult."""

from agentic_devtools.cli.setup.doctor_repair import ArtifactCleanupResult


class TestArtifactCleanupResult:
    """Tests for ArtifactCleanupResult dataclass."""

    def test_success_result(self) -> None:
        r = ArtifactCleanupResult(path="/tmp/foo", success=True)
        assert r.path == "/tmp/foo"
        assert r.success is True
        assert r.error is None

    def test_failure_result(self) -> None:
        r = ArtifactCleanupResult(path="/tmp/bar", success=False, error="Permission denied")
        assert r.path == "/tmp/bar"
        assert r.success is False
        assert r.error == "Permission denied"

    def test_error_defaults_to_none(self) -> None:
        r = ArtifactCleanupResult(path="/x", success=True)
        assert r.error is None
