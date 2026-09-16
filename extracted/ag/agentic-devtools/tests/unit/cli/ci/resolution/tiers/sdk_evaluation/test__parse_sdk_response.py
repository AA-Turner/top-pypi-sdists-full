"""Tests for _parse_sdk_response."""

from agentic_devtools.cli.ci.resolution.models import ResolutionBasis, ResolutionVerdict
from agentic_devtools.cli.ci.resolution.tiers.sdk_evaluation import _parse_sdk_response


def test_valid_resolve() -> None:
    verdict, explanation, is_ambiguous, basis = _parse_sdk_response(
        "VERDICT: RESOLVE\nBASIS: code_change\nEXPLANATION: The typo was fixed."
    )
    assert verdict == ResolutionVerdict.RESOLVE
    assert explanation == "The typo was fixed."
    assert is_ambiguous is False
    assert basis == ResolutionBasis.CODE_CHANGE


def test_valid_unresolve() -> None:
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response("VERDICT: UNRESOLVE\nEXPLANATION: Not addressed.")
    assert verdict == ResolutionVerdict.UNRESOLVE
    assert explanation == "Not addressed."
    assert is_ambiguous is False


def test_case_insensitive() -> None:
    verdict, _, is_ambiguous, _basis = _parse_sdk_response("verdict: resolve\nbasis: code_change\nexplanation: done")
    assert verdict == ResolutionVerdict.RESOLVE
    assert is_ambiguous is False


def test_malformed_response() -> None:
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response("I think the comment was addressed.")
    assert verdict is None
    assert explanation == ""
    assert is_ambiguous is False


def test_ambiguous_response() -> None:
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response(
        "VERDICT: AMBIGUOUS\nEXPLANATION: Not enough context to decide."
    )
    assert verdict is None
    assert explanation == "Not enough context to decide."
    assert is_ambiguous is True


def test_ambiguous_without_explanation() -> None:
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response("VERDICT: AMBIGUOUS")
    assert verdict is None
    assert explanation == ""
    assert is_ambiguous is False


def test_maps_comment_resolve() -> None:
    verdict, _, _, _ = _parse_sdk_response("VERDICT: COMMENT_RESOLVE\nBASIS: code_change\nEXPLANATION: addressed")
    assert verdict == ResolutionVerdict.RESOLVE


def test_maps_comment_unresolve() -> None:
    verdict, _, _, _ = _parse_sdk_response("VERDICT: COMMENT_UNRESOLVE\nEXPLANATION: not addressed")
    assert verdict == ResolutionVerdict.UNRESOLVE


def test_explicit_rejection_maps_to_resolve() -> None:
    verdict, explanation, _, basis = _parse_sdk_response(
        "VERDICT: UNRESOLVE\nBASIS: explicit_rejection\nEXPLANATION: The reviewer explicitly rejected the concern."
    )
    assert verdict == ResolutionVerdict.RESOLVE
    assert explanation
    assert basis == ResolutionBasis.EXPLICIT_REJECTION


def test_out_of_scope_maps_to_resolve() -> None:
    verdict, _, _, basis = _parse_sdk_response(
        "VERDICT: UNRESOLVE\nBASIS: out_of_scope\nEXPLANATION: The requested behavior is out of scope."
    )
    assert verdict == ResolutionVerdict.RESOLVE
    assert basis == ResolutionBasis.OUT_OF_SCOPE


def test_resolve_without_basis_is_malformed() -> None:
    verdict, explanation, is_ambiguous, basis = _parse_sdk_response(
        "VERDICT: RESOLVE\nEXPLANATION: The code change addresses the comment."
    )
    assert verdict is None
    assert explanation == ""
    assert is_ambiguous is False
    assert basis is None


def test_unresolve_basis_maps_to_unresolve() -> None:
    verdict, _, _, basis = _parse_sdk_response(
        "VERDICT: RESOLVE\nBASIS: unresolve\nEXPLANATION: The evidence is insufficient."
    )
    assert verdict == ResolutionVerdict.UNRESOLVE
    assert basis == ResolutionBasis.UNRESOLVE


def test_resolve_without_explanation_is_malformed() -> None:
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response("VERDICT: RESOLVE")
    assert verdict is None
    assert explanation == ""
    assert is_ambiguous is False


def test_uses_last_verdict_when_multiple_at_line_start() -> None:
    """When VERDICT appears at line-start more than once the last occurrence wins."""
    raw = (
        "VERDICT: RESOLVE\n"
        "EXPLANATION: initial impression\n\n"
        "On reflection:\n"
        "VERDICT: UNRESOLVE\n"
        "EXPLANATION: the underlying issue was not fixed"
    )
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response(raw)
    assert verdict == ResolutionVerdict.UNRESOLVE
    assert explanation == "the underlying issue was not fixed"
    assert is_ambiguous is False


def test_ignores_verdict_not_at_line_start() -> None:
    """VERDICT: appearing inline (not at line-start) must not be matched."""
    raw = (
        "My assessment concludes VERDICT: RESOLVE given the diff, "
        "but consider also VERDICT: UNRESOLVE if the scope changes"
    )
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response(raw)
    assert verdict is None
    assert explanation == ""
    assert is_ambiguous is False


def test_echoed_prompt_examples_do_not_shadow_actual_verdict() -> None:
    """Preamble that quotes prompt-style VERDICT lines must not be chosen over the real verdict."""
    raw = (
        "The format you requested is:\n"
        "VERDICT: RESOLVE\n"
        "or\n"
        "VERDICT: UNRESOLVE\n\n"
        "Based on my analysis of the diff:\n"
        "VERDICT: UNRESOLVE\n"
        "EXPLANATION: The null-pointer guard mentioned in the comment is still absent."
    )
    verdict, explanation, is_ambiguous, _basis = _parse_sdk_response(raw)
    assert verdict == ResolutionVerdict.UNRESOLVE
    assert explanation == "The null-pointer guard mentioned in the comment is still absent."
    assert is_ambiguous is False


def test_explanation_searched_after_last_verdict() -> None:
    """EXPLANATION that precedes the last VERDICT is not used."""
    raw = "VERDICT: RESOLVE\nEXPLANATION: first explanation\n\nVERDICT: UNRESOLVE\nEXPLANATION: final explanation"
    verdict, explanation, _is_ambiguous, _basis = _parse_sdk_response(raw)
    assert verdict == ResolutionVerdict.UNRESOLVE
    assert explanation == "final explanation"
