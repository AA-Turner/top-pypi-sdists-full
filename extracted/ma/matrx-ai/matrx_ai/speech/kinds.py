"""The ``speech_script`` typed-message contract as a real ``KindModel``.

A speech script is what a text-to-speech author WRITES: an ordered list of
turns, each spoken by a named speaker, with optional performance direction and
an optional pause after it (``common-docs/systems/agents/typed-messages/FEATURE.md``,
the Text to speech row). One turn is plain single-speaker speech; several turns
are a dialogue.

It is a PART, not a control: it is the content being performed. The controls
that shape HOW it is performed (voice, speed, pause, language, format,
``performance_direction``) stay on the agent's settings, and each vendor's
translator places them where that vendor wants them
(``matrx_ai.speech.compile``).

Registration (label, family, example) lives host-side in
``aidream/kinds/speech.py`` — the package declares the SHAPE, the host
publishes it, exactly as the decision kinds do.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel, KindSubModel
from pydantic import Field, model_validator

__all__ = ["MAX_PAUSE_MS", "SpeechScript", "SpeechTurn"]

#: A pause longer than this is a scene break, not a pause, and every vendor
#: renders it as dead air — refused at authoring time with the limit named.
MAX_PAUSE_MS = 10_000


class SpeechTurn(KindSubModel):
    """One spoken turn. Not a kind: it has no meaning outside its script."""

    speaker: str = Field(
        min_length=1,
        max_length=40,
        description=(
            "The speaker's name. Turns with the same name are the same speaker. "
            "For multi-speaker vendors (Gemini) this is the transcript label."
        ),
    )
    voice: str | None = Field(
        default=None,
        description=(
            "The voice this speaker uses: a literal provider voice id from the "
            "model's catalog, or a {{variable}}. Empty = bound to the agent's "
            "Voice setting (tts_voice)."
        ),
    )
    text: str = Field(min_length=1, description="What is said. Any {{variable}} is filled at run time.")
    direction: str | None = Field(
        default=None,
        description="Free-text performance direction for this turn only (e.g. 'warm, a little amused').",
    )
    pause_after_ms: int | None = Field(
        default=None,
        ge=0,
        le=MAX_PAUSE_MS,
        description="Silence after this turn, in milliseconds.",
    )


class SpeechScript(KindModel, kind="speech_script"):
    """An ordered script of spoken turns — the text-to-speech authoring part."""

    turns: list[SpeechTurn] = Field(min_length=1)

    @model_validator(mode="after")
    def _one_voice_per_speaker(self) -> SpeechScript:
        bound: dict[str, str] = {}
        for index, turn in enumerate(self.turns, start=1):
            voice = (turn.voice or "").strip()
            if not voice:
                continue
            previous = bound.get(turn.speaker)
            if previous is not None and previous != voice:
                raise ValueError(
                    f"Speaker {turn.speaker!r} is given two voices ({previous!r} and "
                    f"{voice!r}, turn {index}). A speaker keeps one voice for the whole "
                    "script — use a different speaker name for a different voice."
                )
            bound[turn.speaker] = voice
        return self

    def speakers(self) -> list[str]:
        """Distinct speaker names in first-appearance order."""
        seen: list[str] = []
        for turn in self.turns:
            if turn.speaker not in seen:
                seen.append(turn.speaker)
        return seen

    def voice_for(self, speaker: str) -> str | None:
        for turn in self.turns:
            if turn.speaker == speaker and (turn.voice or "").strip():
                return (turn.voice or "").strip()
        return None
