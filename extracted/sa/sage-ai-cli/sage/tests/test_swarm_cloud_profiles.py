"""Tests for cloud:* model profiles in the swarm orchestrator.

The existing ``ModelProfile.from_model_id`` uses generic substring
heuristics ("coder", "opus", "instruct", etc.). It works for big-name
models but misses our specific cloud:* deployment, picking sensible-
looking but suboptimal profiles.

We add explicit profiles for each of the 8 sage-hosted models so the
swarm router picks the right one for each task type.
"""

from __future__ import annotations

from sage.core.swarm import ModelProfile, TaskType


class TestCloudModelProfiles:
    """Each cloud:* model has the right strengths assigned."""

    def test_qwen_coder_strengths(self):
        p = ModelProfile.from_model_id("cloud:qwen-coder-7b")
        # Qwen Coder is the coding specialist — should be the swarm's
        # default for implementation/debugging/refactoring tasks.
        assert TaskType.IMPLEMENTATION in p.strengths
        assert TaskType.DEBUGGING in p.strengths
        assert TaskType.REFACTORING in p.strengths

    def test_deepseek_r1_strengths(self):
        p = ModelProfile.from_model_id("cloud:deepseek-r1-7b")
        # R1 is the reasoning specialist — best for architecture + review.
        assert TaskType.ARCHITECTURE in p.strengths
        assert TaskType.REVIEW in p.strengths

    def test_llama_3_1_8b_strengths(self):
        """Llama 3.1 8B is the general-purpose workhorse — good at
        documentation, review, and serves as a sensible fallback."""
        p = ModelProfile.from_model_id("cloud:llama-3-1-8b")
        assert TaskType.DOCUMENTATION in p.strengths
        assert TaskType.REVIEW in p.strengths

    def test_gemma_2_9b_strengths(self):
        """Gemma 2 9B — alternative chat model, good documentation."""
        p = ModelProfile.from_model_id("cloud:gemma-2-9b")
        assert TaskType.DOCUMENTATION in p.strengths

    def test_phi_4_14b_strengths(self):
        """Phi-4 14B — Microsoft's compact powerhouse. Strong all-rounder."""
        p = ModelProfile.from_model_id("cloud:phi-4-14b")
        assert len(p.strengths) >= 2

    def test_mistral_7b_strengths(self):
        """Mistral 7B v0.3 — strong instruction following."""
        p = ModelProfile.from_model_id("cloud:mistral-7b")
        assert TaskType.DOCUMENTATION in p.strengths or TaskType.REVIEW in p.strengths

    def test_llava_next_strengths(self):
        """LLaVA-NeXT is the vision model — strengths leave it out of
        most code-task pipelines; it should NOT be picked for
        implementation by default."""
        p = ModelProfile.from_model_id("cloud:llava-next-7b")
        # Has strengths (defensive), but no false-positive code routing
        assert p.strengths
        # Should not be the implementation default
        assert TaskType.IMPLEMENTATION not in p.strengths

    def test_yi_1_5_strengths(self):
        """Yi 1.5 9B has 32K context — best for tasks involving long inputs.
        We don't have a dedicated 'long-context' TaskType, but it should
        still get a reasonable profile."""
        p = ModelProfile.from_model_id("cloud:yi-1-5-9b")
        assert p.strengths  # Has SOMETHING assigned

    def test_cost_tier_for_cloud_models_is_cheap(self):
        """All our cloud:* models are 7-14B on cheap L4 GPUs.
        None should be flagged 'expensive' (that's reserved for Opus/GPT-4)."""
        for model in [
            "cloud:qwen-coder-7b",
            "cloud:llama-3-1-8b",
            "cloud:deepseek-r1-7b",
            "cloud:gemma-2-9b",
            "cloud:phi-4-14b",
            "cloud:mistral-7b",
            "cloud:llava-next-7b",
            "cloud:yi-1-5-9b",
        ]:
            p = ModelProfile.from_model_id(model)
            assert p.cost_tier in ("cheap", "medium")


class TestRegressionExistingProfiles:
    """The existing heuristics for non-cloud models must not regress."""

    def test_ollama_qwen_coder_still_routes_to_implementation(self):
        p = ModelProfile.from_model_id("ollama:qwen2.5-coder-7b")
        assert TaskType.IMPLEMENTATION in p.strengths

    def test_gpt_4o_still_marked_expensive(self):
        p = ModelProfile.from_model_id("gpt-4o")
        assert p.cost_tier == "expensive"

    def test_unknown_model_gets_safe_defaults(self):
        p = ModelProfile.from_model_id("some-random-model-name")
        # Falls through to the existing default — implementation + docs
        assert p.strengths
        assert p.cost_tier in ("cheap", "medium", "expensive")
