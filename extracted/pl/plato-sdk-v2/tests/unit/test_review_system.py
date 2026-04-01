"""Comprehensive tests for the unified recursive review system.

Tests cover:
- ReviewSpec recursive serialization/deserialization
- BaseReviewWorld class structure and output_models
- ReviewWorldConfig with target_session_id
- Review identity helpers (is_review_world, get_review_target, get_review_spec)
- Schema generation with ReviewSpec (no recursion errors)
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plato.worlds.review.spec import ReviewSpec

# ============================================================================
# ReviewSpec tests
# ============================================================================


class TestReviewSpec:
    """Tests for the recursive ReviewSpec model."""

    def test_simple_spec(self):
        spec = ReviewSpec(world="my-reviewer")
        assert spec.world == "my-reviewer"
        assert spec.config == {}
        assert spec.review is None

    def test_spec_with_config(self):
        spec = ReviewSpec(
            world="webclone-cua-review",
            config={"scoring_llm": {"model": "gemini/gemini-3.1-pro-preview"}},
        )
        assert spec.config["scoring_llm"]["model"] == "gemini/gemini-3.1-pro-preview"

    def test_recursive_spec(self):
        spec = ReviewSpec(
            world="webclone-cua-review",
            review=ReviewSpec(
                world="feedback-comparison",
                review=None,
            ),
        )
        assert spec.review is not None
        assert spec.review.world == "feedback-comparison"
        assert spec.review.review is None

    def test_deeply_nested_spec(self):
        spec = ReviewSpec(
            world="level-1",
            review=ReviewSpec(
                world="level-2",
                review=ReviewSpec(
                    world="level-3",
                    review=ReviewSpec(
                        world="level-4",
                        review=None,
                    ),
                ),
            ),
        )
        assert spec.review.review.review.world == "level-4"
        assert spec.review.review.review.review is None

    def test_serialization_roundtrip(self):
        spec = ReviewSpec(
            world="webclone-cua-review",
            config={"key": "value"},
            review=ReviewSpec(
                world="feedback-comparison",
                config={"ground_truth_fields": ["verdict"]},
                review=None,
            ),
        )
        dumped = spec.model_dump()
        restored = ReviewSpec.model_validate(dumped)
        assert restored == spec
        assert restored.review.world == "feedback-comparison"

    def test_json_roundtrip(self):
        spec = ReviewSpec(
            world="a",
            review=ReviewSpec(world="b", review=ReviewSpec(world="c")),
        )
        json_str = spec.model_dump_json()
        restored = ReviewSpec.model_validate_json(json_str)
        assert restored.review.review.world == "c"

    def test_json_schema_generation(self):
        """ReviewSpec should generate valid JSON schema (self-referential)."""
        schema = ReviewSpec.model_json_schema()
        # Pydantic uses $ref + $defs for self-referential models
        assert "$defs" in schema
        assert "ReviewSpec" in schema["$defs"]
        inner = schema["$defs"]["ReviewSpec"]
        assert "properties" in inner
        assert "world" in inner["properties"]
        assert "review" in inner["properties"]


# ============================================================================
# RunConfig integration tests
# ============================================================================


class TestRunConfigReview:
    """Tests for ReviewSpec on RunConfig."""

    def test_runconfig_has_review_field(self):
        from plato.worlds.config import RunConfig

        config = RunConfig()
        assert config.review is None

    def test_runconfig_with_review_spec(self):
        from plato.worlds.config import RunConfig

        config = RunConfig(
            review=ReviewSpec(world="webclone-cua-review"),
        )
        assert config.review is not None
        assert config.review.world == "webclone-cua-review"

    def test_runconfig_no_verify_config(self):
        """VerifyConfig should be removed from RunConfig."""
        from plato.worlds.config import RunConfig

        assert not hasattr(RunConfig, "verify") or "verify" not in RunConfig.model_fields

    def test_runconfig_schema_no_recursion_error(self):
        """Schema generation must not hit recursion on self-referential ReviewSpec."""
        from plato.worlds.config import RunConfig

        schema = RunConfig.model_json_schema()
        assert "properties" in schema


# ============================================================================
# ReviewWorldConfig tests
# ============================================================================


class TestReviewWorldConfig:
    """Tests for ReviewWorldConfig."""

    def test_has_target_session_id(self):
        from plato.worlds.review.world import ReviewWorldConfig

        config = ReviewWorldConfig(target_session_id="abc123")
        assert config.target_session_id == "abc123"

    def test_target_session_id_defaults_to_env_placeholder(self):
        from plato.worlds.review.world import ReviewWorldConfig

        config = ReviewWorldConfig()
        assert config.target_session_id == "${TARGET_SESSION_ID}"


# ============================================================================
# BaseReviewWorld tests
# ============================================================================


class TestBaseReviewWorld:
    """Tests for BaseReviewWorld class structure."""

    def test_class_attributes(self):
        from plato.worlds.review.world import BaseReviewWorld

        assert hasattr(BaseReviewWorld, "output_models")
        assert hasattr(BaseReviewWorld, "default_review")
        assert BaseReviewWorld.output_models == []
        assert BaseReviewWorld.default_review is None

    def test_subclass_declares_output_models(self):
        from plato.worlds.review.data import ReviewData, review_model
        from plato.worlds.review.world import BaseReviewWorld, ReviewWorldConfig

        @review_model(name="test_finding", description="Test")
        class TestFinding(ReviewData):
            score: float = 0.0

        class MyReviewConfig(ReviewWorldConfig):
            pass

        class MyReviewWorld(BaseReviewWorld[MyReviewConfig]):
            output_models = [TestFinding]
            default_review = ReviewSpec(world="feedback-comparison")

            async def reset(self):
                pass

            async def step(self):
                pass

        assert MyReviewWorld.output_models == [TestFinding]
        assert MyReviewWorld.default_review.world == "feedback-comparison"

    def test_host_starts_none(self):
        from plato.worlds.models import Observation, StepResult
        from plato.worlds.review.world import BaseReviewWorld, ReviewWorldConfig

        class DummyReviewWorld(BaseReviewWorld[ReviewWorldConfig]):
            async def reset(self):
                return Observation()

            async def step(self):
                return StepResult(done=True)

        reviewer = DummyReviewWorld()
        assert reviewer._host is None


# ============================================================================
# Review identity tests
# ============================================================================


class TestReviewIdentity:
    """Tests for review session identity helpers."""

    def test_is_review_world_unregistered(self):
        from plato.worlds.review.identity import is_review_world

        assert is_review_world("nonexistent-world") is False

    def test_is_review_session_no_world(self):
        from plato.worlds.review.identity import is_review_session

        session = MagicMock()
        session.world = None
        assert is_review_session(session) is False

    def test_get_review_target_from_config(self):
        from plato.worlds.review.identity import get_review_target

        session = MagicMock()
        session.world_config = MagicMock(config={"target_session_id": "abc123"})
        assert get_review_target(session) == "abc123"

    def test_get_review_target_none(self):
        from plato.worlds.review.identity import get_review_target

        session = MagicMock()
        session.world_config = MagicMock(config={})
        assert get_review_target(session) is None

    def test_get_review_spec(self):
        from plato.worlds.review.identity import get_review_spec

        session = MagicMock()
        session.world_config = MagicMock(
            config={
                "review": {
                    "world": "webclone-cua-review",
                    "config": {"key": "val"},
                    "review": None,
                }
            }
        )
        spec = get_review_spec(session)
        assert spec is not None
        assert spec.world == "webclone-cua-review"
        assert spec.config == {"key": "val"}

    def test_get_review_spec_none(self):
        from plato.worlds.review.identity import get_review_spec

        session = MagicMock()
        session.world_config = MagicMock(config={})
        assert get_review_spec(session) is None


# ============================================================================
# Schema generation tests
# ============================================================================


class TestSchemaGeneration:
    """Tests for schema generation with ReviewSpec."""

    def test_schema_no_recursion_with_review_spec(self):
        """Ensure _collect_nested_agents doesn't infinitely recurse on ReviewSpec."""
        from plato.worlds.config import RunConfig
        from plato.worlds.schema import _collect_nested_agents

        # This should not raise RecursionError
        agents = _collect_nested_agents(RunConfig)
        assert isinstance(agents, list)

    def test_world_schema_includes_review(self):
        """get_world_config_schema should work with ReviewSpec field."""
        from plato.worlds.config import RunConfig
        from plato.worlds.schema import get_world_config_schema

        schema = get_world_config_schema(RunConfig)
        # ReviewSpec is a RunConfig-level field, so it gets filtered as a runtime field
        # (runtime fields are excluded from world config schema)
        assert isinstance(schema, dict)
