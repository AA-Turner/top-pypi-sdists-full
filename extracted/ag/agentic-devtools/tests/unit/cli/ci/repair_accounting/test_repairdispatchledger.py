"""Durable confirmed-receipt and uncertain-creation lifecycle tests."""

import json
from dataclasses import replace
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.repair_accounting import RepairDispatchLedger


@pytest.fixture
def ledger() -> RepairDispatchLedger:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "dispatch-bot"
    comments: list[IssueCommentInfo] = []
    provider.list_issue_comments.side_effect = lambda _: list(comments)

    def post(pr: int, body: str) -> int:
        comment_id = max((item.id for item in comments), default=0) + 1
        comments.append(IssueCommentInfo(comment_id, "dispatch-bot", body))
        return comment_id

    def update(comment_id: int, body: str) -> None:
        index = next(index for index, item in enumerate(comments) if item.id == comment_id)
        comments[index] = replace(comments[index], body=body)

    provider.post_comment_as_pr_token.side_effect = post
    provider.update_comment_as_pr_token.side_effect = update
    return RepairDispatchLedger(provider, 42, "abc123", 10, "work")


class TestRepairDispatchLedger:
    def test_begin_does_not_consume_budget_and_replay_records_once(self, ledger) -> None:
        ledger.reconcile()
        ledger.begin()
        assert ledger.read()[:2] == (set(), True)
        ledger.record(77)
        ledger.record(77)
        assert ledger.read()[:2] == ({"comment-77"}, False)
        ledger.begin()
        ledger.record("task-88")
        assert ledger.read()[:2] == ({"comment-77", "task-88"}, False)

    def test_record_converges_duplicate_pending_authenticated_records(self, ledger) -> None:
        ledger.begin()
        original = next(
            comment for comment in ledger.provider.list_issue_comments(42) if comment.body.startswith(ledger.marker)
        )
        ledger.provider.post_comment_as_pr_token(42, original.body)

        ledger.record("task-88")

        records = [
            comment
            for comment in ledger.provider.list_issue_comments(42)
            if comment.body.startswith(ledger.marker + "\n")
        ]
        assert len(records) == 2
        assert all(
            json.loads(comment.body.split("\n", 2)[1]) == {"receipts": ["task-88"], "pending": False, "after": 0}
            for comment in records
        )
        assert ledger.read()[:2] == ({"task-88"}, False)

    def test_unresolved_creation_blocks_replacement(self, ledger) -> None:
        ledger.begin()
        with pytest.raises(RuntimeError, match="Unresolved"):
            ledger.begin()
        with pytest.raises(RuntimeError, match="Unresolved"):
            ledger.reconcile()

    def test_unresolved_prior_scope_blocks_changed_work(self, ledger) -> None:
        ledger.begin()
        with pytest.raises(RuntimeError, match="prior repair scope"):
            replace(ledger, review_id=11).begin()

    def test_confirmed_prior_scope_does_not_block_changed_work(self, ledger) -> None:
        ledger.record(77)
        next_scope = replace(ledger, review_id=11)
        next_scope.begin()
        assert next_scope.read()[:2] == (set(), True)

    def test_malformed_prior_scope_cannot_enable_replacement(self, ledger) -> None:
        ledger.provider.post_comment_as_pr_token(42, "<!-- repair-dispatch:v2:another-scope -->\n[]")
        with pytest.raises(RuntimeError, match="prior repair scope"):
            ledger.begin()

    def test_changed_scope_reconciles_authentic_prior_creation_before_replacement(self, ledger) -> None:
        ledger.begin()
        receipt = ledger.provider.post_comment_as_pr_token(42, "@copilot repair\n" + ledger.evidence_marker)
        new_scope = replace(ledger, review_id=11)
        new_scope.reconcile()
        assert ledger.read()[:2] == ({f"comment-{receipt}"}, False)
        new_scope.begin()
        new_scope.record(99)
        new_scope.reconcile()

    def test_changed_scope_cannot_reconcile_an_unknown_prior_creation(self, ledger) -> None:
        ledger.begin()
        with pytest.raises(RuntimeError, match="Unresolved repair creation"):
            replace(ledger, review_id=11).reconcile()

    def test_reconciles_authentic_created_comment(self, ledger) -> None:
        ledger.begin()
        receipt = ledger.provider.post_comment_as_pr_token(42, "@copilot repair\n" + ledger.evidence_marker)
        ledger.reconcile()
        assert ledger.record(receipt) == 1
        assert ledger.read()[:2] == ({f"comment-{receipt}"}, False)

    def test_retires_pending_creation_with_durable_no_creation_evidence(self, ledger) -> None:
        ledger.begin()

        ledger.retire_pending()

        assert ledger.read()[:2] == (set(), False)
        assert any(comment.body == ledger.no_creation_marker for comment in ledger.provider.list_issue_comments(42))

    def test_reconciles_pending_creation_after_retirement_write_failure(self, ledger) -> None:
        ledger.begin()
        original_update = ledger.provider.update_comment_as_pr_token.side_effect

        def fail_update(*_args) -> None:
            raise RuntimeError("write failed")

        ledger.provider.update_comment_as_pr_token.side_effect = fail_update

        with pytest.raises(RuntimeError, match="write failed"):
            ledger.retire_pending()

        assert ledger.read()[1] is True
        ledger.provider.update_comment_as_pr_token.side_effect = original_update
        ledger.reconcile()

        assert ledger.read()[:2] == (set(), False)

    def test_reuses_durable_no_creation_evidence_after_retirement_write_failure(self, ledger) -> None:
        ledger.begin()
        original_update = ledger.provider.update_comment_as_pr_token.side_effect

        def fail_update(*_args) -> None:
            raise RuntimeError("write failed")

        ledger.provider.update_comment_as_pr_token.side_effect = fail_update

        with pytest.raises(RuntimeError, match="write failed"):
            ledger.retire_pending()

        ledger.provider.update_comment_as_pr_token.side_effect = original_update
        ledger.retire_pending()

        comments = ledger.provider.list_issue_comments(42)
        assert sum(comment.body == ledger.no_creation_marker for comment in comments) == 1
        assert ledger.read()[:2] == (set(), False)

    def test_retirement_requires_durable_no_creation_evidence(self, ledger) -> None:
        ledger.begin()
        ledger.provider.post_comment_as_pr_token.side_effect = lambda *_: 99

        with pytest.raises(RuntimeError, match="no-creation evidence"):
            ledger.retire_pending()

        assert ledger.read()[1] is True

    def test_no_creation_reconciliation_requires_read_back(self, ledger) -> None:
        ledger.begin()
        ledger.provider.post_comment_as_pr_token(42, ledger.no_creation_marker)
        ledger.provider.update_comment_as_pr_token.side_effect = lambda *_: None

        with pytest.raises(RuntimeError, match="no-creation reconciliation persistence"):
            ledger.reconcile()

    def test_old_no_creation_evidence_does_not_reconcile_a_new_intent(self, ledger) -> None:
        ledger.begin()
        ledger.retire_pending()
        ledger.begin()

        with pytest.raises(RuntimeError, match="Unresolved repair creation"):
            ledger.reconcile()

    def test_quoted_evidence_marker_is_not_a_receipt(self, ledger) -> None:
        other_marker = "<!-- repair-dispatch:work:other-scope -->"
        ledger.provider.post_comment_as_pr_token(
            42,
            f"@copilot repair\nQuoted evidence: {ledger.evidence_marker}\n{other_marker}",
        )

        assert ledger.read()[:2] == (set(), False)

    def test_quoted_evidence_marker_cannot_reconcile_pending_creation(self, ledger) -> None:
        ledger.begin()
        other_marker = "<!-- repair-dispatch:work:other-scope -->"
        ledger.provider.post_comment_as_pr_token(
            42,
            f"@copilot repair\nQuoted evidence: {ledger.evidence_marker}\n{other_marker}",
        )

        with pytest.raises(RuntimeError, match="Unresolved repair creation"):
            ledger.reconcile()

    def test_completed_scopes_share_one_authenticated_inventory(self, ledger) -> None:
        ledger.record(77)
        replace(ledger, review_id=9).record(88)
        ledger.provider.list_issue_comments.reset_mock()

        ledger.reconcile()

        ledger.provider.list_issue_comments.assert_called_once_with(42)

    def test_old_success_is_not_evidence_for_a_new_pending_creation(self, ledger) -> None:
        receipt = ledger.provider.post_comment_as_pr_token(42, "@copilot repair\n" + ledger.evidence_marker)
        ledger.record(receipt)
        ledger.begin()
        with pytest.raises(RuntimeError, match="Unresolved"):
            ledger.reconcile()

    def test_legacy_dispatches_do_not_consume_modern_work_scopes(self, ledger) -> None:
        ledger.provider.post_comment_as_pr_token(42, "<!-- repair-dispatch:abc123:8 -->")
        assert ledger.read()[0] == set()
        for _ in range(3):
            ledger.provider.post_comment_as_pr_token(42, "@copilot review\n<!-- copilot-trigger:10 -->\nHEAD `abc123`")
        assert ledger.read()[0] == set()
        assert replace(ledger, review_id=11).read()[0] == set()
        assert replace(ledger, head_sha="def456").read()[0] == set()

    def test_retire_pending_clears_intent_without_adding_a_receipt(self, ledger) -> None:
        ledger.begin()
        ledger.retire_pending()
        assert ledger.read()[:2] == (set(), False)
        ledger.retire_pending()
        changed_scope = replace(ledger, review_id=11)
        changed_scope.begin()
        assert changed_scope.read()[:2] == (set(), True)

    def test_retire_pending_requires_read_back(self, ledger) -> None:
        ledger.begin()
        ledger.provider.update_comment_as_pr_token.side_effect = lambda *_: None
        with pytest.raises(RuntimeError, match="retirement could not be confirmed"):
            ledger.retire_pending()

    @pytest.mark.parametrize("receipt", [None, False, 0, -1, "", [], {}])
    def test_requires_a_confirmed_receipt(self, ledger, receipt) -> None:
        with pytest.raises(ValueError, match="receipt"):
            ledger.record(receipt)

    @pytest.mark.parametrize(
        "data",
        [
            [],
            {},
            {"receipts": [], "pending": True},
            {"receipts": "bad", "pending": False, "after": 0},
            {"receipts": [None], "pending": False, "after": 0},
            {"receipts": [""], "pending": False, "after": 0},
            {"receipts": [], "pending": 1, "after": 0},
            {"receipts": [], "pending": False, "after": "bad"},
        ],
    )
    def test_malformed_accounting_fails_closed(self, ledger, data) -> None:
        ledger.provider.post_comment_as_pr_token(42, ledger.marker + "\n" + json.dumps(data))
        with pytest.raises(RuntimeError, match="Invalid"):
            ledger.read()

    def test_begin_requires_read_back(self, ledger) -> None:
        ledger.provider.post_comment_as_pr_token.side_effect = lambda *args: 1
        with pytest.raises(RuntimeError, match="confirmed"):
            ledger.begin()

    def test_record_requires_read_back(self, ledger) -> None:
        ledger.begin()
        ledger.provider.update_comment_as_pr_token.side_effect = lambda *args: None
        with pytest.raises(RuntimeError, match="persistence"):
            ledger.record(77)

    def test_reconcile_requires_read_back(self, ledger) -> None:
        ledger.begin()
        ledger.provider.post_comment_as_pr_token(42, "@copilot repair\n" + ledger.evidence_marker)
        ledger.provider.update_comment_as_pr_token.side_effect = lambda *args: None
        with pytest.raises(RuntimeError, match="persistence"):
            ledger.reconcile()

    def test_reconcile_pending_is_noop_without_intent(self, ledger) -> None:
        ledger._reconcile_pending()

        ledger.provider.update_comment_as_pr_token.assert_not_called()

    def test_reads_evidence_marker_before_terminal_comment_label(self, ledger) -> None:
        receipt = ledger.provider.post_comment_as_pr_token(
            42,
            f"@copilot repair\n{ledger.evidence_marker}\n\n🤖 AI PR Loop ·",
        )

        assert ledger.read()[:2] == ({f"comment-{receipt}"}, False)

    def test_reconciles_pending_dispatch_with_terminal_comment_label(self, ledger) -> None:
        ledger.begin()
        receipt = ledger.provider.post_comment_as_pr_token(
            42,
            f"@copilot repair\n{ledger.evidence_marker}\n\n🤖 AI PR Loop ·",
        )

        ledger.reconcile()

        assert ledger.read()[:2] == ({f"comment-{receipt}"}, False)

    def test_updates_ledger_records_through_pr_token_path(self, ledger) -> None:
        ledger.begin()
        ledger.record(77)

        ledger.provider.update_comment_as_pr_token.assert_called()
        ledger.provider.update_comment.assert_not_called()
