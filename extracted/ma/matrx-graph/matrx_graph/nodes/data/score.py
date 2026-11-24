"""``data.score`` — Score Items: a readable, editable score for every item of a list, in ONE step.

A score is a decision a person edits: which numbers count, how much, and where they top out. Written as
one long expression it is unreadable and its normalizer is typed by hand — the live "Find pages" score
topped out at 62.5 because its divisor was a typed number. Here every part is a named row the Studio
shows and anyone can change, and the normalizer is DERIVED from the declared maxima, never typed.
Design: the contract is this package's FEATURE.md § Score Items.

The stages, in order:

1. **Settings** — ``settings`` are the defaults; the ``overrides`` input (e.g. a research intent's
   ``scoring_overrides.pre_read``) replaces them key by key. A key that is ``locked``, unknown, or of a
   different type than its default is ignored and listed in ``ignored_overrides``. ``effective_settings``
   records every value with its source (``default`` or the ``overrides_source`` input).
2. **Aggregates** — each group goes over a list (``over``) and computes named values: ``weighted_mean``,
   ``mean``, ``max``, ``min``, ``sum``, ``count``. ``scope: item`` runs per item over a related list (the
   item's keyword links); ``scope: all`` runs once over the whole list (the best score in the set).
   A group's ``each`` factors are computed per element first (a rank curve per link).
3. **Factors**, in order — ``expression``, ``curve`` (points + tail), ``bands``, ``clamp``, ``log_scale``,
   ``half_life`` or ``lookup``. A factor reads settings, step inputs, aggregates, ``item`` and every
   EARLIER factor by bare name. ``only_when`` gates it (``if_not`` is the value otherwise).
4. **Maxima** — each factor declares ``max`` (a number or an expression over the settings), or the
   step derives it from the factor's own definition (a curve's best point, a clamp's ``high``...).
5. **Combine** — ``product`` or ``weighted_sum`` over named factors, or an ``expression``.
6. **Normalize** — ``to: 100`` divides by the combine of the declared maxima, then clamps to 0..to.
7. **Then** factors (may read ``combined`` and ``score``), and the **outputs**: named keys, each an
   expression with its own rounding, written onto the item (or under ``write_as``).

Expressions are the ONE sandbox language (``matrx_graph.nodes._sandbox``): a bare declared name reads
that value, so ``1 + authority_boost * (authority / 100)`` is spelled exactly like that.
Users: research pre-read, post-read and video scores; news relevance; SEO search opportunity; lead
scoring; Smart Add ranking; the context-bundle importance.
"""

from __future__ import annotations

import ast
import functools
import hashlib
import json
import math
import re
from datetime import UTC, datetime
from decimal import Decimal
from types import CodeType
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import (
    _SAFE_HELPERS,
    _LoopGuard,
    _loop_counter,
    max_loop_steps,
    validate_expression,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

#: A number, or an expression (text) over the settings and earlier values.
NumberOrExpression = float | int | str
#: A literal value, or an expression (text). A literal text answer is written in quotes: "'reject'".
ValueOrExpression = float | int | bool | str | None

#: Names every expression may read that no author declares.
RESERVED_NAMES = frozenset({"inputs", "item", "items", "combined", "score", "score_version", "now"})
_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
_UNIT_SECONDS = {"seconds": 1.0, "days": 86_400.0, "years": 365.25 * 86_400}


# ---------------------------------------------------------------------------
# Expressions: bare declared names read the value; everything else is the sandbox.
# ---------------------------------------------------------------------------


class _BareNames(ast.NodeTransformer):
    """``authority_boost`` → ``inputs['authority_boost']``, except helpers, ``inputs`` and loop variables."""

    def __init__(self, bound: set[str]) -> None:
        self.bound = bound

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if (
            isinstance(node.ctx, ast.Load)
            and node.id != "inputs"
            and node.id not in _SAFE_HELPERS
            and node.id not in self.bound
            and node.id not in {"None", "True", "False"}
        ):
            return ast.copy_location(
                ast.Subscript(value=ast.Name(id="inputs", ctx=ast.Load()), slice=ast.Constant(node.id), ctx=ast.Load()),
                node,
            )
        return node


def _loop_bound_names(tree: ast.AST) -> set[str]:
    bound: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.comprehension):
            targets = [node.target] if isinstance(node.target, ast.Name) else list(getattr(node.target, "elts", []))
            bound |= {t.id for t in targets if isinstance(t, ast.Name)}
    return bound


