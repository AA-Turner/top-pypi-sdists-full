"""Regex extract + replace nodes.

``text.regex_extract`` returns all matches — either the full match for a
pattern with no groups, or a dict per match when groups are named, or a list
of tuples when groups are positional. Mode is auto-detected so the caller
writes one config shape and gets the natural output.

Items mode: give ``items`` (a list) instead of ``text`` and ``text_path`` (the
text inside each item; empty = the item itself, a list of strings is joined) —
``results`` holds one row per item (its position, the item unchanged, its own
matches), and ``matches`` / ``count`` / ``first`` are every item's matches in
order. Names pulled from search snippets keep the page they came from.
An item with no text there has no matches and is counted in ``unread``.

``text.regex_replace`` is a straight ``re.sub`` with count + flags options.

Python's ``re`` has no per-match timeout, so both judge the pattern before it
runs (:func:`matrx_graph.safe_regex.compile_safe`, ``exponential`` level): the
catastrophic shapes — ``(a+)+``, ``(a{1,3})+``, ``(a|ab)*``, ``(a*)*`` — are
refused with a sentence. Polynomial shapes (``.*a.*b``) and back-references stay
allowed here (saved workflows use them); the input cap — the
``workflow.regex.max_input_chars`` knob (:func:`matrx_graph.knobs.regex_max_input_chars`)
— bounds them.
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph import knobs
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes.text.term_scan import text_at_path
from matrx_graph.safe_regex import UnsafePatternError, compile_safe
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

_MAX_PATTERN_LEN = 2000


def _build_flags(flags_config: dict[str, bool]) -> int:
    out = 0
    if flags_config.get("ignorecase"):
        out |= re.IGNORECASE
    if flags_config.get("multiline"):
        out |= re.MULTILINE
    if flags_config.get("dotall"):
        out |= re.DOTALL
    if flags_config.get("verbose"):
        out |= re.VERBOSE
    return out


def _compile_pattern(pattern: str, flags_config: dict[str, bool]) -> re.Pattern:
    if len(pattern) > _MAX_PATTERN_LEN:
        raise ExecutionError(
            f"regex pattern too long ({len(pattern)} chars); cap is {_MAX_PATTERN_LEN}"
        )
    flags = _build_flags(flags_config)
    try:
        re.compile(pattern, flags)
    except re.error as e:
        raise ExecutionError(f"invalid regex: {e}") from e
    try:
        return compile_safe(pattern, flags=flags, level="exponential", max_length=None)
    except UnsafePatternError as e:
        raise ExecutionError(str(e)) from e


async def _refuse_long_input(text: str) -> None:
    cap = await knobs.regex_max_input_chars()
    if len(text) > cap:
        raise ExecutionError(
            f"regex input too long ({len(text):,} characters; a regex step reads at most {cap:,} — "
            f"knob workflow.regex.max_input_chars). Split the text first (text.split / data.batch)."
        )


# ---------------------------------------------------------------------------
# regex_extract
# ---------------------------------------------------------------------------


class RegexExtractInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None = Field(default=None, description="String to search. Use this or `items`.")
    items: list[JsonValue] | None = Field(
        default=None, description="A list to search; each item's text is read at `text_path`."
    )


class RegexExtractConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pattern: str = Field(
        min_length=1,
        description="Python regex. Named groups preferred for self-documentation.",
        json_schema_extra=field_extras(
            widget="code",
            placeholder=r"(?P<email>\S+@\S+)",
        ),
    )
    ignorecase: bool = Field(
        default=False, description="Case-insensitive matching (re.IGNORECASE)."
    )
    multiline: bool = Field(
        default=False,
        description="`^` and `$` match at each line boundary, not only string "
        "start/end (re.MULTILINE).",
    )
    dotall: bool = Field(default=False, description="`.` also matches newlines (re.DOTALL).")
    verbose: bool = Field(
        default=False,
        description="Allow whitespace and #-comments in the pattern (re.VERBOSE).",
    )
    first_only: bool = Field(
        default=False,
        description="Return only the first match instead of a list of all matches.",
    )
    text_path: str = Field(
        default="",
        description="Items mode: the text inside each item (e.g. 'snippet'); empty = the item itself.",
        json_schema_extra=field_extras(placeholder="snippet"),
    )
    required_message: str | None = Field(
        default=None,
        description="When set, finding no match FAILS the step with this message "
        "instead of emitting an empty result for downstream steps to trip on.",
    )


class RegexItemMatches(KindSubModel):
    index: int = Field(description="Position of the item in `items`.")
    item: JsonValue = Field(description="The item, unchanged.")
    matches: list[JsonValue] = Field(description="This item's matches, shaped as `matches`.")
    count: int = Field(description="How many matches this item has.")
    first: JsonValue = Field(default=None, description="This item's first match, or null.")


class RegexExtractOutput(KindModel, kind="regex_extract_result"):
    matches: list[JsonValue] = Field(
        default_factory=list,
        description="All matches — one entry per match: the full match string "
        "(no groups), a dict (named groups), or a list (positional groups). Named "
        "groups take precedence if a pattern mixes both.",
    )
    count: int = Field(default=0, description="How many matches were found.")
    # first is a convenience for "branch on found/not-found" without indexing.
    first: JsonValue = Field(
        default=None,
        description="The first match, or null when none — for a quick "
        "found/not-found branch without indexing.",
    )
    # Items-mode fields are left out of the dump when null: one-text mode emits exactly the keys the
    # enforced `regex_extract_result` kind published before them (additive until it is republished).
    results: list[RegexItemMatches] | None = Field(
        default=None, description="Items mode only: one row per item with its own matches.",
        exclude_if=lambda v: v is None,
    )
    unread: int | None = Field(
        default=None, description="Items mode only: items with no text at `text_path`.",
        exclude_if=lambda v: v is None,
    )


class RegexExtractExecutor:
    """Return regex matches. Shape follows group naming."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.regex_extract",
        category=NodeCategory.DATA,
        display_name="Find Text Patterns",
        description="Find and pull out pieces of text that match a pattern.",
        input_schema=RegexExtractInput,
        output_schema=RegexExtractOutput,
        config_schema=RegexExtractConfig,
        # No input kind: the step reads one `text` OR a list of `items` (text.term_scan's shape).
        output_kind="regex_extract_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="search",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: RegexExtractInput,
        config: RegexExtractConfig,
    ) -> NodeResult[RegexExtractOutput]:
        _ = ctx
        if (inputs.text is None) == (inputs.items is None):
            raise ExecutionError(
                "text.regex_extract: give either `text` (one text) or `items` (a list), not both and not neither."
            )
        pattern = _compile_pattern(
            config.pattern,
            {
                "ignorecase": config.ignorecase,
                "multiline": config.multiline,
                "dotall": config.dotall,
                "verbose": config.verbose,
            },
        )

        if inputs.text is not None:
            await _refuse_long_input(inputs.text)
            matches = self._find(pattern, inputs.text, config.first_only)
            if not matches and config.required_message:
                raise ExecutionError(config.required_message)
            first = matches[0] if matches else None
            return success(RegexExtractOutput(matches=matches, count=len(matches), first=first))

        assert inputs.items is not None
        results: list[RegexItemMatches] = []
        every: list[Any] = []
        unread = 0
        for index, item in enumerate(inputs.items):
            text, problem = text_at_path(item, config.text_path)
            if problem:
                raise ExecutionError(
                    f"text.regex_extract: item {index} has {problem} at "
                    f"{config.text_path or 'the item itself'!r}. Point `text_path` at the text."
                )
            found: list[Any] = []
            if text is None:
                unread += 1
            else:
                await _refuse_long_input(text)
                found = self._find(pattern, text, config.first_only)
            every.extend(found)
            results.append(RegexItemMatches(
                index=index, item=item, matches=found, count=len(found), first=found[0] if found else None
            ))
        if not every and config.required_message:
            raise ExecutionError(config.required_message)
        return success(RegexExtractOutput(
            matches=every, count=len(every), first=every[0] if every else None, results=results, unread=unread
        ))

    def _find(self, pattern: re.Pattern, text: str, first_only: bool) -> list[Any]:
        if first_only:
            m = pattern.search(text)
            return [self._shape_match(m, pattern)] if m else []
        return [self._shape_match(m, pattern) for m in pattern.finditer(text)]

    @staticmethod
    def _shape_match(m: re.Match, pattern: re.Pattern) -> Any:
        if pattern.groupindex:
            # Named groups — return dict keyed by name
            return {k: v for k, v in m.groupdict().items()}
        if pattern.groups:
            # Positional groups — return tuple as list
            return list(m.groups())
        # No groups — return the full match
        return m.group(0)


