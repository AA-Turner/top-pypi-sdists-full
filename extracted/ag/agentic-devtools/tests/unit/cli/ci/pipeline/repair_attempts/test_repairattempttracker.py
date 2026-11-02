"""Tests for durable per-finding repair reservations."""

import json
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewCommentInfo
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

TRUSTED_LOGIN = "github-actions[bot]"


@pytest.fixture
def provider():
    """In-memory provider with acknowledged durable comment writes, authored by the trusted workflow identity."""
    mock = MagicMock()
    stored: dict[int, str] = {}

    def post_comment(pr_number: int, body: str) -> int:
        comment_id = len(stored) + 1
        stored[comment_id] = body
        return comment_id

    def update_comment(comment_id: int, body: str) -> None:
        stored[comment_id] = body

    def list_issue_comments(pr_number: int) -> list[IssueCommentInfo]:
        return [IssueCommentInfo(id=comment_id, author=TRUSTED_LOGIN, body=body) for comment_id, body in stored.items()]

    mock.find_comment.side_effect = lambda pr, marker: next(
        ((key, body) for key, body in stored.items() if marker in body), None
    )
    mock.get_pr_token_login.return_value = TRUSTED_LOGIN
    mock.list_issue_comments.side_effect = list_issue_comments
    mock.post_comment.side_effect = post_comment
    mock.update_comment.side_effect = update_comment
    mock.list_review_thread_states.return_value = {}
    return mock