@functools.lru_cache(maxsize=4096)
def _program(expr: str) -> tuple[CodeType, bool, str]:
    """Compile ``expr`` once: bare names rewritten, then the sandbox's own walk and loop guard."""
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ExecutionError(f"Invalid expression syntax in {expr!r}: {e}") from e
    tree = ast.fix_missing_locations(_BareNames(_loop_bound_names(tree)).visit(tree))
    text = ast.unparse(tree)
    parsed = validate_expression(text)
    has_loops = any(isinstance(n, ast.comprehension) for n in ast.walk(parsed))
    if has_loops:
        parsed = ast.fix_missing_locations(_LoopGuard().visit(parsed))
    return compile(parsed, "<data.score>", "eval"), has_loops, text


def check_expression(expr: str) -> None:
    """Authoring check: the expression parses and passes the sandbox (no data needed)."""
    _program(expr)


def evaluate(expr: str, names: dict[str, Any], where: str) -> Any:
    code, has_loops, _ = _program(expr)
    namespace: dict[str, Any] = {"__builtins__": {}, "inputs": names, **_SAFE_HELPERS}
    if has_loops:
        namespace["__loop"] = _loop_counter(max_loop_steps())
    try:
        return eval(code, namespace)  # noqa: S307 — compiled from the sandbox-validated tree above
    except KeyError as e:
        name = e.args[0] if e.args else "?"
        if isinstance(name, str) and name not in names:
            known = ", ".join(sorted(k for k in names if not k.startswith("_")))
            raise ExecutionError(f"{where}: {expr!r} reads `{name}`, which is not known here. Known: {known}.") from e
        raise ExecutionError(f"{where}: {expr!r} has no field {name!r}.") from e
    except ExecutionError as e:
        raise ExecutionError(f"{where}: {e}") from e
    except Exception as e:  # noqa: BLE001 — every evaluation failure names the factor and the item
        raise ExecutionError(f"{where}: {expr!r} failed: {type(e).__name__}: {e}") from e


def _value(v: Any, names: dict[str, Any], where: str) -> Any:
    return evaluate(v, names, where) if isinstance(v, str) else v


def _is_number(v: Any) -> bool:
    return isinstance(v, int | float) and not isinstance(v, bool)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


class CurvePoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    up_to: NumberOrExpression = Field(description="This point covers values up to and including this.")
    value: NumberOrExpression = Field(description="The factor's value there.")


class Band(BaseModel):
    """One row of a bands factor: the value when the input falls inside every bound given."""

    model_config = ConfigDict(extra="forbid")

    at_least: NumberOrExpression | None = Field(default=None, description="Input ≥ this.")
    above: NumberOrExpression | None = Field(default=None, description="Input > this.")
    at_most: NumberOrExpression | None = Field(default=None, description="Input ≤ this.")
    below: NumberOrExpression | None = Field(default=None, description="Input < this.")
    value: ValueOrExpression = Field(description="The factor's value in this band.")

    @model_validator(mode="after")
    def _bounded(self) -> Band:
        if self.at_least is not None and self.above is not None:
            raise ValueError("a band takes at_least or above, not both")
        if self.at_most is not None and self.below is not None:
            raise ValueError("a band takes at_most or below, not both")
        return self


FactorType = Literal["expression", "curve", "bands", "clamp", "log_scale", "half_life", "lookup"]


