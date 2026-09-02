"""LLMParams strict wire typing."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.config.custom_tool import CustomTool
from matrx_ai.config.dictionary_config import DictionaryConfig
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.llm_wire_types import ImageLora, TtsVoiceSpeaker
from matrx_ai.config.response_format import (
    OutputSchemaEnvelope,
    ResponseFormatJsonObject,
    ResponseFormatJsonSchema,
    response_format_for_schema,
)


def test_response_format_json_object() -> None:
    params = LLMParams(response_format={"type": "json_object"})
    assert isinstance(params.response_format, ResponseFormatJsonObject)


def test_response_format_json_schema_envelope() -> None:
    params = LLMParams(
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "answer",
                "schema": {"type": "object", "properties": {"ok": {"type": "boolean"}}},
                "strict": True,
            },
        }
    )
    assert isinstance(params.response_format, ResponseFormatJsonSchema)
    inner = params.response_format.json_schema
    assert isinstance(inner, OutputSchemaEnvelope)
    assert inner.name == "answer"


def test_persisted_output_schema_builds_strict_response_format() -> None:
    """Saved agent schemas are dictionaries, not Pydantic model classes."""
    response_format = response_format_for_schema(
        {
            "type": "object",
            "properties": {"assignments": {"type": "array", "items": {"type": "object"}}},
            "required": ["assignments"],
            "additionalProperties": False,
        }
    )

    assert response_format.json_schema is not None
    assert response_format.json_schema.name == "structured_output"
    assert response_format.json_schema.strict is True
    assert response_format.json_schema.schema_ is not None
    assert "assignments" in response_format.json_schema.schema_.properties


def test_custom_tools_typed() -> None:
    params = LLMParams(
        custom_tools=[
            {
                "name": "lookup",
                "description": "Look up a record",
                "input_schema": {
                    "type": "object",
                    "properties": {"id": {"type": "string"}},
                    "required": ["id"],
                },
            }
        ]
    )
    assert params.custom_tools is not None
    assert isinstance(params.custom_tools[0], CustomTool)


def test_custom_tools_rejects_bad_name() -> None:
    with pytest.raises(ValidationError):
        LLMParams(custom_tools=[{"name": "bad name!", "input_schema": {"type": "object"}}])


def test_media_ref_image_input() -> None:
    params = LLMParams(image_input={"file_id": "550e8400-e29b-41d4-a716-446655440000"})
    assert params.image_input is not None
    assert params.image_input.file_id == "550e8400-e29b-41d4-a716-446655440000"


def test_mcp_servers_uuid_validation() -> None:
    with pytest.raises(ValidationError):
        LLMParams(mcp_servers=["not-a-uuid"])
    params = LLMParams(mcp_servers=["550e8400-e29b-41d4-a716-446655440000"])
    assert params.mcp_servers == ["550e8400-e29b-41d4-a716-446655440000"]


def test_tts_voice_multi_speaker() -> None:
    params = LLMParams(
        tts_voice=[
            TtsVoiceSpeaker(name="Host", voice="Orus"),
            TtsVoiceSpeaker(name="Guest", voice="Kore"),
        ]
    )
    assert params.tts_voice is not None
    assert len(params.tts_voice) == 2


def test_tts_voice_elevenlabs_dialogue_turns() -> None:
    params = LLMParams(
        tts_voice=[
            {"text": "Welcome to the show.", "voice_id": "voice-a"},
            {"text": "Thanks for having me.", "voice_id": "voice-b"},
        ]
    )
    assert params.tts_voice is not None
    assert len(params.tts_voice) == 2
    assert params.model_dump(exclude_none=True)["tts_voice"][0] == {
        "text": "Welcome to the show.",
        "voice_id": "voice-a",
    }


def test_tts_voice_rejects_mixed_speaker_and_dialogue_shapes() -> None:
    with pytest.raises(ValidationError):
        LLMParams(
            tts_voice=[
                {"name": "Host", "voice": "Orus"},
                {"text": "Dialogue", "voice_id": "voice-a"},
            ]
        )


def test_image_lora() -> None:
    params = LLMParams(image_loras=[ImageLora(path="/loras/style.safetensors", scale=0.8)])
    assert params.image_loras is not None
    assert params.image_loras[0].path.endswith(".safetensors")


def test_dictionary_config() -> None:
    params = LLMParams(
        dictionary={
            "entries": [{"term": "Matrx", "definition": "The platform"}],
            "custom_entries": [],
        }
    )
    assert isinstance(params.dictionary, DictionaryConfig)
    assert params.dictionary.entries[0].term == "Matrx"


def test_literal_enums() -> None:
    params = LLMParams(
        verbosity="medium",
        tts_quality="fast",
        audio_format="mp3",
        aspect_ratio="16:9",
        resolution="1080p",
        output_format="jpeg",
        style="vivid",
    )
    assert params.verbosity == "medium"


def test_rejects_invalid_literal() -> None:
    with pytest.raises(ValidationError):
        LLMParams(verbosity="yelling")


def test_llm_params_openapi_discriminated_response_format() -> None:
    schema = LLMParams.model_json_schema()
    rf = schema["properties"]["response_format"]["anyOf"][0]
    assert rf["discriminator"]["propertyName"] == "type"


@pytest.mark.parametrize(
    ("alias", "canonical"),
    [
        ("max_tokens", "max_output_tokens"),
        ("n", "count"),
        ("quality", "render_quality"),
        ("output_quality", "encode_quality"),
        ("seconds", "duration_seconds"),
        ("duration", "duration_seconds"),
        ("num_outputs", "count"),
        ("number_of_images", "count"),
    ],
)
def test_llm_params_openapi_exposes_accepted_aliases_as_deprecated(
    alias: str, canonical: str
) -> None:
    properties = LLMParams.model_json_schema()["properties"]

    assert alias in properties
    assert properties[alias]["deprecated"] is True
    assert canonical in properties[alias]["description"]


@pytest.mark.parametrize(
    ("alias", "value", "canonical", "normalized"),
    [
        ("max_tokens", 2048, "max_output_tokens", 2048),
        ("n", 4, "count", 4),
        ("quality", "high", "render_quality", "high"),
        ("output_quality", 85, "encode_quality", 85),
        ("seconds", "8", "duration_seconds", 8),
        ("duration", 6, "duration_seconds", 6),
        ("num_outputs", 3, "count", 3),
        ("number_of_images", 2, "count", 2),
    ],
)
def test_llm_params_schema_aliases_keep_existing_runtime_normalization(
    alias: str, value: object, canonical: str, normalized: object
) -> None:
    params = LLMParams.model_validate({alias: value})

    assert getattr(params, canonical) == normalized
    assert alias not in params.model_dump(exclude_none=True)


@pytest.mark.parametrize(
    "unsupported",
    [
        "size",
        "ratio",
        "image_size",
        "output_mime_type",
        "person_generation",
        "image_format",
        "include_rai_reason",
    ],
)
def test_llm_params_does_not_advertise_unaccepted_provider_output_keys(
    unsupported: str,
) -> None:
    assert unsupported not in LLMParams.model_json_schema()["properties"]
    with pytest.raises(ValidationError):
        LLMParams.model_validate({unsupported: "value"})


def test_model_reference_uuid() -> None:
    params = LLMParams(model="550e8400-e29b-41d4-a716-446655440000")
    assert params.model == "550e8400-e29b-41d4-a716-446655440000"


def test_model_reference_provider_slug() -> None:
    params = LLMParams(model="google/gemini-2.5-pro")
    assert params.model == "google/gemini-2.5-pro"


def test_model_reference_rejects_invalid() -> None:
    with pytest.raises(ValidationError):
        LLMParams(model="not valid slug!")


def test_custom_tool_required_must_exist_in_properties() -> None:
    with pytest.raises(ValidationError):
        LLMParams(
            custom_tools=[
                {
                    "name": "lookup",
                    "input_schema": {
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["missing"],
                    },
                }
            ]
        )


def test_output_schema_envelope_typed_properties() -> None:
    params = LLMParams(
        response_format={
            "type": "json_schema",
            "json_schema": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "answer": {"type": "string", "description": "The answer"},
                    },
                    "required": ["answer"],
                },
            },
        }
    )
    inner = params.response_format.json_schema  # type: ignore[union-attr]
    assert inner is not None
    assert inner.schema_ is not None
    assert inner.schema_.properties["answer"].type == "string"
