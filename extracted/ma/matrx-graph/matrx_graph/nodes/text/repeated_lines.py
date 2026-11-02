"""text.remove_repeated_lines — strip the lines a set of texts all share.

Site menus, footers, cookie banners, "subscribe" boxes: the same lines sit on
most pages of one site. Given a list of texts, every line (trimmed, whitespace
collapsed) found in at least ``min_texts`` of them is removed from every text
and handed back ONCE in ``repeated_lines``. Each text keeps its id so the caller
can rejoin; a text left with nothing is flagged ``emptied``, never dropped.

Grouping look-alike texts is ``data.group``'s job, not this step's.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.checks import flat
from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.nodes.data.filter import LeftOutEntry, left_out_label, step_id
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


class RepeatedLinesInput(KindModel, kind="remove_repeated_lines_request"):
    texts: list[JsonValue] = Field(
        description="The texts to clean: plain strings, or objects with an id and a text field."
    )


class RepeatedLinesConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_texts: int = Field(
        default=3,
        ge=2,
        description="A line is removed when it appears in at least this many of the texts.",
    )
    text_field: str = Field(
        default="text",
        description="For object items: the field holding the text.",
    )
    id_field: str = Field(
        default="id",
        description="For object items: the field holding the id. Plain strings and "
        "items without an id are identified by their position in the list (0, 1, 2...).",
    )
    items_mode: bool = Field(
        default=False,
        description=(
            "Also return the items themselves: `kept_items` holds every item with its text "
            "replaced by the cleaned text (objects keep their other fields), items left with "
            "nothing are listed in `left_out` instead, and `repeated_text` holds the removed "
            "lines once, as one text. Off: only the per-text answers."
        ),
    )


class CleanedText(KindSubModel):
    id: JsonValue = Field(description="The item's id (or its position when it has none).")
    text: str = Field(description="The text with the repeated lines removed.")
    removed: int = Field(description="How many lines were removed from this text.")
    emptied: bool = Field(description="True when nothing is left in this text.")


class RepeatedLinesOutput(KindModel, kind="repeated_lines_result"):
    items: list[CleanedText] = Field(
        description="Every input text in the original order, with repeated lines removed."
    )
    repeated_lines: list[str] = Field(
        description="Each removed line once, in the order first seen."
    )
    emptied_ids: list[JsonValue] = Field(
        description="Ids of texts that have nothing left (or had nothing to begin with)."
    )
    text_count: int = Field(description="How many texts were read.")
    kept_items: list[JsonValue] | None = Field(
        default=None,
        description="With `items_mode`: the items with something left, in order, text replaced by the cleaned text.",
    )
    left_out: list[LeftOutEntry] | None = Field(
        default=None,
        description="With `items_mode`: the items left with nothing, by position and id, with the reason and step.",
    )
    repeated_text: str | None = Field(
        default=None, description="With `items_mode`: the removed lines once, joined by line breaks."
    )


class RemoveRepeatedLinesExecutor:
    """Remove lines that repeat across many texts."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.remove_repeated_lines",
        category=NodeCategory.DATA,
        display_name="Remove Repeated Lines",
        description=(
            "Take out the lines that repeat across many texts (menus, footers, "
            "cookie banners) and list them once."
        ),
        input_schema=RepeatedLinesInput,
        input_kind="remove_repeated_lines_request",
        output_schema=RepeatedLinesOutput,
        config_schema=RepeatedLinesConfig,
        output_kind="repeated_lines_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="list-x",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: RepeatedLinesInput,
        config: RepeatedLinesConfig,
    ) -> NodeResult[RepeatedLinesOutput]:
        ids: list[JsonValue] = []
        texts: list[str] = []
        for position, item in enumerate(inputs.texts):
            if item is None:
                ids.append(position)
                texts.append("")
            elif isinstance(item, str):
                ids.append(position)
                texts.append(item)
            elif isinstance(item, dict):
                value = item.get(config.text_field)
                if value is None:
                    value = ""
                if not isinstance(value, str):
                    return failure(
                        "text_not_a_string",
                        f"Item {position} has a '{config.text_field}' that is not text.",
                    )
                item_id = item.get(config.id_field)
                ids.append(position if item_id is None else item_id)
                texts.append(value)
            else:
                return failure(
                    "item_not_text",
                    f"Item {position} is neither text nor an object with a "
                    f"'{config.text_field}' field.",
                )

        # Lines compare by ``flat`` (the platform's one text folding: markdown marks, pipes,
        # curly quotes, width, whitespace), the same as brand discovery's site-wide lines.
        # Blank lines are kept exactly as they were.
        lines_of = [t.split("\n") for t in texts]
        seen_in: dict[str, int] = {}
        wording: dict[str, str] = {}  # first-seen original wording of each line
        for lines in lines_of:
            for ln in lines:
                key = flat(ln)
                if key:
                    wording.setdefault(key, ln.strip())
            for key in {flat(ln) for ln in lines} - {""}:
                seen_in[key] = seen_in.get(key, 0) + 1
        repeated = {k for k, n in seen_in.items() if n >= config.min_texts}

        items: list[CleanedText] = []
        for item_id, lines in zip(ids, lines_of, strict=True):
            kept = [ln for ln in lines if flat(ln) not in repeated]
            removed = len(lines) - len(kept)
            emptied = not any(flat(ln) for ln in kept)
            items.append(
                CleanedText(
                    id=item_id,
                    text="" if emptied else "\n".join(kept),
                    removed=removed,
                    emptied=emptied,
                )
            )
        repeated_lines = [wording[k] for k in wording if k in repeated]
        kept_items: list[JsonValue] | None = None
        left_out: list[LeftOutEntry] | None = None
        if config.items_mode:
            kept_items, left_out = [], []
            for position, (item, cleaned) in enumerate(zip(inputs.texts, items, strict=True)):
                if cleaned.emptied:
                    left_out.append(
                        LeftOutEntry(
                            item=position,
                            label=left_out_label(item, position, config.id_field) if isinstance(item, dict) else f"Item {position}",
                            reason=f"nothing left but lines repeated in {config.min_texts}+ items (or no text)",
                            step=step_id(ctx),
                        )
                    )
                elif isinstance(item, dict):
                    kept_items.append({**item, config.text_field: cleaned.text})
                else:
                    kept_items.append(cleaned.text)
        return success(
            RepeatedLinesOutput(
                items=items,
                repeated_lines=repeated_lines,
                emptied_ids=[i.id for i in items if i.emptied],
                text_count=len(items),
                kept_items=kept_items,
                left_out=left_out,
                repeated_text="\n".join(repeated_lines) if config.items_mode else None,
            )
        )
