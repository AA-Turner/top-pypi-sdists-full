"""Text manipulation primitives: template, split, join, slug, word_count.

These are pure convenience nodes. Everything they do is theoretically
possible via ``data.transform``, but writing a sandboxed expression for
"lower-case and replace spaces with hyphens" is painful. Shipping them
as dedicated nodes makes the common-case workflows readable.

``text.template`` uses a deliberately restricted placeholder syntax
(``{{name}}``) rather than Jinja — Jinja's full surface is a security
surface we don't want to audit here. Placeholders resolve by key lookup
against ``variables``; missing keys become empty strings.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.well_known import TextValue
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}")


def _resolve_placeholder(path: str, variables: dict[str, Any]) -> str:
    """Dotted-path lookup; missing parts → empty string."""
    current: Any = variables
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return ""
    if current is None:
        return ""
    return str(current)


# ---------------------------------------------------------------------------
# text.template
# ---------------------------------------------------------------------------


class TemplateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template: str = Field(
        description="String with ``{{placeholder}}`` slots.",
    )
    variables: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Map of placeholder name → replacement value.",
    )


class TemplateOutput(KindModel, kind="template_render_result"):
    text: str = Field(description="The template with every {{placeholder}} filled in.")
    missing_keys: list[str] = Field(
        default_factory=list,
        description="Placeholder names that had no value in `variables` (each was "
        "rendered as an empty string).",
    )


class TemplateExecutor:
    """Fill ``{{placeholder}}`` slots in a string. Missing keys → empty."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.template",
        category=NodeCategory.DATA,
        display_name="Fill a Template",
        description="Fill in the blanks of a text template with your values.",
        input_schema=TemplateInput,
        output_schema=TemplateOutput,
        output_kind="template_render_result",
        # THE one node whose INPUT carries placeholders on purpose.
        renders_input_templates=True,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="type",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: TemplateInput,
        config: BaseModel,
    ) -> NodeResult[TemplateOutput]:
        _ = ctx, config
        missing: list[str] = []

        def _sub(m: re.Match) -> str:
            key = m.group(1)
            # Walk dotted paths but reject on first missing segment.
            parts = key.split(".")
            current: Any = inputs.variables
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    missing.append(key)
                    return ""
            return "" if current is None else str(current)

        rendered = _PLACEHOLDER_RE.sub(_sub, inputs.template)
        # missing_keys is DOMAIN data (soft/informational), not a node
        # failure — a template with unfilled slots still renders.
        return success(TemplateOutput(text=rendered, missing_keys=missing))


# ---------------------------------------------------------------------------
# text.split
# ---------------------------------------------------------------------------


class SplitInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="The text to split into parts.")


class SplitConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    delimiter: str = Field(
        default="\n",
        description="Delimiter to split on. Use '\\n' for newlines, ',' for CSV-like.",
    )
    regex: bool = Field(
        default=False,
        description="Treat ``delimiter`` as a regex pattern.",
    )
    max_splits: int = Field(
        default=0,
        ge=0,
        description="Cap on the number of splits (0 = unlimited). N splits ⇒ N+1 parts.",
    )
    strip: bool = Field(
        default=False,
        description="Strip whitespace from each part.",
    )
    drop_empty: bool = Field(
        default=False,
        description="Drop empty-string parts after splitting.",
    )


class SplitOutput(KindModel, kind="split_result"):
    parts: list[str] = Field(description="The pieces of the text after splitting.")
    count: int = Field(description="How many parts were produced.")


class SplitExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.split",
        category=NodeCategory.DATA,
        display_name="Split Text",
        description="Split text into a list wherever a separator appears.",
        input_schema=SplitInput,
        output_schema=SplitOutput,
        config_schema=SplitConfig,
        input_kind="text",
        output_kind="split_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="split",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SplitInput,
        config: SplitConfig,
    ) -> NodeResult[SplitOutput]:
        _ = ctx
        if config.regex:
            parts = re.split(
                config.delimiter,
                inputs.text,
                maxsplit=config.max_splits if config.max_splits > 0 else 0,
            )
        else:
            # ``max_splits`` is a cap on SPLITS, not on parts — N splits yield
            # N+1 parts, matching ``re.split(maxsplit=…)`` on the regex branch
            # above. The ``- 1`` that used to live here made ``max_splits=1``
            # perform ZERO splits on this branch while the regex branch
            # performed one: the same config silently meant two different
            # things, and the plain branch returned the text UNSPLIT.
            parts = inputs.text.split(
                config.delimiter, config.max_splits if config.max_splits > 0 else -1
            )

        if config.strip:
            parts = [p.strip() for p in parts]
        if config.drop_empty:
            parts = [p for p in parts if p]

        return success(SplitOutput(parts=parts, count=len(parts)))


