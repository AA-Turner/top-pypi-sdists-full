"""Unit tests for the image pipeline action schemas + helpers."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.graph_nodes.image_pipeline_actions import (
    ConceptGenerateInput,
    ConceptGenerateOutput,
    ImageConcept,
    ImagePipelineError,
    ImagePromptSpec,
    ImageQcInput,
    ImageQcVerdict,
    PromptWriteInput,
    PromptWriteOutput,
)

# ---------------------------------------------------------------------------
# ImageConcept
# ---------------------------------------------------------------------------


def test_image_concept_default_style_is_empty_string():
    c = ImageConcept(name="Sun", description="A glowing star")
    assert c.suggested_style == ""


def test_image_concept_rejects_extra_fields():
    with pytest.raises(ValidationError):
        ImageConcept(name="x", description="y", extra="nope")  # type: ignore[call-arg]


def test_image_concept_requires_non_empty_name_and_description():
    with pytest.raises(ValidationError):
        ImageConcept(name="", description="y")
    with pytest.raises(ValidationError):
        ImageConcept(name="x", description="")


# ---------------------------------------------------------------------------
# ConceptGenerateInput
# ---------------------------------------------------------------------------


def test_concept_input_num_concepts_bounds():
    ConceptGenerateInput(topic="x", num_concepts=1)
    ConceptGenerateInput(topic="x", num_concepts=10)
    with pytest.raises(ValidationError):
        ConceptGenerateInput(topic="x", num_concepts=0)
    with pytest.raises(ValidationError):
        ConceptGenerateInput(topic="x", num_concepts=11)


def test_concept_input_default_model():
    inp = ConceptGenerateInput(topic="x")
    assert "sonnet" in inp.model.lower() or "claude" in inp.model.lower()


def test_concept_output_holds_list():
    out = ConceptGenerateOutput(
        concepts=[
            ImageConcept(name="A", description="d1"),
            ImageConcept(name="B", description="d2"),
        ]
    )
    assert len(out.concepts) == 2


# ---------------------------------------------------------------------------
# ImagePromptSpec / PromptWriteInput
# ---------------------------------------------------------------------------


def test_prompt_spec_defaults():
    spec = ImagePromptSpec(prompt="A cat in a hat")
    assert spec.aspect_ratio == "1:1"
    assert spec.negative_prompt == ""
    assert spec.style == ""


def test_prompt_write_input_n_prompts_bounds():
    concept = ImageConcept(name="X", description="d")
    PromptWriteInput(concept=concept, n_prompts=1)
    PromptWriteInput(concept=concept, n_prompts=5)
    with pytest.raises(ValidationError):
        PromptWriteInput(concept=concept, n_prompts=0)
    with pytest.raises(ValidationError):
        PromptWriteInput(concept=concept, n_prompts=6)


def test_prompt_write_output_round_trip():
    out = PromptWriteOutput(
        prompts=[ImagePromptSpec(prompt="p1"), ImagePromptSpec(prompt="p2")]
    )
    dumped = out.model_dump()
    assert len(dumped["prompts"]) == 2


# ---------------------------------------------------------------------------
# ImageQcVerdict
# ---------------------------------------------------------------------------


def test_qc_verdict_success_no_failure_modes():
    v = ImageQcVerdict(passed=True, confidence=0.9, reasoning="looks good")
    assert v.failure_modes == []
    assert v.suggested_retry_prompt is None


def test_qc_verdict_confidence_bounds():
    with pytest.raises(ValidationError):
        ImageQcVerdict(passed=False, confidence=1.5, reasoning="r")
    with pytest.raises(ValidationError):
        ImageQcVerdict(passed=False, confidence=-0.1, reasoning="r")


def test_qc_verdict_rejects_extra_fields():
    with pytest.raises(ValidationError):
        ImageQcVerdict(  # type: ignore[call-arg]
            passed=True, confidence=0.5, reasoning="r", surprise="nope"
        )


# ---------------------------------------------------------------------------
# ImageQcInput — needs at least one image source
# ---------------------------------------------------------------------------


async def test_qc_input_raises_when_no_image_provided(monkeypatch):
    """The qc_judge action raises ImagePipelineError when called with neither URL nor base64."""
    from matrx_ai.graph_nodes.image_pipeline_actions import image_qc_judge

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-used")
    inputs = ImageQcInput(image_url=None, image_b64=None)

    with pytest.raises(ImagePipelineError, match="image_url or image_b64"):
        await image_qc_judge(None, inputs)  # type: ignore[arg-type]


async def test_qc_input_raises_when_no_api_key(monkeypatch):
    from matrx_ai.graph_nodes.image_pipeline_actions import image_qc_judge

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    inputs = ImageQcInput(image_url="https://example.com/x.png")

    with pytest.raises(ImagePipelineError, match="ANTHROPIC_API_KEY"):
        await image_qc_judge(None, inputs)  # type: ignore[arg-type]


async def test_qc_uses_multimodal_funnel_and_friendly_model(monkeypatch):
    from matrx_ai.graph_nodes import image_pipeline_actions as module

    captured = {}

    async def fake_structured(**kwargs):
        captured.update(kwargs)
        return ImageQcVerdict(passed=True, confidence=0.95, reasoning="On brief.")

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(module, "llm_messages_to_pydantic", fake_structured)
    inputs = ImageQcInput(
        image_b64="aGVsbG8=",
        image_mime_type="image/png",
        model="claude-sonnet-4-6",
    )

    result = await module.image_qc_judge(None, inputs)  # type: ignore[arg-type]

    assert result.result.verdict.passed is True
    assert captured["model"] == "claude-sonnet-4-6"
    image = captured["messages"][0]["content"][0]
    assert image == {
        "type": "image",
        "base64_data": "aGVsbG8=",
        "mime_type": "image/png",
    }
