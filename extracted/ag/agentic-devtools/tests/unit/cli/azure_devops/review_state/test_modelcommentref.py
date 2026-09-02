"""Tests for the ModelCommentRef dataclass."""

from agentic_devtools.cli.azure_devops.review_state import ModelCommentRef, ReviewStatus


class TestModelCommentRef:
    """Tests for ModelCommentRef serialization and defaults."""

    def test_creation_with_defaults(self):
        ref = ModelCommentRef(modelId="Claude Opus 4.6")
        assert ref.modelId == "Claude Opus 4.6"
        assert ref.commentId == 0
        assert ref.continuationCommentIds == []
        assert ref.status == ReviewStatus.UNREVIEWED.value
        assert ref.timestamp is None

    def test_to_dict(self):
        ref = ModelCommentRef(
            modelId="GPT-5.5",
            commentId=42,
            continuationCommentIds=[43, 44],
            status=ReviewStatus.APPROVED.value,
            timestamp="2026-02-25T10:00:00Z",
        )
        d = ref.to_dict()
        assert d == {
            "modelId": "GPT-5.5",
            "commentId": 42,
            "continuationCommentIds": [43, 44],
            "status": "approved",
            "timestamp": "2026-02-25T10:00:00Z",
        }

    def test_from_dict_round_trip(self):
        ref = ModelCommentRef(
            modelId="GPT-5.5",
            commentId=42,
            continuationCommentIds=[43, 44],
            status=ReviewStatus.NEEDS_WORK.value,
            timestamp="2026-02-25T10:00:00Z",
        )
        restored = ModelCommentRef.from_dict(ref.to_dict())
        assert restored == ref

    def test_from_dict_tolerates_missing_optional_fields(self):
        restored = ModelCommentRef.from_dict({"modelId": "m1", "commentId": 7})
        assert restored.modelId == "m1"
        assert restored.commentId == 7
        assert restored.continuationCommentIds == []
        assert restored.status == ReviewStatus.UNREVIEWED.value
        assert restored.timestamp is None
