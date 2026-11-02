"""``speech.budget`` — a target duration becomes a spoken word target.

The writer of anything that will be read aloud (a podcast script, a voice-over)
is told how many words to write; this step computes that number from the ONE
pace answer (:mod:`matrx_graph.speech_pace`, the ``speech/pace_wpm`` setting for
the run's organization). ``target_word_count`` and ``target_duration_seconds``
are the variable names the script Mandates declare, so an edge maps them
straight onto the writer. ``band_min``/``band_max`` are what a length check
accepts (±20%).

A duration that is not a positive whole number of seconds is a Failure — a
writer told "about NaN words" is worse than a run that stops and says why.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.model import KindModel
from matrx_graph.speech_pace import speech_budget
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


class SpeechBudgetInput(BaseModel):
    model_config = ConfigDict(extra="ignore")

    target_seconds: int | str = Field(
        description=(
            "How long the spoken result should run, in seconds. A form's text value "
            "('120') is accepted."
        )
    )
    language: str = Field(
        default="",
        description="The language it will be spoken in (recorded; per-language pace is not set yet).",
    )


class SpeechBudgetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SpeechBudgetOutput(KindModel, kind="speech_budget"):
    target_duration_seconds: int = Field(description="The requested length in seconds.")
    target_word_count: int = Field(description="How many spoken words fill that length.")
    band_min: int = Field(description="Fewest words a length check accepts.")
    band_max: int = Field(description="Most words a length check accepts.")
    wpm: int = Field(description="The speaking pace used, in words per minute.")
    pace_source: str = Field(description="Where the pace came from.")
    language: str = Field(description="The language passed in.")


class SpeechBudgetExecutor:
    """Turn a target duration into a spoken word target from the speaking-pace setting."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="speech.budget",
        category=NodeCategory.DATA,
        display_name="Speech Budget",
        description="Turn a length in seconds into how many words to write for it.",
        input_schema=SpeechBudgetInput,
        output_schema=SpeechBudgetOutput,
        output_kind="speech_budget",
        config_schema=SpeechBudgetConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="timer",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SpeechBudgetInput,
        config: SpeechBudgetConfig,
    ) -> NodeResult[SpeechBudgetOutput]:
        _ = config
        raw = inputs.target_seconds
        try:
            seconds = int(str(raw).strip()) if isinstance(raw, str) else int(raw)
        except ValueError:
            return failure(
                "duration_invalid",
                f"The target length {raw!r} is not a whole number of seconds.",
            )
        try:
            budget = await speech_budget(seconds, organization_id=ctx.organization_id)
        except ValueError as e:
            return failure("duration_invalid", str(e))
        return success(
            SpeechBudgetOutput(
                target_duration_seconds=budget.target_duration_seconds,
                target_word_count=budget.target_word_count,
                band_min=budget.band_min,
                band_max=budget.band_max,
                wpm=budget.wpm,
                pace_source=budget.pace_source,
                language=inputs.language,
            )
        )
