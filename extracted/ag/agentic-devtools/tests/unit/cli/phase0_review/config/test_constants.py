"""Tests for Phase 0 review contract constants."""

from agentic_devtools.cli.phase0_review import config


def test_normative_constants_are_frozen():
    assert config.SCHEMA_VERSION == "phase0_factual_review_input/v1"
    assert config.PROCESSING_TIMEOUT_SECONDS == 120.0
    assert config.TRUNCATION_THRESHOLD_BYTES == 102_400
    assert config.FACTUAL_REVIEW_INPUT_STATE_KEY == "phase0.factualReviewInputPath"
    assert config.INTEGRITY_STATE_KEY == "phase0.integrityPath"
