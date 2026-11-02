"""Tests for classifying ref-update conflicts."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.reconciliation.ref_head_writer import _is_ref_conflict

_REF = "/repos/owner/repo/git/ref/heads/custom-state"


def test_structured_409_is_a_conflict() -> None:
    api, sha_from = Mock(), Mock()

    assert _is_ref_conflict(
        GitHubApiError(409),
        _REF,
        "H0",
        api=api,
        sha_from=sha_from,
    )

    api.assert_not_called()
    sha_from.assert_not_called()


@pytest.mark.parametrize(
    ("status", "message", "current_sha", "expected", "reads_ref"),
    [
        (403, "409 Conflict", "H0", False, False),
        (500, "422 Update is not a fast-forward", "H0", False, False),
        (422, "409 Conflict", "H0", False, True),
        (409, "422 Validation Failed", "H0", True, False),
    ],
)
def test_structured_status_takes_precedence_over_text(
    status: int,
    message: str,
    current_sha: str,
    expected: bool,
    reads_ref: bool,
) -> None:
    api = Mock(return_value="ref")
    sha_from = Mock(return_value=current_sha)

    assert (
        _is_ref_conflict(
            GitHubApiError(status, safe_message=message),
            _REF,
            "H0",
            api=api,
            sha_from=sha_from,
        )
        is expected
    )

    if reads_ref:
        api.assert_called_once_with(_REF)
        sha_from.assert_called_once_with("ref", "object", "sha")
    else:
        api.assert_not_called()
        sha_from.assert_not_called()


def test_text_409_fallback_is_a_conflict() -> None:
    api, sha_from = Mock(), Mock()

    assert _is_ref_conflict(
        RuntimeError("409 Conflict"),
        _REF,
        "H0",
        api=api,
        sha_from=sha_from,
    )

    api.assert_not_called()
    sha_from.assert_not_called()


def test_text_422_fallback_detects_a_moved_ref() -> None:
    api = Mock(return_value="ref")
    sha_from = Mock(return_value="H1")

    assert _is_ref_conflict(
        RuntimeError("422 Validation Failed"),
        _REF,
        "H0",
        api=api,
        sha_from=sha_from,
    )

    api.assert_called_once_with(_REF)
    sha_from.assert_called_once_with("ref", "object", "sha")


def test_reason_bearing_422_is_a_conflict_without_reading_ref() -> None:
    api, sha_from = Mock(), Mock()

    assert _is_ref_conflict(
        RuntimeError("422 Update is not a fast-forward"),
        _REF,
        "H0",
        api=api,
        sha_from=sha_from,
    )

    api.assert_not_called()
    sha_from.assert_not_called()


@pytest.mark.parametrize(("current_sha", "expected"), [("H1", True), ("H0", False)])
def test_sanitized_422_compares_current_ref_head(current_sha: str, expected: bool) -> None:
    api, sha_from = Mock(return_value="ref"), Mock(return_value=current_sha)

    assert (
        _is_ref_conflict(
            GitHubApiError(422),
            _REF,
            "H0",
            api=api,
            sha_from=sha_from,
        )
        is expected
    )

    api.assert_called_once_with(_REF)
    sha_from.assert_called_once_with("ref", "object", "sha")


@pytest.mark.parametrize(
    ("api", "sha_from"),
    [
        (Mock(side_effect=RuntimeError("read failed")), Mock()),
        (Mock(return_value="invalid"), Mock(side_effect=RuntimeError("invalid SHA"))),
    ],
)
def test_sanitized_422_read_failure_or_invalid_sha_is_not_a_conflict(api: Mock, sha_from: Mock) -> None:
    assert not _is_ref_conflict(
        GitHubApiError(422),
        _REF,
        "H0",
        api=api,
        sha_from=sha_from,
    )
