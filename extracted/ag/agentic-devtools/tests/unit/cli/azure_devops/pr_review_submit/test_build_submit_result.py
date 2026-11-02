"""Tests for build_submit_result."""

from agentic_devtools.cli.azure_devops.pr_review_submit import (
    SUBMIT_RESULT_SCHEMA_VERSION,
    build_submit_result,
)


def _submittable(file_key, file_path):
    return {"fileKey": file_key, "filePath": file_path, "item": {}}


class TestBuildSubmitResult:
    def test_dry_run_with_no_outcomes(self):
        result = build_submit_result(
            pr_id=5,
            commit_hash="abc",
            dry_run=True,
            submittable=[_submittable("a", "/a")],
            skipped=[{"fileKey": "s", "reason": "status:pending"}],
            stale=[{"fileKey": "t", "errors": ["bad"]}],
            item_outcomes={},
            generated_utc="2026-06-25T00:00:00+00:00",
        )
        assert result["schemaVersion"] == SUBMIT_RESULT_SCHEMA_VERSION
        assert result["dryRun"] is True
        assert result["accepted"] == ["a"]
        assert result["posted"] == []
        assert result["counts"] == {
            "accepted": 1,
            "posted": 0,
            "markedViewed": 0,
            "failed": 0,
            "skipped": 1,
            "stale": 1,
        }

    def test_posted_and_failed_mix(self):
        result = build_submit_result(
            pr_id=5,
            commit_hash="abc",
            dry_run=False,
            submittable=[_submittable("a", "/a"), _submittable("b", "/b")],
            skipped=[],
            stale=[],
            item_outcomes={
                "a": {"status": "posted", "error": None, "attempts": 1},
                "b": {"status": "failed", "error": "boom", "attempts": 2},
            },
            generated_utc="t",
        )
        assert result["posted"] == ["a"]
        assert result["markedViewed"] == ["a"]
        assert result["retriable"] == ["b"]
        assert result["failed"] == [{"fileKey": "b", "filePath": "/b", "error": "boom", "attempts": 2}]
        assert result["counts"]["posted"] == 1
        assert result["counts"]["failed"] == 1
        assert result["counts"]["markedViewed"] == 1
