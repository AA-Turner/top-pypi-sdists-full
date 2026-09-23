"""The speech_script part: validation, the catalog speaker cap, and the three
vendor wires (ElevenLabs, Gemini TTS, OpenAI) — forcing functions on the exact
request each translator builds.

Every translator test drives the REAL translator code with a recorded-shape
provider response; only the network client and persistence are stubbed, and the
assertions are on what would have gone over the wire.
"""

from __future__ import annotations

import base64
from typing import Any

import pytest

from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.speech_script_config import SpeechScriptContent
from matrx_ai.db.message_parts import validate_message_content
from matrx_ai.speech.compile import (
    SpeechScriptRefusal,
    compile_elevenlabs,
    compile_google,
    compile_openai,
    find_speech_script,
    speaker_cap,
)
from matrx_ai.testing.profile_factory import make_profile

TTS_CAPS = {"input": ["text"], "output": ["audio"], "features": [], "interaction": "turn"}
V3_CAPS = {**TTS_CAPS, "features": ["dialogue"]}

PODCAST_TURNS = [
    {
        "speaker": "Maya",
        "voice": "kore",
        "text": "Welcome to Deep Dive. Today {{guest_name}} joins us to talk about {{topic}}.",
        "direction": "warm and upbeat, like greeting an old friend",
        "pause_after_ms": 500,
    },
    {
        "speaker": "Sam",
        "voice": "puck",
        "text": "Thanks, Maya. {{topic}} is having a moment, so let's get into it.",
        "direction": "curious, slightly amused",
    },
]


def _profile(model: str, caps: dict, rules: dict, voices: tuple[str, ...], wire: str):
    return make_profile(
        model_name=model, wire_format=wire, capabilities=caps, rules=rules
    ).model_copy(update={"tts_voice_ids": voices, "tts_default_voice_id": voices[0]})


def _gemini():
    return _profile(
        "gemini-2.5-flash-preview-tts",
        TTS_CAPS,
        {"multi_speaker": {"clamp": {"max": 2}}, "performance_direction": {}},
        ("kore", "puck", "charon"),
        "google_chat",
    )


def _eleven_v3():
    return _profile(
        "eleven_v3",
        V3_CAPS,
        {"multi_speaker": {"clamp": {"max": 10}}, "performance_direction": {}},
        ("kore", "puck", "voiceC"),
        "elevenlabs_chat",
    )


def _openai():
    return _profile(
        "gpt-4o-mini-tts", TTS_CAPS, {"performance_direction": {}}, ("coral", "kore"), "openai_chat"
    )


def _config(turns: list[dict], **settings: Any) -> UnifiedConfig:
    content = SpeechScriptContent(turns=[dict(t) for t in turns])
    config = UnifiedConfig(
        model="m",
        messages=[UnifiedMessage(role="user", content=[content])],
        **settings,
    )
    config.messages[0].replace_variables({"guest_name": "Dr. Lena Ortiz", "topic": "sleep science"})
    return config


# --------------------------------------------------------------------------- part


def test_part_round_trips_with_its_kind_marker():
    stored = validate_message_content([{"type": "speech_script", "turns": PODCAST_TURNS}])
    assert stored[0]["__kind"] == "speech_script"
    assert [t["speaker"] for t in stored[0]["turns"]] == ["Maya", "Sam"]


def test_part_refuses_an_empty_script_and_a_speaker_with_two_voices():
    with pytest.raises(ValueError):
        validate_message_content([{"type": "speech_script", "turns": []}])
    with pytest.raises(ValueError, match="two voices"):
        validate_message_content(
            [
                {
                    "type": "speech_script",
                    "turns": [
                        {"speaker": "Maya", "voice": "kore", "text": "a"},
                        {"speaker": "Maya", "voice": "puck", "text": "b"},
                    ],
                }
            ]
        )


def test_variables_fill_text_and_the_script_is_found():
    config = _config(PODCAST_TURNS)
    script = find_speech_script(config)
    assert script is not None
    assert "Dr. Lena Ortiz" in script.turns[0].text and "{{" not in script.turns[0].text