# ---------------------------------------------------------------------------
# text.join
# ---------------------------------------------------------------------------


class JoinInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    parts: list[str] = Field(description="Strings to join.")


class JoinConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    separator: str = Field(
        default="\n",
        description="String inserted between parts.",
    )
    prefix: str = Field(default="", description="Prepended to the result.")
    suffix: str = Field(default="", description="Appended to the result.")


#: ``text.join`` answers with the well-known ``text`` kind itself (§4.4: reuse,
#: never re-mint). The private ``{text: str}`` class this alias replaced was one
#: of THREE copies of that one shape.
JoinOutput = TextValue


class JoinExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.join",
        category=NodeCategory.DATA,
        display_name="Join Text",
        description="Join a list of text pieces into one, with a separator between them.",
        input_schema=JoinInput,
        output_schema=JoinOutput,
        config_schema=JoinConfig,
        # `text` since its 2026-08-21 object re-seed ({"text": str}) — the exact
        # shape of JoinOutput. It replaced `text_result`, minted only because
        # the old scalar `text` was undeclarable.
        output_kind="text",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="minus",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: JoinInput,
        config: JoinConfig,
    ) -> NodeResult[JoinOutput]:
        _ = ctx
        body = config.separator.join(inputs.parts)
        return success(JoinOutput(text=f"{config.prefix}{body}{config.suffix}"))


# ---------------------------------------------------------------------------
# text.slug
# ---------------------------------------------------------------------------


class SlugInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="The text to turn into a slug.")


class SlugConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_length: int = Field(default=80, ge=1, le=500, description="Trim slug to this many chars.")
    separator: str = Field(
        default="-",
        description="Character(s) used to separate words.",
        json_schema_extra=field_extras(widget="text"),
    )


class SlugOutput(KindModel, kind="slug_result"):
    slug: str = Field(
        description="The URL/filename-safe slug — lowercase ASCII with runs of "
        "non-alphanumerics collapsed to the separator."
    )


class SlugExecutor:
    """URL / filename slugifier — ASCII, lowercase, normalized separators."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.slug",
        category=NodeCategory.DATA,
        display_name="Make URL-Friendly",
        description="Turn text into a clean version safe for links and file names.",
        input_schema=SlugInput,
        output_schema=SlugOutput,
        config_schema=SlugConfig,
        input_kind="text",
        output_kind="slug_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="link-2",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SlugInput,
        config: SlugConfig,
    ) -> NodeResult[SlugOutput]:
        _ = ctx
        # Unicode → ASCII, strip diacritics
        normalized = unicodedata.normalize("NFKD", inputs.text)
        ascii_bytes = normalized.encode("ascii", "ignore").decode("ascii")
        lowered = ascii_bytes.lower()
        # Collapse runs of non-alphanumeric into the separator
        slug = re.sub(r"[^a-z0-9]+", config.separator, lowered)
        slug = slug.strip(config.separator)
        if len(slug) > config.max_length:
            slug = slug[: config.max_length].rstrip(config.separator)
        return success(SlugOutput(slug=slug))


# ---------------------------------------------------------------------------
# text.word_count
# ---------------------------------------------------------------------------


class WordCountInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="The text to measure.")


class WordCountOutput(KindModel, kind="word_count_result"):
    characters: int = Field(description="Total character count, including whitespace.")
    characters_no_spaces: int = Field(description="Character count excluding all whitespace.")
    words: int = Field(description="Number of words (runs of word characters).")
    sentences: int = Field(description="Number of sentences (split on '.', '!', '?').")
    paragraphs: int = Field(description="Number of paragraphs (blocks separated by blank lines).")
    lines: int = Field(description="Number of lines.")


class WordCountExecutor:
    """Length / structural metrics on a block of text."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.word_count",
        category=NodeCategory.DATA,
        display_name="Word Count",
        description="Count the characters, words, sentences, and paragraphs in a text.",
        input_schema=WordCountInput,
        output_schema=WordCountOutput,
        input_kind="text",
        output_kind="word_count_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="hash",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: WordCountInput,
        config: BaseModel,
    ) -> NodeResult[WordCountOutput]:
        _ = ctx, config
        # THE ONE TEXT COUNTER — response length checks count with the same
        # function, so a step's word count and a check's word count never disagree.
        from matrx_graph.checks import text_metrics

        metrics = text_metrics(inputs.text)

        return success(
            WordCountOutput(**metrics)
        )
