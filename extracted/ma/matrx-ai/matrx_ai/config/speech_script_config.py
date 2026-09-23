"""The ``speech_script`` content part — ordered spoken turns for text to speech.

WHY A PART AND NOT A CONTROL (`common-docs/systems/agents/typed-messages/FEATURE.md`,
the Text to speech row): the script is the CONTENT being performed. It rides in
``UnifiedMessage.content`` beside text and media exactly like every other part.
The controls that shape the performance (voice, speed, pause, language, format,
``performance_direction``) live on the agent's settings.

**Parts are semantic; translators decide the wire.** Each TTS translator asks
``matrx_ai.speech.compile`` for its own rendering of the same script (ElevenLabs
dialogue turns with inline audio tags, a Gemini director's-notes + labelled
transcript, an OpenAI input + ``instructions``). ``to_transcript()`` here is the
vendor-neutral reading a TEXT model (or a human) sees.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_ai.speech.kinds import SpeechScript

__all__ = ["SpeechScriptContent"]


@dataclass
class SpeechScriptContent:
    type: Literal["speech_script"] = "speech_script"
    turns: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def typed(self) -> SpeechScript:
        """The validated kind instance — the contract, enforced."""
        return SpeechScript(turns=self.turns)

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = self.typed().model_dump(mode="json", exclude_none=True)
        result["type"] = "speech_script"
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result

    def replace_variables(self, variables: dict[str, Any]) -> bool:
        """Substitute ``{{variable}}`` in every author-written slot of every turn.

        Slots: ``text``, ``direction``, ``voice`` (a voice bound to a variable)
        and ``speaker`` (a name can be a variable too — ``{{guest_name}}``).
        Values pass through ``prompt_safe_value``, the same door text parts use.
        Never drops the part: returns False always.
        """
        if not variables:
            return False
        from matrx_ai.config.prompt_values import prompt_safe_value

        rendered = {name: prompt_safe_value(value) for name, value in variables.items()}

        def fill(value: Any) -> Any:
            if not isinstance(value, str):
                return value
            for name, replacement in rendered.items():
                value = value.replace(f"{{{{{name}}}}}", replacement)
            return value

        self.turns = [
            {key: (fill(val) if key in ("text", "direction", "voice", "speaker") else val)
             for key, val in dict(turn).items()}
            for turn in self.turns
        ]
        return False

    def get_output(self) -> str:
        """Nothing — a script is what was ASKED to be spoken, never the answer."""
        return ""

    def to_transcript(self) -> str:
        """The neutral reading: one ``Speaker: text`` line per turn."""
        script = self.typed()
        if len(script.speakers()) == 1:
            return "\n".join(turn.text.strip() for turn in script.turns)
        return "\n".join(f"{turn.speaker}: {turn.text.strip()}" for turn in script.turns)

    # A text-generating model that is handed a script sees its transcript as
    # text — never a silent drop. TTS translators never reach these: they
    # compile the script through ``matrx_ai.speech.compile`` instead.
    def to_google(self) -> dict[str, Any] | None:
        text = self.to_transcript()
        return {"text": text} if text else None

    def to_openai(self, role: str = "user") -> dict[str, Any] | None:
        text = self.to_transcript()
        if not text:
            return None
        return {"type": "output_text" if role == "assistant" else "input_text", "text": text}

    def to_anthropic(self) -> dict[str, Any] | None:
        text = self.to_transcript()
        return {"type": "text", "text": text} if text else None
