"""Tests for deferral marker functions."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.deferral import (
    _DEFERRAL_SENTINEL,
    deactivate_deferral_marker,
    post_deferral_marker,
    read_active_deferral,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _marker_comment(comment_id: int, payload: dict[str, object]) -> IssueCommentInfo:
    return IssueCommentInfo(
        id=comment_id,
        author="copilot",
        body=f"{_DEFERRAL_SENTINEL}{json.dumps(payload)} -->",
    )


class TestPostDeferralMarker:
    """Tests for post_deferral_marker."""

    def test_posts_marker_when_no_existing(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        result = post_deferral_marker(provider, 1, 100)

        assert result is True
        provider.post_comment.assert_called_once()
        body = provider.post_comment.call_args[0][1]
        assert _DEFERRAL_SENTINEL in body
        assert '"review_id": "100"' in body
        assert '"active": true' in body
        payload_json = body.split(_DEFERRAL_SENTINEL, maxsplit=1)[1].rsplit(" -->", maxsplit=1)[0]
        payload = json.loads(payload_json)
        assert payload["deferred_until"].endswith("Z")

    def test_skips_when_active_marker_exists(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        provider.list_issue_comments.return_value = [
            _marker_comment(
                42,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": True,
                },
            )
        ]

        result = post_deferral_marker(provider, 1, 100)

        assert result is False
        provider.post_comment.assert_not_called()

    def test_skips_when_inactive_marker_exists_for_same_review(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        provider.list_issue_comments.return_value = [
            _marker_comment(
                42,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": False,
                },
            )
        ]

        result = post_deferral_marker(provider, 1, 100)

        assert result is False
        provider.post_comment.assert_not_called()

    def test_returns_false_on_post_failure(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        provider.post_comment.side_effect = RuntimeError("API error")

        result = post_deferral_marker(provider, 1, 100)

        assert result is False

    def test_reraises_provider_rate_limit_error(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        provider.post_comment.side_effect = ProviderRateLimitError(60.0)

        import pytest

        with pytest.raises(ProviderRateLimitError):
            post_deferral_marker(provider, 1, 100)

    def test_deactivate_reraises_provider_rate_limit_error(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        provider.list_issue_comments.return_value = [
            _marker_comment(
                42,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": True,
                },
            )
        ]
        provider.update_comment.side_effect = ProviderRateLimitError(60.0)

        import pytest

        with pytest.raises(ProviderRateLimitError):
            deactivate_deferral_marker(provider, 1, 100)

    def test_read_active_deferral_reraises_rate_limit_on_comment_lookup(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.side_effect = ProviderRateLimitError(60.0)

        import pytest

        with pytest.raises(ProviderRateLimitError):
            read_active_deferral(provider, 1, 100)

    def test_read_active_deferral_reraises_rate_limit_on_pr_token_login_lookup(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        provider.list_issue_comments.return_value = [
            _marker_comment(
                42,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": True,
                },
            )
        ]
        provider.get_pr_token_login.side_effect = ProviderRateLimitError(60.0)

        import pytest

        with pytest.raises(ProviderRateLimitError):
            read_active_deferral(provider, 1, 100)


class TestReadActiveDeferral:
    """Tests for read_active_deferral."""

    def test_returns_none_when_no_marker(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_payload_when_active_and_unexpired(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": future,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is not None
        assert result["review_id"] == "100"
        assert result["active"] is True

    def test_returns_none_when_expired(self) -> None:
        provider = MagicMock()
        past = (datetime.now(UTC) - timedelta(minutes=10)).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": past,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_none_when_expired_with_z_suffix(self) -> None:
        provider = MagicMock()
        past = (datetime.now(UTC) - timedelta(minutes=10)).isoformat().replace("+00:00", "Z")
        payload = {
            "review_id": "100",
            "deferred_until": past,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_none_when_expired_with_naive_timestamp(self) -> None:
        provider = MagicMock()
        past = (datetime.now(UTC) - timedelta(minutes=10)).replace(tzinfo=None).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": past,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_none_when_inactive(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": future,
            "active": False,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_none_when_review_id_mismatch(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "999",
            "deferred_until": future,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_prefers_newest_matching_marker(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        provider.list_issue_comments.return_value = [
            _marker_comment(
                41,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": True,
                    "posted_at": "older",
                },
            ),
            _marker_comment(
                42,
                {
                    "review_id": "999",
                    "deferred_until": future,
                    "active": True,
                },
            ),
            _marker_comment(
                43,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": True,
                    "posted_at": "newer",
                },
            ),
        ]

        result = read_active_deferral(provider, 1, 100)

        assert result is not None
        assert result["posted_at"] == "newer"


class TestReadActiveDeferralEdgeCases:
    """Additional edge-case tests for read_active_deferral."""

    def test_returns_none_when_find_comment_raises(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.side_effect = RuntimeError("API error")

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_none_when_payload_unparseable(self) -> None:
        provider = MagicMock()
        # Valid sentinel but invalid JSON after it
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=42,
                author="copilot",
                body=f"{_DEFERRAL_SENTINEL}not-valid-json -->",
            )
        ]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_none_when_payload_is_not_object(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=42,
                author="copilot",
                body=f"{_DEFERRAL_SENTINEL}[1,2,3] -->",
            )
        ]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_payload_when_deferred_until_invalid_date(self) -> None:
        """Invalid deferred_until is treated as unexpired (fail-open)."""
        provider = MagicMock()
        payload = {
            "review_id": "100",
            "deferred_until": "not-a-date",
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is not None
        assert result["active"] is True

    def test_returns_payload_when_deferred_until_empty(self) -> None:
        """Empty deferred_until string skips expiry check (branch 134->147)."""
        provider = MagicMock()
        payload = {
            "review_id": "100",
            "deferred_until": "",
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = read_active_deferral(provider, 1, 100)

        assert result is not None
        assert result["active"] is True

    def test_returns_none_when_no_end_marker(self) -> None:
        """No closing ' -->' means _parse_deferral_payload returns None."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=42,
                author="copilot",
                body=f'{_DEFERRAL_SENTINEL}{{"review_id": "100", "active": true}}',
            )
        ]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_returns_none_when_sentinel_not_in_body(self) -> None:
        """Body without sentinel means _parse_deferral_payload returns None."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=42, author="copilot", body="some random comment body")
        ]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_ignores_marker_from_unauthorized_author(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": future,
            "active": True,
        }
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=42,
                author="random-user",
                body=f"{_DEFERRAL_SENTINEL}{json.dumps(payload)} -->",
            )
        ]

        result = read_active_deferral(provider, 1, 100)

        assert result is None

    def test_accepts_marker_from_github_actions_bot(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": future,
            "active": True,
        }
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=42,
                author="github-actions[bot]",
                body=f"{_DEFERRAL_SENTINEL}{json.dumps(payload)} -->",
            )
        ]

        result = read_active_deferral(provider, 1, 100)

        assert result is not None
        assert result["review_id"] == "100"


class TestDeactivateDeferralMarker:
    """Tests for deactivate_deferral_marker."""

    def test_deactivates_existing_marker(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": future,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        with patch.dict("os.environ", {"GITHUB_RUN_ID": "12345"}):
            result = deactivate_deferral_marker(provider, 1, 100)

        assert result is True
        provider.update_comment.assert_called_once()
        updated_body = provider.update_comment.call_args[0][1]
        assert '"active": false' in updated_body

    def test_returns_false_when_no_marker(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        result = deactivate_deferral_marker(provider, 1, 100)

        assert result is False

    def test_returns_false_when_find_comment_raises(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.side_effect = RuntimeError("API error")

        result = deactivate_deferral_marker(provider, 1, 100)

        assert result is False

    def test_returns_false_when_payload_unparseable(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=42,
                author="copilot",
                body=f"{_DEFERRAL_SENTINEL}invalid-json -->",
            )
        ]

        result = deactivate_deferral_marker(provider, 1, 100)

        assert result is False

    def test_returns_false_when_review_id_mismatch(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "999",
            "deferred_until": future,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]

        result = deactivate_deferral_marker(provider, 1, 100)

        assert result is False

    def test_returns_false_when_update_comment_raises(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        payload = {
            "review_id": "100",
            "deferred_until": future,
            "active": True,
        }
        provider.list_issue_comments.return_value = [_marker_comment(42, payload)]
        provider.update_comment.side_effect = RuntimeError("update failed")

        with patch.dict("os.environ", {"GITHUB_RUN_ID": "12345"}):
            result = deactivate_deferral_marker(provider, 1, 100)

        assert result is False

    def test_deactivates_newest_matching_active_marker(self) -> None:
        provider = MagicMock()
        future = (datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        provider.list_issue_comments.return_value = [
            _marker_comment(
                41,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": True,
                },
            ),
            _marker_comment(
                42,
                {
                    "review_id": "999",
                    "deferred_until": future,
                    "active": True,
                },
            ),
            _marker_comment(
                43,
                {
                    "review_id": "100",
                    "deferred_until": future,
                    "active": True,
                },
            ),
        ]

        with patch.dict("os.environ", {"GITHUB_RUN_ID": "12345"}):
            result = deactivate_deferral_marker(provider, 1, 100)

        assert result is True
        provider.update_comment.assert_called_once()
        assert provider.update_comment.call_args[0][0] == 43