# ----------------------------------------------------------------- speaker cap


def test_speaker_cap_is_catalog_data():
    assert speaker_cap(_gemini()) == 2
    assert speaker_cap(_eleven_v3()) == 10
    assert speaker_cap(_openai()) == 1  # no multi_speaker rule = one voice


def test_three_speakers_are_refused_on_gemini_with_the_remedy():
    turns = PODCAST_TURNS + [{"speaker": "Ava", "voice": "charon", "text": "And me."}]
    with pytest.raises(SpeechScriptRefusal, match="at most 2 speakers"):
        compile_google(find_speech_script(_config(turns)), _config(turns), _gemini())


def test_two_speakers_are_refused_on_openai():
    config = _config(PODCAST_TURNS)
    with pytest.raises(SpeechScriptRefusal, match="at most 1 speaker"):
        compile_openai(find_speech_script(config), config, _openai())


def test_an_unfilled_voice_variable_is_refused():
    turns = [{"speaker": "Maya", "voice": "{{host_voice}}", "text": "Hello."}]
    config = _config(turns)
    with pytest.raises(SpeechScriptRefusal, match="host_voice"):
        compile_openai(find_speech_script(config), config, _openai())


# ------------------------------------------------------------------ ElevenLabs


def test_elevenlabs_v3_places_direction_as_inline_tags_and_uses_dialogue():
    config = _config(PODCAST_TURNS, performance_direction="podcast energy")
    compiled = compile_elevenlabs(find_speech_script(config), config, _eleven_v3())
    assert compiled.use_dialogue is True
    assert compiled.turns[0]["text"].startswith("[warm and upbeat, like greeting an old friend] ")
    assert compiled.turns[0]["text"].endswith("[short pause]")
    assert compiled.turns[0]["voice_id"] == "kore" and compiled.turns[1]["voice_id"] == "puck"


def test_elevenlabs_non_v3_drops_direction_loudly_and_uses_ssml_breaks():
    flash = _profile(
        "eleven_flash_v2_5",
        TTS_CAPS,
        {"multi_speaker": {"clamp": {"max": 1}}, "performance_direction": {"supported": False}},
        ("kore",),
        "elevenlabs_chat",
    )
    turns = [
        {"speaker": "Maya", "voice": "kore", "text": "One.", "direction": "whisper", "pause_after_ms": 1200},
        {"speaker": "Maya", "voice": "kore", "text": "Two."},
    ]
    config = _config(turns)
    compiled = compile_elevenlabs(find_speech_script(config), config, flash)
    assert compiled.use_dialogue is False
    assert compiled.turns[0]["text"] == 'One. <break time="1.2s" />'
    assert "[whisper]" not in compiled.turns[0]["text"]
    assert any("not sent" in note for note in compiled.notes)


class _FakeEmitter:
    def __init__(self) -> None:
        self.infos: list[Any] = []
        self.data: list[Any] = []

    async def send_info(self, payload: Any) -> None:
        self.infos.append(payload)

    async def send_data(self, payload: Any) -> None:
        self.data.append(payload)


def _recorded_dialogue_response():
    """Shape of a real /v1/text-to-dialogue/with-timestamps response."""
    from elevenlabs.types.audio_with_timestamps_and_voice_segments_response_model import (
        AudioWithTimestampsAndVoiceSegmentsResponseModel,
    )

    text = "[warm] Hi there. Hello."
    starts = [i * 0.1 for i in range(len(text))]
    return AudioWithTimestampsAndVoiceSegmentsResponseModel.model_validate(
        {
            "audio_base64": base64.b64encode(b"ID3fake-mp3-bytes").decode(),
            "alignment": {
                "characters": list(text),
                "character_start_times_seconds": starts,
                "character_end_times_seconds": [s + 0.1 for s in starts],
            },
            "normalized_alignment": None,
            "voice_segments": [
                {
                    "voice_id": "kore",
                    "start_time_seconds": 0.0,
                    "end_time_seconds": 1.6,
                    "character_start_index": 0,
                    "character_end_index": 16,
                    "dialogue_input_index": 0,
                },
                {
                    "voice_id": "puck",
                    "start_time_seconds": 1.6,
                    "end_time_seconds": 2.3,
                    "character_start_index": 16,
                    "character_end_index": 23,
                    "dialogue_input_index": 1,
                },
            ],
        }
    )


