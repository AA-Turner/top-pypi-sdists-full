"""``data.rules`` — an ordered decision table: values in, a label + reason + score out.

The general problem (GAP 3 in the generic-only STEP-CENSUS): "decide what this
is, by rules a person can read" — a certainty for every search result, which of
seven paths to take, whether an agent's proof passes, how relevant a news item
is. Each was a custom Python step. This is the one primitive for the class.

Settings:

* ``rules`` — ordered rows ``{when: <predicate>, then: {label, reason?, score?, …}}``.
  ``when`` is the SAME sandboxed expression language ``data.filter`` /
  ``data.transform`` / ``control.branch`` use (``nodes/_sandbox.py``) — never a
  second one. ``then.reason`` interpolates ``{dot.path}`` placeholders with the
  shared ``render_template_string`` (``nodes/_template.py``). Every other
  ``then`` field is carried through as written.
* ``mode`` — ``first_match`` (default: the first row whose ``when`` is truthy)
  or ``all_match`` (every truthy row, the first is the headline).
* ``default`` — the ``then`` used when no row matches. Absent + no match →
  ``label: null`` and ``matched: false``; never an exception.
* ``items_path`` — a dot path into the inputs naming a LIST. Each element is
  decided on its own and returned beside its result, plus counts per label.
* ``write_fields`` (list mode) — each element (an object) comes back in
  ``updated_items`` with the deciding row's ``fields`` written onto it; a field
  no row set keeps the element's own value, and an element nothing decided is
  unchanged. ``decision_keys`` also writes the row's label / reason / score under
  the names given. Replaces the merge/override template after a rules step.
* ``sum_scores`` (``all_match`` only) — every decision also carries
  ``total_score``: the sum of the ``score`` of every matching row (a row
  without a score adds 0; nothing matched → the default's score, else 0), so a
  ranking reads ONE number while ``matches`` keeps each row's reason. With
  ``write_fields``, ``decision_keys: {"total_score": "rank"}`` writes it onto the
  element. One table of +/- points is a lead score, a person-or-business tally,
  a candidate rank.
* ``rules`` from a run input — ``{"$input": "query_patterns"}`` lets a caller
  edit the table per run (the declared input's default stands in when saving);
  every run's table goes through this model, so a bad predicate fails the step
  naming its row, exactly as an authored one is refused.
* ``split_by_label`` (list mode) — ``by_label`` holds one plain list per label
  (the elements themselves, updated when ``write_fields`` is on), so each
  group feeds the next step directly instead of an unwrap step per label.

What ``inputs`` is inside ``when`` and ``{…}`` in ``reason``:

* single mode — the node's whole input payload (``inputs['hosts']``);
* list mode — the same payload plus ``item`` (the current element) and
  ``index`` (its position): ``inputs['item']['host'] in inputs['hosts']``.
  The element always sits under ``item``, so a list of plain strings needs no
  ``{'value': …}`` wrapper and the inert-predicate trap (``bind_item``) cannot
  arise.

It LABELS; it never routes. Conditional edges on ``label`` do the routing
(Rule 9: no edge capability is duplicated here).
"""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval, validate_expression
from matrx_graph.nodes._template import render_template_string, resolve_path
from matrx_graph.nodes.data.filter import LeftOutEntry, left_out_label, step_id
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

#: Names list mode adds to the bound payload. A payload that already carries
#: one is refused rather than silently shadowed.
_ITEM_KEY = "item"
_INDEX_KEY = "index"


class RulesInput(BaseModel):
    """Whatever the incoming edges deliver; every key is readable as ``inputs['<key>']``."""

    model_config = ConfigDict(extra="allow")