# ---------------------------------------------------------------------------
# regex_replace
# ---------------------------------------------------------------------------


class RegexReplaceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="The text to run substitutions on.")


class RegexReplaceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pattern: str = Field(min_length=1, description="Python regex.")
    replacement: str = Field(
        default="",
        description="Replacement. Use ``\\1``, ``\\2``, ``\\g<name>`` for groups.",
    )
    count: int = Field(
        default=0,
        ge=0,
        description="Max replacements. 0 = unbounded.",
    )
    ignorecase: bool = Field(
        default=False, description="Case-insensitive matching (re.IGNORECASE)."
    )
    multiline: bool = Field(
        default=False,
        description="`^` and `$` match at each line boundary (re.MULTILINE).",
    )
    dotall: bool = Field(default=False, description="`.` also matches newlines (re.DOTALL).")


class RegexReplaceOutput(KindModel, kind="regex_replace_result"):
    text: str = Field(description="The text after substitutions.")
    replacements: int = Field(description="How many substitutions were made.")


class RegexReplaceExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.regex_replace",
        category=NodeCategory.DATA,
        display_name="Replace Text Patterns",
        description="Find pieces of text that match a pattern and replace them.",
        input_schema=RegexReplaceInput,
        output_schema=RegexReplaceOutput,
        config_schema=RegexReplaceConfig,
        input_kind="text",
        output_kind="regex_replace_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="replace",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: RegexReplaceInput,
        config: RegexReplaceConfig,
    ) -> NodeResult[RegexReplaceOutput]:
        _ = ctx
        await _refuse_long_input(inputs.text)

        pattern = _compile_pattern(
            config.pattern,
            {
                "ignorecase": config.ignorecase,
                "multiline": config.multiline,
                "dotall": config.dotall,
                "verbose": False,
            },
        )

        new_text, n = pattern.subn(config.replacement, inputs.text, count=config.count)
        return success(RegexReplaceOutput(text=new_text, replacements=n))