@pytest.mark.asyncio
async def test_elevenlabs_translator_sends_dialogue_and_returns_word_alignment(monkeypatch):
    from matrx_ai.providers.eleven_labs import elevenlabs_api
    from matrx_ai.providers.eleven_labs.elevenlabs_api import ElevenLabsChat

    sent: dict[str, Any] = {}

    class _Dialogue:
        def convert_with_timestamps(self, **kwargs: Any):
            sent["dialogue"] = kwargs
            return _recorded_dialogue_response()

    class _Speech:
        def convert_with_timestamps(self, **kwargs: Any):  # pragma: no cover - must not run
            raise AssertionError("a multi-turn v3 script must use Text-to-Dialogue")

    class _Client:
        text_to_dialogue = _Dialogue()
        text_to_speech = _Speech()

    captured: dict[str, Any] = {}

    async def _fake_save(self, **kwargs: Any):
        captured.update(kwargs)
        return "saved"

    monkeypatch.setattr(ElevenLabsChat, "_save_and_emit", _fake_save)
    monkeypatch.setattr(elevenlabs_api, "stamp_call_meta", lambda **_: None)

    async def _no_capture(**_: Any) -> None:
        return None

    monkeypatch.setattr(elevenlabs_api, "emit_explicit_context_analysis", _no_capture)
    monkeypatch.setattr(ElevenLabsChat, "_tts_stream_id", staticmethod(lambda: "stream-1"))
    chat = ElevenLabsChat.__new__(ElevenLabsChat)
    chat.client = _Client()
    emitter = _FakeEmitter()
    config = _config(PODCAST_TURNS, language_code="en")

    result = await chat._execute_speech_script(
        config, _eleven_v3(), emitter, "eleven_v3", find_speech_script(config)
    )

    assert result == "saved"
    inputs = sent["dialogue"]["inputs"]
    assert [i["voice_id"] for i in inputs] == ["kore", "puck"]
    assert inputs[0]["text"].startswith("[warm and upbeat")
    assert "Dr. Lena Ortiz" in inputs[0]["text"]
    assert sent["dialogue"]["language_code"] == "en"
    assert sent["dialogue"]["output_format"] == "mp3_44100_128"
    assert captured["all_audio_bytes"] == b"ID3fake-mp3-bytes"
    alignment = captured["extra_audio_metadata"]["alignment"]
    words = [w["text"] for w in alignment["words"]]
    assert words == ["Hi", "there.", "Hello."], words  # the [warm] tag is not a word
    assert alignment["words"][0]["start_ms"] == 700
    assert [s["voice_id"] for s in alignment["voice_segments"]] == ["kore", "puck"]
    performed = captured["extra_audio_metadata"]["speech_script"]
    assert performed["turns"][0]["text"].startswith("Welcome to Deep Dive. Today Dr. Lena Ortiz")


# ---------------------------------------------------------------------- Gemini


