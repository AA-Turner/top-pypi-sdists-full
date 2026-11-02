"""Tests for compute_prompt_hash."""

import hashlib

from agentic_devtools.cli.azure_devops.pr_review_answers import compute_prompt_hash


class TestComputePromptHash:
    def test_matches_hashlib(self):
        assert compute_prompt_hash("hello") == hashlib.sha256(b"hello").hexdigest()

    def test_deterministic(self):
        assert compute_prompt_hash("payload") == compute_prompt_hash("payload")

    def test_empty(self):
        assert compute_prompt_hash("") == hashlib.sha256(b"").hexdigest()
