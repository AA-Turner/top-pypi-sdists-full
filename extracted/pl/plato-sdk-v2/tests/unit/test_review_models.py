"""Tests for the review model schema system."""

from __future__ import annotations

from typing import Annotated

import pytest
from pydantic import BaseModel, Field

from plato.worlds.review import (
    FeedbackField,
    RenderHint,
    ReviewData,
    collect_review_schemas,
    get_review_model_meta,
    review_model,
    review_model_to_json_schema,
)
from plato.worlds.review.result import ReviewFinding, ReviewResult, ReviewSignal

# ---------------------------------------------------------------------------
# Test fixtures — sample review models
# ---------------------------------------------------------------------------


@review_model(name="test_score", description="Test score model")
class TestScoreReview(ReviewData):
    score: Annotated[float, RenderHint(widget="score_bar")] = Field(ge=0.0, le=1.0)
    evidence: Annotated[str, RenderHint(widget="markdown")] = ""
    passed: Annotated[bool, RenderHint(widget="pass_fail_badge")] = False

    class Feedback(BaseModel):
        accurate: Annotated[bool, FeedbackField(widget="boolean", label="Score accurate?")] = True
        notes: Annotated[str, FeedbackField(widget="textarea")] = ""


@review_model(name="test_error", description="Test error model")
class TestErrorReview(ReviewData):
    exception_type: Annotated[str, RenderHint(widget="code_snippet")] = ""
    message: Annotated[str, RenderHint(widget="markdown")] = ""


@review_model(name="test_with_options", description="Model with widget options")
class TestOptionsReview(ReviewData):
    severity: Annotated[
        str,
        RenderHint(widget="severity_badge", options={"colors": {"high": "red", "low": "green"}}),
    ] = ""


# ---------------------------------------------------------------------------
# @review_model decorator tests
# ---------------------------------------------------------------------------


class TestReviewModelDecorator:
    def test_stores_metadata(self) -> None:
        meta = get_review_model_meta(TestScoreReview)
        assert meta is not None
        assert meta.name == "test_score"
        assert meta.description == "Test score model"

    def test_sets_type_default(self) -> None:
        instance = TestScoreReview(score=0.8)
        assert instance.type == "test_score"

    def test_type_field_serialized(self) -> None:
        instance = TestScoreReview(score=0.5, evidence="good")
        data = instance.to_data()
        assert data["type"] == "test_score"
        assert data["score"] == 0.5
        assert data["evidence"] == "good"

    def test_rejects_non_basemodel(self) -> None:
        with pytest.raises(TypeError, match="BaseModel"):

            @review_model(name="bad", description="bad")
            class NotAModel:
                pass

    def test_none_for_undecorated_class(self) -> None:
        class Plain(ReviewData):
            pass

        assert get_review_model_meta(Plain) is None


# ---------------------------------------------------------------------------
# Schema generation tests
# ---------------------------------------------------------------------------


class TestReviewModelToJsonSchema:
    def test_basic_schema_structure(self) -> None:
        schema = review_model_to_json_schema(TestScoreReview)
        assert schema["type"] == "object"
        assert "properties" in schema
        assert schema["description"] == "Test score model"

    def test_type_property_is_const(self) -> None:
        schema = review_model_to_json_schema(TestScoreReview)
        type_prop = schema["properties"]["type"]
        assert type_prop["const"] == "test_score"
        assert type_prop["default"] == "test_score"

    def test_render_hints_injected(self) -> None:
        schema = review_model_to_json_schema(TestScoreReview)
        props = schema["properties"]

        assert props["score"]["x-render-hint"] == {"widget": "score_bar"}
        assert props["evidence"]["x-render-hint"] == {"widget": "markdown"}
        assert props["passed"]["x-render-hint"] == {"widget": "pass_fail_badge"}

    def test_render_hint_with_label(self) -> None:
        # The Feedback model's 'accurate' field has a label
        schema = review_model_to_json_schema(TestScoreReview)
        fb_schema = schema["x-feedback-schema"]
        assert fb_schema["properties"]["accurate"]["x-feedback"]["label"] == "Score accurate?"

    def test_render_hint_with_options(self) -> None:
        schema = review_model_to_json_schema(TestOptionsReview)
        severity_hint = schema["properties"]["severity"]["x-render-hint"]
        assert severity_hint["widget"] == "severity_badge"
        assert severity_hint["options"] == {"colors": {"high": "red", "low": "green"}}

    def test_feedback_schema_included(self) -> None:
        schema = review_model_to_json_schema(TestScoreReview)
        assert "x-feedback-schema" in schema
        fb = schema["x-feedback-schema"]
        assert fb["type"] == "object"
        assert "accurate" in fb["properties"]
        assert "notes" in fb["properties"]
        assert fb["properties"]["accurate"]["x-feedback"]["widget"] == "boolean"
        assert fb["properties"]["notes"]["x-feedback"]["widget"] == "textarea"

    def test_no_feedback_schema_when_missing(self) -> None:
        schema = review_model_to_json_schema(TestErrorReview)
        assert "x-feedback-schema" not in schema

    def test_raises_for_undecorated(self) -> None:
        class Plain(ReviewData):
            pass

        with pytest.raises(ValueError, match="not decorated"):
            review_model_to_json_schema(Plain)


