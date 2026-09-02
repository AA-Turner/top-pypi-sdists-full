"""Tests for derive_attempt_id."""

from agentic_devtools.cli.azure_devops.pr_review_answers import derive_attempt_id


class TestDeriveAttemptId:
    def test_deterministic_and_length(self):
        first = derive_attempt_id("key", "commit", "hash")
        assert first == derive_attempt_id("key", "commit", "hash")
        assert len(first) == 12

    def test_varies_with_inputs(self):
        assert derive_attempt_id("key", "commit", "hash") != derive_attempt_id("key2", "commit", "hash")
