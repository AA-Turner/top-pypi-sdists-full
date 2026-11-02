"""Tests for check_answer_freshness."""

from agentic_devtools.cli.azure_devops.pr_review_write import check_answer_freshness


def _scaffold():
    return {
        "promptHash": "p",
        "commitHash": "c",
        "attemptId": "a",
        "reviewMode": "diff",
        "filePath": "/src/a.ts",
        "prId": 123,
        "reviewDepth": "full",
    }


def _answer():
    return {
        "promptHash": "p",
        "commitHash": "c",
        "attemptId": "a",
        "reviewMode": "diff",
        "filePath": "/src/a.ts",
        "prId": 123,
        "reviewDepth": "full",
    }


class TestCheckAnswerFreshness:
    def test_fresh(self):
        assert check_answer_freshness(_answer(), _scaffold()) == []

    def test_stale_prompt_hash(self):
        answer = {**_answer(), "promptHash": "x"}
        assert any("promptHash" in e for e in check_answer_freshness(answer, _scaffold()))

    def test_stale_commit_hash(self):
        answer = {**_answer(), "commitHash": "x"}
        assert any("commitHash" in e for e in check_answer_freshness(answer, _scaffold()))

    def test_stale_attempt_id(self):
        answer = {**_answer(), "attemptId": "x"}
        assert any("attemptId" in e for e in check_answer_freshness(answer, _scaffold()))

    def test_non_dict_answer(self):
        # All 3 freshness fields + 4 scaffold-locked fields = 7 errors when
        # both sides diverge (answer=None vs scaffold values).
        errors = check_answer_freshness("nope", _scaffold())
        assert len(errors) == 7

    # --- scaffold-locked field checks ---

    def test_review_mode_spoofed(self):
        answer = {**_answer(), "reviewMode": "binary"}
        errors = check_answer_freshness(answer, _scaffold())
        assert any("reviewMode" in e and "scaffold mismatch" in e for e in errors)

    def test_file_path_spoofed(self):
        answer = {**_answer(), "filePath": "/evil/path.ts"}
        errors = check_answer_freshness(answer, _scaffold())
        assert any("filePath" in e and "scaffold mismatch" in e for e in errors)

    def test_pr_id_spoofed(self):
        answer = {**_answer(), "prId": 999}
        errors = check_answer_freshness(answer, _scaffold())
        assert any("prId" in e and "scaffold mismatch" in e for e in errors)

    def test_review_depth_spoofed(self):
        answer = {**_answer(), "reviewDepth": "light"}
        errors = check_answer_freshness(answer, _scaffold())
        assert any("reviewDepth" in e and "scaffold mismatch" in e for e in errors)

    def test_review_depth_none_matches_scaffold_none(self):
        scaffold = {**_scaffold(), "reviewDepth": None}
        answer = {**_answer(), "reviewDepth": None}
        assert check_answer_freshness(answer, scaffold) == []

    def test_scaffold_missing_locked_field_matches_absent_in_answer(self):
        # When the scaffold doesn't have reviewDepth at all, missing from answer is also fine.
        scaffold = {k: v for k, v in _scaffold().items() if k != "reviewDepth"}
        answer = {k: v for k, v in _answer().items() if k != "reviewDepth"}
        assert check_answer_freshness(answer, scaffold) == []