class Factor(BaseModel):
    """One named part of the score."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, description="Lower-case name; later factors read it by this name.")
    type: FactorType = Field(
        description=(
            "expression: `of` is the value. curve: points over `of`. bands: the first band `of` falls in. "
            "clamp: `of` held between low and high. log_scale: log10(of + 1) / saturates_at, 0..1. "
            "half_life: 0.5 per half_life of age since the time `of`. lookup: `table[of]`."
        )
    )
    label: str = Field(default="", description="What this factor means, in plain words.")
    of: str = Field(min_length=1, description="The expression this factor reads (for `expression`, its value).")
    points: list[CurvePoint] = Field(default_factory=list, description="curve: points in order, lowest up_to first.")
    tail: NumberOrExpression | None = Field(default=None, description="curve: the value past the last point.")
    bands: list[Band] = Field(default_factory=list, description="bands: rows in order; the first that fits wins.")
    default: ValueOrExpression = Field(default=None, description="bands / lookup: the value when nothing fits.")
    low: NumberOrExpression | None = Field(default=None, description="clamp: the lowest value.")
    high: NumberOrExpression | None = Field(default=None, description="clamp: the highest value.")
    saturates_at: NumberOrExpression | None = Field(
        default=None, description="log_scale: log10(of + 1) at which the factor reaches 1."
    )
    half_life: NumberOrExpression | None = Field(default=None, description="half_life: age that halves the factor.")
    unit: Literal["seconds", "days", "years"] = Field(default="years", description="half_life: the age unit.")
    table: dict[str, ValueOrExpression] = Field(default_factory=dict, description="lookup: value per key.")
    missing: ValueOrExpression = Field(
        default=None, description="The value when `of` is empty (None) — or below 0 for log_scale."
    )
    only_when: str = Field(default="", description="Compute only when this is true; else `if_not`.")
    if_not: ValueOrExpression = Field(default=None, description="The value when `only_when` is false.")
    max: NumberOrExpression | None = Field(
        default=None,
        description="Declared maximum (number or expression over the settings). Empty: derived from the factor.",
    )
    min: NumberOrExpression | None = Field(
        default=None, description="Declared minimum. Empty: derived from the factor where it can be."
    )

    @model_validator(mode="after")
    def _shape(self) -> Factor:
        needs = {
            "curve": ("points", bool(self.points)),
            "bands": ("bands", bool(self.bands)),
            "log_scale": ("saturates_at", self.saturates_at is not None),
            "half_life": ("half_life", self.half_life is not None),
            "lookup": ("table", bool(self.table)),
            "clamp": ("low or high", self.low is not None or self.high is not None),
        }
        if self.type in needs and not needs[self.type][1]:
            raise ValueError(f"factor {self.name!r}: a {self.type} factor needs {needs[self.type][0]}")
        return self

    def expressions(self) -> list[str]:
        out = [self.of] + ([self.only_when] if self.only_when else [])
        values: list[Any] = [self.tail, self.default, self.low, self.high, self.saturates_at, self.half_life,
                             self.missing, self.if_not, self.max, self.min]
        values += [v for p in self.points for v in (p.up_to, p.value)]
        values += [v for b in self.bands for v in (b.at_least, b.above, b.at_most, b.below, b.value)]
        values += list(self.table.values())
        return out + [v for v in values if isinstance(v, str)]


class AggregateValue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, description="Lower-case name; factors read it by this name.")
    op: Literal["weighted_mean", "mean", "max", "min", "sum", "count"]
    of: str = Field(default="", description="Per element: the value (empty for count). Empty values are skipped.")
    weight: str = Field(default="", description="weighted_mean: per element, its weight.")
    empty: ValueOrExpression = Field(default=None, description="The value when the list has nothing to aggregate.")
    label: str = Field(default="", description="What this value means, in plain words.")

    @model_validator(mode="after")
    def _shape(self) -> AggregateValue:
        if self.op != "count" and not self.of:
            raise ValueError(f"aggregate {self.name!r}: {self.op} needs `of`")
        if self.op == "weighted_mean" and not self.weight:
            raise ValueError(f"aggregate {self.name!r}: weighted_mean needs `weight`")
        return self


class AggregateGroup(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    over: str = Field(min_length=1, description="The list to go over (e.g. item['keyword_links'], or items).")
    as_: str = Field(default="each", alias="as", description="The name each element is read by.")
    scope: Literal["item", "all"] = Field(
        default="item", description="item: per item over its own list. all: once, over the whole list."
    )
    each: list[Factor] = Field(default_factory=list, description="Factors computed per element first.")
    values: list[AggregateValue] = Field(min_length=1, description="The named aggregates.")


class Combine(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["product", "weighted_sum", "expression"]
    of: list[str] = Field(default_factory=list, description="product / weighted_sum: the factor names, in order.")
    weights: dict[str, NumberOrExpression] = Field(
        default_factory=dict, description="weighted_sum: weight per factor name (a number or a setting's name)."
    )
    expression: str = Field(default="", description="expression: the combined value over the factors.")
    max: NumberOrExpression | None = Field(default=None, description="expression: its declared maximum.")
    missing: NumberOrExpression | None = Field(
        default=None, description="The value used for a factor that came out empty (e.g. a neutral 0.5)."
    )

    @model_validator(mode="after")
    def _shape(self) -> Combine:
        if self.op == "expression" and not self.expression:
            raise ValueError("combine: op expression needs `expression`")
        if self.op != "expression" and not self.of:
            raise ValueError(f"combine: {self.op} needs `of` (the factor names)")
        if self.op == "weighted_sum":
            missing = [n for n in self.of if n not in self.weights]
            extra = [n for n in self.weights if n not in self.of]
            if missing or extra:
                raise ValueError(f"combine: weights must name exactly the factors in `of` (missing {missing}, extra {extra})")
        return self


class Normalize(BaseModel):
    model_config = ConfigDict(extra="forbid")

    to: float = Field(default=100.0, gt=0, description="The best reachable item scores exactly this.")


class OutputKey(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, description="The output field name.")
    value: str = Field(default="", description="Expression for its value; empty reads the name `key`.")
    round: int | None = Field(default=None, ge=0, le=12, description="Digits; 0 = a whole number; empty = as is.")
    label: str = Field(default="", description="What this output means, in plain words.")


class ScoreConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    settings: dict[str, JsonValue] = Field(
        default_factory=dict, description="Named defaults; every expression reads them by name."
    )
    setting_labels: dict[str, str] = Field(default_factory=dict, description="What each setting means.")
    locked: list[str] = Field(default_factory=list, description="Settings the `overrides` input may not change.")
    overrides_section: str = Field(
        default="", description="Read overrides[section] instead of the whole `overrides` input (e.g. pre_read)."
    )
    aggregates: list[AggregateGroup] = Field(default_factory=list, description="Lists to aggregate first.")
    factors: list[Factor] = Field(default_factory=list, description="The score's named parts, in order.")
    combine: Combine | None = Field(default=None, description="How the factors make one value.")
    normalize: Normalize | None = Field(
        default=None, description="Divide by the best reachable combined value (derived), times `to`."
    )
    then: list[Factor] = Field(default_factory=list, description="Factors after the score (read combined, score).")
    outputs: list[OutputKey] = Field(min_length=1, description="The named, rounded keys written per item.")
    write_as: str = Field(default="", description="Write the keys under this field of the item; empty: on the item.")

    @model_validator(mode="after")
    def _consistent(self) -> ScoreConfig:
        declared: list[tuple[str, str]] = [(n, "setting") for n in self.settings]
        for g in self.aggregates:
            declared.append((g.as_, "aggregate element"))
            declared += [(f.name, "per-element factor") for f in g.each]
            declared += [(v.name, "aggregate") for v in g.values]
        declared += [(f.name, "factor") for f in self.factors]
        declared += [(f.name, "then factor") for f in self.then]
        seen: dict[str, str] = {}
        for name, what in declared:
            if not _NAME.match(name):
                raise ValueError(f"data.score: {what} name {name!r} must be lower-case letters, digits and _")
            if name in RESERVED_NAMES or name in _SAFE_HELPERS:
                raise ValueError(f"data.score: {what} name {name!r} is taken by the language; rename it")
            if name in seen:
                raise ValueError(f"data.score: {name!r} is both a {seen[name]} and a {what}; give each its own name")
            seen[name] = what
        unknown_locked = sorted(set(self.locked) - set(self.settings))
        if unknown_locked:
            raise ValueError(f"data.score: locked {unknown_locked} are not settings")
        unknown_labels = sorted(set(self.setting_labels) - set(self.settings))
        if unknown_labels:
            raise ValueError(f"data.score: setting_labels {unknown_labels} are not settings")
        factor_names = [f.name for f in self.factors]
        if self.combine is not None:
            absent = [n for n in self.combine.of if n not in factor_names]
            if absent:
                raise ValueError(f"data.score: combine reads {absent}, which are not factors")
        if self.normalize is not None:
            if self.combine is None:
                raise ValueError("data.score: normalize divides the combined value; add combine")
            if self.combine.op == "expression" and self.combine.max is None:
                raise ValueError("data.score: normalize needs the combine expression's declared max")
            by_name = {f.name: f for f in self.factors}
            for n in self.combine.of:
                f = by_name[n]
                if f.max is None and f.type == "expression":
                    raise ValueError(f"data.score: factor {n!r} is combined and normalized; declare its max")
        keys = [o.key for o in self.outputs]
        if len(set(keys)) != len(keys):
            raise ValueError("data.score: each output key appears once")
        for expr in self._expressions():
            try:
                check_expression(expr)
            except ExecutionError as e:
                raise ValueError(f"data.score: {e}") from e
        return self

    def declared_names(self) -> set[str]:
        names = set(self.settings) | {f.name for f in [*self.factors, *self.then]}
        for g in self.aggregates:
            names |= {g.as_} | {f.name for f in g.each} | {v.name for v in g.values}
        return names

    def _expressions(self) -> list[str]:
        out: list[str] = []
        for g in self.aggregates:
            out.append(g.over)
            for f in g.each:
                out += f.expressions()
            for v in g.values:
                out += [e for e in (v.of, v.weight) if e]
                if isinstance(v.empty, str):
                    out.append(v.empty)
        for f in [*self.factors, *self.then]:
            out += f.expressions()
        if self.combine is not None:
            out += [w for w in self.combine.weights.values() if isinstance(w, str)]
            out += [e for e in (self.combine.expression, self.combine.max, self.combine.missing) if isinstance(e, str) and e]
        out += [o.value or o.key for o in self.outputs]
        return out


# ---------------------------------------------------------------------------
# Input / output
# ---------------------------------------------------------------------------


class _ScoreFields(BaseModel):
    items: list[JsonValue] = Field(description="The items to score.")
    overrides: dict[str, JsonValue] | None = Field(
        default=None, description="Values that replace settings key by key (e.g. an intent's scoring_overrides)."
    )
    overrides_source: str = Field(
        default="overrides", description="Where the overrides came from, recorded per value (e.g. intent:news)."
    )
    score_version: str | None = Field(
        default=None,
        description=(
            "A name for the scoring that ran; empty (the norm): a digest of the definition and the settings that "
            "applied, so only a real scoring change gives a new version."
        ),
    )
    now: str | None = Field(default=None, description="ISO time half_life ages are measured to; empty: the clock.")


class ScoreRequest(KindModel, _ScoreFields, kind="score_items_request"):
    """The request kind: the declared fields (the scheduler checks only these against the kind)."""


class ScoreInput(_ScoreFields):
    # extra="allow": every other input is readable by name (e.g. topic_keyword_weight); the kind
    # check reads the declared fields only (scheduler._kind_contract_inputs).
    model_config = ConfigDict(extra="allow")


class EffectiveSetting(KindSubModel):
    value: JsonValue = Field(description="The value this run used.")
    default: JsonValue = Field(description="The step's default.")
    source: str = Field(description="'default', or where the override came from.")


class IgnoredOverride(KindSubModel):
    key: str
    value: JsonValue
    reason: str


class Normalizer(KindSubModel):
    combined_max: float = Field(description="The best reachable combined value, from the declared maxima.")
    to: float = Field(description="The score that best value maps to.")


class ScoreOutput(KindModel, kind="scored_items_result"):
    items: list[JsonValue] = Field(description="The items, in input order, with their output keys written.")
    effective_settings: dict[str, EffectiveSetting] = Field(description="Every setting with its value and source.")
    ignored_overrides: list[IgnoredOverride] = Field(description="Overrides that were not applied, and why.")
    normalizer: Normalizer | None = Field(default=None, description="The derived divisor, when normalized.")
    score_version: str = Field(description="The version that scored these items.")


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


def _same_type(default: Any, value: Any) -> bool:
    if _is_number(default):
        return _is_number(value)
    if isinstance(default, bool):
        return isinstance(value, bool)
    return type(default) is type(value)


def merge_settings(
    config: ScoreConfig, overrides: dict[str, Any] | None, source: str
) -> tuple[dict[str, Any], dict[str, EffectiveSetting], list[IgnoredOverride]]:
    """Defaults, then each override that names an unlocked setting with a value of the same type."""
    raw = overrides or {}
    if config.overrides_section:
        section = raw.get(config.overrides_section)
        raw = section if isinstance(section, dict) else {}
    values = dict(config.settings)
    sources = dict.fromkeys(values, "default")
    ignored: list[IgnoredOverride] = []
    for key, value in raw.items():
        if key not in config.settings:
            ignored.append(IgnoredOverride(key=key, value=value, reason="not a setting of this step"))
        elif key in config.locked:
            ignored.append(IgnoredOverride(key=key, value=value, reason="locked on this step"))
        elif not _same_type(config.settings[key], value):
            ignored.append(IgnoredOverride(key=key, value=value, reason=f"not a {type(config.settings[key]).__name__}"))
        else:
            values[key], sources[key] = value, source
    effective = {
        k: EffectiveSetting(value=values[k], default=config.settings[k], source=sources[k]) for k in config.settings
    }
    return values, effective, ignored


def _parse_time(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if isinstance(value, str) and value:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    return None


def _in_band(x: Any, band: Band, names: dict[str, Any], where: str) -> bool:
    if band.at_least is not None and not x >= _value(band.at_least, names, where):
        return False
    if band.above is not None and not x > _value(band.above, names, where):
        return False
    if band.at_most is not None and not x <= _value(band.at_most, names, where):
        return False
    return not (band.below is not None and not x < _value(band.below, names, where))


def factor_value(f: Factor, names: dict[str, Any], now: datetime, where: str) -> Any:
    """``_factor_value``, answered in ONE kind of number: a curve, bands or lookup whose possible values mix
    whole and decimal numbers answers decimals (a band worth ``1`` beside bands worth ``1.08`` is 1.0, as the
    code path's ``1.0`` literal says it; a stored breakdown would otherwise read 1 for some items, 1.08 for others)."""
    v = _factor_value(f, names, now, where)
    if type(v) is int and f.type in ("curve", "bands", "lookup"):
        if any(type(c) is float for c in _choices(f, names, f"{where}, factor {f.name!r}")):
            return float(v)
    return v


def _choices(f: Factor, names: dict[str, Any], where: str) -> list[Any]:
    if f.type == "curve":
        raw = [p.value for p in f.points] + ([f.tail] if f.tail is not None else [])
    elif f.type == "bands":
        raw = [b.value for b in f.bands] + ([f.default] if f.default is not None else [])
    else:
        raw = list(f.table.values()) + ([f.default] if f.default is not None else [])
    out = []
    for r in raw:
        try:
            out.append(_value(r, names, where))
        except Exception:  # a value naming something this item lacks: not a choice to weigh here
            continue
    return out


def _factor_value(f: Factor, names: dict[str, Any], now: datetime, where: str) -> Any:
    where = f"{where}, factor {f.name!r}"
    if f.only_when and not evaluate(f.only_when, names, where + " (only_when)"):
        return _value(f.if_not, names, where)
    x = evaluate(f.of, names, where)
    if f.type == "expression":
        return x
    if x is None:
        return _value(f.missing, names, where)
    if f.type == "curve":
        for p in f.points:
            if x <= _value(p.up_to, names, where):
                return _value(p.value, names, where)
        return _value(f.tail, names, where)
    if f.type == "bands":
        for b in f.bands:
            if _in_band(x, b, names, where):
                return _value(b.value, names, where)
        return _value(f.default, names, where)
    if f.type == "clamp":
        given = x
        if f.high is not None:
            x = min(_value(f.high, names, where), x)
        if f.low is not None:
            x = max(_value(f.low, names, where), x)
        # A bound taken keeps the value's own kind of number: 1.0 clamped at a high of 1 stays 1.0, as
        # Python's min(1.0, x) would say it, never the integer bound (a stored score would read 1, not 1.0).
        return float(x) if isinstance(given, float) and not isinstance(x, bool) and isinstance(x, int) else x
    if f.type == "log_scale":
        if x < 0:
            return _value(f.missing, names, where)
        return min(1.0, max(0.0, math.log10(float(x) + 1) / _value(f.saturates_at, names, where)))
    if f.type == "half_life":
        at = _parse_time(x)
        if at is None:
            return _value(f.missing, names, where)
        age = max(0.0, (now - at).total_seconds() / _UNIT_SECONDS[f.unit])
        return 0.5 ** (age / _value(f.half_life, names, where))
    # lookup
    key = x if isinstance(x, str) else json.dumps(x)
    return _value(f.table[key], names, where) if key in f.table else _value(f.default, names, where)


def _numbers(values: list[Any]) -> list[float] | None:
    return values if values and all(_is_number(v) for v in values) else None


def declared_bound(f: Factor, names: dict[str, Any], which: Literal["max", "min"]) -> float | None:
    """The factor's declared max/min, else what its own definition shows."""
    where = f"factor {f.name!r} ({which})"
    declared = f.max if which == "max" else f.min
    pick = max if which == "max" else min
    if declared is not None:
        bound = _value(declared, names, where)
    else:
        candidates: list[Any]
        if f.type == "curve":
            candidates = [_value(p.value, names, where) for p in f.points] + (
                [_value(f.tail, names, where)] if f.tail is not None else []
            )
        elif f.type == "bands":
            candidates = [_value(b.value, names, where) for b in f.bands] + (
                [_value(f.default, names, where)] if f.default is not None else []
            )
        elif f.type == "lookup":
            candidates = [_value(v, names, where) for v in f.table.values()] + (
                [_value(f.default, names, where)] if f.default is not None else []
            )
        elif f.type == "clamp":
            edge = f.high if which == "max" else f.low
            candidates = [_value(edge, names, where)] if edge is not None else []
        elif f.type in ("log_scale", "half_life"):
            candidates = [1.0 if which == "max" else 0.0]
        else:
            candidates = []
        nums = _numbers(candidates)
        if nums is None:
            return None
        bound = pick(nums)
    # The values it can take besides its definition: `missing`, and `if_not` when gated.
    others = [_value(f.missing, names, where)] + ([_value(f.if_not, names, where)] if f.only_when else [])
    if not _is_number(bound) or any(v is not None and not _is_number(v) for v in others):
        return None
    return pick([bound, *(v for v in others if v is not None)])


def _aggregate(v: AggregateValue, rows: list[dict[str, Any]], names: dict[str, Any], where: str) -> Any:
    where = f"{where}, aggregate {v.name!r}"
    if v.op == "count":
        return len(rows)
    pairs: list[tuple[Any, Any]] = []
    for row in rows:
        value = evaluate(v.of, row, where)
        if value is None:
            continue
        weight = evaluate(v.weight, row, where) if v.op == "weighted_mean" else None
        if v.op == "weighted_mean" and weight is None:
            continue
        pairs.append((value, weight))
    if not pairs:
        return _value(v.empty, names, where)
    values = [p[0] for p in pairs]
    if v.op == "sum":
        return sum(values)
    if v.op == "max":
        return max(values)
    if v.op == "min":
        return min(values)
    if v.op == "mean":
        return sum(values) / len(values)
    total_weight = sum(p[1] for p in pairs)
    if not total_weight:
        return _value(v.empty, names, where)
    return sum(value * weight for value, weight in pairs) / total_weight


def _run_group(g: AggregateGroup, names: dict[str, Any], now: datetime, where: str) -> dict[str, Any]:
    listed = evaluate(g.over, names, f"{where}, aggregate over")
    if listed is None:
        listed = []
    if not isinstance(listed, list | tuple):
        raise ExecutionError(f"{where}: aggregate `over` {g.over!r} gave a {type(listed).__name__}, not a list.")
    rows: list[dict[str, Any]] = []
    for n, element in enumerate(listed):
        row = {**names, g.as_: element}
        for f in g.each:
            row[f.name] = factor_value(f, row, now, f"{where}, {g.as_} {n}")
        rows.append(row)
    return {v.name: _aggregate(v, rows, names, where) for v in g.values}


def _combined(c: Combine, values: dict[str, Any], names: dict[str, Any], where: str) -> Any:
    if c.op == "expression":
        return evaluate(c.expression, names, f"{where}, combine")
    terms: list[tuple[str, Any]] = []
    for n in c.of:
        v = values[n]
        if v is None:
            if c.missing is None:
                raise ExecutionError(f"{where}: factor {n!r} came out empty and combine has no `missing` value.")
            v = _value(c.missing, names, where)
        terms.append((n, v))
    if c.op == "product":
        total = terms[0][1]
        for _, v in terms[1:]:
            total = total * v
        return total
    # Python's own sum (compensated since 3.12), the same arithmetic a sum() expression gets.
    return sum(_value(c.weights[n], names, f"{where}, weight of {n!r}") * v for n, v in terms)


def combined_max(config: ScoreConfig, names: dict[str, Any]) -> float:
    """The best reachable combined value: the combine applied to the declared maxima (DERIVED)."""
    c = config.combine
    assert c is not None
    if c.op == "expression":
        return float(_value(c.max, names, "combine max"))
    by_name = {f.name: f for f in config.factors}
    fill = _value(c.missing, names, "combine missing") if c.missing is not None else None

    def bound(n: str, which: Literal["max", "min"]) -> float:
        b = declared_bound(by_name[n], names, which)
        if b is None:
            raise ExecutionError(
                f"data.score: factor {n!r} has no {which} to normalize by; declare its `{which}`."
            )
        return (max if which == "max" else min)(b, fill) if _is_number(fill) else b

    if c.op == "product":
        total = bound(c.of[0], "max")
        for n in c.of[1:]:
            total = total * bound(n, "max")
        return total
    weights = [(n, _value(c.weights[n], names, f"weight of {n!r}")) for n in c.of]
    return sum(w * bound(n, "max" if w >= 0 else "min") for n, w in weights)


def _rounded(v: Any, digits: int | None) -> Any:
    if digits is None or not _is_number(v):
        return v
    # Rounded to digits is a decimal number (2 rounded to 4 digits is 2.0, as the code's float sums say it);
    # 0 digits is a whole number.
    return round(v) if digits == 0 else round(float(v), digits)


#: Definition keys that never change a score: words for people, and the override plumbing whose effect is already in
#: the effective values (``locked`` / ``overrides_section`` only decide WHICH overrides apply).
_COSMETIC_KEYS = frozenset({"label", "setting_labels", "locked", "overrides_section"})


def _canon(value: Any) -> str:
    """One text per JSON value that a database can reproduce exactly: object keys sorted by code point, no spaces,
    every number in plain decimal with no trailing zeros (``1.0`` and ``1`` are one number; ``1e-09`` is
    ``0.000000001``), strings JSON-escaped with non-ASCII kept. The SQL twin is ``research.scoring_canon(jsonb)``."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        text = format(Decimal(repr(value) if isinstance(value, float) else str(value)).normalize(), "f")
        return "0" if text in ("-0", "0") else text
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, dict):
        return "{" + ",".join(_canon(str(k)) + ":" + _canon(value[k]) for k in sorted(value, key=str)) + "}"
    if isinstance(value, list | tuple):
        return "[" + ",".join(_canon(v) for v in value) + "]"
    return json.dumps(str(value), ensure_ascii=False)


def _scoring_only(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _scoring_only(v) for k, v in value.items() if k not in _COSMETIC_KEYS}
    if isinstance(value, list):
        return [_scoring_only(v) for v in value]
    return value


def scoring_digest(config: ScoreConfig, effective: dict[str, Any]) -> str:
    """A stable hash of what decides a score: the definition as written (minus its words for people) with every
    setting at the value this run used — the defaults plus the overrides that actually applied. Same scoring, same
    digest, whatever else a publish changed; any weight, curve, band, formula or applied-override change gives
    another. ``config:`` + the first 12 hex of sha256 over :func:`_canon`; the database computes the same
    (``research.scoring_version``) to say whether a stored score is out of date."""
    body = _scoring_only(config.model_dump(mode="json", by_alias=True, exclude_unset=True))
    body["settings"] = effective
    return "config:" + hashlib.sha256(_canon(body).encode()).hexdigest()[:12]


def score_items(
    config: ScoreConfig,
    items: list[Any],
    *,
    others: dict[str, Any] | None = None,
    overrides: dict[str, Any] | None = None,
    overrides_source: str = "overrides",
    score_version: str | None = None,
    now: str | datetime | None = None,
) -> ScoreOutput:
    """Score every item under ``config`` — the whole step, callable without a run."""
    others = dict(others or {})
    settings, effective, ignored = merge_settings(config, overrides, overrides_source)
    clash = sorted(set(others) & (config.declared_names() | RESERVED_NAMES))
    if clash:
        raise ExecutionError(f"data.score: inputs named {clash} collide with names this step declares; rename them.")
    instant = _parse_time(now) if now is not None else datetime.now(UTC)
    if instant is None:
        raise ExecutionError(f"data.score: `now` {now!r} is not an ISO-8601 time.")
    version = score_version or scoring_digest(config, settings)
    base: dict[str, Any] = {**others, **settings, "items": items, "now": instant, "score_version": version}

    for g in config.aggregates:
        if g.scope == "all":
            base.update(_run_group(g, base, instant, "the whole list"))

    normalizer: Normalizer | None = None
    if config.normalize is not None:
        cmax = combined_max(config, base)
        if not _is_number(cmax) or cmax <= 0:
            raise ExecutionError(f"data.score: the best reachable combined value is {cmax!r}; it must be above 0.")
        normalizer = Normalizer(combined_max=cmax, to=config.normalize.to)

    out_items: list[Any] = []
    for index, item in enumerate(items):
        where = f"item {index}"
        names = {**base, "item": item}
        for g in config.aggregates:
            if g.scope == "item":
                names.update(_run_group(g, names, instant, where))
        factors: dict[str, Any] = {}
        for f in config.factors:
            factors[f.name] = names[f.name] = factor_value(f, names, instant, where)
        if config.combine is not None:
            combined = _combined(config.combine, factors, names, where)
            names["combined"] = combined
            if normalizer is not None:
                to = normalizer.to
                names["score"] = max(0.0, min(to, combined / normalizer.combined_max * to))
            else:
                names["score"] = combined
        for f in config.then:
            names[f.name] = factor_value(f, names, instant, where)
        keys = {
            o.key: _rounded(evaluate(o.value or o.key, names, f"{where}, output {o.key!r}"), o.round)
            for o in config.outputs
        }
        if config.write_as:
            if not isinstance(item, dict):
                raise ExecutionError(f"data.score: item {index} is not an object, so write_as cannot add to it.")
            out_items.append({**item, config.write_as: keys})
        elif isinstance(item, dict):
            out_items.append({**item, **keys})
        else:
            raise ExecutionError(f"data.score: item {index} is not an object; set write_as or score objects.")

    return ScoreOutput(
        items=out_items,
        effective_settings=effective,
        ignored_overrides=ignored,
        normalizer=normalizer,
        score_version=version,
    )


class ScoreExecutor:
    """Settings + overrides → aggregates → factors → combine → normalize (derived) → named outputs."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.score",
        category=NodeCategory.DATA,
        display_name="Score Items",
        description=(
            "Score every item from named factors, weights and curves you can read and change; "
            "the top of the scale comes from each factor's maximum, never typed in."
        ),
        input_schema=ScoreInput,
        input_kind="score_items_request",
        output_schema=ScoreOutput,
        output_kind="scored_items_result",
        config_schema=ScoreConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="gauge",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ScoreInput,
        config: ScoreConfig,
    ) -> NodeResult[ScoreOutput]:
        payload = inputs.model_dump(mode="json")
        items = payload.pop("items")
        overrides = payload.pop("overrides")
        source = payload.pop("overrides_source")
        version = payload.pop("score_version")
        now = payload.pop("now")
        payload = {k: v for k, v in payload.items() if not k.startswith("__")}
        return success(
            score_items(
                config,
                items,
                others=payload,
                overrides=overrides,
                overrides_source=source,
                score_version=version,
                now=now,
            )
        )