class RuleThen(BaseModel):
    """What a matching row says: ``label``/``reason``/``score``, plus any extra
    named values under ``fields`` (``{"path": "deep", "review": true}``). In the
    output ``then`` row the ``fields`` are spread flat beside label/reason/score,
    so a downstream step reads ``then.path``."""

    model_config = ConfigDict(extra="forbid")

    label: str | None = Field(
        default=None,
        description="The answer this row gives — the value conditional edges route on.",
    )
    reason: str | None = Field(
        default=None,
        description=(
            "Why, in plain words. ``{dot.path}`` placeholders are filled from the "
            "same `inputs` the predicate sees (``{item.title}``, ``{hosts}``); a "
            "path that is not there renders empty."
        ),
    )
    score: float | None = Field(
        default=None, description="A number for this answer (a certainty, a rank)."
    )
    fields: dict[str, JsonValue] = Field(
        default_factory=dict,
        description=(
            "Extra named values this row answers with (a path name, a review mark, a "
            "tier). Spread flat into the output `then` row; string values (nested too) fill ``{dot.path}`` like `reason`."
        ),
    )

    @model_validator(mode="after")
    def _fields_do_not_shadow(self) -> RuleThen:
        clash = sorted(set(self.fields) & {"label", "reason", "score"})
        if clash:
            raise ValueError(
                f"`fields` may not repeat {clash}; set them as the row's own label/reason/score."
            )
        return self


class Rule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    when: str = Field(
        min_length=1,
        description=(
            "Predicate over `inputs` (the shared sandbox: comparisons, `in`, "
            "`and`/`or`, `len`, `coalesce`, …). Truthy = this row matches."
        ),
        json_schema_extra=field_extras(
            widget="code",
            code_language="python",
            placeholder="inputs['item']['host'] in inputs['hosts']",
        ),
    )
    then: RuleThen = Field(description="What this row answers when it matches.")


class RulesConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rules: list[Rule] = Field(
        min_length=1,
        description=(
            "Ordered rows; order is the priority in first_match mode. May come from a run input "
            "({\"$input\": name}, the input's default standing in at save time); the run's table is "
            "checked like an authored one."
        ),
        json_schema_extra={"x-run-input": True},
    )
    mode: Literal["first_match", "all_match"] = Field(
        default="first_match",
        description=(
            "first_match: the first matching row decides. all_match: every "
            "matching row is returned; the first is the headline."
        ),
        json_schema_extra=field_extras(widget="select"),
    )
    default: RuleThen | None = Field(
        default=None,
        description=(
            "The answer when no row matches. Without one, an unmatched value "
            "gets label null and matched false."
        ),
    )
    items_path: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Dot path into the inputs naming a list (``results`` or "
            "``search.items``). Each element is decided on its own as "
            "`inputs['item']`, with its position as `inputs['index']`."
        ),
    )

    write_fields: bool = Field(
        default=False,
        description=(
            "List mode: write the deciding row's `fields` onto each element (an object) and "
            "return them in `updated_items`. A field no row set keeps the element's value."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )
    sum_scores: bool = Field(
        default=False,
        description=(
            "all_match: also return `total_score` — the sum of every matching row's score "
            "(a row with no score adds 0; nothing matched: the default's score, else 0). "
            "Per element in list mode, for ranking."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )
    decision_keys: dict[Literal["label", "reason", "score", "total_score"], str] = Field(
        default_factory=dict,
        description=(
            "With `write_fields`: also write the deciding row's label / reason / score (and, with "
            "`sum_scores`, `total_score`) onto "
            "each element under these names (`{\"label\": \"choice\", \"score\": \"probability\"}`). "
            "A row that leaves one empty keeps the element's own value."
        ),
    )
    split_by_label: bool = Field(
        default=False,
        description=(
            "List mode: also return `by_label` — one plain list of elements per label "
            "(updated elements when `write_fields` is on)."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )

    left_out_labels: list[str] = Field(
        default_factory=list,
        description=(
            "List mode: elements whose label is one of these are left out — returned in `left_out` "
            "(position, label, the row's reason, this step) and not in `kept_items`, which holds the "
            "rest in order (updated elements when `write_fields` is on). Empty: off."
        ),
    )
    left_out_label_path: str = Field(
        default="",
        description="With `left_out_labels`: path to each element's id or label (e.g. 'url'); empty = 'Item N'.",
    )

    @model_validator(mode="after")
    def _list_options_need_a_list(self) -> RulesConfig:
        if (self.write_fields or self.split_by_label or self.left_out_labels) and self.items_path is None:
            raise ValueError(
                "`write_fields`, `split_by_label` and `left_out_labels` decide a list: set `items_path` too."
            )
        return self

    @model_validator(mode="after")
    def _sum_needs_all_match(self) -> RulesConfig:
        if self.sum_scores and self.mode != "all_match":
            raise ValueError("`sum_scores` adds up every matching row: set `mode` to all_match.")
        if "total_score" in self.decision_keys and not self.sum_scores:
            raise ValueError("`decision_keys.total_score` writes the sum: turn `sum_scores` on.")
        return self

    @model_validator(mode="after")
    def _predicates_are_legal(self) -> RulesConfig:
        # Authoring-time refusal: a predicate the sandbox would reject is named
        # with its row now, not discovered by the first run that reaches it.
        for index, rule in enumerate(self.rules):
            try:
                validate_expression(rule.when)
            except ExecutionError as e:
                raise ValueError(f"rule {index} ({rule.when!r}): {e}") from e
        return self


class RuleHit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule: int = Field(description="Position of the matching row in `rules`.")
    then: dict[str, JsonValue] = Field(
        description="That row's answer, with its reason filled in."
    )


class RuleDecision(BaseModel):
    """One decision — the whole input's (single mode) or one element's (list mode)."""

    model_config = ConfigDict(extra="forbid")

    label: str | None = Field(
        default=None, description="The deciding row's label (or the default's); null when nothing decided."
    )
    reason: str | None = Field(default=None, description="The deciding row's reason, filled in.")
    score: float | None = Field(default=None, description="The deciding row's score.")
    matched: bool = Field(
        default=False,
        description="True when a rule matched; false when the default (or nothing) answered.",
    )
    matched_rules: list[int] = Field(
        default_factory=list, description="Positions of every matching row, in order."
    )
    total_score: float | None = Field(
        default=None,
        description="With `sum_scores`: the sum of every matching row's score (absent when the option is off).",
        # Left out of the dump when null: a table without `sum_scores` emits exactly the keys the
        # enforced `rules_result` kind published before this field (additive until it is republished).
        exclude_if=lambda v: v is None,
    )
    then: dict[str, JsonValue] | None = Field(
        default=None,
        description="The full deciding row (label, reason, score and any extra fields); null when nothing decided.",
    )
    matches: list[RuleHit] = Field(
        default_factory=list,
        description="Every matching row with its filled-in answer (one at most in first_match mode).",
    )


class RuledItem(RuleDecision):
    item: JsonValue = Field(description="The list element this decision is about, unchanged.")
    index: int = Field(description="The element's position in the list.")


class RulesOutput(RuleDecision, KindModel, kind="rules_result"):
    """Single mode: the decision fields. List mode: ``items`` + ``counts``; the
    top-level decision fields then stay empty except ``matched`` (true when any
    element matched a rule) and ``matched_rules`` (every row that matched any element)."""

    items: list[RuledItem] | None = Field(
        default=None, description="List mode only: every element beside its own decision."
    )
    counts: dict[str, int] | None = Field(
        default=None, description="List mode only: how many elements got each label."
    )
    unlabeled: int | None = Field(
        default=None, description="List mode only: elements no row and no default labelled."
    )
    updated_items: list[JsonValue] | None = Field(
        default=None,
        description="List mode with `write_fields`: every element in order, the deciding row's "
        "fields written onto it (an element nothing decided is unchanged).",
    )
    by_label: dict[str, list[JsonValue]] | None = Field(
        default=None,
        description="List mode with `split_by_label`: the elements of each label, in order "
        "(unlabelled elements are in none).",
    )
    kept_items: list[JsonValue] | None = Field(
        default=None,
        description="List mode with `left_out_labels`: every element not left out, in order "
        "(updated elements when `write_fields` is on).",
    )
    left_out: list[LeftOutEntry] | None = Field(
        default=None,
        description="List mode with `left_out_labels`: each element left out by position and label, "
        "with the deciding row's reason (else its label) and this step's id.",
    )


def _fill_value(value: JsonValue, bound: dict[str, Any]) -> JsonValue:
    """Fill ``{dot.path}`` in every string inside ``value`` (recursively), exactly as ``reason`` is filled."""
    if isinstance(value, str):
        return render_template_string(value, bound, whole_key="inputs")[0]
    if isinstance(value, list):
        return [_fill_value(v, bound) for v in value]
    if isinstance(value, dict):
        return {k: _fill_value(v, bound) for k, v in value.items()}
    return value


def _fill(then: RuleThen, bound: dict[str, Any]) -> dict[str, JsonValue]:
    reason = then.reason
    if reason:
        reason, _ = render_template_string(reason, bound, whole_key="inputs")
    fields = {k: _fill_value(v, bound) for k, v in then.fields.items()}
    return {"label": then.label, "reason": reason, "score": then.score, **fields}


def _decide(config: RulesConfig, bound: dict[str, Any], *, where: str) -> RuleDecision:
    hits: list[RuleHit] = []
    for index, rule in enumerate(config.rules):
        try:
            passed = safe_eval(rule.when, bound)
        except ExecutionError as e:
            raise ExecutionError(f"data.rules: rule {index} ({rule.when!r}){where}: {e}") from e
        except KeyError as e:
            raise ExecutionError(
                f"data.rules: rule {index} ({rule.when!r}){where} asked for {e.args[0]!r}, "
                f"which is not there. The values it can read are {sorted(bound)}"
                + (
                    f"; the item's keys are {sorted(bound[_ITEM_KEY])}"
                    if isinstance(bound.get(_ITEM_KEY), dict)
                    else ""
                )
                + ". Guard an optional field first: `'x' in inputs['item'] and inputs['item']['x'] > 1`."
            ) from e
        except Exception as e:  # noqa: BLE001 — a TypeError/IndexError/ZeroDivision in an author's predicate
            raise ExecutionError(
                f"data.rules: rule {index} ({rule.when!r}){where} could not be evaluated: "
                f"{type(e).__name__}: {e}"
            ) from e
        if passed:
            hits.append(RuleHit(rule=index, then=_fill(rule.then, bound)))
            if config.mode == "first_match":
                break
    total: float | None = None
    if config.sum_scores:
        total = float(sum(float(hit.then.get("score") or 0) for hit in hits))  # type: ignore[arg-type]
        if not hits and config.default is not None:
            total = float(config.default.score or 0)
    if hits:
        head = hits[0].then
        return RuleDecision(
            total_score=total,
            label=head.get("label"),  # type: ignore[arg-type]
            reason=head.get("reason"),  # type: ignore[arg-type]
            score=head.get("score"),  # type: ignore[arg-type]
            matched=True,
            matched_rules=[hit.rule for hit in hits],
            then=head,
            matches=hits,
        )
    if config.default is not None:
        row = _fill(config.default, bound)
        return RuleDecision(
            total_score=total,
            label=row.get("label"),  # type: ignore[arg-type]
            reason=row.get("reason"),  # type: ignore[arg-type]
            score=row.get("score"),  # type: ignore[arg-type]
            matched=False,
            then=row,
        )
    return RuleDecision(total_score=total)


class RulesExecutor:
    """Ordered decision table over the inputs (or over each element of a list)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.rules",
        category=NodeCategory.DATA,
        display_name="Rules",
        description="Decide a label, reason and score from ordered rules.",
        input_schema=RulesInput,
        output_schema=RulesOutput,
        config_schema=RulesConfig,
        output_kind="rules_result",
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
        inputs: RulesInput,
        config: RulesConfig,
    ) -> NodeResult[RulesOutput]:
        payload = inputs.model_dump(mode="json")

        if config.items_path is None:
            decision = _decide(config, payload, where="")
            return success(RulesOutput(**decision.model_dump()))

        elements = resolve_path(payload, config.items_path, label="inputs")
        if not isinstance(elements, list):
            raise ExecutionError(
                f"data.rules: items_path {config.items_path!r} is a "
                f"{type(elements).__name__}, not a list. Point it at the list to decide per element."
            )
        clash = sorted(k for k in (_ITEM_KEY, _INDEX_KEY) if k in payload)
        if clash:
            raise ExecutionError(
                f"data.rules: list mode adds {_ITEM_KEY!r} and {_INDEX_KEY!r} to `inputs`, but the "
                f"inputs already carry {clash}. Rename that input so the predicate is not ambiguous."
            )

        items: list[RuledItem] = []
        updated: list[JsonValue] = []
        by_label: dict[str, list[JsonValue]] = {}
        counts: dict[str, int] = {}
        unlabeled = 0
        kept_items: list[JsonValue] = []
        left_out: list[LeftOutEntry] = []
        dropping = set(config.left_out_labels)
        seen_rules: list[int] = []
        for index, element in enumerate(elements):
            bound = {**payload, _ITEM_KEY: element, _INDEX_KEY: index}
            decision = _decide(config, bound, where=f" on item {index} of {len(elements)}")
            items.append(RuledItem(item=element, index=index, **decision.model_dump()))
            plain = element
            if config.write_fields:
                plain = _write_fields(element, decision, index, config.decision_keys)
                updated.append(plain)
            if config.split_by_label and decision.label is not None:
                by_label.setdefault(decision.label, []).append(plain)
            if dropping and decision.label in dropping:
                left_out.append(
                    LeftOutEntry(
                        item=index,
                        label=left_out_label(element, index, config.left_out_label_path),
                        reason=decision.reason or decision.label or "",
                        step=step_id(ctx),
                    )
                )
            elif dropping:
                kept_items.append(plain)
            if decision.label is None:
                unlabeled += 1
            else:
                counts[decision.label] = counts.get(decision.label, 0) + 1
            for rule in decision.matched_rules:
                if rule not in seen_rules:
                    seen_rules.append(rule)
        return success(
            RulesOutput(
                matched=any(item.matched for item in items),
                matched_rules=sorted(seen_rules),
                items=items,
                counts=counts,
                unlabeled=unlabeled,
                updated_items=updated if config.write_fields else None,
                by_label=by_label if config.split_by_label else None,
                kept_items=kept_items if dropping else None,
                left_out=left_out if dropping else None,
            )
        )


_DECISION_KEYS = frozenset({"label", "reason", "score"})


def _write_fields(
    element: Any, decision: RuleDecision, index: int, decision_keys: dict[str, str]
) -> JsonValue:
    """``element`` with the deciding row's own ``fields`` (and, under ``decision_keys``,
    its label / reason / score) written onto it."""
    if not isinstance(element, dict):
        raise ExecutionError(
            f"data.rules: write_fields writes onto objects, but item {index} is a "
            f"{type(element).__name__}. Turn write_fields off, or decide a list of objects."
        )
    then = decision.then or {}
    fields = {k: v for k, v in then.items() if k not in _DECISION_KEYS}
    for key, name in decision_keys.items():
        if key == "total_score":
            if decision.total_score is not None:
                fields[name] = decision.total_score
        elif then.get(key) is not None:
            fields[name] = then[key]
    return {**element, **fields}
