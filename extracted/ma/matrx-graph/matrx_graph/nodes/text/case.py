"""``text.case`` — tidy the case and spacing of a text or a list of texts.

Lower / upper / title / casefold, trim the ends, collapse runs of whitespace.
A list comes back as a list in the same order; a missing value (None) stays
None. The sandbox expression helpers (``lower``/``casefold`` in ``_sandbox``)
cover one value inside a condition; the sandbox has no comprehensions, so a
LIST of addresses or names can only be normalized by a step — this one.
"""

from __future__ import annotations

import re
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

CaseMode = Literal["keep", "lower", "upper", "title", "casefold"]

_SPACES_RE = re.compile(r"\s+")
# A "word" for title case is a run between whitespace or hyphens, so
# "mary-jane o'neil" -> "Mary-Jane O'neil" (never str.title()'s "Don'T").
_WORD_RE = re.compile(r"[^\s\-]+")


class TextCaseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str | list[str | None] | None = Field(
        default=None,
        description="One text, or a list of texts. Missing values stay missing.",
    )


class TextCaseConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case: CaseMode = Field(
        default="keep",
        description="keep · lower · upper · title (each word capitalized) · "
        "casefold (lower, also for 'ß' and similar).",
        json_schema_extra=field_extras(widget="select"),
    )
    trim: bool = Field(default=True, description="Remove spaces at the start and end.")
    collapse_spaces: bool = Field(
        default=True, description="Turn every run of spaces, tabs and line breaks into one space."
    )


class TextCaseOutput(KindModel, kind="text_case_result"):
    text: str | list[str | None] | None = Field(
        description="The tidied text, or the tidied list in the same order."
    )
    changed: int = Field(description="How many texts were different after tidying.")


def _title(text: str) -> str:
    return _WORD_RE.sub(lambda m: m[0][:1].upper() + m[0][1:].lower(), text)


def tidy_text(text: str, config: TextCaseConfig) -> str:
    if config.collapse_spaces:
        text = _SPACES_RE.sub(" ", text)
    if config.trim:
        text = text.strip()
    if config.case == "lower":
        text = text.lower()
    elif config.case == "upper":
        text = text.upper()
    elif config.case == "casefold":
        text = text.casefold()
    elif config.case == "title":
        text = _title(text)
    return text


class TextCaseExecutor:
    """Normalize case and whitespace on a text or a list of texts."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.case",
        category=NodeCategory.DATA,
        display_name="Change Text Case",
        description="Change text to lower, upper or title case and tidy its spaces.",
        input_schema=TextCaseInput,
        output_schema=TextCaseOutput,
        config_schema=TextCaseConfig,
        output_kind="text_case_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="case-sensitive",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: TextCaseInput,
        config: TextCaseConfig,
    ) -> NodeResult[TextCaseOutput]:
        _ = ctx
        value = inputs.text
        if value is None:
            return success(TextCaseOutput(text=None, changed=0))
        if isinstance(value, str):
            out = tidy_text(value, config)
            return success(TextCaseOutput(text=out, changed=int(out != value)))
        tidied = [None if v is None else tidy_text(v, config) for v in value]
        changed = sum(1 for before, after in zip(value, tidied, strict=True) if before != after)
        return success(TextCaseOutput(text=tidied, changed=changed))


__all__ = ["TextCaseConfig", "TextCaseExecutor", "TextCaseInput", "TextCaseOutput", "tidy_text"]
