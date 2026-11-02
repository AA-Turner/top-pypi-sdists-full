"""Tests for build_answer_skeleton."""

from agentic_devtools.cli.azure_devops.pr_review_answers import (
    build_answer_skeleton,
    derive_attempt_id,
)


class TestBuildAnswerSkeleton:
    def test_full_fields(self):
        skeleton = build_answer_skeleton(
            pr_id=1,
            commit_hash="abc",
            file_key="k",
            file_path="/a",
            review_mode="diff",
            review_depth="deep",
            prompt_hash="ph",
        )
        assert skeleton["schemaVersion"] == 1
        assert skeleton["prId"] == 1
        assert skeleton["commitHash"] == "abc"
        assert skeleton["fileKey"] == "k"
        assert skeleton["filePath"] == "/a"
        assert skeleton["reviewMode"] == "diff"
        assert skeleton["reviewDepth"] == "deep"
        assert skeleton["promptHash"] == "ph"
        assert skeleton["attemptId"] == derive_attempt_id("k", "abc", "ph")
        assert skeleton["status"] == "pending"
        assert skeleton["outcome"] is None
        assert skeleton["summary"] is None
        assert skeleton["suggestions"] == []
        assert skeleton["needsInfo"] is None
        assert skeleton["reviewer"] is None
        assert skeleton["confidence"] is None

    def test_empty_commit_and_none_depth(self):
        skeleton = build_answer_skeleton(
            pr_id=1,
            commit_hash="",
            file_key="k",
            file_path="/a",
            review_mode="binary",
            review_depth=None,
            prompt_hash="ph",
        )
        assert skeleton["commitHash"] == ""
        assert skeleton["reviewDepth"] is None
