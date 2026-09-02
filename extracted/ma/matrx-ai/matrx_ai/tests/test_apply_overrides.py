"""UnifiedConfig.apply_overrides normalization."""

from __future__ import annotations

from matrx_files.cloud_sync.media_ref import MediaRef

from matrx_ai.config.dictionary_config import DictionaryConfig
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.llm_wire_types import ImageLora, TtsVoiceSpeaker
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.tools.models import CustomTool


def _base_config() -> UnifiedConfig:
    return UnifiedConfig(model="gpt-4o", messages=MessageList(_messages=[]))


def test_apply_overrides_response_format_becomes_dict() -> None:
    config = _base_config()
    config.apply_overrides(
        LLMParams(
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "answer",
                    "schema": {"type": "object", "properties": {"ok": {"type": "boolean"}}},
                },
            }
        )
    )
    assert isinstance(config.response_format, dict)
    assert config.response_format["type"] == "json_schema"
    assert (
        BaseTranslator.build_openai_chat_response_format(config.response_format, "groq") is not None
    )


def test_apply_overrides_custom_tools_are_runtime_objects() -> None:
    config = _base_config()
    config.apply_overrides(
        LLMParams(
            custom_tools=[
                {
                    "name": "lookup",
                    "input_schema": {
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"],
                    },
                }
            ]
        )
    )
    assert len(config.custom_tools) == 1
    assert isinstance(config.custom_tools[0], CustomTool)
    assert hasattr(config.custom_tools[0], "get_provider_format")


def test_apply_overrides_dictionary_becomes_dictionary_config() -> None:
    config = _base_config()
    config.apply_overrides(
        LLMParams(
            dictionary={
                "entries": [{"term": "Matrx", "definition": "The platform"}],
            }
        )
    )
    assert isinstance(config.dictionary, DictionaryConfig)
    assert config.dictionary.entries[0].term == "Matrx"


def test_apply_overrides_compaction_settings_becomes_dict() -> None:
    config = _base_config()
    config.apply_overrides(LLMParams(compaction_settings={"tier2_minimal_prune": True}))
    assert config.compaction_settings == {"tier2_minimal_prune": True}


def test_apply_overrides_tts_voice_multi_speaker_dicts() -> None:
    config = _base_config()
    config.apply_overrides(
        LLMParams(
            tts_voice=[
                TtsVoiceSpeaker(name="Host", voice="Orus"),
                TtsVoiceSpeaker(name="Guest", voice="Kore"),
            ]
        )
    )
    assert isinstance(config.tts_voice, list)
    assert config.tts_voice[0]["voice"] == "Orus"
    voice_cfg = config.tts_voice_config
    assert voice_cfg is not None
    assert len(voice_cfg.speakers) == 2


def test_apply_overrides_tts_voice_dialogue_turns() -> None:
    # The podcast 3+-host band passes ElevenLabs text_to_dialogue turns as
    # [{text, voice_id}] (built by _dialogue_to_elevenlabs_turns). The day
    # LLMParams became typed (2026-08-08) this shape was missing from the
    # TtsVoice union and EVERY 3+-host podcast audio stage 500'd in prod.
    config = _base_config()
    config.apply_overrides(
        LLMParams(
            tts_voice=[
                {"text": "Welcome to the show.", "voice_id": "pNInz6obpgDQGcFmaJgB"},
                {"text": "Glad to be here.", "voice_id": "EXAVITQu4vr4xnSDxMaL"},
            ]
        )
    )
    assert isinstance(config.tts_voice, list)
    assert config.tts_voice[0]["voice_id"] == "pNInz6obpgDQGcFmaJgB"
    assert config.tts_voice[1]["text"] == "Glad to be here."
    voice_cfg = config.tts_voice_config
    assert voice_cfg is not None
    assert [turn.to_dict() for turn in voice_cfg.dialogue_turns] == [
        {"text": "Welcome to the show.", "voice_id": "pNInz6obpgDQGcFmaJgB"},
        {"text": "Glad to be here.", "voice_id": "EXAVITQu4vr4xnSDxMaL"},
    ]


def test_apply_overrides_media_ref_passthrough() -> None:
    config = _base_config()
    ref = MediaRef(file_id="550e8400-e29b-41d4-a716-446655440000")
    config.apply_overrides(LLMParams(image_input=ref))
    assert config.image_input is ref
    assert config.image_input.file_id == ref.file_id


def test_apply_overrides_image_loras_dicts() -> None:
    config = _base_config()
    config.apply_overrides(
        LLMParams(image_loras=[ImageLora(path="/loras/style.safetensors", scale=0.8)])
    )
    assert config.image_loras == [{"path": "/loras/style.safetensors", "scale": 0.8}]


def test_max_output_tokens_normalizes_decimal_request_values() -> None:
    params = LLMParams(max_output_tokens=48_303.04)
    assert params.max_output_tokens == 48_303

    alias_params = LLMParams(max_tokens="48000.99")
    assert alias_params.max_output_tokens == 48_000


def test_unified_config_normalizes_decimal_persisted_values() -> None:
    direct = UnifiedConfig(
        model="claude-test",
        messages=MessageList(_messages=[]),
        max_output_tokens=48_303.04,
    )
    restored = UnifiedConfig.from_dict(
        {
            "model": "claude-test",
            "messages": [],
            "max_output_tokens": 48_303.04,
        }
    )

    assert direct.max_output_tokens == 48_303
    assert restored.max_output_tokens == 48_303
