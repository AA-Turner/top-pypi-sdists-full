from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.name_gender import gender_for_name, normalize_gender

# ============================================================================
# Canonical quality-mode vocabulary. Model assignment lives only in
# ``ai.offering.metadata.tts.quality_tiers``.
# ============================================================================
TTS_QUALITY_HIGH = "high_quality"
TTS_QUALITY_FAST = "fast"
TTS_QUALITY_MODES: frozenset[str] = frozenset({TTS_QUALITY_HIGH, TTS_QUALITY_FAST})


# ============================================================================
# TTSSpeaker — single speaker entry for multi-speaker TTS (Google only)
# ============================================================================


@dataclass
class TTSSpeaker:
    """One name→voice binding for Google multi-speaker TTS.

    ``gender`` is OPTIONAL and populated by callers that already know it (the
    podcast pipeline resolves one for every speaker through THE GENDER CHAIN).
    It is not sent to any provider — it exists so that when the script's speaker
    labels differ from the configured names, adoption can re-point each voice at
    a name of the SAME gender. Without it, adoption paired names positionally
    and happily gave a male character a female voice.
    """

    name: str
    voice: str
    gender: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> TTSSpeaker:
        return cls(name=data["name"], voice=data["voice"], gender=data.get("gender", "") or "")

    def to_dict(self) -> dict[str, str]:
        out = {"name": self.name, "voice": self.voice}
        if self.gender:
            out["gender"] = self.gender
        return out

    def resolved_gender(self) -> str:
        """This speaker's gender: declared value first, then the name table,
        then "" (genuinely unknown — the caller must not pretend otherwise)."""
        return gender_for_name(self.name, self.gender)


# ============================================================================
# Multi-speaker voice pool (optional, host-injected)
#
# Adoption can only REPAIR a gender mismatch if it knows which voices are male
# and which are female. That truth lives in the ``ai.voices`` catalog, which the
# config layer must not read, so the host injects it once at startup / pool
# refresh. Unconfigured, adoption still pairs by gender (which fixes the common
# inversion) and simply keeps the voice it cannot prove wrong.
# ============================================================================

_VOICE_GENDER: dict[str, str] = {}
_VOICES_BY_GENDER: dict[str, list[str]] = {"male": [], "female": []}


def configure_multi_speaker_voice_pool(pool: list[tuple[str, str]]) -> None:
    """Register ``(voice_id, gender)`` pairs for the multi-speaker (Google) pool.

    Idempotent and replace-in-full: call it again after a catalog refresh."""
    _VOICE_GENDER.clear()
    _VOICES_BY_GENDER["male"] = []
    _VOICES_BY_GENDER["female"] = []
    for voice_id, gender in pool:
        if not voice_id:
            continue
        normalized = normalize_gender(gender)
        _VOICE_GENDER[voice_id] = normalized
        if normalized in _VOICES_BY_GENDER:
            _VOICES_BY_GENDER[normalized].append(voice_id)


def voice_gender(voice_id: str) -> str:
    """Gender of a pooled voice, or "" when the pool has not been injected or
    doesn't know this voice. Never guesses."""
    found = _VOICE_GENDER.get(voice_id, "")
    return "" if found in ("", "neutral") else found


# ============================================================================
# TTSVoiceConfig — unified voice configuration for all providers
#
# Three modes — determined by which field is populated:
#
#   Single-speaker:  voice is a non-empty string, speakers/dialogue_turns empty.
#                    Works with Google, OpenAI, Groq, xAI, ElevenLabs.
#
#   Multi-speaker:   voice is None, speakers has 2+ TTSSpeaker entries.
#                    Google only. Non-Google providers collapse to speakers[0].
#
#   Dialogue:        dialogue_turns has 1+ DialogueTurn entries (text+voice_id).
#                    ElevenLabs text_to_dialogue only. Each turn carries its
#                    own voice_id — no global voice config needed.
#
# Provider translation: to_google(), to_openai(), to_groq(), to_xai(),
# to_elevenlabs(). Each method enforces its own constraints.
# ============================================================================


