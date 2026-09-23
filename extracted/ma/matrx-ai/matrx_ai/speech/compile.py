"""One speech script, three wires — the provider-free half of TTS translation.

Every TTS leader converged on NATURAL-LANGUAGE delivery direction rather than
an enum (typed-message design §2), so ``performance_direction`` is free text and
each translator places it where its vendor wants it:

* **ElevenLabs v3** (dialogue-capable models) — inline audio tags: each turn's
  text is prefixed ``[direction]``; pauses become ``[short pause]`` /
  ``[pause]`` / ``[long pause]``. Multi-turn scripts go to Text-to-Dialogue,
  one turn to the single-voice endpoint. Non-v3 models (flash, multilingual)
  cannot take direction: it is DROPPED LOUDLY (a spoken tag would be read
  aloud) and pauses become SSML ``<break>``.
* **Gemini TTS** — a director's-notes paragraph BEFORE the transcript (scene,
  global direction, per-line direction, pauses, pace) and a ``Name: text``
  transcript whose names map to voices through ``multi_speaker_voice_config``.
* **OpenAI** — one speaker only; the direction (global + per-line) goes to
  ``instructions``, speed to ``speed``.

The speaker cap is catalog DATA — the offering's ``multi_speaker`` rule
(``clamp.max``); a model without the rule speaks with one voice. Exceeding it is
refused here, before any paid call, with the remedy named.

Nothing in this module does I/O; every function is a pure transform so the
translators' forcing-function tests can pin the exact wire.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from matrx_ai.speech.kinds import SpeechScript

if TYPE_CHECKING:  # pragma: no cover
    from matrx_ai.catalog.models import ResolvedCallProfile
    from matrx_ai.config.unified_config import UnifiedConfig

__all__ = [
    "CompiledElevenLabs",
    "CompiledGoogle",
    "CompiledOpenAI",
    "SpeechScriptRefusal",
    "attach_script_to_audio",
    "compile_elevenlabs",
    "compile_google",
    "compile_openai",
    "direction_supported",
    "find_speech_script",
    "script_metadata",
    "speaker_cap",
    "validate_speaker_cap",
]

#: ElevenLabs' own documented voice_settings.speed range.
ELEVENLABS_SPEED_RANGE = (0.7, 1.2)
#: OpenAI audio.speech ``speed`` range.
OPENAI_SPEED_RANGE = (0.25, 4.0)
#: ElevenLabs SSML <break> caps at three seconds.
ELEVENLABS_MAX_BREAK_S = 3.0


class SpeechScriptRefusal(ValueError):
    """The script cannot be performed by this model as written — with the remedy."""


# ---------------------------------------------------------------------------
# Locating the script + the speaker cap
# ---------------------------------------------------------------------------


def find_speech_script(config: UnifiedConfig) -> SpeechScript | None:
    """The speech script of the LAST user message that carries one.

    A TTS call performs the latest script; earlier turns of a conversation are
    history, not a second request.
    """
    from matrx_ai.config.speech_script_config import SpeechScriptContent

    for message in reversed(list(config.messages)):
        if getattr(message, "role", None) not in ("user", None):
            continue
        for content in getattr(message, "content", None) or []:
            if isinstance(content, SpeechScriptContent):
                return content.typed()
    return None


def speaker_cap(profile: ResolvedCallProfile) -> int | None:
    """How many distinct speakers this model performs in one request.

    Read from the offering's ``multi_speaker`` control rule — ``clamp.max`` is
    the cap; a supported rule without a clamp is uncapped (``None``); no rule,
    or ``supported: false``, is one voice.
    """
    rule = profile.controls.rules.get("multi_speaker")
    if rule is None or not rule.supported:
        return 1
    if rule.clamp is not None and rule.clamp.max is not None:
        return max(1, int(rule.clamp.max))
    return None


def validate_speaker_cap(script: SpeechScript, profile: ResolvedCallProfile) -> list[str]:
    speakers = script.speakers()
    cap = speaker_cap(profile)
    if cap is not None and len(speakers) > cap:
        raise SpeechScriptRefusal(
            f"This speech script has {len(speakers)} speakers ({', '.join(speakers)}) but "
            f"{profile.model_name} performs at most {cap} speaker"
            f"{'' if cap == 1 else 's'} per request. Merge speakers or choose a model "
            "with a higher speaker cap (ElevenLabs v3 performs up to 10)."
        )
    return speakers


def direction_supported(profile: ResolvedCallProfile) -> bool:
    """Does this offering take free-text performance direction at all?

    Catalog data: the offering's ``performance_direction`` rule. OpenAI's
    tts-1 has no ``instructions`` field and ElevenLabs' non-v3 models read tags
    aloud — their rules say ``supported: false``, so direction is dropped
    LOUDLY instead of 400ing or being spoken.
    """
    rule = profile.controls.rules.get("performance_direction")
    return rule is not None and rule.supported


def _resolve_voices(
    script: SpeechScript,
    config: UnifiedConfig,
    profile: ResolvedCallProfile,
    *,
    resolve: Any = None,
) -> dict[str, str]:
    """speaker -> provider voice id. An unbound speaker takes the Voice setting."""
    if resolve is None:
        from matrx_ai.catalog.resolve import resolve_tts_voice as resolve

    setting_voice = config.tts_voice if isinstance(config.tts_voice, str) else None
    voices: dict[str, str] = {}
    for speaker in script.speakers():
        literal = script.voice_for(speaker)
        if literal and "{{" in literal:
            raise SpeechScriptRefusal(
                f"Speaker {speaker!r} is bound to the variable {literal} but no value "
                "was supplied for it. Fill the variable with a voice id from this model."
            )
        try:
            voices[speaker] = resolve(profile, literal or setting_voice)
        except Exception as exc:
            raise SpeechScriptRefusal(
                f"Speaker {speaker!r}: {exc}"
            ) from exc
    return voices


def _pause_seconds(ms: int | None, default_ms: int | None) -> float:
    value = ms if ms is not None else default_ms
    return max(0.0, (value or 0) / 1000.0)


# ---------------------------------------------------------------------------
# ElevenLabs
# ---------------------------------------------------------------------------


@dataclass
class CompiledElevenLabs:
    turns: list[dict[str, str]]
    use_dialogue: bool
    language_code: str | None = None
    speed: float | None = None
    notes: list[str] = field(default_factory=list)


def _v3_pause_tag(seconds: float) -> str:
    if seconds <= 0:
        return ""
    if seconds < 0.7:
        return "[short pause]"
    if seconds < 2.0:
        return "[pause]"
    return "[long pause]"


def compile_elevenlabs(
    script: SpeechScript,
    config: UnifiedConfig,
    profile: ResolvedCallProfile,
    *,
    resolve: Any = None,
) -> CompiledElevenLabs:
    validate_speaker_cap(script, profile)
    voices = _resolve_voices(script, config, profile, resolve=resolve)
    tags_ok = bool(profile.capabilities.supports_dialogue) and direction_supported(profile)
    use_dialogue = tags_ok and len(script.turns) > 1
    notes: list[str] = []
    global_direction = (getattr(config, "performance_direction", None) or "").strip()
    default_pause = getattr(config, "turn_pause_ms", None)

    turns: list[dict[str, str]] = []
    dropped_direction = False
    for index, turn in enumerate(script.turns):
        direction = (turn.direction or "").strip() or global_direction
        text = turn.text.strip()
        if direction:
            if tags_ok:
                text = f"[{direction}] {text}"
            else:
                dropped_direction = True
        is_last = index == len(script.turns) - 1
        seconds = _pause_seconds(turn.pause_after_ms, None if is_last else default_pause)
        if seconds > 0:
            if profile.capabilities.supports_dialogue:
                text = f"{text} {_v3_pause_tag(seconds)}"
            else:
                capped = min(seconds, ELEVENLABS_MAX_BREAK_S)
                text = f'{text} <break time="{capped:.1f}s" />'
        turns.append({"text": text, "voice_id": voices[turn.speaker]})

    if dropped_direction:
        notes.append(
            f"{profile.model_name} does not take performance direction (only ElevenLabs "
            "v3 reads audio tags); the direction was not sent. Choose eleven_v3 to use it."
        )

    speed = getattr(config, "speech_speed", None)
    if speed is not None:
        if use_dialogue:
            notes.append(
                "ElevenLabs Text-to-Dialogue has no speed setting; speed was not sent."
            )
            speed = None
        else:
            low, high = ELEVENLABS_SPEED_RANGE
            clamped = min(max(float(speed), low), high)
            if clamped != speed:
                notes.append(f"Speed {speed} is outside ElevenLabs' {low}–{high}; sent {clamped}.")
            speed = clamped

    language = (getattr(config, "language_code", None) or "").strip() or None
    return CompiledElevenLabs(
        turns=turns,
        use_dialogue=use_dialogue,
        language_code=language,
        speed=speed,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Gemini TTS
# ---------------------------------------------------------------------------


@dataclass
class CompiledGoogle:
    director_notes: str
    transcript: str
    speakers: list[tuple[str, str]]  # (name, voice) in first-appearance order
    language_code: str | None = None

    def speech_config_payload(self) -> dict[str, Any]:
        payload: dict[str, Any]
        if len(self.speakers) > 1:
            payload = {
                "multi_speaker_voice_config": {
                    "speaker_voice_configs": [
                        {
                            "speaker": name,
                            "voice_config": {"prebuilt_voice_config": {"voice_name": voice}},
                        }
                        for name, voice in self.speakers
                    ]
                }
            }
        else:
            payload = {
                "voice_config": {"prebuilt_voice_config": {"voice_name": self.speakers[0][1]}}
            }
        if self.language_code:
            payload["language_code"] = self.language_code
        return payload

    def prompt(self) -> str:
        if not self.director_notes:
            return self.transcript
        return f"{self.director_notes}\n\n{self.transcript}"


def compile_google(
    script: SpeechScript,
    config: UnifiedConfig,
    profile: ResolvedCallProfile,
    *,
    resolve: Any = None,
) -> CompiledGoogle:
    speakers = validate_speaker_cap(script, profile)
    voices = _resolve_voices(script, config, profile, resolve=resolve)
    multi = len(speakers) > 1
    global_direction = (getattr(config, "performance_direction", None) or "").strip()
    default_pause = getattr(config, "turn_pause_ms", None)
    speed = getattr(config, "speech_speed", None)

    # Director's notes are PROSE sentences — never a line-leading "Label:",
    # which Gemini would read as a speaker turn.
    notes: list[str] = []
    if global_direction:
        notes.append(f"Perform the whole transcript like this — {global_direction.rstrip('.')}.")
    if speed is not None and float(speed) != 1.0:
        notes.append(f"Speak at about {float(speed):g} times the normal pace.")
    for index, turn in enumerate(script.turns, start=1):
        who = f"line {index} ({turn.speaker})" if multi else f"line {index}"
        if (turn.direction or "").strip():
            notes.append(f"For {who}, {turn.direction.strip().rstrip('.')}.")
        is_last = index == len(script.turns)
        seconds = _pause_seconds(turn.pause_after_ms, None if is_last else default_pause)
        if seconds > 0:
            notes.append(f"After {who}, pause for about {seconds:g} seconds.")
    director = ""
    if notes:
        intro = (
            "Read the transcript below aloud. Director's notes follow; do not read them."
        )
        director = intro + "\n" + "\n".join(f"- {n}" for n in notes) + "\n\nTranscript follows."

    if multi:
        transcript = "\n".join(f"{turn.speaker}: {turn.text.strip()}" for turn in script.turns)
    else:
        transcript = "\n".join(turn.text.strip() for turn in script.turns)

    language = (getattr(config, "language_code", None) or "").strip() or None
    return CompiledGoogle(
        director_notes=director,
        transcript=transcript,
        speakers=[(name, voices[name]) for name in speakers],
        language_code=language,
    )


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------


@dataclass
class CompiledOpenAI:
    input_text: str
    voice: str
    instructions: str | None
    speed: float | None
    notes: list[str] = field(default_factory=list)


def compile_openai(
    script: SpeechScript,
    config: UnifiedConfig,
    profile: ResolvedCallProfile,
    *,
    resolve: Any = None,
) -> CompiledOpenAI:
    speakers = validate_speaker_cap(script, profile)
    voices = _resolve_voices(script, config, profile, resolve=resolve)
    takes_direction = direction_supported(profile)
    global_direction = (getattr(config, "performance_direction", None) or "").strip()
    default_pause = getattr(config, "turn_pause_ms", None)
    lines: list[str] = []
    if global_direction:
        lines.append(global_direction)
    language = (getattr(config, "language_code", None) or "").strip()
    if language:
        lines.append(f"Speak in the language with code {language}.")
    multi_turn = len(script.turns) > 1
    parts: list[str] = []
    for index, turn in enumerate(script.turns, start=1):
        if (turn.direction or "").strip():
            label = f"Paragraph {index}" if multi_turn else "Delivery"
            lines.append(f"{label}: {turn.direction.strip()}")
        is_last = index == len(script.turns)
        seconds = _pause_seconds(turn.pause_after_ms, None if is_last else default_pause)
        if seconds > 0:
            lines.append(f"Pause for about {seconds:g} seconds after paragraph {index}.")
        parts.append(turn.text.strip())
    notes: list[str] = []
    if lines and not takes_direction:
        notes.append(
            f"{profile.model_name} has no instructions field, so the performance "
            "direction and pauses were not sent. Choose gpt-4o-mini-tts to use them."
        )
        lines = []
    speed = getattr(config, "speech_speed", None)
    if speed is not None:
        low, high = OPENAI_SPEED_RANGE
        clamped = min(max(float(speed), low), high)
        if clamped != speed:
            notes.append(f"Speed {speed} is outside OpenAI's {low}–{high}; sent {clamped}.")
        speed = clamped
    return CompiledOpenAI(
        input_text="\n\n".join(parts),
        voice=voices[speakers[0]],
        instructions="\n".join(lines) or None,
        speed=speed,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# The script travels with the audio it produced
# ---------------------------------------------------------------------------


def script_metadata(script: SpeechScript) -> dict[str, Any]:
    """The performed script (variables already filled) as audio-part metadata.

    The runner shows the player WITH the script beside it; a transcript read
    months later still knows what was said by whom without the request row.
    """
    return script.model_dump(mode="json", exclude_none=True)


def attach_script_to_audio(response: Any, config: UnifiedConfig) -> None:
    """Stamp ``metadata.speech_script`` on every audio part of ``response``."""
    script = find_speech_script(config)
    if script is None or response is None:
        return
    from matrx_ai.config.media_config import AudioContent

    payload = script_metadata(script)
    for message in getattr(response, "messages", None) or []:
        for content in getattr(message, "content", None) or []:
            if isinstance(content, AudioContent):
                content.metadata = {**(content.metadata or {}), "speech_script": payload}
