from agentic_devtools.ai_providers.availability import _looks_like_base_ref_response


def test__looks_like_base_ref_response_handles_clause_boundaries() -> None:
    assert _looks_like_base_ref_response("base_ref 'refs/heads/release/1.2' was not found")
    assert _looks_like_base_ref_response("base_ref is invalid")
    # ref-scoped co-occurrence signal in the same clause as a base_ref marker
    assert _looks_like_base_ref_response("base_ref 'X': no such ref")
    assert not _looks_like_base_ref_response("base_ref validation succeeded. custom_agent is not found")
    assert not _looks_like_base_ref_response("base_ref validation succeeded in phase 1. custom_agent is not found")
    assert not _looks_like_base_ref_response("base_ref validation succeeded! custom_agent is not found")
    assert not _looks_like_base_ref_response("base_ref validation succeeded? custom_agent is not found")
    assert not _looks_like_base_ref_response("base_ref validation succeeded, but custom_agent is not found")
    # Exclamation/question marks embedded in a ref value are not treated as sentence boundaries
    assert _looks_like_base_ref_response("base_ref 'refs/heads/feature!foo' was not found")


def test__looks_like_base_ref_response_rejects_success_then_unrelated_failure() -> None:
    # "not found" belongs to an unrelated subject in the same clause — base_ref succeeded.
    assert not _looks_like_base_ref_response("base_ref validation succeeded and repository not found")
    # "passed" as success indicator must also prevent a false match.
    assert not _looks_like_base_ref_response("base_ref validation passed and repository not found")
    # A genuine base_ref failure with no success indicator between marker and phrase must match.
    assert _looks_like_base_ref_response("base_ref 'refs/heads/main' does not exist")
    assert _looks_like_base_ref_response("base_ref: refs/heads/main does not exist")
    assert _looks_like_base_ref_response("base_ref 'refs/heads/gone' was not found")
    # Ref-scoped signal ("ref not found") must also be guarded: "repository ref not found"
    # contains "ref not found" as a substring — base_ref succeeded, so must not match.
    assert not _looks_like_base_ref_response("base_ref validation succeeded and repository ref not found")
    assert not _looks_like_base_ref_response("base_ref validation passed and repository ref not found")
    assert not _looks_like_base_ref_response("base_ref validation pending and repository ref not found")
    assert not _looks_like_base_ref_response("base_ref validation pending and repository not found")


def test__looks_like_base_ref_response_ignores_success_indicator_substrings_in_ref_names() -> None:
    assert _looks_like_base_ref_response("base_ref 'refs/heads/bypassed-check' was not found")
    assert _looks_like_base_ref_response("base_ref 'refs/heads/passed-check' was not found")
    assert _looks_like_base_ref_response("base_ref 'refs/heads/succeeded-release' does not exist")


def test__looks_like_base_ref_response_handles_escaped_apostrophe_in_ref_value() -> None:
    # Apostrophes are valid in Git ref names; an escaped apostrophe inside a single-quoted
    # value must not truncate the match and must still return True.
    assert _looks_like_base_ref_response("base_ref 'refs/heads/it\\'s-gone' was not found")
    assert _looks_like_base_ref_response("base_ref 'refs/heads/it\\'s-gone' does not exist")


def test__looks_like_base_ref_response_accepts_backtick_quoted_ref_values() -> None:
    assert _looks_like_base_ref_response("base_ref `refs/heads/feature;foo` was not found")


def test__looks_like_base_ref_response_accepts_echoed_value_invalid_and_missing_phrases() -> None:
    assert _looks_like_base_ref_response("base_ref 'refs/heads/does-not-exist' is invalid")
    assert _looks_like_base_ref_response("base_ref 'refs/heads/does-not-exist' is missing")


def test__looks_like_base_ref_response_ignores_failure_phrase_before_marker() -> None:
    # "not found" in the tail of the segment determines the result, not the pre-marker occurrence.
    assert _looks_like_base_ref_response("not found: base_ref not found")
    # "not found" only before the marker (not in tail) — should not match.
    assert not _looks_like_base_ref_response("not found: base_ref still processing")


def test__looks_like_base_ref_response_rejects_identifier_prefix_false_positives() -> None:
    # "database_ref is invalid" contains "base_ref is invalid" as a substring but the
    # marker is not at an identifier boundary — must not be classified as a base_ref failure.
    assert not _looks_like_base_ref_response("database_ref is invalid")
    assert not _looks_like_base_ref_response("database_ref is missing")


def test__looks_like_base_ref_response_rejects_signal_prefix_false_positives() -> None:
    assert not _looks_like_base_ref_response("base_ref is invalidated")
    assert not _looks_like_base_ref_response("base_ref was missingness")


def test__looks_like_base_ref_response_binds_to_later_marker_occurrence() -> None:
    # The first "base_ref" mention never resolves into a failure ("validation completed"),
    # but a later "base_ref" mention in the same segment is directly bound to the failure
    # phrase. Every marker occurrence must be considered, not just the first.
    assert _looks_like_base_ref_response(
        "base_ref validation completed and base_ref 'refs/heads/does-not-exist' was not found"
    )
