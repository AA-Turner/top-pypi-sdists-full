"""Tests for check_answer_scope."""

from agentic_devtools.cli.azure_devops.pr_review_write import check_answer_scope


class TestCheckAnswerScope:
    def test_matching_scope(self):
        assert check_answer_scope({"fileKey": "k"}, "k", {"fileKey": "k"}) == []

    def test_answer_key_mismatch(self):
        errors = check_answer_scope({"fileKey": "other"}, "k", {"fileKey": "k"})
        assert any("answer fileKey" in e for e in errors)

    def test_answer_non_dict(self):
        errors = check_answer_scope("nope", "k", {"fileKey": "k"})
        assert any("answer fileKey" in e for e in errors)

    def test_scaffold_key_mismatch(self):
        errors = check_answer_scope({"fileKey": "k"}, "k", {"fileKey": "other"})
        assert any("scaffold fileKey" in e for e in errors)
