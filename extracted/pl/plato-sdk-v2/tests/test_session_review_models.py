"""Tests for built-in session review models."""

from plato.worlds.base import BaseWorld
from plato.worlds.review import collect_review_schemas, get_review_model_meta, review_model_to_json_schema
from plato.worlds.session_review_models import (
    DEFAULT_REVIEW_MODELS,
    ReviewFindingFeedback,
    SessionChunkSummary,
    SessionReviewIssue,
    SessionReviewRecommendation,
    SessionReviewSummary,
)


class TestSessionReviewModels:
    """Test that session review models are properly decorated and structured."""

    def test_default_review_models_has_all_four(self):
        assert len(DEFAULT_REVIEW_MODELS) == 4
        assert SessionReviewIssue in DEFAULT_REVIEW_MODELS
        assert SessionReviewRecommendation in DEFAULT_REVIEW_MODELS
        assert SessionChunkSummary in DEFAULT_REVIEW_MODELS
        assert SessionReviewSummary in DEFAULT_REVIEW_MODELS

    def test_session_review_issue_has_meta(self):
        meta = get_review_model_meta(SessionReviewIssue)
        assert meta is not None
        assert meta.name == "session_review_issue"

    def test_session_review_recommendation_has_meta(self):
        meta = get_review_model_meta(SessionReviewRecommendation)
        assert meta is not None
        assert meta.name == "session_review_recommendation"

    def test_session_chunk_summary_has_meta(self):
        meta = get_review_model_meta(SessionChunkSummary)
        assert meta is not None
        assert meta.name == "session_chunk_summary"

    def test_session_review_summary_has_meta(self):
        meta = get_review_model_meta(SessionReviewSummary)
        assert meta is not None
        assert meta.name == "session_review_summary"

    def test_issue_schema_generation(self):
        schema = review_model_to_json_schema(SessionReviewIssue)
        assert "properties" in schema
        assert "title" in schema["properties"]
        assert "severity" in schema["properties"]
        assert "supporting_span_ids" in schema["properties"]

    def test_recommendation_schema_generation(self):
        schema = review_model_to_json_schema(SessionReviewRecommendation)
        assert "properties" in schema
        assert "title" in schema["properties"]
        assert "priority" in schema["properties"]
        assert "category" in schema["properties"]

    def test_chunk_summary_schema_generation(self):
        schema = review_model_to_json_schema(SessionChunkSummary)
        assert "properties" in schema
        assert "chunk_id" in schema["properties"]
        assert "summary" in schema["properties"]
        assert "span_count" in schema["properties"]

    def test_summary_schema_generation(self):
        schema = review_model_to_json_schema(SessionReviewSummary)
        assert "properties" in schema
        assert "summary" in schema["properties"]
        assert "issue_count" in schema["properties"]
        assert "recommendation_count" in schema["properties"]

    def test_issue_instantiation_and_type(self):
        issue = SessionReviewIssue(
            title="Test issue",
            description="Something went wrong",
            severity="high",
            category="correctness",
            supporting_span_ids=["span-1", "span-2"],
        )
        assert issue.type == "session_review_issue"
        data = issue.to_data()
        assert data["title"] == "Test issue"
        assert data["type"] == "session_review_issue"

    def test_recommendation_instantiation_and_type(self):
        rec = SessionReviewRecommendation(
            title="Use caching",
            description="Cache API responses to reduce latency",
            priority="high",
            category="performance",
            supporting_span_ids=["span-1"],
        )
        assert rec.type == "session_review_recommendation"
        data = rec.to_data()
        assert data["priority"] == "high"
        assert data["type"] == "session_review_recommendation"

    def test_chunk_summary_instantiation_and_type(self):
        cs = SessionChunkSummary(
            chunk_id="chunk-0001",
            summary="Agent completed login flow",
            span_count=42,
            highlights="- Logged in successfully\n- Navigated to dashboard",
        )
        assert cs.type == "session_chunk_summary"
        data = cs.to_data()
        assert data["chunk_id"] == "chunk-0001"

    def test_summary_instantiation(self):
        summary = SessionReviewSummary(
            summary="Session had issues",
            issue_count=3,
            recommendation_count=2,
            inspected_chunks=5,
            review_kind="overview",
        )
        assert summary.type == "session_review_summary"

    def test_feedback_model(self):
        fb = ReviewFindingFeedback(verdict="agree", comment="Looks correct")
        assert fb.verdict == "agree"
        assert fb.comment == "Looks correct"

    def test_all_models_have_feedback(self):
        """Every review model should have a Feedback class for user input."""
        for model in DEFAULT_REVIEW_MODELS:
            assert hasattr(model, "Feedback"), f"{model.__name__} missing Feedback"
            assert model.Feedback is ReviewFindingFeedback

    def test_base_world_has_default_review_models(self):
        for model in DEFAULT_REVIEW_MODELS:
            assert model in BaseWorld.review_models

    def test_collect_review_schemas_from_base_world(self):
        schemas = collect_review_schemas(BaseWorld)
        assert "session_review_issue" in schemas
        assert "session_review_recommendation" in schemas
        assert "session_chunk_summary" in schemas
        assert "session_review_summary" in schemas
