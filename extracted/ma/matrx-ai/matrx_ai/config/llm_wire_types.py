"""Strict wire types for ``LLMParams`` fields beyond plain scalars."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AspectRatio = Literal[
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
]

MediaResolution = Literal["480p", "720p", "1080p", "4k", "1K", "2K", "4K"]

ImageStyle = Literal["vivid", "natural"]

AudioFormat = Literal[
    "mp3",
    "wav",
    "ogg",
    "opus",
    "aac",
    "flac",
    "pcm",
    "mulaw",
    "alaw",
]

TtsQuality = Literal["high_quality", "fast"]

Verbosity = Literal["low", "medium", "high"]

MediaOutputFormat = Literal[
    "jpeg",
    "png",
    "webp",
    "base64",
    "url",
    "text",
    "json_object",
    "json_schema",
]


class TtsVoiceSpeaker(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Speaker label in multi-speaker TTS scripts.")
    voice: str = Field(description="Provider-native voice id or name.")
    gender: str = Field(
        default="",
        description=(
            "Optional speaker gender ('male' / 'female'). Never sent to a provider — "
            "it lets TTSVoiceConfig pair voices with the SCRIPT's speaker labels by "
            "gender when the two disagree, instead of positionally (which inverted "
            "speakers: a male character voiced female)."
        ),
    )


class TtsDialogueTurn(BaseModel):
    """One pre-rendered dialogue turn for ElevenLabs ``text_to_dialogue`` — the
    podcast pipeline's ``[{text, voice_id}]`` shape (built per run by
    ``_dialogue_to_elevenlabs_turns``). Omitting this from the union broke every
    3+-host podcast audio stage the day LLMParams became typed (2026-08-08)."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(description="Spoken text for this turn.")
    voice_id: str = Field(description="Provider-native voice id speaking this turn.")


TtsVoice = str | list[TtsVoiceSpeaker] | list[TtsDialogueTurn]


class ImageLora(BaseModel):
    """Together FLUX LoRA reference — passed through to the provider API."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(description="LoRA weights path or URL.")
    scale: float = Field(description="Blend strength (provider-native scale).")


class CompactionSettings(BaseModel):
    """Optional overrides for the 5-tier context compaction pipeline.

    Rarely sent by clients today — reserved for explicit compaction control.
    """

    model_config = ConfigDict(extra="forbid")

    tier2_minimal_prune: bool | None = None
    tier3_content_to_retrieval: bool | None = None
    tier4_threshold_trim: bool | None = None
    tier5_hard_compression: bool | None = None
