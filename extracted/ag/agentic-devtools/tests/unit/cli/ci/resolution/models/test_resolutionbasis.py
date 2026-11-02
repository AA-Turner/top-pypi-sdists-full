"""Tests for ResolutionBasis."""

from agentic_devtools.cli.ci.resolution.models import ResolutionBasis


def test_all_members_have_expected_values() -> None:
    assert list(ResolutionBasis) == [
        ResolutionBasis.CODE_CHANGE,
        ResolutionBasis.EXPLICIT_REJECTION,
        ResolutionBasis.OUT_OF_SCOPE,
        ResolutionBasis.UNRESOLVE,
    ]
    assert [basis.value for basis in ResolutionBasis] == [
        "code_change",
        "explicit_rejection",
        "out_of_scope",
        "unresolve",
    ]
