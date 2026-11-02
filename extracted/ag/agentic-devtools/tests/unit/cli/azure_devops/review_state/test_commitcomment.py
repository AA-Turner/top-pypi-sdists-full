"""Tests for the CommitComment dataclass."""

from agentic_devtools.cli.azure_devops.review_state import (
    CommitComment,
    ModelCommentRef,
    ReviewStatus,
)


class TestCommitComment:
    """Tests for CommitComment serialization, defaults, and helpers."""

    def test_creation_with_defaults(self):
        cc = CommitComment(commitHash="a" * 40)
        assert cc.commitHash == "a" * 40
        assert cc.threadId == 0
        assert cc.models == []
        assert cc.status == ReviewStatus.UNREVIEWED.value
        assert cc.timestamp is None
        assert cc.rootCommentId == 0

    def test_root_comment_id_uses_first_model(self):
        cc = CommitComment(
            commitHash="b" * 40,
            threadId=10,
            models=[
                ModelCommentRef(modelId="m1", commentId=100),
                ModelCommentRef(modelId="m2", commentId=200),
            ],
        )
        assert cc.rootCommentId == 100

    def test_get_model(self):
        ref = ModelCommentRef(modelId="m1", commentId=100)
        cc = CommitComment(commitHash="c" * 40, models=[ref])
        assert cc.get_model("m1") is ref
        assert cc.get_model("missing") is None

    def test_upsert_model_returns_existing(self):
        ref = ModelCommentRef(modelId="m1", commentId=100)
        cc = CommitComment(commitHash="d" * 40, models=[ref])
        got = cc.upsert_model("m1")
        assert got is ref
        assert len(cc.models) == 1

    def test_upsert_model_appends_new(self):
        cc = CommitComment(commitHash="e" * 40, models=[ModelCommentRef(modelId="m1")])
        got = cc.upsert_model("m2")
        assert got.modelId == "m2"
        assert len(cc.models) == 2
        assert cc.models[1] is got

    def test_to_from_dict_round_trip(self):
        cc = CommitComment(
            commitHash="f" * 40,
            threadId=10,
            models=[
                ModelCommentRef(modelId="m1", commentId=100, continuationCommentIds=[101]),
                ModelCommentRef(modelId="m2", commentId=200),
            ],
            status=ReviewStatus.NEEDS_WORK.value,
            timestamp="2026-02-25T10:00:00Z",
        )
        restored = CommitComment.from_dict(cc.to_dict())
        assert restored == cc

    def test_from_dict_tolerates_missing_optional_fields(self):
        restored = CommitComment.from_dict({"commitHash": "g" * 40})
        assert restored.commitHash == "g" * 40
        assert restored.threadId == 0
        assert restored.models == []
        assert restored.status == ReviewStatus.UNREVIEWED.value
        assert restored.timestamp is None
