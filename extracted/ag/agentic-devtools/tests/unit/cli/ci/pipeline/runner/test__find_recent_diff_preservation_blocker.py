"""Tests for _find_recent_diff_preservation_blocker."""

from __future__ import annotations

import base64
import json
from typing import Any, cast
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.runner import (
    DiffPreservationBlockerLookupError,
    _find_recent_diff_preservation_blocker,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _blocker_comment(payload: dict[str, object]) -> str:
    encoded = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()).decode()
    return f"<!-- agdt:diff-preservation-blocker:{encoded.rstrip('=')} -->"


def _encoded_comment_from_object(payload: object) -> str:
    encoded = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()).decode()
    return f"<!-- agdt:diff-preservation-blocker:{encoded.rstrip('=')} -->"


class TestFindRecentDiffPreservationBlocker:
    """Tests for persisted cross-run diff-preservation blockers."""

    def test_returns_none_when_no_comment(self) -> None:
        provider = MagicMock()
        provider.find_comment.side_effect = [None, None]

        assert _find_recent_diff_preservation_blocker(provider, 1) is None

    def test_returns_none_when_login_lookup_is_unavailable(self) -> None:
        provider = MagicMock()

        assert _find_recent_diff_preservation_blocker(provider, 1) is None
        provider.find_comment.assert_not_called()

    def test_returns_none_for_invalid_payload(self) -> None:
        provider = MagicMock()
        provider.find_comment.side_effect = [
            (10, "<!-- agdt:diff-preservation-blocker:bm90LWpzb24 -->"),
            None,
        ]

        assert _find_recent_diff_preservation_blocker(provider, 1) is None

    def test_returns_none_for_non_dict_payload(self) -> None:
        provider = MagicMock()
        provider.find_comment.side_effect = [
            (10, _encoded_comment_from_object(["not", "a", "dict"])),
            None,
        ]

        assert _find_recent_diff_preservation_blocker(provider, 1) is None

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("baseline_head", ""),
            ("baseline_files", ["", 123]),
            ("baseline_hash", None),
            ("baseline_hash_available", "yes"),
            ("fingerprint_supported", "yes"),
            ("allow_file_removal", "yes"),
            ("intentional_noop", "yes"),
        ],
    )
    def test_returns_none_for_invalid_payload_fields(self, field: str, value: object) -> None:
        provider = MagicMock()
        payload: dict[str, object] = {
            "baseline_head": "deadbeef",
            "baseline_files": ["fix.py"],
            "baseline_hash": "same-hash",
            "baseline_hash_available": True,
            "fingerprint_supported": True,
        }
        payload[field] = value
        provider.find_comment.side_effect = [
            (10, _blocker_comment(payload)),
            None,
        ]

        assert _find_recent_diff_preservation_blocker(provider, 1) is None

    def test_rejects_invalid_intentional_noop_field_type(self) -> None:
        provider = MagicMock()
        payload: dict[str, object] = {
            "baseline_head": "deadbeef",
            "baseline_files": ["fix.py"],
            "baseline_hash": "same-hash",
            "baseline_hash_available": True,
            "fingerprint_supported": True,
            "allow_file_removal": True,
            "intentional_noop": "yes",
        }
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=10, author="trusted-bot", body=_blocker_comment(payload)),
        ]

        with pytest.raises(DiffPreservationBlockerLookupError, match="latest authenticated"):
            _find_recent_diff_preservation_blocker(provider, 1)

    def test_does_not_use_unauthenticated_marker(self) -> None:
        provider = MagicMock()

        assert _find_recent_diff_preservation_blocker(provider, 1) is None
        provider.find_comment.assert_not_called()

    def test_uses_latest_trusted_author_blocker(self) -> None:
        provider = MagicMock()
        older_payload = {
            "baseline_head": "older",
            "baseline_files": ["a.py"],
            "baseline_hash": "old-hash",
            "baseline_hash_available": True,
            "fingerprint_supported": True,
        }
        latest_payload = {
            "baseline_head": "latest",
            "baseline_files": ["b.py"],
            "baseline_hash": "new-hash",
            "baseline_hash_available": False,
            "fingerprint_supported": False,
            "allow_file_removal": False,
            "intentional_noop": False,
        }
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=10, author="trusted-bot", body=_blocker_comment(older_payload)),
            IssueCommentInfo(id=11, author="someone-else", body=_blocker_comment(latest_payload)),
            IssueCommentInfo(id=12, author="trusted-bot", body=_blocker_comment(latest_payload)),
        ]

        assert _find_recent_diff_preservation_blocker(provider, 1) == latest_payload
        provider.find_comment.assert_not_called()

    def test_trusted_author_path_ignores_blocker_after_newer_clear_marker(self) -> None:
        provider = MagicMock()
        payload = {
            "baseline_head": "deadbeef",
            "baseline_files": ["fix.py"],
            "baseline_hash": "same-hash",
            "baseline_hash_available": True,
            "fingerprint_supported": True,
        }
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=10, author="trusted-bot", body=_blocker_comment(payload)),
            IssueCommentInfo(
                id=11, author="trusted-bot", body="<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->"
            ),
        ]

        assert _find_recent_diff_preservation_blocker(provider, 1) is None

    def test_trusted_author_path_rejects_latest_invalid_blocker(self) -> None:
        provider = MagicMock()
        older_payload = {
            "baseline_head": "deadbeef",
            "baseline_files": ["fix.py"],
            "baseline_hash": "same-hash",
            "baseline_hash_available": True,
            "fingerprint_supported": True,
        }
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=10, author="trusted-bot", body=_blocker_comment(older_payload)),
            IssueCommentInfo(id=11, author="trusted-bot", body="<!-- agdt:diff-preservation-blocker:bm90LWpzb24 -->"),
        ]

        with pytest.raises(DiffPreservationBlockerLookupError, match="latest authenticated"):
            _find_recent_diff_preservation_blocker(provider, 1)

    def test_returns_none_when_login_lookup_raises(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login.side_effect = RuntimeError("lookup failed")

        with pytest.raises(RuntimeError, match="failed to resolve authenticated blocker identity"):
            _find_recent_diff_preservation_blocker(provider, 1)
        provider.find_comment.assert_not_called()

    def test_returns_none_when_login_lookup_returns_non_string(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login.return_value = 123

        assert _find_recent_diff_preservation_blocker(provider, 1) is None
        provider.find_comment.assert_not_called()

    def test_returns_none_when_trusted_comments_have_no_blocker(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=10, author="trusted-bot", body="not-a-blocker"),
            IssueCommentInfo(
                id=11, author="someone-else", body="<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->"
            ),
        ]

        assert _find_recent_diff_preservation_blocker(provider, 1) is None

    def test_returns_none_when_login_lookup_is_not_callable(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login = ""

        assert _find_recent_diff_preservation_blocker(provider, 1) is None
        provider.find_comment.assert_not_called()

    def test_returns_none_when_login_lookup_uses_provider_default(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login = CIPlatformProvider.get_pr_token_login.__get__(provider, CIPlatformProvider)

        assert _find_recent_diff_preservation_blocker(provider, 1) is None
        provider.list_issue_comments.assert_not_called()

    @pytest.mark.parametrize("login", [123, ""])
    def test_raises_when_authenticated_login_is_unusable(self, login: object) -> None:
        class _Provider:
            def get_pr_token_login(self) -> object:
                return login

        with pytest.raises(RuntimeError, match="authenticated blocker identity"):
            _find_recent_diff_preservation_blocker(cast(Any, _Provider()), 1)

    def test_uses_latest_clear_marker_id_when_trusted_comments_are_unsorted(self) -> None:
        provider = MagicMock()
        payload = {
            "baseline_head": "deadbeef",
            "baseline_files": ["fix.py"],
            "baseline_hash": "same-hash",
            "baseline_hash_available": True,
            "fingerprint_supported": True,
        }
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=11, author="trusted-bot", body="<!-- agdt:diff-preservation-blocker-cleared:feedbeef -->"
            ),
            IssueCommentInfo(
                id=10, author="trusted-bot", body="<!-- agdt:diff-preservation-blocker-cleared:deadc0de -->"
            ),
            IssueCommentInfo(id=9, author="trusted-bot", body=_blocker_comment(payload)),
        ]

        assert _find_recent_diff_preservation_blocker(provider, 1) is None

    def test_reraises_rate_limit_from_login_lookup(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )

        with pytest.raises(ProviderRateLimitError):
            _find_recent_diff_preservation_blocker(provider, 1)