class TestRepairAttemptTracker:
    @pytest.mark.parametrize(
        "error",
        [
            RuntimeError("label unavailable"),
            ProviderRateLimitError(provider="github", credential_identity="test"),
        ],
    )
    def test_label_failure_still_notifies_once_and_retries_label(self, provider, caplog, error):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"root:101"})
        provider.add_label.side_effect = error
        root = ReviewCommentInfo(id=101, path="", body="Fix", html_url="")
        new_root = ReviewCommentInfo(id=103, path="", body="Other fix", html_url="")

        assert tracker.filter_review(10, [root, new_root], set()) == [new_root]
        assert "label unavailable" in caplog.text or "rate limit" in caplog.text.lower()
        provider.add_label.side_effect = None
        reloaded = RepairAttemptTracker(provider, 42, "abc")
        assert reloaded.filter_review(10, [root, new_root], set()) == [new_root]

        assert provider.add_label.call_count == 2
        assert sum("Human intervention" in c.args[1] for c in provider.post_comment.call_args_list) == 1

    def test_escalation_marker_rate_limits_propagate(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        provider.list_issue_comments.side_effect = ProviderRateLimitError(provider="github", credential_identity="test")
        with pytest.raises(ProviderRateLimitError):
            tracker.escalate("root:101")
        provider.add_label.assert_not_called()
        provider.post_comment.assert_not_called()

    @pytest.mark.parametrize("pr_number", [0, -1, True, "42"])
    def test_invalid_pr(self, provider, pr_number):
        with pytest.raises(ValueError, match="PR number"):
            RepairAttemptTracker(provider, pr_number, "abc")

    @pytest.mark.parametrize("sha", ["", "x -->", None])
    def test_invalid_head(self, provider, sha):
        with pytest.raises(ValueError, match="HEAD"):
            RepairAttemptTracker(provider, 42, sha)

    @pytest.mark.parametrize(
        "comment_id, body",
        [
            ("1", "<!-- repair-dispatch-findings:42:abc:v1 -->\n{}"),
            (0, "<!-- repair-dispatch-findings:42:abc:v1 -->\n{}"),
            (1, "<!-- repair-dispatch-findings:42:abc:v2 -->\n{}"),
            (1, "<!-- repair-dispatch-findings:42:abc:v1 -->"),
            (1, "<!-- repair-dispatch-findings:42:abc:v1 -->\n{}\n🤖 AI PR Loop ·"),
        ],
    )
    def test_invalid_marker_envelope(self, provider, comment_id, body):
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=comment_id, author=TRUSTED_LOGIN, body=body)]
        with pytest.raises(ValueError, match="marker"):
            RepairAttemptTracker(provider, 42, "abc")

    def test_untrusted_author_marker_is_ignored(self, provider):
        """An arbitrary PR commenter cannot forge the reservation marker to suppress new attempts."""
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=999,
                author="random-pr-commenter",
                body="<!-- repair-dispatch-findings:42:abc:v1 -->\n" + json.dumps({"attempted": ["root:101"]}),
            )
        ]
        tracker = RepairAttemptTracker(provider, 42, "abc")
        assert tracker.attempted == set()
        assert tracker.comment_id is None

    def test_missing_workflow_identity_fails_closed_when_marker_exists(self, provider):
        """An unresolvable workflow identity must fail closed rather than trust an unverified marker."""
        provider.get_pr_token_login.return_value = ""
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="anyone",
                body="<!-- repair-dispatch-findings:42:abc:v1 -->\n{}",
            )
        ]
        with pytest.raises(ValueError, match="workflow identity"):
            RepairAttemptTracker(provider, 42, "abc")

    def test_missing_workflow_identity_is_harmless_without_a_marker(self, provider):
        """Identity resolution is only required once a candidate marker is actually found."""
        provider.get_pr_token_login.return_value = ""
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = []
        tracker = RepairAttemptTracker(provider, 42, "abc")
        assert tracker.attempted == set()

    @pytest.mark.parametrize(
        "data",
        [
            None,
            [],
            {},
            {"attempted": None},
            {"attempted": [1]},
            {"attempted": ["root:0"]},
            {"attempted": ["synthetic:1:0"]},
        ],
    )
    def test_invalid_marker_payload(self, provider, data):
        provider.post_comment(42, "<!-- repair-dispatch-findings:42:abc:v1 -->\n" + json.dumps(data))
        with pytest.raises(ValueError, match="identities"):
            RepairAttemptTracker(provider, 42, "abc")

    def test_corrupt_json(self, provider):
        provider.post_comment(42, "<!-- repair-dispatch-findings:42:abc:v1 -->\nbroken")
        with pytest.raises(ValueError):
            RepairAttemptTracker(provider, 42, "abc")

    def test_unknown_version_fails_closed(self, provider):
        provider.post_comment(42, "<!-- repair-dispatch-findings:42:abc:v2 -->\n{}")
        with pytest.raises(ValueError, match="marker"):
            RepairAttemptTracker(provider, 42, "abc")

    def test_reservation_survives_reload_and_head_change_is_eligible(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"root:101", "ci"})
        reloaded = RepairAttemptTracker(provider, 42, "abc")
        assert reloaded.attempted == {"root:101", "ci"}
        reloaded.reserve({"synthetic:10:-1"})
        assert RepairAttemptTracker(provider, 42, "abc").attempted == {"root:101", "ci", "synthetic:10:-1"}
        assert RepairAttemptTracker(provider, 42, "def").attempted == set()
        assert RepairAttemptTracker(provider, 43, "abc").attempted == set()

    @pytest.mark.parametrize("keys", [set(), {"root:101"}])
    def test_empty_or_duplicate_reservation_is_rejected(self, provider, keys):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"root:101"})
        with pytest.raises(ValueError):
            tracker.reserve(keys)

    @pytest.mark.parametrize("comment_id", [None, False, 0, "1"])
    def test_unacknowledged_reservation_fails(self, provider, comment_id):
        provider.post_comment.side_effect = None
        provider.post_comment.return_value = comment_id
        with pytest.raises(ValueError, match="persisted"):
            RepairAttemptTracker(provider, 42, "abc").reserve({"ci"})

    def test_unconfirmed_write_fails_closed(self, provider):
        provider.post_comment.side_effect = None
        provider.post_comment.return_value = 1
        with pytest.raises(ValueError, match="confirmed"):
            RepairAttemptTracker(provider, 42, "abc").reserve({"ci"})

    @pytest.mark.parametrize("comment_id", [True, 2])
    def test_malformed_readback_cannot_confirm_a_reservation(self, provider, comment_id):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        provider.find_comment.side_effect = lambda *_: (comment_id, provider.post_comment.call_args.args[1])
        with pytest.raises(ValueError, match="confirmed"):
            tracker.reserve({"ci"})

    def test_failed_update_keeps_prior_attempt(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"ci"})
        provider.update_comment.side_effect = RuntimeError("write failed")
        with pytest.raises(RuntimeError):
            tracker.reserve({"root:101"})
        assert RepairAttemptTracker(provider, 42, "abc").attempted == {"ci"}

    def test_release_persists_definitive_no_creation_reservation(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"ci", "root:101"})

        tracker.release({"ci"})

        assert tracker.attempted == {"root:101"}
        assert RepairAttemptTracker(provider, 42, "abc").attempted == {"root:101"}
        tracker.release({"root:101"})
        assert RepairAttemptTracker(provider, 42, "abc").attempted == set()

    @pytest.mark.parametrize("keys", [set(), {"root:101"}])
    def test_release_requires_an_active_reservation(self, provider, keys):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        with pytest.raises(ValueError, match="reservation"):
            tracker.release(keys)

    def test_failed_release_keeps_prior_attempt(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"ci"})
        provider.update_comment.side_effect = RuntimeError("write failed")

        with pytest.raises(RuntimeError, match="write failed"):
            tracker.release({"ci"})

        assert tracker.attempted == {"ci"}
        assert RepairAttemptTracker(provider, 42, "abc").attempted == {"ci"}

    def test_release_requires_persisted_reservation(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.attempted.add("ci")

        with pytest.raises(ValueError, match="not persisted"):
            tracker.release({"ci"})

    @pytest.mark.parametrize("readback", [None, (2, "wrong"), True])
    def test_unconfirmed_release_keeps_prior_attempt(self, provider, readback):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"ci"})
        if readback is True:
            body = provider.find_comment(42, tracker.prefix)[1]
            provider.find_comment.side_effect = lambda *_: (True, body)
        else:
            provider.find_comment.side_effect = lambda *_: readback

        with pytest.raises(ValueError, match="release could not be confirmed"):
            tracker.release({"ci"})

        assert tracker.attempted == {"ci"}

    def test_repeated_reservations_use_migrated_comment_id(self, provider):
        legacy_body = "<!-- repair-dispatch-findings:42:abc:v1 -->\n" + json.dumps({"attempted": ["ci"]})
        current = {"id": 99, "body": legacy_body}
        provider.get_trusted_loop_comment_logins.return_value = {"legacy-pat", TRUSTED_LOGIN}
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=99, author="legacy-pat", body=legacy_body),
        ]

        def find_comment(_pr_number, marker):
            return (current["id"], current["body"]) if marker in current["body"] else None

        def update_comment(comment_id, body):
            if comment_id == 99:
                current["id"] = 100
                current["body"] = body
                return 100
            current["body"] = body
            return None

        provider.find_comment.side_effect = find_comment
        provider.update_comment.side_effect = update_comment
        tracker = RepairAttemptTracker(provider, 42, "abc")

        tracker.reserve({"root:101"})
        tracker.reserve({"root:102"})

        assert [call.args[0] for call in provider.update_comment.call_args_list] == [99, 100]
        assert tracker.comment_id == 100
        assert "root:102" in current["body"]
        provider.post_comment.assert_not_called()

    def test_rejects_invalid_comment_id_returned_during_migration(self, provider):
        legacy_body = "<!-- repair-dispatch-findings:42:abc:v1 -->\n" + json.dumps({"attempted": ["ci"]})
        provider.get_trusted_loop_comment_logins.return_value = {TRUSTED_LOGIN}
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=99, author=TRUSTED_LOGIN, body=legacy_body),
        ]
        provider.update_comment.side_effect = None
        provider.update_comment.return_value = 0
        tracker = RepairAttemptTracker(provider, 42, "abc")

        with pytest.raises(ValueError, match="migration returned an invalid comment ID"):
            tracker.reserve({"root:101"})

    @pytest.mark.parametrize("comment_id", [0, True, None])
    def test_invalid_finding_identity(self, comment_id):
        comment = ReviewCommentInfo(id=comment_id, path="", body="", html_url="")
        with pytest.raises(ValueError, match="finding ID"):
            RepairAttemptTracker.finding_key(10, comment)

    def test_native_roots_and_synthetic_ids_have_different_scopes(self):
        root = ReviewCommentInfo(id=101, path="", body="", html_url="")
        synthetic = ReviewCommentInfo(id=-1, path="", body="", html_url="")
        reply = ReviewCommentInfo(id=102, path="", body="", html_url="", in_reply_to_id=101)
        assert RepairAttemptTracker.finding_key(10, root) == RepairAttemptTracker.finding_key(20, root)
        assert RepairAttemptTracker.finding_key(10, synthetic) != RepairAttemptTracker.finding_key(20, synthetic)
        assert RepairAttemptTracker.finding_key(10, reply) is None

    @pytest.mark.parametrize("review_id", [0, True, None])
    def test_invalid_review_identity(self, review_id):
        comment = ReviewCommentInfo(id=101, path="", body="", html_url="")
        with pytest.raises(ValueError, match="review ID"):
            RepairAttemptTracker.finding_key(review_id, comment)

    @pytest.mark.parametrize("parent_id", [0, -1, True, "101"])
    def test_invalid_parent_identity(self, parent_id):
        comment = ReviewCommentInfo(id=102, path="", body="", html_url="", in_reply_to_id=parent_id)
        with pytest.raises(ValueError, match="parent finding ID"):
            RepairAttemptTracker.finding_key(10, comment)

    def test_attempted_answered_root_escalates_once_but_new_work_remains(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"root:101", "synthetic:10:-1"})
        root = ReviewCommentInfo(id=101, path="", body="", html_url="")
        reply = ReviewCommentInfo(id=102, path="", body="Fixed", html_url="", in_reply_to_id=101)
        synthetic = ReviewCommentInfo(id=-1, path="", body="", html_url="")
        new_root = ReviewCommentInfo(id=103, path="", body="", html_url="")
        assert tracker.filter_review(10, [root, reply, synthetic, new_root], set()) == [new_root]
        tracker.filter_review(10, [root], set())
        assert sum("Human intervention" in c.args[1] for c in provider.post_comment.call_args_list) == 2
        provider.add_label.assert_called_with(42, "ai-pr-loop:agent-failed")
        provider.assign_issue.assert_not_called()
        assert tracker.filter_review(20, [synthetic], set()) == [synthetic]

    def test_resolved_attempted_roots_do_not_escalate(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        tracker.reserve({"root:101"})
        root = ReviewCommentInfo(id=101, path="", body="", html_url="")
        assert tracker.filter_review(10, [root], {101}) == []
        provider.add_label.assert_not_called()

    @pytest.mark.parametrize("comments", [None, {}, [None]])
    def test_invalid_review_comment_collection(self, provider, comments):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        with pytest.raises(ValueError, match="comments"):
            tracker.filter_review(10, comments, set())

    @pytest.mark.parametrize(
        "comment_id, body",
        [
            (0, "<!-- repair-dispatch-escalation:v1:42:abc:root:101 -->\nHuman intervention required"),
            ("1", "<!-- repair-dispatch-escalation:v1:42:abc:root:101 -->\nHuman intervention required"),
            (1, "<!-- repair-dispatch-escalation:v1:42:abc:root:101 -->"),
        ],
    )
    def test_malformed_escalation_fails_closed(self, provider, comment_id, body):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = [IssueCommentInfo(id=comment_id, author=TRUSTED_LOGIN, body=body)]
        with pytest.raises(ValueError, match="escalation marker"):
            tracker.escalate("root:101")

    def test_untrusted_author_escalation_marker_does_not_suppress_notification(self, provider):
        """A forged escalation marker from an untrusted author must not block the human notification."""
        marker = "<!-- repair-dispatch-escalation:v1:42:abc:root:101 -->"
        tracker = RepairAttemptTracker(provider, 42, "abc")
        provider.list_issue_comments.side_effect = None
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=999, author="random-pr-commenter", body=f"{marker}\nFake notice")
        ]
        tracker.escalate("root:101")
        assert provider.post_comment.call_args is not None
        assert "Human intervention" in provider.post_comment.call_args.args[1]

    def test_unacknowledged_escalation_fails(self, provider):
        tracker = RepairAttemptTracker(provider, 42, "abc")
        provider.post_comment.side_effect = None
        provider.post_comment.return_value = None
        with pytest.raises(ValueError, match="escalation was not persisted"):
            tracker.escalate("root:101")

    def test_required_thread_states(self, provider):
        provider.list_review_thread_states.return_value = {101: (True, False), 102: (False, True)}
        assert RepairAttemptTracker(provider, 42, "abc").resolved_ids() == {101}

    @pytest.mark.parametrize(
        "states", [None, {True: (True, False)}, {0: (True, False)}, {1: None}, {1: (True,)}, {1: (1, False)}]
    )
    def test_invalid_thread_states(self, provider, states):
        provider.list_review_thread_states.return_value = states
        with pytest.raises(ValueError, match="thread state"):
            RepairAttemptTracker(provider, 42, "abc").resolved_ids()

    def test_thread_rate_limits_propagate(self, provider):
        provider.list_review_thread_states.side_effect = ProviderRateLimitError(
            provider="github", credential_identity="test"
        )
        with pytest.raises(ProviderRateLimitError):
            RepairAttemptTracker(provider, 42, "abc").resolved_ids()
