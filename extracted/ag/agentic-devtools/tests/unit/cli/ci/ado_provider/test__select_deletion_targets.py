"""Tests for the ado_provider._select_deletion_targets selector."""

from __future__ import annotations

from agentic_devtools.cli.ci.ado_provider import _select_deletion_targets

_MARKER = "<!-- agdt-review:v1 type:overall-summary -->\nOverall summary."
_V2_MARKER = "<!-- agdt-review:v2 type:consolidated pr:30781 commit:abc123 -->\nIn progress."
_V1_CONSOLIDATED_MARKER = "<!-- agdt-review:v1 type:consolidated pr:30781 commit:abc123 -->\nIn progress."
_INVALID_MARKER = "<!-- agdt-review:v1 type:bogus -->\nNot a known type."


class TestSelectDeletionTargets:
    """Tests for the deletion-target selector."""

    def test_selects_marker_comment(self) -> None:
        threads = [{"id": 1, "comments": [{"id": 2, "commentType": "text", "content": _MARKER}]}]
        targets = _select_deletion_targets(threads, None)
        assert len(targets) == 1
        assert targets[0].thread_id == 1
        assert targets[0].comment_id == 2
        assert targets[0].marker_type == "overall-summary"

    def test_selects_v2_consolidated_marker_comment(self) -> None:
        """The cleanup selector recognizes v2 consolidated review comments."""
        threads = [{"id": 3, "comments": [{"id": 4, "commentType": "text", "content": _V2_MARKER}]}]

        targets = _select_deletion_targets(threads, None)

        assert len(targets) == 1
        assert targets[0].thread_id == 3
        assert targets[0].comment_id == 4
        assert targets[0].marker_type == "consolidated"

    def test_skips_v1_consolidated_marker(self) -> None:
        """The cleanup selector treats consolidated markers as v2-only."""
        threads = [{"id": 3, "comments": [{"id": 4, "commentType": "text", "content": _V1_CONSOLIDATED_MARKER}]}]
        assert _select_deletion_targets(threads, None) == []

    def test_skips_deleted_thread(self) -> None:
        threads = [{"id": 1, "isDeleted": True, "comments": [{"id": 2, "content": _MARKER}]}]
        assert _select_deletion_targets(threads, None) == []

    def test_skips_deleted_comment(self) -> None:
        threads = [{"id": 1, "comments": [{"id": 2, "content": _MARKER, "isDeleted": True}]}]
        assert _select_deletion_targets(threads, None) == []

    def test_skips_non_text_comment(self) -> None:
        threads = [{"id": 1, "comments": [{"id": 2, "content": _MARKER, "commentType": "system"}]}]
        assert _select_deletion_targets(threads, None) == []

    def test_skips_non_marker_without_author_match(self) -> None:
        threads = [{"id": 1, "comments": [{"id": 2, "commentType": "text", "content": "plain"}]}]
        assert _select_deletion_targets(threads, None) == []

    def test_skips_invalid_marker_type_without_author_match(self) -> None:
        threads = [{"id": 1, "comments": [{"id": 2, "commentType": "text", "content": _INVALID_MARKER}]}]
        assert _select_deletion_targets(threads, None) == []

    def test_selects_by_author_substring_when_not_marker(self) -> None:
        threads = [
            {
                "id": 3,
                "comments": [
                    {
                        "id": 4,
                        "commentType": "text",
                        "content": "plain",
                        "author": {"displayName": "Bot Account"},
                    },
                ],
            }
        ]
        targets = _select_deletion_targets(threads, "bot")
        assert len(targets) == 1
        assert targets[0].marker_type is None

    def test_selects_by_author_substring_when_marker_type_invalid(self) -> None:
        threads = [
            {
                "id": 5,
                "comments": [
                    {
                        "id": 6,
                        "commentType": "text",
                        "content": _INVALID_MARKER,
                        "author": {"displayName": "Bot Account"},
                    },
                ],
            }
        ]
        targets = _select_deletion_targets(threads, "bot")
        assert len(targets) == 1
        assert targets[0].marker_type is None

    def test_handles_thread_with_no_comments(self) -> None:
        threads = [{"id": 1, "comments": None}]
        assert _select_deletion_targets(threads, None) == []
