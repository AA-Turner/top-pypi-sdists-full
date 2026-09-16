"""Tests for scope matching and candidate-filter evaluation."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.cli.ci.reconciliation.models import RepositoryTarget, TriStateValue
from agentic_devtools.cli.ci.reconciliation.scope import (
    create_scope_snapshot,
    evaluate_candidate_filter,
    matches_observation_scope,
)


def test_evaluate_candidate_filter_respects_precedence() -> None:
    result, errors = evaluate_candidate_filter(
        "target_branch_match OR NOT draft_state AND unresolved_reviews",
        {
            "target_branch_match": TriStateValue.FALSE,
            "draft_state": TriStateValue.FALSE,
            "unresolved_reviews": TriStateValue.TRUE,
            "author_association": TriStateValue.TRUE,
            "mergeability_state": TriStateValue.TRUE,
            "labels": TriStateValue.TRUE,
        },
    )
    assert result == TriStateValue.TRUE
    assert errors == ()


def test_evaluate_candidate_filter_invalid_operand_fails_closed() -> None:
    result, errors = evaluate_candidate_filter("unknown_operand", {})
    assert result == TriStateValue.UNKNOWN
    assert errors


def test_evaluate_candidate_filter_rejects_unrecognized_syntax() -> None:
    result, errors = evaluate_candidate_filter("target_branch_match ??? AND draft_state", {})
    assert result is TriStateValue.UNKNOWN
    assert errors == ("invalid candidate-filter syntax",)


def test_evaluate_candidate_filter_rejects_invalid_gap_between_tokens() -> None:
    result, errors = evaluate_candidate_filter("target_branch_match ??? draft_state", {})
    assert result is TriStateValue.UNKNOWN
    assert errors == ("invalid candidate-filter syntax",)


def test_evaluate_candidate_filter_rejects_trailing_syntax() -> None:
    result, errors = evaluate_candidate_filter("target_branch_match ???", {})
    assert result is TriStateValue.UNKNOWN
    assert errors == ("invalid candidate-filter syntax",)


def test_evaluate_candidate_filter_missing_operands_reports_errors() -> None:
    result, errors = evaluate_candidate_filter(
        "target_branch_match AND author_association",
        {"target_branch_match": TriStateValue.TRUE},
    )
    assert result == TriStateValue.UNKNOWN
    assert any("missing operand value" in error for error in errors)


def test_scope_matching_honors_disabled_targets() -> None:
    targets = (
        RepositoryTarget(repository="owner/repo", target_branch="main", enabled=False),
        RepositoryTarget(repository="owner/repo", target_branch="release", enabled=True),
    )
    assert not matches_observation_scope(repository="owner/repo", target_branch="main", targets=targets)
    assert matches_observation_scope(repository="owner/repo", target_branch="release", targets=targets)


def test_create_scope_snapshot_is_deterministic() -> None:
    now = datetime(2026, 9, 15, 12, 0, tzinfo=UTC)
    targets = (RepositoryTarget(repository="owner/repo", target_branch="main", enabled=True),)
    first = create_scope_snapshot(targets=targets, candidate_filter_expression="target_branch_match", now=now)
    second = create_scope_snapshot(targets=targets, candidate_filter_expression="target_branch_match", now=now)
    assert first.fingerprint == second.fingerprint
    assert first.epoch_id == second.epoch_id


def test_evaluate_candidate_filter_parentheses_and_false_and_unknown_paths() -> None:
    values = {
        "target_branch_match": TriStateValue.FALSE,
        "author_association": TriStateValue.TRUE,
        "draft_state": TriStateValue.UNKNOWN,
        "mergeability_state": TriStateValue.TRUE,
        "unresolved_reviews": TriStateValue.FALSE,
        "labels": TriStateValue.FALSE,
    }
    false_result, _ = evaluate_candidate_filter(
        "(target_branch_match AND author_association) OR unresolved_reviews",
        values,
    )
    unknown_result, _ = evaluate_candidate_filter(
        "NOT draft_state",
        values,
    )
    assert false_result == TriStateValue.FALSE
    assert unknown_result == TriStateValue.UNKNOWN


def test_evaluate_candidate_filter_reports_parse_shape_errors() -> None:
    unexpected_token_result, errors = evaluate_candidate_filter(
        "target_branch_match labels",
        {"target_branch_match": TriStateValue.TRUE, "labels": TriStateValue.TRUE},
    )
    expected_closing_result, closing_errors = evaluate_candidate_filter(
        "(target_branch_match author_association)",
        {"target_branch_match": TriStateValue.TRUE},
    )
    missing_closing_result, missing_closing_errors = evaluate_candidate_filter(
        "(target_branch_match",
        {"target_branch_match": TriStateValue.TRUE},
    )
    missing_operand_result, missing_operand_errors = evaluate_candidate_filter("", {})
    assert unexpected_token_result == TriStateValue.UNKNOWN
    assert any("unexpected token" in message for message in errors)
    assert expected_closing_result == TriStateValue.UNKNOWN
    assert any("expected ')'" in message or "expected ')'" in message for message in closing_errors)
    assert missing_closing_result == TriStateValue.UNKNOWN
    assert any("unexpected end of expression" in message for message in missing_closing_errors)
    assert missing_operand_result == TriStateValue.UNKNOWN
    assert any("missing operand" in message or "unexpected end" in message for message in missing_operand_errors)


def test_evaluate_candidate_filter_not_true_and_or_unknown() -> None:
    values = {
        "target_branch_match": TriStateValue.TRUE,
        "labels": TriStateValue.UNKNOWN,
        "unresolved_reviews": TriStateValue.FALSE,
    }
    not_result, _ = evaluate_candidate_filter("NOT target_branch_match", values)
    or_unknown_result, _ = evaluate_candidate_filter("labels OR unresolved_reviews", values)
    assert not_result == TriStateValue.FALSE
    assert or_unknown_result == TriStateValue.UNKNOWN