@dataclass
class TTSVoiceConfig:
    voice: str | None = None
    speakers: list[TTSSpeaker] = field(default_factory=list)
    # ElevenLabs dialogue turns — each turn carries its own voice_id inline.
    # When set, this config is in "dialogue" mode and to_elevenlabs() is the
    # authoritative translation path. Other provider methods are not applicable.
    dialogue_turns: list[DialogueTurn] = field(default_factory=list)

    # ------------------------------------------------------------------ #
    # Construction                                                         #
    # ------------------------------------------------------------------ #

    @classmethod
    def from_config(cls, settings: Any) -> TTSVoiceConfig | None:
        raw = getattr(settings, "tts_voice", None)
        if raw is None:
            return None

        if isinstance(raw, str):
            if not raw.strip():
                return None
            return cls(voice=raw)

        if isinstance(raw, list):
            if not raw:
                return None

            first = raw[0]
            if not isinstance(first, dict):
                return None

            # Detect ElevenLabs dialogue turns: dicts with "voice_id" (not "voice"/"name")
            if "voice_id" in first:
                turns = [DialogueTurn.from_dict(t) for t in raw]
                return cls(dialogue_turns=turns)

            if len(raw) == 1:
                voice_name = first.get("voice")
                return cls(voice=voice_name)

            return cls(speakers=[TTSSpeaker.from_dict(s) for s in raw])

        return None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TTSVoiceConfig:
        return cls(
            voice=data.get("voice"),
            speakers=[TTSSpeaker.from_dict(s) for s in data.get("speakers", [])],
            dialogue_turns=[DialogueTurn.from_dict(t) for t in data.get("dialogue_turns", [])],
        )

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def is_multi_speaker(self) -> bool:
        return len(self.speakers) > 1

    @property
    def is_dialogue(self) -> bool:
        """True when this config carries ElevenLabs dialogue turns."""
        return bool(self.dialogue_turns)

    @property
    def is_configured(self) -> bool:
        return bool(self.voice) or bool(self.speakers) or bool(self.dialogue_turns)

    def _primary_voice(self) -> str | None:
        if self.voice:
            return self.voice
        if self.speakers:
            return self.speakers[0].voice
        return None

    def strip_speaker_labels(self, text: str) -> str:
        """Remove speaker labels from transcript text for single-speaker providers.

        Handles any label format where a known speaker name appears at the start
        of a line followed by a colon and optional whitespace — regardless of
        script or language.  Only strips labels for names defined in self.speakers.

        Called by non-Google providers when collapsing a multi-speaker config to
        a single voice, so the model doesn't read out "Alex:" as part of the text.

        Examples:
            "Alex: Hello.\nSarah: Hi!"  →  "Hello.\nHi!"
            "الکس: سلام\nسارا: خوبم"   →  "سلام\nخوبم"
        """
        if not self.speakers:
            return text

        import re

        names = [re.escape(s.name) for s in self.speakers]
        pattern = re.compile(
            r"^(?:" + "|".join(names) + r")\s*:\s*",
            re.MULTILINE,
        )
        return pattern.sub("", text)

    # ------------------------------------------------------------------ #
    # Speaker-name adoption (Google multi-speaker only)                    #
    #                                                                      #
    # Google's multi-speaker TTS maps each transcript label ("Alex: …") to #
    # a voice. The SCRIPT is the source of truth for who speaks — the       #
    # configured speaker NAMES are just arbitrary labels bound to voices    #
    # (the script agent and the audio agent don't coordinate names, so they #
    # routinely differ, e.g. script "Jake/Chloe" vs config "Alex/Sarah").  #
    # So when they differ we make the voice CONFIG adopt the script's names #
    # — keeping each voice — and leave the transcript COMPLETELY UNTOUCHED. #
    # (The old direction rewrote the transcript to match the config, i.e.   #
    # edited the script to fit the settings, which is backwards.)           #
    #                                                                      #
    # Conservative: acts only when the transcript's distinct speaker labels #
    # map 1:1 onto the configured speakers (after dropping any leading      #
    # preamble line). Anything ambiguous is left for validate_speaker_names #
    # to reject.                                                            #
    # ------------------------------------------------------------------ #

    # Matches a line-leading "Label:" — the only structure Google accepts as
    # a speaker turn. Label is bounded (<=40 chars, no embedded colon/newline)
    # so prose colons ("Note: ...") that happen to lead a line are still
    # filtered out later by the repeated-occurrence / tail logic.
    _LABEL_RE = re.compile(r"^[ \t]*([^\n:]{1,40}?)[ \t]*:", re.MULTILINE)

    @staticmethod
    def _iter_user_text_parts(google_contents: list[Any]) -> list[Any]:
        parts: list[Any] = []
        for content in google_contents:
            if isinstance(content, dict):
                role = content.get("role")
                content_parts = content.get("parts", []) or []
            else:
                role = getattr(content, "role", None)
                content_parts = getattr(content, "parts", None) or []
            if role != "user":
                continue
            parts.extend(content_parts)
        return parts

    @staticmethod
    def _part_text(part: Any) -> str:
        if isinstance(part, dict):
            return part.get("text") or ""
        return getattr(part, "text", None) or ""

    def adopt_script_speaker_names(self, google_contents: list[dict[str, Any]]) -> None:
        if not self.is_multi_speaker:
            return

        configured = [s.name for s in self.speakers if s.name]
        if len(configured) < 2:
            return

        parts = [p for p in self._iter_user_text_parts(google_contents) if self._part_text(p)]
        if not parts:
            return

        full_text = "\n".join(self._part_text(p) for p in parts)

        # Distinct line-leading labels, in first-appearance order, with counts.
        counts: dict[str, int] = {}
        order: list[str] = []
        for match in self._LABEL_RE.finditer(full_text):
            label = match.group(1).strip()
            # A real speaker label is a bare name. Skip JSON-ish artifacts — a
            # quoted key like `"id":` from any context/manifest blob that ever
            # reaches the transcript — so they can never be adopted as a speaker
            # name (the audio agents now skip context entirely, but this keeps
            # adoption robust regardless of what lands in the text).
            if not label or '"' in label:
                continue
            if label not in counts:
                counts[label] = 0
                order.append(label)
            counts[label] += 1

        # Which distinct labels are the dialogue's actual speakers? Two signals,
        # tried in order:
        #   • Recurrence: in a full dialogue the real speakers alternate (>=2
        #     turns each) while a one-off colon line ("Title:", "Current date:")
        #     appears once and is dropped — when the recurring set already
        #     numbers the configured speakers, trust it.
        #   • Tail of the distinct set: a SHORT dialogue — above all the
        #     test-mode truncated script (one turn per host) — has nothing
        #     recur, so every speaker appears exactly once. A leading preamble
        #     line that slips through ("read this aloud:") would inflate the
        #     count, but the real transcript always comes LAST, so the speakers
        #     are the final len(configured) distinct labels.
        recurring = [label for label in order if counts[label] >= 2]
        if len(recurring) == len(configured):
            candidates = recurring
        elif len(order) >= len(configured):
            candidates = order[-len(configured) :]
        else:
            return

        # Config already uses the script's names (set-equal regardless of
        # speaking order) — nothing to adopt.
        if set(candidates) == set(configured):
            return

        # Anchor-preserving adoption: keep every configured name the script
        # already uses (and its voice); rename only the configured names the
        # script did NOT use onto the script's drifted labels. The transcript is
        # never modified — the script is the source of truth for who speaks.
        #
        # 🚨 PAIRING IS BY GENDER, NOT BY POSITION. Preserving the voice palette
        # while pairing positionally INVERTS speakers: config
        # [Sarah→female voice, Owen→male voice] against script [Marcus, Elena]
        # gave Marcus the female voice and Elena the male one, in an episode
        # where they call each other by name. Position says nothing about who a
        # name belongs to; only gender does. Positional order survives ONLY as
        # the tiebreak for pairs where neither side resolves a gender.
        configured_set = set(configured)
        candidate_set = set(candidates)
        missing = [name for name in configured if name not in candidate_set]
        drifted = [label for label in candidates if label not in configured_set]
        if not drifted or len(drifted) != len(missing):
            return

        by_name = {s.name: s for s in self.speakers}
        movers = [by_name[name] for name in missing if name in by_name]
        if len(movers) != len(missing):
            return

        adopt: dict[str, str] = {}  # config name -> script label
        adopted: list[TTSSpeaker] = []
        for speaker, label in self._pair_for_adoption(movers, drifted):
            adopt[speaker.name] = label
            speaker.name = label
            adopted.append(speaker)
            want = gender_for_name(label)
            if want:
                speaker.gender = want

        vcprint(
            f"[Google TTS] Voice config adopted the script's speaker names "
            f"{list(adopt.values())} (renamed from {list(adopt.keys())}), paired by "
            f"gender. Transcript untouched — the script is the source of truth.",
            color="cyan",
        )
        self._repair_adopted_voice_genders(adopted)

    @staticmethod
    def _pair_for_adoption(
        movers: list[TTSSpeaker], labels: list[str]
    ) -> list[tuple[TTSSpeaker, str]]:
        """Decide which configured speaker adopts which drifted script label.

        Gender first: each label goes to a still-unpaired speaker whose own
        gender matches, so the voice that answers to "Elena" is the one that was
        already female. Whatever gender cannot decide (unknown on one or both
        sides, or an unbalanced cast) falls back to first-appearance order —
        the previous behaviour, now the LAST resort instead of the only rule."""
        remaining = list(movers)
        pairs: list[tuple[TTSSpeaker, str]] = []
        undecided: list[str] = []
        for label in labels:
            want = gender_for_name(label)
            match = (
                next((s for s in remaining if s.resolved_gender() == want), None) if want else None
            )
            if match is None:
                undecided.append(label)
                continue
            remaining.remove(match)
            pairs.append((match, label))
        for label, speaker in zip(undecided, remaining):
            pairs.append((speaker, label))
        return pairs

    def _repair_adopted_voice_genders(self, adopted: list[TTSSpeaker]) -> None:
        """After adoption, re-draw any voice that now contradicts the name it
        answers to.

        Gender pairing fixes an inversion by SWAPPING which voice takes which
        name, but that only works when the cast holds a voice of each needed
        gender. A script whose drifted labels are both male, against a config of
        one male + one female voice, leaves someone mismatched no matter how the
        pairing runs — and shipping a mismatch is the exact defect. So the
        correct-gender voice is preferred over the curated one: draw an unused
        voice of the right gender from the injected pool.

        No pool injected (or no voice of that gender in it) → keep the voice and
        say so loudly. Silence is what let this ship for months."""
        if not _VOICE_GENDER:
            return
        taken = {s.voice for s in self.speakers}
        # ONLY the speakers that changed identity. A speaker the script already
        # named keeps the voice upstream cast for it — this method exists to
        # clean up after adoption, not to second-guess the cast.
        for speaker in adopted:
            want = speaker.resolved_gender()
            if not want:
                continue
            actual = voice_gender(speaker.voice)
            if not actual or actual == want:
                continue
            pool = [v for v in _VOICES_BY_GENDER.get(want, []) if v not in taken]
            if not pool:
                vcprint(
                    f"[Google TTS] Speaker '{speaker.name}' is {want} but voice "
                    f"{speaker.voice} is {actual}, and no unused {want} voice is "
                    "available to repair it. Sending as-is.",
                    color="red",
                )
                continue
            replacement = pool[0]
            vcprint(
                f"[Google TTS] GENDER MISMATCH REPAIRED after name adoption: "
                f"'{speaker.name}' is {want} but held {speaker.voice} ({actual}) — "
                f"swapped to {replacement}. A correct-gender voice beats a curated one.",
                color="yellow",
            )
            taken.discard(speaker.voice)
            taken.add(replacement)
            speaker.voice = replacement

    # ------------------------------------------------------------------ #
    # Validation                                                           #
    # ------------------------------------------------------------------ #

    def validate_speaker_names(self, google_contents: list[dict[str, Any]]) -> None:
        if not self.is_multi_speaker:
            return

        full_text = ""
        for content in google_contents:
            if content.get("role") == "user":
                for part in content.get("parts", []):
                    if isinstance(part, dict):
                        text = part.get("text") or ""
                    else:
                        text = getattr(part, "text", None) or ""
                    full_text += text

        missing = [s.name for s in self.speakers if s.name and s.name not in full_text]
        if missing:
            configured = [s.name for s in self.speakers]
            raise ValueError(
                f"[Google TTS] Speaker name mismatch: {missing} not found in message text. "
                f"All configured speakers {configured} must appear as exact labels in the "
                f"transcript (e.g. 'Alex: ...'). Names are case-sensitive and must match "
                f"exactly, including non-Latin scripts."
            )

    # ------------------------------------------------------------------ #
    # Provider translation — Google                                        #
    # ------------------------------------------------------------------ #

    def to_google(self, google_contents: list[dict[str, Any]]) -> Any:
        from google.genai import types

        if not self.is_configured:
            return None

        if self.is_multi_speaker:
            # Make the voice config adopt the script's speaker names (the script
            # is canonical; voices stay put and the transcript is never touched),
            # then validate as the final safety net.
            self.adopt_script_speaker_names(google_contents)
            self.validate_speaker_names(google_contents)
            return types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker=s.name,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=s.voice)
                            ),
                        )
                        for s in self.speakers
                    ]
                )
            )

        return types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=self.voice)
            )
        )

    # ------------------------------------------------------------------ #
    # Provider translation — ElevenLabs                                   #
    # Dialogue mode: returns batched turns for text_to_dialogue API.      #
    # Single-speaker mode: wraps the single text+voice_id as one turn.    #
    # Multi-speaker (Google-style) is not applicable; raises clearly.     #
    # ------------------------------------------------------------------ #

    def to_elevenlabs(
        self, text: str | None = None, model: str | None = None
    ) -> tuple[list[list[dict[str, str]]], str]:
        """Translate to ElevenLabs batched dialogue inputs.

        Returns:
            batches: list of batches, each batch is a list of
                     {"text": ..., "voice_id": ...} dicts ready for the SDK.
            model:   resolved model string (e.g. "eleven_v3").
        """
        if not model or not model.strip():
            raise ValueError("ElevenLabs TTS requires a catalog-resolved model id.")
        resolved_model = model.strip()

        if self.is_dialogue:
            batches = batch_dialogue_turns(self.dialogue_turns)
            return [[t.to_elevenlabs_input() for t in batch] for batch in batches], resolved_model

        if self.speakers:
            raise ValueError(
                "TTSVoiceConfig is in Google multi-speaker mode (name→voice mapping). "
                "ElevenLabs requires turns with inline voice_id. "
                "Pass tts_voice as a list of {text, voice_id} dicts instead."
            )

        # Single-speaker: wrap the provided text as one turn
        if not text:
            raise ValueError("ElevenLabs single-speaker TTS requires text input.")
        voice_id = self.voice or ""
        if not voice_id:
            raise ValueError("ElevenLabs TTS requires a voice_id.")
        turn = DialogueTurn(text=text, voice_id=voice_id)
        batches = batch_dialogue_turns([turn])
        return [[t.to_elevenlabs_input() for t in batch] for batch in batches], resolved_model

    # ------------------------------------------------------------------ #
    # Serialisation                                                        #
    # ------------------------------------------------------------------ #

    def to_storage_dict(self) -> dict[str, Any]:
        return {
            "voice": self.voice,
            "speakers": [s.to_dict() for s in self.speakers],
            "dialogue_turns": [t.to_dict() for t in self.dialogue_turns],
        }


