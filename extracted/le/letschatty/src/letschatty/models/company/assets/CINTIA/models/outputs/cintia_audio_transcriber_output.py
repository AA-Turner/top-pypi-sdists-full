"""CintiaAudioTranscriberOutput — decision output for the audio transcriber PGP.

Unlike responder / tagger / smart-follow-up, the audio transcriber is a
fire-and-forget PGP that does not produce an AiOutput or messages. Its
"decision output" is a lightweight receipt of the transcription attempt,
stored with flat fields directly on the subclass (no ``data`` wrapper).

Both the real transcription result and the "skipped" marker (when the
message already carries a transcription) round-trip through this model.
"""

from typing import Literal, Optional

from pydantic import ConfigDict, Field

from .cintia_decision_output import DecisionOutput, DecisionOutputType


class CintiaAudioTranscriberOutput(DecisionOutput):
    type: Literal[DecisionOutputType.AUDIO_TRANSCRIBER] = DecisionOutputType.AUDIO_TRANSCRIBER
    status: Optional[str] = Field(
        default=None,
        description="Transcription outcome — e.g. 'ok', 'fallback', 'skipped'",
    )
    message_id: Optional[str] = Field(
        default=None,
        description="ID of the audio message that was transcribed",
    )
    transcription_length: Optional[int] = Field(
        default=None,
        description="Length in characters of the transcription stored on the message",
    )
    fallback: Optional[bool] = Field(
        default=None,
        description="True if the fallback transcription path was used",
    )

    # Accept any additional flat fields historical docs may have carried
    # without failing validation on load.
    model_config = ConfigDict(extra="allow")
