"""Tests for ErrorClass enum."""

from __future__ import annotations

from agentic_devtools.cli.setup.fixloop import ErrorClass


class TestErrorClass:
    """Verify ErrorClass enum has exactly 11 members with correct names."""

    def test_has_exactly_eleven_members(self) -> None:
        assert len(ErrorClass) == 11

    def test_member_names(self) -> None:
        expected = {
            "SUCCESS",
            "MISSING_DEPENDENCY",
            "STALE_PARTIAL_INSTALL",
            "CERT_CA_FETCH",
            "MANAGED_CLI_MISSING",
            "PATH_PROFILE_NOT_UPDATED",
            "GIT_HOOKS_NOT_CONFIGURED",
            "SKILL_INJECTION_PERMS",
            "TRANSIENT_NETWORK",
            "AUTH_SECRET",
            "UNKNOWN",
        }
        assert {m.name for m in ErrorClass} == expected

    def test_member_values_are_strings(self) -> None:
        for member in ErrorClass:
            assert isinstance(member.value, str)