# ============================================================================
# GroqTTSRegistry — structural wire constraints for Groq Orpheus TTS
# ============================================================================


class GroqTTSRegistry:
    SUPPORTED_FORMATS: frozenset[str] = frozenset({"wav"})
    MAX_INPUT_LENGTH: int = 200

    @classmethod
    def resolve_format(cls, response_format: str | None = None) -> str:
        if response_format and response_format.strip().lower() in cls.SUPPORTED_FORMATS:
            return response_format.strip().lower()
        return "wav"

    @classmethod
    def validate_input_length(cls, text: str) -> str:
        if len(text) > cls.MAX_INPUT_LENGTH:
            return text[: cls.MAX_INPUT_LENGTH]
        return text


# ============================================================================
# XAITTSRegistry — structural wire constraints for xAI Grok TTS.
# ============================================================================


class XAITTSRegistry:
    _LANGUAGES: dict[str, str] = {
        "auto": "Auto-detect",
        "en": "English",
        "ar-eg": "Arabic (Egypt)",
        "ar-sa": "Arabic (Saudi Arabia)",
        "ar-ae": "Arabic (United Arab Emirates)",
        "bn": "Bengali",
        "zh": "Chinese (Simplified)",
        "fr": "French",
        "de": "German",
        "hi": "Hindi",
        "id": "Indonesian",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "pt-br": "Portuguese (Brazil)",
        "pt-pt": "Portuguese (Portugal)",
        "ru": "Russian",
        "es-mx": "Spanish (Mexico)",
        "es-es": "Spanish (Spain)",
        "tr": "Turkish",
        "vi": "Vietnamese",
    }
    VALID_LANGUAGES: frozenset[str] = frozenset(_LANGUAGES.keys())
    VALID_CODECS: frozenset[str] = frozenset({"mp3", "wav", "pcm", "mulaw", "alaw"})
    VALID_SAMPLE_RATES: frozenset[int] = frozenset({8000, 16000, 22050, 24000, 44100, 48000})
    VALID_BIT_RATES: frozenset[int] = frozenset({32000, 64000, 96000, 128000, 192000})
    MAX_TEXT_LENGTH: int = 15_000
    DEFAULT_LANGUAGE: str = "en"
    DEFAULT_CODEC: str = "mp3"
    DEFAULT_SAMPLE_RATE: int = 24000
    DEFAULT_BIT_RATE: int = 128000

    @classmethod
    def resolve_language(cls, language: str | None = None) -> str:
        if language:
            normalised = language.strip().lower()
            if normalised in cls.VALID_LANGUAGES:
                return normalised
        return cls.DEFAULT_LANGUAGE

    @classmethod
    def resolve_codec(cls, codec: str | None = None) -> str:
        if codec:
            normalised = codec.strip().lower()
            if normalised in cls.VALID_CODECS:
                return normalised
        return cls.DEFAULT_CODEC

    @classmethod
    def resolve_sample_rate(cls, sample_rate: int | None = None) -> int:
        if sample_rate is not None and sample_rate in cls.VALID_SAMPLE_RATES:
            return sample_rate
        return cls.DEFAULT_SAMPLE_RATE

    @classmethod
    def resolve_bit_rate(cls, bit_rate: int | None = None, codec: str | None = None) -> int | None:
        resolved_codec = cls.resolve_codec(codec)
        if resolved_codec != "mp3":
            return None
        if bit_rate is not None and bit_rate in cls.VALID_BIT_RATES:
            return bit_rate
        return cls.DEFAULT_BIT_RATE

    @classmethod
    def resolve_output_format(
        cls,
        codec: str | None = None,
        sample_rate: int | None = None,
        bit_rate: int | None = None,
    ) -> dict:
        resolved_codec = cls.resolve_codec(codec)
        result: dict = {
            "codec": resolved_codec,
            "sample_rate": cls.resolve_sample_rate(sample_rate),
        }
        resolved_br = cls.resolve_bit_rate(bit_rate, resolved_codec)
        if resolved_br is not None:
            result["bit_rate"] = resolved_br
        return result

    @classmethod
    def languages(cls) -> dict[str, str]:
        return dict(cls._LANGUAGES)

    @classmethod
    def validate_text_length(cls, text: str, truncate: bool = False) -> str:
        if len(text) <= cls.MAX_TEXT_LENGTH:
            return text
        if truncate:
            return text[: cls.MAX_TEXT_LENGTH]
        raise ValueError(
            f"Text length {len(text):,} exceeds the {cls.MAX_TEXT_LENGTH:,} "
            f"character limit. Use truncate=True or the WebSocket endpoint."
        )