# ---------------------------------------------------------------------------
# collect_review_schemas tests
# ---------------------------------------------------------------------------


class TestCollectReviewSchemas:
    def test_collects_from_world_class(self) -> None:
        class FakeWorld:
            review_models = [TestScoreReview, TestErrorReview]

        schemas = collect_review_schemas(FakeWorld)
        assert "test_score" in schemas
        assert "test_error" in schemas
        assert len(schemas) == 2

    def test_empty_when_no_review_models(self) -> None:
        class FakeWorld:
            pass

        schemas = collect_review_schemas(FakeWorld)
        assert schemas == {}

    def test_raises_for_undecorated_model(self) -> None:
        class BadModel(ReviewData):
            pass

        class FakeWorld:
            review_models = [BadModel]

        with pytest.raises(ValueError, match="not decorated"):
            collect_review_schemas(FakeWorld)

    def test_schema_keys_match_model_names(self) -> None:
        class FakeWorld:
            review_models = [TestScoreReview, TestOptionsReview]

        schemas = collect_review_schemas(FakeWorld)
        assert set(schemas.keys()) == {"test_score", "test_with_options"}


# ---------------------------------------------------------------------------
# Integration with ReviewFinding
# ---------------------------------------------------------------------------


class TestReviewFindingIntegration:
    def test_finding_accepts_review_data(self) -> None:
        data = TestScoreReview(score=0.9, evidence="looks great", passed=True)
        finding = ReviewFinding(
            signal=ReviewSignal.PASS,
            title="test-task",
            data=data,
        )
        assert finding.data is not None
        assert finding.data.type == "test_score"
        assert finding.data.score == 0.9  # type: ignore[attr-defined]

    def test_finding_serializes_data_to_dict(self) -> None:
        data = TestScoreReview(score=0.7, passed=True)
        finding = ReviewFinding(
            signal=ReviewSignal.PASS,
            title="test",
            data=data,
        )
        serialized = finding.model_dump()
        assert isinstance(serialized["data"], dict)
        assert serialized["data"]["type"] == "test_score"
        assert serialized["data"]["score"] == 0.7

    def test_result_with_review_data(self) -> None:
        result = ReviewResult(
            signal=ReviewSignal.PASS,
            summary="all good",
            data=TestScoreReview(score=1.0, passed=True),
        )
        serialized = result.model_dump()
        assert serialized["data"]["type"] == "test_score"

    def test_finding_none_data(self) -> None:
        finding = ReviewFinding(
            signal=ReviewSignal.SKIP,
            title="skip",
        )
        assert finding.data is None
        serialized = finding.model_dump()
        assert serialized["data"] is None


# ---------------------------------------------------------------------------
# Schema integration with world schema pipeline
# ---------------------------------------------------------------------------


class TestWorldSchemaIntegration:
    def test_get_world_schema_includes_review_schemas(self) -> None:
        from plato.worlds.schema import get_world_schema

        class FakeWorld:
            name = "test-world"
            review_models = [TestScoreReview, TestErrorReview]

            @classmethod
            def get_config_class(cls):
                from plato.worlds.config import RunConfig

                return RunConfig

        schema = get_world_schema(FakeWorld)
        assert "review_schemas" in schema
        assert schema["review_schemas"] is not None
        assert "test_score" in schema["review_schemas"]
        assert "test_error" in schema["review_schemas"]

    def test_get_world_schema_none_when_no_review_models(self) -> None:
        from plato.worlds.schema import get_world_schema

        class FakeWorld:
            name = "empty-world"
            review_models = []

            @classmethod
            def get_config_class(cls):
                from plato.worlds.config import RunConfig

                return RunConfig

        schema = get_world_schema(FakeWorld)
        assert schema["review_schemas"] is None
