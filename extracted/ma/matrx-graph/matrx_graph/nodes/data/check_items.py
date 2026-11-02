"""``data.check_items`` — check every item of a list against what was sent; keep what passes.

The general problem (generic-only STEP-CENSUS GAP 2, "answer checks"): an agent
answers with a list (quotes, ids, labels, evidence keys, citations) and code
must decide, before anything is saved, which items are honest — is the quote
really in the page sent, is every id one that was sent and answered once, is
every label one of the allowed ones, is nothing forbidden mentioned. Sixteen
custom steps did this by hand. This step is the one primitive for the class.

The checks run in THE one check engine, :func:`matrx_graph.checks.check_items`
(beside the response checks ``length`` / ``host``); the verbatim folding is the
engine's :func:`~matrx_graph.checks.flat` / :func:`~matrx_graph.checks.folded`,
which aidream's reader steps import too.

Inputs: ``items`` (the list) plus anything else on the step's edges; a check
names those other inputs by dot path (``source: page_text``,
``allowed_from: sent_ids``, ``terms_from: register.terms``). Works on a whole
answer or inside a For Each item (one batch's answer with that batch's text).

It KEEPS and DROPS; it never routes. Conditional edges on ``passed`` /
``dropped`` route (Rule 9: no edge capability is duplicated here).
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from pydantic import model_validator

from matrx_graph.checks import (
    ItemCheckConfigError,
    ItemsCheckResult,
    ItemCheckSpec,
    _dig,
    _MISSING,
    check_items,
    parse_item_checks,
)
from matrx_graph.errors import ExecutionError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


class CheckItemsInput(BaseModel):
    # extra="allow": the text sent, the ids sent, the allowed labels, the
    # forbidden terms — whatever else arrives on the edges — are what the
    # checks name by dot path.
    model_config = ConfigDict(extra="allow")
    items: list[JsonValue] = Field(description="The list to check (an agent's answer, one batch of it, …).")


class CheckItemsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    checks: list[ItemCheckSpec] = Field(
        default_factory=list,
        description=(
            "The checks, each over one field of every item: verbatim (the text is in `source`), "
            "in_set (one of `allowed` / `allowed_from`), once (an id sent, answered at most once), "
            "same_set (exactly one answer per id sent), max_length, not_contains (`terms` / "
            "`terms_from`, optional `fuzzy`), pattern (`patterns` / `patterns_from` regular expressions, "
            "`mode` must or must_not, `ignore_case`), required. Any check can apply only to some items "
            "(`when_path` + `when_in`). Each says on_fail: drop_item or fail."
        ),
    )
    checks_from: str | None = Field(
        default=None,
        description="The input (dot path) holding more checks, in the same shape as `checks` — a shared "
        "step's caller passes its own. Checked when the step runs by the same rules as `checks`; "
        "they run after `checks`.",
    )

    @model_validator(mode="after")
    def _some_checks(self) -> CheckItemsConfig:
        if not self.checks and not self.checks_from:
            raise ValueError("data.check_items needs `checks` or `checks_from`.")
        return self


class CheckItemsOutput(ItemsCheckResult, KindModel, kind="checked_items_result"):
    """The kept items, every dropped item with its reasons, counts by reason, and id-set reports.

    Kind ``checked_items_result``, registered in ``aidream/kinds/data_ops.py`` (ships with this code)."""


class CheckItemsExecutor:
    """Run the item checks; drop failing items (or fail the step for on_fail=fail checks)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.check_items",
        category=NodeCategory.DATA,
        display_name="Check Items",
        description="Check each list item against what was sent or a pattern; keep the items that pass.",
        input_schema=CheckItemsInput,
        input_kind="items",
        output_schema=CheckItemsOutput,
        config_schema=CheckItemsConfig,
        output_kind="checked_items_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="list-checks",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: CheckItemsInput,
        config: CheckItemsConfig,
    ) -> NodeResult[CheckItemsOutput]:
        values = {k: v for k, v in inputs.model_dump(mode="json").items() if k != "items"}
        try:
            checks = list(config.checks)
            if config.checks_from:
                got = _dig(values, config.checks_from)
                if got is _MISSING and ctx is not None:
                    # A caller that sends no extra checks is the common case for a shared unit
                    # (mandate.ask_and_check, 2026-10-27): nothing extra runs. Absent is still
                    # SAID, so a misspelt name is seen, not silent.
                    await ctx.flag_for_review(
                        "check_items.checks_from_absent",
                        f"`checks_from` names '{config.checks_from}', which this step was not given, "
                        "so no extra checks ran.",
                        category="unexpected_path",
                    )
                # Absent, null or [] = nothing extra to check; any other non-list is refused.
                if got is not _MISSING and got is not None and got != []:
                    checks += parse_item_checks(got, f"checks_from '{config.checks_from}'")
            result = check_items(list(inputs.items), checks, values)
        except ItemCheckConfigError as e:
            raise ExecutionError(f"data.check_items: {e}") from e
        if result.failed_checks:
            first = next(
                (r for rej in result.rejected for r in rej.reasons if r.check in result.failed_checks),
                None,
            )
            missing = {k: s.missing for k, s in result.sets.items() if s.missing and k in result.failed_checks}
            why = (
                f"item {next(rej.index for rej in result.rejected if first in rej.reasons)}: {first.detail}"
                if first
                else f"ids sent but not answered: {missing}"
            )
            return failure(
                "items_check_failed",
                f"The answer failed {', '.join(result.failed_checks)} ({why}).",
                details={"report": result.model_dump(mode="json")},
            )
        return success(CheckItemsOutput(**result.model_dump()))