def test_gemini_translator_maps_speakers_and_puts_direction_before_the_transcript():
    from google.genai import types

    from matrx_ai.providers.google.translator import GoogleTranslator

    config = _config(PODCAST_TURNS, performance_direction="a relaxed morning show")
    config.system_instruction = None
    result = GoogleTranslator().to_google(config, _gemini())
    speech = result["config"].speech_config
    assert isinstance(speech, types.SpeechConfig)
    mapped = [
        (s.speaker, s.voice_config.prebuilt_voice_config.voice_name)
        for s in speech.multi_speaker_voice_config.speaker_voice_configs
    ]
    assert mapped == [("Maya", "kore"), ("Sam", "puck")]
    text = result["contents"][0]["parts"][0]["text"]
    notes, transcript = text.split("Transcript follows.")
    assert "a relaxed morning show" in notes
    assert "For line 1 (Maya), warm and upbeat" in notes
    assert "After line 1 (Maya), pause for about 0.5 seconds" in notes
    assert transcript.strip().splitlines() == [
        "Maya: Welcome to Deep Dive. Today Dr. Lena Ortiz joins us to talk about sleep science.",
        "Sam: Thanks, Maya. sleep science is having a moment, so let's get into it.",
    ]
    # The notes never hold a line-leading "Label:" Gemini would read as a speaker.
    for line in notes.splitlines():
        head = line.split(":", 1)[0]
        assert ":" not in line or len(head) > 40 or head.strip().startswith("-"), line


def test_a_text_model_sees_the_transcript_not_nothing():
    content = SpeechScriptContent(turns=PODCAST_TURNS)
    assert content.to_anthropic()["text"].startswith("Maya: Welcome")


# ---------------------------------------------------------------------- OpenAI


@pytest.mark.asyncio
async def test_openai_translator_sends_instructions_and_speed(monkeypatch):
    from matrx_ai.providers.openai import openai_api

    sent: dict[str, Any] = {}

    class _Speech:
        async def create(self, **kwargs: Any):
            sent.update(kwargs)
            raise RuntimeError("stop after the wire is built")

    class _Audio:
        speech = _Speech()

    class _Client:
        audio = _Audio()

    monkeypatch.setattr(openai_api, "stamp_call_meta", lambda **_: None)
    chat = openai_api.OpenAIChat.__new__(openai_api.OpenAIChat)
    chat.client = _Client()
    turns = [
        {"speaker": "Maya", "voice": "kore", "text": "Hello {{guest_name}}.", "direction": "bright", "pause_after_ms": 800},
        {"speaker": "Maya", "voice": "kore", "text": "Let's begin."},
    ]
    config = _config(turns, performance_direction="calm narrator", speech_speed=1.1)
    with pytest.raises(RuntimeError, match="stop after"):
        await chat._execute_tts(config, _openai(), _FakeEmitter(), "gpt-4o-mini-tts")
    assert sent["voice"] == "kore"
    assert sent["input"] == "Hello Dr. Lena Ortiz.\n\nLet's begin."
    assert sent["instructions"].splitlines() == [
        "calm narrator",
        "Paragraph 1: bright",
        "Pause for about 0.8 seconds after paragraph 1.",
    ]
    assert sent["speed"] == 1.1


def test_tts1_takes_no_direction_and_says_so():
    tts1 = _profile(
        "tts-1", TTS_CAPS, {"performance_direction": {"supported": False}}, ("coral",), "openai_chat"
    )
    turns = [{"speaker": "N", "voice": "coral", "text": "Hi.", "direction": "sad"}]
    config = _config(turns)
    compiled = compile_openai(find_speech_script(config), config, tts1)
    assert compiled.instructions is None
    assert compiled.notes and "not sent" in compiled.notes[0]


def test_plain_text_tts_is_untouched_by_the_script_path():
    config = UnifiedConfig(
        model="m", messages=[UnifiedMessage(role="user", content=[TextContent(text="Hi")])]
    )
    assert find_speech_script(config) is None


# ------------------------------------------------------------ honest refusal


@pytest.mark.parametrize("provider", ["elevenlabs", "google", "openai"])
def test_a_refused_script_is_never_retried_and_names_the_remedy(provider):
    from matrx_ai.providers import errors

    classify = {
        "elevenlabs": errors.classify_elevenlabs_error,
        "google": errors.classify_google_error,
        "openai": errors.classify_openai_error,
    }[provider]
    refusal = SpeechScriptRefusal("This speech script has 3 speakers but X performs at most 2.")
    info = classify(refusal)
    assert info.is_retryable is False
    assert info.error_type == "speech_script_refused"
    assert "at most 2" in info.user_message