# ============================================================================
# DialogueTurn — a single speaker turn for ElevenLabs text_to_dialogue
#
# Each turn carries both the text and the voice_id inline, which is how
# ElevenLabs' dialogue API works. This differs from other providers where
# voice config is global (one voice for the whole request).
# ============================================================================


@dataclass
class DialogueTurn:
    text: str
    voice_id: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> DialogueTurn:
        return cls(text=data["text"], voice_id=data["voice_id"])

    def to_dict(self) -> dict[str, str]:
        return {"text": self.text, "voice_id": self.voice_id}

    def to_elevenlabs_input(self) -> dict[str, str]:
        """Return the dict format the ElevenLabs SDK expects."""
        return {"text": self.text, "voice_id": self.voice_id}


# ============================================================================
# ElevenLabs dialogue batching — structural API limit only.
# ============================================================================


_ELEVENLABS_MAX_CHARS_PER_BATCH = 4800


def batch_dialogue_turns(turns: list[DialogueTurn]) -> list[list[DialogueTurn]]:
    batches: list[list[DialogueTurn]] = []
    current: list[DialogueTurn] = []
    current_len = 0
    for turn in turns:
        turn_len = len(turn.text)
        if current and current_len + turn_len > _ELEVENLABS_MAX_CHARS_PER_BATCH:
            batches.append(current)
            current = []
            current_len = 0
        current.append(turn)
        current_len += turn_len
    if current:
        batches.append(current)
    return batches
